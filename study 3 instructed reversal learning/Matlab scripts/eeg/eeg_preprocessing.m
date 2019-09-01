%===============================
% PRE-PROCESSING SCRIPT
% AUTHOR: SANTIAGO MUÑOZ-MOLDES
% DATE: JULY 2019
%===============================

clear
close all
clc

%% SETUP AND FOLDER CREATION
% root
root_dir = '/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/analysis/eeg/';
cd(root_dir)
addpath('./scripts/')

% create folders
path_data = '/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/data/raw/';
if ~exist('./preprocessed/'); mkdir('./preprocessed/'); end %#ok<*EXIST>
if ~exist('./ica/'); mkdir('./ica/'); end %#ok<*EXIST>
if ~exist('./interpolated/'); mkdir('./interpolated/'); end %#ok<*EXIST>
if ~exist('./reref/'); mkdir('./reref/'); end %#ok<*EXIST>
if ~exist('./clean/'); mkdir('./clean/'); end %#ok<*EXIST>

% adds fieldtrip to the matlab path + the relevant subdirectories
path_ft = '/Users/santiago/Documents/MATLAB/fieldtrip';
addpath(path_ft);
ft_defaults;

%participants
subjects = 1:70;

% load the biosemi 64 channel template that has channel coordinates and
% names
cfg        = [];
cfg.layout = 'biosemi64.lay';
layout = ft_prepare_layout(cfg);

%one electrode's label is wrong in all recordings, 'T6' instead of 'T8'.
%I modify the layout so that the wrong electrode is read (otherwise
%skipped)
layout.labelmod = layout.label;
layout.labelmod{52, 1} = 'T6';  % wrong label

%% DATA EPOCHING, FILTERING AND DOWNSAMPLING

tic
for i=1:length(subjects)
    
    %the trigger values are not the same in all datafiles.
    %triggers for each subject  are defined here below.
    if i == 2 || i > 14
        cs_pos    = 65292;
        cs_neg    = 65293;
        ucs       = 65294;
        iti_start = 65295;
    else
        cs_pos    = 12;
        cs_neg    = 13;
        ucs       = 14;
        iti_start = 15;
    end
    
    % define the filename each iteration
    filename = strcat('EEG_ECG_P', num2str(i), '.bdf');
    dataset  = fullfile(path_data, filename);
    
    % epochs-of-interest are defined
    cfg                     = [];
    cfg.dataset             = dataset;
    cfg.trialdef.eventtype  = 'STATUS';         % Channel containing triggers. use 'STATUS' for .bdf, 'trigger' for .set files
    cfg.trialdef.eventvalue = [cs_neg cs_pos];  % event value(s);
    cfg.trialdef.prestim    = .2;               % before stimulation (sec), only use positive value
    cfg.trialdef.poststim   = .8;               % after stimulation (sec) , only use positive value
    cfg.bpfilter            = 'yes';            % band-pass filter
    cfg.bpfreq              = [.1 30];
    cfg.bpfilttype          = 'fir';            % band-pass filter type. 'fir' is MATLAB's `fir1`
    cfg.padding             = 3;                % length in seconds to which epochs are padded (to reduce artifacts at epoch boundaries)
    cfg.channel             = layout.labelmod;  % custom electrode list (modified to include the wrong label)
    cfg = ft_definetrial(cfg);    % define the epochs-of-interest
    data = ft_preprocessing(cfg);
    
    %edit the wrong channel label directly in the data structure
    data.label{52,1} = 'T8';
    
    %downsample data
    cfg                    = [];
    cfg.resamplefs         = 256;        % 256 Hz is sufficient for ERPs
    data = ft_resampledata(cfg, data);
    
    %save as .mat
    save(fullfile(root_dir, 'preprocessed', num2str(i)), 'data')
    
end
toc %Elapsed time is 2264 seconds.

%% VISUAL INSPECTION OF CHANNELS
% loop through participants and open a GUI to inspect trials and channels.
% Detect bad channels prior to ICA, and write down labels on separate file.
% Pressing quit skips to the next participant.

