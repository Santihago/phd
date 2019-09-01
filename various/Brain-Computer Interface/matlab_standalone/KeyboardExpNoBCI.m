cd C:\Users\ULB\Desktop\Santiago\experiment_IB\matlab_scripts\behavioral

% Title  : KEYBOARD INTENTIONAL BINDING
% Date   : May 2016
% Author : Santiago Munoz Moldes, ULB

%#ok<*ST2NM> % Remove these warnings

%% A1. INITIALIZE

% Clear the workspace and the screen
sca;
clear all;
close all;

% Experiment Info
%Type = 'keyboard'; %and not keyboard
ExperimentInfo.Name = 'Keyboard_IntentionalBinding';
ts=fix(clock);
ExperimentInfo.Date = sprintf('%02d-%02d-%d_%02d-%02d-%02d', ts(3), ts(2), ts(1), ts(4), ts(5), ts(6));
ExperimentInfo.Location = 'ULB labs in Brussels';

% Adjustable variables
% nblocks = 2;
ntrials = 40; % The total number of trials
Intervals = [0.2,0.5,0.8]; % All three possible intervals: 200ms, 500ms, 800ms
trialTime = 120; % Allowed response time for each trial: 2 minutes

% Initialize variables to save time later
WaitSecs(0.3) % Access the WaitSecs MEX file here to save time later;
test = GetSecs; % Access the GetSecs MEX file here to save time later;
Interval = [];
realInterval = [];
keyInput = {};

%% A2. SPECIAL SETTINGS
% Disable all sync tests and warnings 

% Disable sync tests
Screen('Preference', 'SkipSyncTests', 1)
% Disable all visual alerts
Screen('Preference','VisualDebugLevel', 0);
% Disable all output to the command window
Screen('Preference','SuppressAllWarnings', 1);

%% A3. PARTICIPANT INFORMATION AND OUTPUT FILE

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

%% A4. PSYCHTOOLBOX SOUND SETTINGS

InitializePsychSound(1);
nrchannels = 2;
freq = 48000;
beepLengthSecs = 0.2;
pahandle = PsychPortAudio('Open', [], 1, [], freq, nrchannels, [], 0.015);
PsychPortAudio('Volume', pahandle, 0.5);
myBeep = MakeBeep(500, beepLengthSecs, freq);

% Test sound to start the ASIO4ALL DRIVER
disp('Testing sound....')
PsychPortAudio('FillBuffer', pahandle, [myBeep; myBeep]); %biaural
PsychPortAudio('Start', pahandle);
WaitSecs(5);

%% A5. PSYCHTOOLBOX SCREEN SETTINGS

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

% For debugging only!!!!
% opaqueforHID allows mouse to click behind the screen
%PsychDebugWindowConfiguration(0, 0.5)

% Open an on screen window % background color
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

%% A6. SHOW INSTRUCTIONS (images) and wait for response after each image

instructions1=imread('InstructionsBCIIB_1_EN.jpg');
instructions1Texture= Screen('MakeTexture', window, instructions1);
Screen('DrawTexture', window, instructions1Texture, [],[],0);
Screen(window, 'Flip');
KbWait;
WaitSecs(0.3)

instructions2=imread('InstructionsBCIIB_2_EN.jpg');
instructions2Texture= Screen('MakeTexture', window, instructions2);
Screen('DrawTexture', window, instructions2Texture, [],[],0);
Screen(window, 'Flip');
KbWait;
WaitSecs(0.3)

instructions3=imread('InstructionsBCIIB_3_EN.jpg');
instructions3Texture= Screen('MakeTexture', window, instructions3);
Screen('DrawTexture', window, instructions3Texture, [],[],0);
Screen(window, 'Flip');
KbWait;
WaitSecs(0.3)

%% B.1 START EXPERIMENT

% Draw the empty circle to the screen
Screen('FrameOval', window, darkgrey, centeredRect, 8); % Circle color is washed out, to indicate that trial has not started
Screen('Flip', window);

