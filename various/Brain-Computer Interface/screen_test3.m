% Clear the workspace and the screen
sca;
close all;
clearvars;

% Here we call some default settings for setting up Psychtoolbox
PsychDefaultSetup(2);

% Get the screen numbers
screens = Screen('Screens');

% Draw to the external screen if avaliable
screenNumber = max(screens);

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

% For Ovals we set a miximum diameter up to which it is perfect for
maxDiameter = max(baseRect) * 1.01;

% Center the rectangle on the centre of the screen
centeredRect = CenterRectOnPointd(baseRect, xCenter, yCenter);

penWidth = 1;
penHeight = 1;

% Draw the rect to the screen
Screen('FrameOval', window, rectColor, centeredRect, 8);
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Draw the rect to the screen
Screen('FillOval', window, rectColor, centeredRect, maxDiameter);
Screen('Flip', window);

% Wait for a key press
KbStrokeWait;

% Clear the screen
sca;