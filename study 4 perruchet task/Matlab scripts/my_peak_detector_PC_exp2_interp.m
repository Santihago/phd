%% Custom R-peak detector using FieldTrip and heart_peak_detect.m
% Author: Santiago Munoz Moldes, Universite Libre de Bruxelles
% ----------
% Requirements:
% fieldtrip toolbox must be in 'fieldTripPath'
% heart_peak_detect.m must be in 'scriptsDir'
% ECG .bdf files must be in 'sourceDir'
% ----------
% ECG files:
% ECG files contain data from 3 channels
% We are only going to use 1 channel

clear all; close all;  %#ok<*CLALL>
%% Define folders
cd('/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/PC/exp_2/')
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
%participantList = [7:31]; % participants not excluded

% Time windows in seconds
%timeBefore = 7;  % Total time before read from data
%timeAfter = 7;  % Total time after read from data

% Select n beats before, and n beats after
%nBefore = 5;
%nAfter = 4;
%%
%participantList = [2:5 7:31]; % participants not excluded
%participantList = [14:31]; % participants not excluded

% Time windows in seconds
%timeBefore = 12;  % Total time before read from data
%timeAfter = 9;  % Total time after read from data

% Select n beats before, and n beats after
%nBefore = 8;
%nAfter = 7;

%check p29, file looks file but threw error
excluded = [6 10 20 29 34 39];
%participantList = setdiff(1:41, excluded); % participants not excluded
participantList = setdiff(1:41, excluded); % participants not excluded


%%


% If response to noise analysis
destinDir     = './analysis/preprocessed/CS/interpolated/';

% Time windows in seconds
interp_before = 5;  % Baseline length
interp_after = 9;  % Baseline length
timeBefore = interp_before + 2;  % Total time before read from data
timeAfter = interp_after + 2;  % Total time after read from data

% Query points for the interpolated data (range in seconds)
sr = 2;  % Sampling rate of upsamples/interpolated data
xq = -1*interp_before:(1/sr):interp_after; % window of interest (also defined later)


