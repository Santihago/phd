cd C:\Users\ULB\Desktop\Santiago\experiment_IB\matlab_scripts
addpath(genpath('C:\Users\ULB\Documents\BCILAB-master\dependencies\liblsl-Matlab'))

% Title  : ASYNCHRONOUS BCI BASED ON EEG POWER, WITH AN INTENTIONAL BINDING
%          QUESTION ON EVERY TRIAL
% Date   : August 2016
% Author : Santiago Munoz Moldes, ULB

% This script receives stimulations from OpenVibe through the labStreamingLayer.
% It needs a separate session of Openvibe with
% an active online scenario. 

%#ok<*ST2NM> % Remove these warnings

%% INITIALIZE

% Clear the workspace and the screen
sca;
clear all;
close all;

% Experiment Info
%Type = 'bci'; %and not keyboard
ExperimentInfo.Name = 'BCI_IntentionalBinding';
ts=fix(clock);
ExperimentInfo.Date = sprintf('%02d-%02d-%d_%02d-%02d-%02d', ts(3), ts(2), ts(1), ts(4), ts(5), ts(6));
ExperimentInfo.Ethics = 'ULB 054/2015';

% Adjustable variables
ntrials = 40;
Intervals = [0.2,0.5,0.8]; % in seconds
trialTime = 120; % in seconds
targetStim = 33024; % 'OVTK_StimulationId_Label_00', the stimulation received from OpenVibe


% Initialize variables to save time later
WaitSecs(0.3) % Access the WaitSecs MEX file here to save time later;
test = GetSecs; % Access the WaitSecs MEX file here to save time later;
Interval = [];
realInterval = [];
keyInput = {};

% Some Keyboard settings
KbName('UnifyKeyNames');

% Disable sync tests
Screen('Preference', 'SkipSyncTests', 1)
% Disable all visual alerts
Screen('Preference','VisualDebugLevel', 0);
% Disable all output to the command window
Screen('Preference','SuppressAllWarnings', 1);

ID = input ('Nom et prénom participant:  ','s');
Num = input ('Numero participant:  ','s');
age = input ('Age: ', 's');
lat = input ('lateralite? (droite[1], gauche[2])  ', 's');
session = input ('Session Nr.:  ', 's');

disp('  ')

% Double-check info

disp(['Experiment is about to start for ' ID ]); %disp pour afficher
ok = input ('Is it correct ? yes [1] or no [0]: ', 's');
if ~strcmp(ok,'1') %L'exp s'arrete si on ne comfirme pas.
    disp('Experience annulee')
    return
end

% Output file name

fileNamePs = strcat(ExperimentInfo.Name, '_ID_', Num, '_', ID, 'session', session, '_', ExperimentInfo.Date, '.txt');

% Make sure file does not exist yet

if exist (fileNamePs,'file')
    ok = input ('WARNING: file '' fileNamePs '' already exists. Overwrite ? Yes [y] ou No [n]: ', 's');
    if ~strcmp(ok,'y')%Experiment stops if no response.
        disp('Experiment cancelled.')
        return
    end
end

% Open text file %'at' will append data at the end, 'wt' overwrites
fid = fopen(fileNamePs,'wt');
% fprintf(fid,'%s tested the %s at %s. \n',...
%     ID, ExperimentInfo.Date, ExperimentInfo.Location);
fprintf(fid,'%s, %s, %s, %s, %s\n',...
    'ParticipantNumber', 'TrialNumber', 'RandomInterval', 'RealInterval', 'EstimatedInterval');
fclose(fid);

%% PREPARE LAB STREAMING LAYER

% Instantiate the library
disp('Loading the library...');
lib = lsl_loadlib();

% resolve a stream...
disp('Resolving a Markers stream...');
result = {};
while isempty(result)
    result = lsl_resolve_byprop(lib,'type','Markers'); end

% create a new inlet
disp('Opening an inlet...');
inlet = lsl_inlet(result{1});


%% Psychtoolbox Sound Setup
InitializePsychSound(1);
nrchannels = 2;
freq = 48000;
beepLengthSecs = 0.2;
pahandle = PsychPortAudio('Open', [], 1, [], freq, nrchannels, [], 0.015);
PsychPortAudio('Volume', pahandle, 0.5);
myBeep = MakeBeep(500, beepLengthSecs, freq);

% Testing sound to start the ASIO4ALL sound driver
disp('Testing sound....')
PsychPortAudio('FillBuffer', pahandle, [myBeep; myBeep]); %biaural
PsychPortAudio('Start', pahandle);
WaitSecs(5);

%% Psychtolbox Screen Setup

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');
screenNumber = max(screens); % xternal screen if available

% Define colors
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
darkgrey = 0.90; % value between 0 and 1 for PsychImaging
lightgrey = 0.97;
rectColor = black;

% ONLY FOR DEBUGGING!!!!
% first argument allows mouse to click behind the screen
% PsychDebugWindowConfiguration(0, 0.5)

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, lightgrey);

