%% Custom R-peak detector using FieldTrip and heart_peak_detect.m
% Author: Santiago Munoz Moldes, Universite Libre de Bruxelles
% ----------
% Requirements:
% fieldtrip toolbox must be in 'fieldTripPath'
% heart_peak_detect.m must be in 'scriptsDir'
% ECG .bdf files must be in 'sourceDir'
% ----------
% ECG files:
% ECG files contain data from 3 channels (and 128 trials + rest period)
% We are only going to use 2 channels for a lead II bipolar configuration.

clear all; close all;  %#ok<*CLALL>
%% Define folders
cd('/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/')
scriptsDir    = './analysis/scripts/';
psypyDir      = './data/behavData/';
sourceDir     = './data/raw/';
destinDir     = './analysis/preprocessed/'; if ~exist(destinDir); mkdir(destinDir); end %#ok<*EXIST>
%fieldTripPath = '/Users/santiago/Documents/MATLAB/fieldtrip-20180315';
fieldTripPath = '/Users/santiago/Documents/MATLAB/fieldtrip';
addpath(fieldTripPath); ft_defaults
addpath(scriptsDir)

%% Read the data using FieldTrip

% Included participants
%participantList = [1 3:29]; % participants not excluded
%participantList = [10:13 15:44]; % participants not excluded
participantList = [3 10 12 26 30 33 38 40 41]; % participants not excluded
good = [5 6 8 9 13 16:19 22:25 27:29 31 32 34:36 39 42];
bad = [1 2 4 7 11 15 20 37 43 44];
verybad = [3 10 12 26 30 33 38 40 41];
save = [4 10 11 20];

participantList = [11 20 4]; % participants not excluded
participantList = [64]; % participants not excluded

% Time windows in seconds
timeBefore = 5;  % Total time before read from data
timeAfter = 9;  % Total time after read from data