WaitSecs(2)

% START TRIAL LOOP
for trial = 1:ntrials
    Interval = randsample(Intervals,1); % Set the interval for the trial
    
    %B2. Circle appears in grey, with letters on top
    Screen('FrameOval', window, darkgrey, centeredRect, 8);
    DrawFormattedText(window, 'Trial starting in 3 seconds.', 'center', screenYpixels * 0.20, black);
    Screen('Flip', window)
    WaitSecs(1)
    Screen('FrameOval', window, darkgrey, centeredRect, 8);
    DrawFormattedText(window, 'Trial starting in 3 seconds..', 'center', screenYpixels * 0.20, black);
    Screen('Flip', window)
    WaitSecs(1)
    Screen('FrameOval', window, darkgrey, centeredRect, 8);
    DrawFormattedText(window, 'Trial starting in 3 seconds...', 'center', screenYpixels * 0.20, black);
    Screen('Flip', window)
    WaitSecs(1)
    
    %B3. Change color of circle to black, to mark beginning of trial
    Screen('FrameOval', window, black, centeredRect, 8);
    Screen('Flip', window)
    
    curTime = GetSecs;
    while true
        %B4. Start counting time for trial
        if GetSecs-curTime <= trialTime % How much time has elapsed
            [keyIsDown, secs, keyCode, deltaSecs]=KbCheck;
            if strcmp(KbName(keyCode), 'n')==~1
                continue;
            elseif strcmp(KbName(keyCode), 'n')==1 % If 'n' is pressed
                
                % TIMER START
                startInterval= GetSecs;
                
                %4.  Fill the circle
                Screen('FillOval', window, black, centeredRect, maxDiameter);
                Screen('Flip', window);
                
                WaitSecs(0.2)
                
                %3.  Empty the circle
                Screen('FrameOval', window, rectColor, centeredRect, 8);
                Screen('Flip', window);
                
                %4.  Wait a random interval
                WaitSecs(Interval);
                
                %5.  Play the beep
                PsychPortAudio('FillBuffer', pahandle, [myBeep; myBeep]);
                PsychPortAudio('Start', pahandle);
                WaitSecs(0.2);
                
                % Timer END
                realInterval = (GetSecs - startInterval)-0.4;
                % The logic here is that by measuring before the screen and after the beep and
                % removing both durations, I account for the jitter of both
                
                % Wait some time
                WaitSecs(randi([1800,2600])/1000);
                
                % Position instructions
                
                xx = 391;
                yy = 385;
                x2 = round(screenXpixels/2+xx/2);
                y2 = round(screenYpixels/3+yy/2);
                
                % Get response
                
                tstring = 'Use the numbers on the keyboard to estimate \n \n the interval in miliseconds (1-1000) between \n \n the action and the beep:';
                DrawFormattedText(window, tstring, 'center', screenYpixels * 0.20, black);
                reply=Ask(window,'Interval estimation (SHIFT + NUM) :  ',[],[],'GetChar',[200, 550, x2, y2],[],22);
                Screen(window, 'Flip');
                WaitSecs(0.1)
                
                keyInput = str2double(reply);
                
                % Write in text file
                realInterval = realInterval * 1000; % to get in ms
                Interval = Interval * 1000;
                NumID = str2num(Num);
                P = [NumID, trial, Interval, realInterval, keyInput];
                fid = fopen(fileNamePs,'at');
                fprintf(fid,'\n%d,%d,%.4g,%.4g,%d', P);
                fclose(fid);
                
                WaitSecs(0.1)
                
                % Draw the empty rect back to the screen
                Screen('FrameOval', window, darkgrey, centeredRect, 8);
                Screen('Flip', window);
                
                WaitSecs(1.5)
                
                break;
                
            end
            break;
        end
        break;
    end
    
end

%% Wrap it up

sca
PsychPortAudio('Stop', pahandle)
PsychPortAudio('Close', pahandle)
disp('DONE!')