for i=1:length(subjects)
    
    %load file
    datafile = fullfile(root_dir, 'preprocessed', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %keep track of number on console
    disp(strcat('Subject number: >>>', num2str(i), '<<<'))
    
    %open GUI for visual inspection
    cfg                   = [];
    cfg.layout            = 'biosemi64.lay';
    cfg.channel           = {'EEG'};          %show only EEG channels (in case non-EEG are in data)
    ft_rejectvisual(cfg, data);
    
end

%% ICA DECOMPOSITION
% Perform Independent Component Analysis decomposition to detect eye blinks
% This step loads the file containing the bad channels for each participant
% and excludes them from the ICA decomposition. It then runs ICA for each
% participant.

% load the .mat file with the rej_chan for each subject (from visual
% inspection)
rej_chan_file = fullfile(root_dir, 'scripts', 'rej_chan.mat');
load(rej_chan_file)

tic
for i=1:length(subjects)
    
    %load data
    datafile = fullfile(root_dir, 'preprocessed', strcat(num2str(i), '.mat'));
    load(datafile);
    
    cfg         = [];
    cfg.method  = 'runica';                     % requires eeglab installation
    cfg.channel = rej_chan{i};                  % rejected channels from file
    data_ica = ft_componentanalysis(cfg, data);
    
    %save data
    save(fullfile(root_dir, 'ica', 'pre', num2str(i)), 'data_ica')
end
toc % Elapsed time is 1687.153059 seconds for 60 participants.


%% INSPECT ICA COMPONENTS
% This step allows to see the ICA components for each participant. It will
% open a GUI and show a scalp map and the continuous data for each
% component.
% I take note of components to reject (eye blinks) on a separate file.

for i=1:length(subjects)
    
    %load data
    datafile = fullfile(root_dir, 'ica', 'pre', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %browse components
    cfg                  = [];
    cfg.viewmode         = 'component';
    cfg.continuous       = 'yes';           % Forces the epochs next to each other
    cfg.blocksize        = 10;
    cfg.channels         = 1:9;             % Number of components per page
    cfg.zlim             = 'maxmin';        % Scale for scalp map colors
    cfg.compscale        = 'local';         % Scale each component separately
    cfg.layout           = 'biosemi64.lay'; % Load the electrode layout
    ft_databrowser(cfg, data_ica);
    
end

%% REJECT ICA COMPONENTS
% This step allows to remove the rejected components. A file containing the
% indices of the components for each participant (created above) is loaded
% and the components are removed. The components are removed from the
% original dataset, prior to electrode exclusion.
% Also reloading the `data` in each iteration

% load a .mat file with the rej_comp for each subject (from visual
% inspection)
rej_comp_file = fullfile(root_dir, 'scripts', 'rej_comp.mat');
load(rej_comp_file)

for i=1:length(subjects)
    
    %load ica weights
    datafile = fullfile(root_dir, 'ica', 'pre', strcat(num2str(i), '.mat'));
    load(datafile);
    %load original data
    datafile = fullfile(root_dir, 'preprocessed', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %select components to reject
    cfg                  = [];
    cfg.component        = rej_comp{i};
    data_ica_clean = ft_rejectcomponent(cfg, data_ica, data);  % the 3rd input `data` to return to the original dataset
    
    %save data
    save(fullfile(root_dir, 'ica', 'post', num2str(i)), 'data_ica_clean')
    
end

%% VISUALISE DATA AFTER ICA; DETECT BAD CHANNELS
% Browse the data and identify bad channels (again). Write down the bad
% channels on a separate file (itp_chan.mat / itp_chan_list.m)
% These channels will be interpolated on the next step

for i=1:length(subjects)
    
    %load ica-cleaned data
    datafile = fullfile(root_dir, 'ica', 'post', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %visual data inspection (close with 'q')
    %cfg                   = [];
    %cfg.viewmode          = 'butterfly';  % 'vertical'
    %ft_databrowser(cfg, data_ica_clean)
    
    %view trial x electrode activation
    cfg                   = [];
    cfg.layout            = 'biosemi64.lay';
    cfg.method            = 'summary';
    ft_rejectvisual(cfg, data_ica_clean);
    
end


%% ELECTRODE INTERPOLATION
% This step loads the file with the channels to interpolate, and 
% interpolates them using the electrode layout

% load the .mat file with the intpl channels for each subject (from visual
% inspection)
itp_chan_file = fullfile(root_dir, 'scripts', 'itp_chan.mat');
load(itp_chan_file)

%prepare a file with electrode neighbours values
cfg                  = [];
cfg.method           = 'template';
cfg.template         = 'biosemi64_neighb.mat';
cfg.layout           = 'biosemi64.lay';
cfg.channel          = 'eeg';
cfg.feedback         = 'yes';                  % opens a window
neighbours = ft_prepare_neighbours(cfg);

for i=1:length(subjects)
    
    %load data cleaned from bad components 
    datafile = fullfile(root_dir, 'ica', 'post', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %interpolate electrode
    cfg            = [];
    cfg.badchannel = itp_chan{i};  % IMPORTANT TO HAVE ';' (e.g. {'AF7'; 'FT8'}) in
                                   % between electrode labels, so they are stored as a vertical cell. 
                                   % Because ft_channelrepair (line 162) concatenates *vertically*
                                   % with cfg.missingchannel.
    cfg.method     = 'average';     %'weighted' not good for channels next to each other
    cfg.elec       = ft_read_sens('standard_1020.elc');
    cfg.neighbours = neighbours;
    data_intpl = ft_channelrepair(cfg, data_ica_clean);
    
    %save data
    save(fullfile(root_dir, 'interpolated', num2str(i)), 'data_intpl')
    
end


%% RE-REFERENCING AND BASELINE CORRECTION
% this step re-references data to the mean of all channels, and performs
% de-meaning to substract the baseline (-2 0) for each epoch.

for i=1:length(subjects)
    
    %load interpolated data
    datafile = fullfile(root_dir, 'interpolated', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %re-reference and de-mean
    cfg = [];
    cfg.reref           = 'yes';
    cfg.refchannel      = 'all';
    cfg.refmethod       = 'avg';                      % common ref
    cfg.demean          = 'yes';                      % baseline correction
    cfg.baselinewindow  = [-inf 0];
    data_reref = ft_preprocessing(cfg, data_intpl);  
    
    %save data
    save(fullfile(root_dir, 'reref', num2str(i)), 'data_reref')
    
end

%% REMOVE TRIALS
%using the visual rejection tool, trials with abnormal range are removed.
%only 0-8 for each participant, usually around 3-5. the discarded trials
%are not removed from the dataset, only replaced by NaNs

%once focusing on whole data, and once focusing on electrodes of interest
%much stricter on electrodes of interest

    %prepare a file with electrode neighbours values
    cfg                  = [];
    cfg.method           = 'template';
    cfg.template         = 'biosemi64_neighb.mat';
    cfg.layout           = 'biosemi64.lay';
    cfg.channel          = 'eeg';
    cfg.feedback         = 'yes';                  % opens a window
    cfg.elec              = ft_read_sens('standard_1020.elc');
    neighbours = ft_prepare_neighbours(cfg);

for i=1:length(subjects)
    
    %load re-referenced and baseline corrected data
    datafile = fullfile(root_dir, 'reref', strcat(num2str(i), '.mat'));
    load(datafile);
    
    %keep track of number on console
    disp(strcat('Subject number: >>>', num2str(i), '<<<'))
    
    %view trial x electrode activation
    cfg             = [];
    cfg.layout      = 'biosemi64.lay';
    cfg.method      = 'summary';
    cfg.metric      = 'maxabs';
    cfg.channel     = {'PO8', 'Pz', 'POz'};
    ft_rejectvisual(cfg, data_reref);
    
    %view trial x electrode activation
    cfg             = [];
    cfg.layout      = 'biosemi64.lay';
    cfg.method      = 'summary';
    cfg.keeptrial   = 'nan';  % fills trial with NaN
    cfg.keepchannel = 'repair';
    cfg.neighbours  = neighbours;
    cfg.metric      = 'maxabs';
    data_clean = ft_rejectvisual(cfg, data_reref);
    
    %save data
    save(fullfile(root_dir, 'clean', num2str(i)), 'data_clean')
    
end

% FIND TRIALS
% data_clean.trial{1,trial}(:,:)



%% ADD TRIAL INFO
%this step could have been done earlier

% load trial info from file. file was built on R.
% the trial info is structured as 70 (subjects) x 80
% (trial). only reversal info is included as 1 or 0 (could add more info
% if necessary)
t_info = csvread('trial_info.csv',1,0);

for i=1:length(subjects)
    
    %load clean data
    datafile = fullfile(root_dir, 'clean', strcat(num2str(i), '.mat'));
    load(datafile);
    
    b=num2str(data_clean.trialinfo(:,1)); %get trigger column as string (for next step)
    data_clean.trialinfo(:,2) = str2num(b(:,end));      % last digit of trigger
    data_clean.trialinfo(:,3) = i;                      % Subject number
    data_clean.trialinfo(:,4) = 1:80;                   % Trial number (total)
    data_clean.trialinfo(:,5) = [1:20 1:20 1:20 1:20];  % Trial number (block)
    %data_clean.trialinfo(:,5) = [zeros(1,20) ones(1,20) zeros(1,20) ones(1,20)];  % Instructed Reversal (only for instructed)
    data_clean.trialinfo(:,6) = t_info(:,i); % Reversal info from file
    
    %save data (overwrite)
    save(fullfile(root_dir, 'clean', num2str(i)), 'data_clean')
    
    disp(strcat('Adding trial information to subject', {' '}, num2str(i)))
    
end

%% VISUALISE CLEAN DATA


i = 60;

%load data cleaned from bad components 
datafile = fullfile(root_dir, 'ica', 'post', strcat(num2str(i), '.mat'));
load(datafile);
%load interpolated data
datafile = fullfile(root_dir, 'interpolated', strcat(num2str(i), '.mat'));
load(datafile);
%load clean data
datafile = fullfile(root_dir, 'clean', strcat(num2str(i), '.mat'));
load(datafile);

%visual data inspection (close with 'q')
cfg                   = [];
cfg.viewmode          = 'butterfly';  % 'vertical'
ft_databrowser(cfg, data_ica_clean)

%visual data inspection (close with 'q')
cfg                   = [];
cfg.viewmode          = 'butterfly';  % 'vertical'
ft_databrowser(cfg, data_intpl)

%visual data inspection (close with 'q')
cfg                   = [];
cfg.viewmode          = 'butterfly';  % 'vertical'
ft_databrowser(cfg, data_clean)