%% START LOOPING THROUGH PARTICIPANTS
for subjIndex = 1:length(participantList)
    
    % Set subject number and filename
    thisSubj = participantList(subjIndex);
    thisECGFilename = strcat(sourceDir,'EEG_ECG_P', num2str(thisSubj),'.bdf');
    
    % TRIGGERS - EVENT MARKERS
    % By accident, the trigger values are not the same in all datafiles.
    % For participant ==2, and for participant >14, the numbers are
    % different. They are defined here below.
    if thisSubj == 2 || thisSubj > 14
        CSPositive = 65292;
        CSNegative = 65293;
        UCS = 65294;
        ITIStart = 65295;
    else
        CSPositive = 12;
        CSNegative = 13;
        UCS = 14;
        ITIStart = 15;
    end
    
    
    % SET LEAD DEPENDING ON SUBJECT
    % For some subjects the EXG-EXG1 lead II disposition did not provide
    % 100% heartbeat detections (usually due to movement or sweat
    % artifacts. This is solved in some cases by referencing the EXG1 to an
    % electrode from the EEG, since EXG2 was usually the one picking up
    % movement and sweat artifacts. For those I've selected another
    % reference: 'C4'. This ref in particilar results in 1/10 ms increase
    % in IBI values, but since they are constant they do not affect
    % relative IBI measures (corrected for baseline).
    
    refchannel = 'C4';
    channelname = 'C4-EXG1';
    
    
    %% Read trial data windows from file
    
    cfg                     = [];
    cfg.dataset             = thisECGFilename; % your filename with file extension;
    cfg.channel             = {'EXG1' 'EXG2' 'Cz'};
    cfg.trialdef.eventtype  = 'STATUS'; % trigger channel in Biosemi
    cfg.trialdef.eventvalue = [CSNegative CSPositive]; % event value(s)
    cfg.trialdef.prestim    = timeBefore; % before stimulation (sec), only use positive value
    cfg.trialdef.poststim   = timeAfter; % after stimulation (sec) , only use positive value
    cfg.reref               = 'yes';
    cfg.refchannel          = 'EXG2';  % re-reference  %'Cz'
    cfg.refmethod           = 'bipolar';  % we get a single ECG lead II channel
    cfg                     = ft_definetrial(cfg);
    cfg.method              = 'trial';
    lead_II = ft_preprocessing(cfg);
    
    %% START LOOPING THROUGH TRIALS
    
    % Create an output table for each participant
    trialN = length(lead_II.trial);
    cols = 13;
    outputTable = zeros(trialN, cols);
    
    % Upload here information about each trial (from psychopy file)
    % Read psychopy csv file
    %fname = strcat(psypyDir, 'behavData_P', num2str(thisSubj),'.csv');
    %T = readtable(fname);  % Read entire data file
    %dur = T{:,10};  % Select one column with face durations
    %durs = dur==3;  % Convert from strings to boolean vector
    
    % Add to fieldtrip's trial info
    %ll = length(lead_II.trialinfo);
    %lead_II.trialinfo(:,2) = durs(1:ll);  % Take as much as nr of ft trials
    
    for thisTrial = 1:trialN
        disp(thisTrial)
        try
            % detect heart peaks P Q R S T.
            % Everything is based on detecting the R peaks.
            cfg            = [];
            cfg.trials     = thisTrial;
            cfg.channel    = 'EXG1-EXG2'; % 'Cz-EXG1';
            cfg.thresh     = 3;
            cfg.plotthresh = 'yes';  % allowing the user to edit the threshold
            cfg.plotbeat   = 'yes';  % see template HB
            cfg.plotcorr   = 'yes';  % a figure with all heart beats is shown. The user is asked whether or not they want to change the threshold of the correlation. In last resort, outlier heart beats (based on interbeat interval) can be remodeled.
            cfg.plotfinal  = 'no';
            cfg.lpfilter   = 'yes';
            cfg.lpfreq     = 15;
            [HeartBeats]   = heart_peak_detect(cfg,lead_II);
            
            %% Retrieve R peaks
            % more info with [HeartBeats.R_sample] or [HeartBeats.R_time]
            
            % R-peaks list
            R_samples = [HeartBeats.R_sample];
            R_times = [HeartBeats.R_time];
            
            %% Select a fixed number of beats
            % Get time point where stimulus is presented in sample points of ECG
            % recording (relative to each trial)
            eventTime = lead_II.fsample * timeBefore;
            idx = find(R_samples-eventTime>0, 1);  % Index index in R_samples of 1st R-peak
            % Select n beats before, and n beats after
            nBefore = 3;
            nAfter = 8;
            %try
            sel_beats = R_samples(idx-nBefore:idx+(nAfter-1));
            sel_times = R_times(idx-nBefore:idx+(nAfter-1));
            
            %% Transform to IBI intervals
            % We calculate the time between each beat and the previous
            RR = diff(sel_beats)/lead_II.fsample;  % (!WE LOSE THE FIRST BEAT!)
            
            %% Save  data
            % Add to table  (row, column)
            outputTable(thisTrial, 1) = thisSubj;  % static
            outputTable(thisTrial, 2) = thisTrial;  % static
            outputTable(thisTrial, 3) = lead_II.trialinfo(thisTrial,1);  % trigger value
            outputTable(thisTrial, 4:13) = RR;  % add the 10 RR to the table
            
        catch
            % If peaks not found (e.g. faulty recording), continue
            warning('Not enough R peaks found')
            disp(thisTrial)
            
            try % Try again, this time with manual selection
                % detect heart peaks P Q R S T.
                % Everything is based on detecting the R peaks.
                cfg            = [];
                cfg.trials     = thisTrial;
                cfg.channel    = 'EXG1-EXG2'; % 'Cz-EXG1';
                cfg.thresh     = 3;
                cfg.plotthresh = 'yes';  % allowing the user to edit the threshold
                cfg.plotbeat   = 'yes';  % see template HB
                cfg.plotcorr   = 'yes';  % a figure with all heart beats is shown. The user is asked whether or not they want to change the threshold of the correlation. In last resort, outlier heart beats (based on interbeat interval) can be remodeled.
                cfg.plotfinal  = 'no';
                cfg.lpfilter   = 'yes';
                cfg.lpfreq     = 15;
                [HeartBeats]   = heart_peak_detect(cfg,lead_II);
                
                %% Retrieve R peaks
                % more info with [HeartBeats.R_sample] or [HeartBeats.R_time]
                
                % R-peaks list
                R_samples = [HeartBeats.R_sample];
                R_times = [HeartBeats.R_time];
                
                %% Select a fixed number of beats
                % Get time point where stimulus is presented in sample points of ECG
                % recording (relative to each trial)
                eventTime = lead_II.fsample * timeBefore;
                idx = find(R_samples-eventTime>0, 1);  % Index index in R_samples of 1st R-peak
                % Select n beats before, and n beats after
                nBefore = 3;
                nAfter = 8;
                %try
                sel_beats = R_samples(idx-nBefore:idx+(nAfter-1));
                sel_times = R_times(idx-nBefore:idx+(nAfter-1));
                
                %% Transform to IBI intervals
                % We calculate the time between each beat and the previous
                RR = diff(sel_beats)/lead_II.fsample;  % (!WE LOSE THE FIRST BEAT!)
                
                %% Save  data
                % Add to table  (row, column)
                outputTable(thisTrial, 1) = thisSubj;  % static
                outputTable(thisTrial, 2) = thisTrial;  % static
                outputTable(thisTrial, 3) = lead_II.trialinfo(thisTrial,1);  % trigger value
                outputTable(thisTrial, 4:13) = RR;  % add the 10 RR to the table
            catch
                %% Save  data
                % Add to table  (row, column)
                outputTable(thisTrial, 1) = thisSubj;  % static
                outputTable(thisTrial, 2) = thisTrial;  % static
                outputTable(thisTrial, 3) = lead_II.trialinfo(thisTrial,1);  % trigger value
                outputTable(thisTrial, 4:13) = NaN(1,10);  % add NaN
            end
        end
        
        
    end
    %% Save this participant
    % Set filename
    csvOutFilename = strcat(destinDir, 'ecg_IBI_P', num2str(thisSubj),'_', datestr(now, 30), '.csv');
    % Save
    csvwrite(csvOutFilename, outputTable)
    
end
