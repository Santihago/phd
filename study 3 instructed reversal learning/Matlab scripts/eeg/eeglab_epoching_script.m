%% 1.0 Open data with EEGLAB

clear
close all
clc


%% Define folders
root_dir     =  '/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/analysis/eeg/';
cd(root_dir)
path_data     = '/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/data/raw/';
path_scripts  = './scripts/';
path_destin   = './filtered/'; if ~exist(path_destin); mkdir(path_destin); end %#ok<*EXIST>

path_eeglab   = '/Users/santiago/Documents/MATLAB/eeglab14_1_2b';

%  adds fieldtrip to the matlab path + the relevant subdirectories
addpath(path_scripts)
addpath(path_eeglab);

%participants
subjects = 1:70;

for i=1:length(subjects)
        
    % Because I'm unable to read the triggers of a Biosemi file with Fieldtrip
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    
    % define the filename each iteration
    filename = strcat('EEG_ECG_P', num2str(i));
    dataset  = fullfile(path_data, strcat(filename, '.bdf'));
    
    setfilename = strcat(filename, '.set');
    
    % 1.1 Import file
    % File > Import > .BDF
    EEG = pop_biosig(dataset);
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off');
    
    % 1.2 Downgrade to 256 Hz
    EEG = pop_resample( EEG, 256);
    
    % Bandpass FIR filter (new default is Matlab's 'fir1')
    %EEG = pop_eegfilt( EEG, .1, 30, [], [0]); % High pass filter the data with cutoff frequency of 1 Hz.
    EEG = pop_eegfiltnew(EEG, 0.1, 30);
    
    % Below, create a new dataset with the name filtered Continuous EEG Data
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, CURRENTSET, 'setname', 'filtered Continuous EEG Data');% Now CURRENTSET= 2
    
    % 1.3 Epoch data {events}, [time points]
    %EEG = pop_epoch( EEG, {  '30'  '92'  }, [-3         3.1], 'epochinfo', 'yes');
    %EEG = eeg_checkset( EEG );
    
    % 1.4 Add comments
    %comments = 'This is a comment';
    %EEG = pop_editset(EEG, 'setname', 'Here the title', 'subject', '1', ...
    %    'condition', '1', 'session', [1], 'comments', strvcat(comments));
    %[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    
    %eeglab redraw
    
    % 1.5 Save file
    EEG = pop_saveset( EEG, 'filename', setfilename, 'filepath', path_destin);
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    
    clear ALLCOM
    clear EEG
    clear comments
    clear CURRENTSTUDY
    clear eeglabUpdater
    clear PLUGINLIST
    clear STUDY
    
end