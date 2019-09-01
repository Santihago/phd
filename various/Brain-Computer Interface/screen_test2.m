
w=Screen('OpenWindow', 0);
cycleRefresh=Screen('GetFlipInterval', w); 
[width, height]=Screen('WindowSize', w);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Get color
color = [0 0 0];
centeredRect = CenterRectOnPointd(baseRect, xCenter, yCenter);

% Draw the rect to the screen
Screen('FillOval', w, color, centeredRect);

% Flip to the screen
Screen('Flip', w);

% Wait for a key press
[secs, keyCode, deltaSecs]=KbWait

% Clear the screen
sca;