% Get the size of the on screen window
[screenXpixels, screenYpixels] = Screen('WindowSize', window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Make a base Rect of 200 by 250 pixels
baseRect = [0 0 200 200];

% For ovals we set a miximum diameter up to which it is perfect for
maxDiameter = max(baseRect) * 1.01;

% Center the rectangle on the centre of the screen
centeredRect = CenterRectOnPointd(baseRect, xCenter, yCenter);

% Show instruction images and wait for response after each image
instructions1=imread('InstructionsBCIIB_1_EN.jpg');
instructions1Texture= Screen('MakeTexture', window, instructions1);
Screen('DrawTexture', window, instructions1Texture, [],[],0);
Screen(window, 'Flip');
KbWait;
WaitSecs(0.3);

instructions2=imread('InstructionsBCIIB_2_EN.jpg');
instructions2Texture= Screen('MakeTexture', window, instructions2);
Screen('DrawTexture', window, instructions2Texture, [],[],0);
Screen(window, 'Flip');
KbWait;
WaitSecs(0.3);

instructions3=imread('InstructionsBCIIB_3_EN.jpg');
instructions3Texture= Screen('MakeTexture', window, instructions3);
Screen('DrawTexture', window, instructions3Texture, [],[],0);
Screen(window, 'Flip');
KbWait;
WaitSecs(0.3);

%% Draw the empty circle to the screen
Screen('FrameOval', window, darkgrey, centeredRect, 8); % Circle color is washed out, to indicate that trial has not started
Screen('Flip', window);

WaitSecs(2);

for trial = 1:ntrials
    
    Interval = randsample(Intervals,1); % call = ~0-8ms
    
    %1. Circle appears but in grey with letters on top
    Screen('FrameOval', window, darkgrey, centeredRect, 8);
    DrawFormattedText(window, 'Trial starting in 3 seconds.', 'center', screenYpixels * 0.20, black);
    Screen('Flip', window);
    WaitSecs(1);
    Screen('FrameOval', window, darkgrey, centeredRect, 8);
    DrawFormattedText(window, 'Trial starting in 2 seconds..', 'center', screenYpixels * 0.20, black);
    Screen('Flip', window);
    WaitSecs(1);
    Screen('FrameOval', window, darkgrey, centeredRect, 8);
    DrawFormattedText(window, 'Trial starting in 1 seconds...', 'center', screenYpixels * 0.20, black);
    Screen('Flip', window);
    WaitSecs(1);
    
    %2. Change color of circle to black, to mark beginning of trial
    Screen('FrameOval', window, black, centeredRect, 8);
    Screen('Flip', window) ;
    
    % Clean stim queue
    flushinput(t)
    
    curTime = GetSecs;
    while true
        %2. Start counting time
        if GetSecs-curTime <= trialTime % How much time has elapsed
            disp('Now receiving data...');
            % get data from the inlet
            [mrks,ts] = inlet.pull_sample();
            % and display it
            fprintf('got %d at time %.5f\n',mrks(1),ts);
            
            readStim = mrks;
            
             if (targetStim==readStim)==~1                          
                continue;
            elseif (target==readStim)==1  % If stimulation is received
                
                % TIMER START
                startInterval= GetSecs;
                
                %4.  Fill the circle
                Screen('FillOval', window, black, centeredRect, maxDiameter);
                Screen('Flip', window);
                
                WaitSecs(0.2)
                
                %3.  Empty the circle
                Screen('FrameOval', window, rectColor, centeredRect, 8);
                Screen('Flip', window);
                
                %4.  Wait the random interval
                WaitSecs(Interval);
                
                %5.  Play the beep
                PsychPortAudio('FillBuffer', pahandle, [myBeep; myBeep]);
                PsychPortAudio('Start', pahandle);
                WaitSecs(0.2);
                
                % Timer END
                realInterval = (GetSecs - startInterval)-0.4;
                % The logic here is that by measuring before the screen and after the beep and
                % removing both durations, I account for the jitter of both
                
                % Wait some random time
                WaitSecs(randi([1800,2600])/1000);
                
                % Position instructions
                
                xx = 391;
                yy = 385;
                x2 = round(screenXpixels/2+xx/2);
                y2 = round(screenYpixels/3+yy/2);
                
                % Get response
                
                tstring = 'Use the numbers on the keyboard to estimate \n \n the interval in miliseconds (1-1000) between \n \n the action and the beep:';
                DrawFormattedText(window, tstring, 'center', screenYpixels * 0.20, black);
                FlushEvents('keyDown')
                reply=Ask(window,'Interval estimation :  ',[],[],'GetChar',[200, 550, x2, y2],[],22);
                Screen(window, 'Flip');
                WaitSecs(0.1);
                
                keyInput = str2double(reply);
                
                % Write in text file
                realInterval = realInterval * 1000; % to get in ms
                Interval = Interval * 1000;
                NumID = str2num(Num);
                P = [ NumID, trial, Interval, realInterval, keyInput];
                fid = fopen(fileNamePs,'at');
                fprintf(fid,'\n%d,%d,%.4g,%.4g,%d', P);
                fclose(fid);
                
                WaitSecs(0.1);
                
                % Draw the empty rect back to the screen
                Screen('FrameOval', window, darkgrey, centeredRect, 8);
                Screen('Flip', window);
                
                WaitSecs(1.5);
                
                break;
                
            end
            break;
        end
        break;
    end
    
end

%% Wrap it up

sca;
PsychPortAudio('Stop', pahandle);
PsychPortAudio('Close', pahandle);
disp('DONE!');