%% START LOOPING THROUGH PARTICIPANTS
for subjIndex = 1:length(participantList)
    
    % Set subject number and filename
    thisSubj = participantList(subjIndex);
    thisECGFilename = strcat(sourceDir,'ECG_P', num2str(thisSubj),'.bdf');
    
    % TRIGGERS - EVENT MARKERS
    CS = 65291;
    UCS = 65294;
    ITIStart = 65295;
    
    % SET LEAD DEPENDING ON SUBJECT
    % The reference was placed on the right clavicule. We recorded 3
    % channels: EXG1: right lower coastal arch, EXG2: left lower coastal
    % arch, and EXG3: left ankle.
    
    channelname = 'EXG2';
    
    
    %% Read trial data windows from file
    
    cfg                     = [];
    cfg.dataset             = thisECGFilename; % your filename with file extension;
    cfg.channel             = {channelname};
    cfg.trialdef.eventtype  = 'STATUS'; % trigger channel in Biosemi
    cfg.trialdef.eventvalue = CS; % event value(s)
    cfg.trialdef.prestim    = timeBefore; % before stimulation (sec), only use positive value
    cfg.trialdef.poststim   = timeAfter; % after stimulation (sec) , only use positive value
    cfg.implicitref         = [];  % all zeros reference because ref not in file
    cfg                     = ft_definetrial(cfg);
    cfg.method              = 'trial';
    lead_II = ft_preprocessing(cfg);
    
    %% START LOOPING THROUGH TRIALS
    
    % Create an output table for each participant
    trialN = length(lead_II.trial);
    cols = 3+(length(xq));
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
            cfg.channel    = 'EXG2';
            cfg.thresh     = 3;
            cfg.plotthresh = 'no';  % allowing the user to edit the threshold
            cfg.plotbeat   = 'no';  % see template HB
            cfg.plotcorr   = 'no';  % a figure with all heart beats is shown. The user is asked whether or not they want to change the threshold of the correlation. In last resort, outlier heart beats (based on interbeat interval) can be remodeled.
            cfg.plotfinal  = 'no';
            cfg.lpfilter   = 'yes';
            cfg.lpfreq     = 30;
            [HeartBeats]   = heart_peak_detect(cfg,lead_II);
            
            %% Retrieve R peaks
            % more info with [HeartBeats.R_sample] or [HeartBeats.R_time]
            
            % R-peaks list
            R_samples = [HeartBeats.R_sample];
            R_times = [HeartBeats.R_time];
            
            %% Transform to RR intervals
            % We calculate the time between each beat and the previous
            %RR = diff(sel_beats)/lead_II.fsample;  % (!WE LOSE THE FIRST BEAT!)
            RR = diff(R_samples)/lead_II.fsample;  % (!WE LOSE THE FIRST BEAT!)
            BPM = 60./RR;  % Convert to BPM units
                      
            % Check number of beats detected
            % 10 would be the minimum for 43 BPM min and 14 seconds time window
            assert(length(BPM) > 10)
            
            %% Outliers
            % Remove RR greater or smaller than 0.45s - 1.40s
            low_limit = 43; %1.4s RR
            high_limit = 133; %0.45s RR
            BPM((BPM< low_limit) | (BPM > high_limit)) = nan;
            
            % Now check for other outliers based on MEDIAN ABSOLUTE
            % DEVIATION (this sets a maximum deviance around median)
            % Median +- 30 BPMB
            BPM_med = median(BPM);
            %BPM_dev = BPM_med/2;  % a proportion of the median or
            BPM_dev = 30; % an absolute value
            BPM((BPM>BPM_med+BPM_dev) | (BPM<BPM_med-BPM_dev)) = nan;
            
            % check if number of NaN is > X and throw error otherwise
            % which goes directly to catch
            max_rej = 2;
            assert(sum(isnan(BPM)) < max_rej)
            
            
            %% Interpolation of RR intervals (1-D interpolation)
            
            %x = sel_times(2:end);  % sample points (e.g. time), we ignore the first to match size of RR
            x = R_times(2:end);  % sample points (e.g. time), we ignore the first to match size of RR
            v = BPM;  % corresponding values
            %sr = 10;  % Sampling rate of upsamples/interpolated data
            interpolated = interp1(x,v,xq,'spline');
            %plot(x,60./v,'o',xq,60./y,':.') % With RR values
            %plot(x,v,'o',xq,y,':.') % With RR values
            
            %y = interp(data,srOutput)  % Another simpler way to upsample
            % https://nl.mathworks.com/matlabcentral/answers/146575-best-interpolation-for-rr-intervals
            
            
            %% Save  data
            % Add to table  (row, column)
            outputTable(thisTrial, 1) = thisSubj;  % static
            outputTable(thisTrial, 2) = thisTrial;  % static
            outputTable(thisTrial, 3) = lead_II.trialinfo(thisTrial,1);  % trigger value
            outputTable(thisTrial, 4:cols) = interpolated;  % add the 10 RR to the table
            
        catch
            % If peaks not found (e.g. faulty recording), continue
            warning('Not enough R peaks found')
            disp(thisTrial)
            
            try % Try again, this time with manual selection
                % detect heart peaks P Q R S T.
                % Everything is based on detecting the R peaks.
                cfg            = [];
                cfg.trials     = thisTrial;
                cfg.channel    = 'EXG2';
                cfg.thresh     = 3;
                cfg.plotthresh = 'yes';  % allowing the user to edit the threshold
                cfg.plotbeat   = 'no';  % see template HB
                cfg.plotcorr   = 'yes';  % a figure with all heart beats is shown. The user is asked whether or not they want to change the threshold of the correlation. In last resort, outlier heart beats (based on interbeat interval) can be remodeled.
                cfg.plotfinal  = 'no';
                cfg.lpfilter   = 'yes';
                cfg.lpfreq     = 30;
                [HeartBeats]   = heart_peak_detect(cfg,lead_II);
                
                %% Retrieve R peaks
                % more info with [HeartBeats.R_sample] or [HeartBeats.R_time]
                
                % R-peaks list
                R_samples = [HeartBeats.R_sample];
                R_times = [HeartBeats.R_time];
                
                %% Transform to RR intervals
                % We calculate the time between each beat and the previous
                %RR = diff(sel_beats)/lead_II.fsample;  % (!WE LOSE THE FIRST BEAT!)
                RR = diff(R_samples)/lead_II.fsample;  % (!WE LOSE THE FIRST BEAT!)
                BPM = 60./RR;  % Convert to BPM units
                
                % Check number of beats detected
                % 10 would be the minimum for 43 BPM min and 14 seconds time window
                assert(length(BPM) > 10)
                
                %% Outliers
                % Remove RR greater or smaller than 0.45s - 1.40s
                low_limit = 43; %1.4s RR
                high_limit = 133; %0.45s RR
                BPM((BPM< low_limit) | (BPM > high_limit)) = nan;
                
                % Now check for other outliers based on MEDIAN ABSOLUTE
                % DEVIATION (this sets a maximum deviance around median)
                % Median +- 30 BPMB
                BPM_med = median(BPM);
                %BPM_dev = BPM_med/2;  % a proportion of the median or
                BPM_dev = 30; % an absolute value 
                BPM((BPM>BPM_med+BPM_dev) | (BPM<BPM_med-BPM_dev)) = nan;
                
                % check if number of NaN is > X and throw error otherwise
                % which goes directly to catch
                max_rej = 2;
                assert(sum(isnan(BPM)) < max_rej)
                    
                %% Interpolation of RR intervals (1-D interpolation)
                
                %x = sel_times(2:end);  % sample points (e.g. time), we ignore the first to match size of RR
                x = R_times(2:end);  % sample points (e.g. time), we ignore the first to match size of RR
                v = BPM;  % corresponding values
                %sr = 10;  % Sampling rate of upsamples/interpolated data
                interpolated = interp1(x,v,xq,'spline');
                %plot(x,60./v,'o',xq,60./y,':.') % With RR values
                %plot(x,v,'o',xq,y,':.') % With RR values
                
                %y = interp(data,srOutput)  % Another simpler way to upsample
                % https://nl.mathworks.com/matlabcentral/answers/146575-best-interpolation-for-rr-intervals
                
                
                %% Save  data
                % Add to table  (row, column)
                outputTable(thisTrial, 1) = thisSubj;  % static
                outputTable(thisTrial, 2) = thisTrial;  % static
                outputTable(thisTrial, 3) = lead_II.trialinfo(thisTrial,1);  % trigger value
                outputTable(thisTrial, 4:cols) = interpolated;  % add the 10 RR to the table

            catch
                %% Save  data
                % Add to table  (row, column)
                outputTable(thisTrial, 1) = thisSubj;  % static
                outputTable(thisTrial, 2) = thisTrial;  % static
                outputTable(thisTrial, 3) = lead_II.trialinfo(thisTrial,1);  % trigger value
                outputTable(thisTrial, 4:cols) = NaN(1,(length(xq)));  % add NaN
            end
        end
        
        
    end
    %% Save this participant
    % Set filename
    csvOutFilename = strcat(destinDir, 'ecg_interp_P', num2str(thisSubj),'_', datestr(now, 30), '.csv');
    % Save
    csvwrite(csvOutFilename, outputTable)
    
end
