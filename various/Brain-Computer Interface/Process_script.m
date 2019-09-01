+++%% INITIALIZE

% Clear the workspace and the screen
sca;
clearvars; % supprime toutes les variabls creees precedemment
close all; % ferme toutes les fenetres ouvertes precedemment

NomExperience = 'BCI_IntentionalBinding_v1';

SsID = input ('Nom et prénom participant:  ','s');
SsNum = input ('Numero participant:  ','s');
age = input ('Age: ', 's');
lat = input ('lateralite? (droite[1], gauche[2])  ', 's');

disp('  ')

% Double-check info

disp(['L''experience commence pour le sujet ' SsID ]); %disp pour afficher
ok = input ('Est-ce correct ? oui [1] or non [0]: ', 's');
if ~strcmp(ok,'1') %L'exp s'arr?Áte si on ne comfirme pas.
    disp('Experience annulee')
    return
end

% Output file name

fileNamePs = strcat(NomExperience, '_Participant_', SsNum, '_', SsID, '.txt');

% Make sure file does not exist yet

if exist (fileNamePs,'file')
    ok = input ('Attention, le fichier '' fileNamePs '' existe deja. L''ecraser ? Oui [o] ou Non [n]: ', 's');
    if ~strcmp(ok,'o')%L'expérience  s'arrète si on ne comfirme pas.
        disp('Experience annulee')
        return
    end
end

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');
screenNumber = max(screens); % xternal screen if available

% Define colors
white = WhiteIndex(screenNumber);
black = BlackIndex(screenNumber);
grey = 0.95; % value between 0 and 1 for PsychImaging
rectColor = black;

% Open an on screen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey);

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

% Draw the empty rect to the screen
Screen('FrameOval', window, rectColor, centeredRect, 8);
Screen('Flip', window);

% Initialize PsychSound
InitializePsychSound(1);

% Initialize variables
Ivls = [0.2,0.5,0.8];
WaitSecs(0.3) % Access the MEX file here to save time later;
Ivl = [];
realIvl = [];
keyInput = {};

% Open text file
fid = fopen('fileNamePs.txt','at');

%% PROCESS

OVgetStimulation. - -- --- -- -- - - - - - -  -- - - - -

stim 0 = 0;
stim 1 = 1;

if stimulation == 0
    
    Do Nothing (screen should already be fliped to 'empty' in Initialize)
    
elseif stimulation == 1
    
    % Fill the circle
    Screen('FillOval', window, rectColor, centeredRect, maxDiameter);
    Screen('Flip', window);
    
    WaitSecs(0.2)
    curtime= GetSecs;
    
    % Empty the circle
    Screen('FrameOval', window, rectColor, centeredRect, 8);
    Screen('Flip', window);
    
    % Wait a random interval
    Ivl = randsample(Ivls,1); % call = ~0-8ms
    WaitSecs(Ivl)
    
    % Play the beep (call = ~35 ms)
    Beeper(250,0.4,0.2)
    
    % Curtime 2
    realIvl = (GetSecs - curtime)+0.2; % I add the circle-time because if I measure curtime before the circle, I get jitter from the call?
    
    % Get participant's estimation
    
        ImageRec=imread('instructionsPencil.jpg'); %Instructions
    
        % Position Instructions
    
        xx = 391;
        yy = 385;

        x1 = round(width/2-xx/2);
        x2 = round(width/2+xx/2);
        y1 = round(height/3-yy/2);
        y2 = round(height/3+yy/2);
    
        % Get response

        Screen('Putimage', window, ImageRec, [x1, y1, x2, y2])
        reply=Ask(window,'Estimation de lintervalle :  ',[],[],'GetChar',[200, 550, x2, y2],[],22);
        Screen(window, 'Flip')
        WaitSecs(0.1)

        keyInput = str2num(reply);
    
    % Wait for a key press
    KbStrokeWait;
    
    % Write in text file
    C = ['ParticipantNumber', 'TrialNumber', 'Random Interval, ''Estimated Interval', 'Real Interval' ];% column names
    P = [SsID, TrNum, Ivl, keyInput, realIvl];
    fprintf(fid,'%s\t%s\t%s\t%s\t%s\n', C);
    fprintf(fid,'%s\t%s\t%.1f\t%.4f\t%.4f\n', P);
    
    % WaitSecs(0.3)
    
    % Draw the empty rect back to the screen
    Screen('FrameOval', window, rectColor, centeredRect, 8);
    Screen('Flip', window);
    
    WaitSecs(0.3)
    
end




%% UNINITIALIZE

% Close text file
fclose(fid);

% Close PsychAudio

% Clear the screen
sca;
