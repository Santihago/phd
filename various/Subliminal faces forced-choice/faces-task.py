#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.84.2),
    on Mon May  8 15:30:11 2017
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'heart_task'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='#B8B8B8', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "instruction"
instructionClock = core.Clock()
Consigne = visual.TextStim(win=win, name='Consigne',
    text=u"Deux visages vous seront pr\xe9sent\xe9s rapidement, de sorte que l'un des deux restera cach\xe9. Vous devrez indiquer si le visage cach\xe9 \xe9tait neutre ou \xe9motionnel. \n\nPour r\xe9pondre, soyez attentifs \xe0 vos ressentis corporels. Certains visages pourraient avoir une influence l\xe9g\xe8re sur votre rythme cardiaque.\n\nSi vous ne savez pas, essayez de deviner.",
    font='Arial',
    pos=(0, 0), height=20, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "trial"
trialClock = core.Clock()
# Import functions from heart_santi.py
import heart_santi


# Start the monitor (will connect to 'COM4')
Monitor = heart_santi.Heart_Monitor()


# FOR ITI JITTERING

# define relevant parameters:
min_duration = 10  # number of frames
max_duration = 60  #  4 seconds at 60 Hz
number_of_trials = 96

# get an array of random integers:
ITIs = randint(low=min_duration, high=max_duration + 1, size=number_of_trials)

# convert from a numpy array to a standard Python list if preferred:
ITIs = list(ITIs) 


ITI = visual.TextStim(win=win, name='ITI',
    text='Any text\n\nincluding line breaks',
    font='Arial',
    pos=(0, 0), height=1.0, wrapWidth=None, ori=0, 
    color=1.0, colorSpace='rgb', opacity=1,
    depth=-3.0);
fixation = visual.TextStim(win=win, name='fixation',
    text=u'\u2022',
    font='Arial',
    pos=(0, 0), height=40, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-4.0);
scrambled = visual.ImageStim(
    win=win, name='scrambled',
    image='noise_face1_image2.jpg', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
subliminal = visual.ImageStim(
    win=win, name='subliminal',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)
neutral = visual.ImageStim(
    win=win, name='neutral',
    image='sin', mask=None,
    ori=0, pos=(0, -15), size=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)
text_2 = visual.TextStim(win=win, name='text_2',
    text='Visage neutre (i) \n\nou\n\nvisage emotionnel (o)',
    font='Arial',
    pos=(0, 0), height=20, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-8.0);

# Initialize components for Routine "end"
endClock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='Merci!',
    font='Arial',
    pos=(0, 0), height=20, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instruction"-------
t = 0
instructionClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_3 = event.BuilderKeyResponse()
# keep track of which components have finished
instructionComponents = [Consigne, key_resp_3]
for thisComponent in instructionComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instruction"-------
while continueRoutine:
    # get current time
    t = instructionClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Consigne* updates
    if t >= 0.0 and Consigne.status == NOT_STARTED:
        # keep track of start time/frame for later
        Consigne.tStart = t
        Consigne.frameNStart = frameN  # exact frame index
        Consigne.setAutoDraw(True)
    
    # *key_resp_3* updates
    if t >= 0.0 and key_resp_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_3.tStart = t
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_3.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_3.keys = theseKeys[-1]  # just the last key pressed
            key_resp_3.rt = key_resp_3.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instruction"-------
for thisComponent in instructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
    key_resp_3.keys=None
thisExp.addData('key_resp_3.keys',key_resp_3.keys)
if key_resp_3.keys != None:  # we had a response
    thisExp.addData('key_resp_3.rt', key_resp_3.rt)
thisExp.nextEntry()
# the Routine "instruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trialLoop = data.TrialHandler(nReps=2, method='fullRandom', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('stimuli_micah.xlsx'),
    seed=None, name='trialLoop')
thisExp.addLoop(trialLoop)  # add the loop to the experiment
thisTrialLoop = trialLoop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
if thisTrialLoop != None:
    for paramName in thisTrialLoop.keys():
        exec(paramName + '= thisTrialLoop.' + paramName)

for thisTrialLoop in trialLoop:
    currentLoop = trialLoop
    # abbreviate parameter names if possible (e.g. rgb = thisTrialLoop.rgb)
    if thisTrialLoop != None:
        for paramName in thisTrialLoop.keys():
            exec(paramName + '= thisTrialLoop.' + paramName)
    
    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    
    # get the next ITI (assuming they are in a list):
    current_ITI = ITIs.pop()
    
    # manually record the ITI in the data for this trial:
    thisExp.addData('ITI', current_ITI)
    
    ITI.setColor('white', colorSpace='rgb')
    ITI.setFont('Arial')
    ITI.setHeight(0.01)
    subliminal.setImage(Subliminal_face)
    neutral.setImage(Neutral_face)
    key_resp_2 = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [ITI, fixation, scrambled, subliminal, neutral, text_2, key_resp_2]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # Check the USB port for recorded heartbeats
        
        Monitor.listen_for_beat()
        
        if frameN == 1:  # -2s 
            Monitor.RR_intervals = ([])  # reset
        if frameN == 166:  # 0s 
            Beats, BPM = Monitor.summary()
            trialLoop.addData("Beats_Pre",Beats)
            trialLoop.addData("BPM_Pre",BPM)
            Monitor.RR_intervals = ([])  # reset
            
        if frameN == 167: 
            Monitor.RR_intervals = ([])  # reset
        if frameN == 413:   # +4s 
            Beats, BPM = Monitor.summary()
            trialLoop.addData("Beats_Post",Beats)
            trialLoop.addData("BPM_Post",BPM)
            Monitor.RR_intervals = ([])  # reset
        
        # *ITI* updates
        if frameN >= 0 and ITI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ITI.tStart = t
            ITI.frameNStart = frameN  # exact frame index
            ITI.setAutoDraw(True)
        if ITI.status == STARTED and frameN >= (ITI.frameNStart + current_ITI):
            ITI.setAutoDraw(False)
        
        # *fixation* updates
        if frameN >= 120 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        if fixation.status == STARTED and frameN >= (fixation.frameNStart + 30):
            fixation.setAutoDraw(False)
        
        # *scrambled* updates
        if frameN >= 150 and scrambled.status == NOT_STARTED:
            # keep track of start time/frame for later
            scrambled.tStart = t
            scrambled.frameNStart = frameN  # exact frame index
            scrambled.setAutoDraw(True)
        if scrambled.status == STARTED and frameN >= (scrambled.frameNStart + 15):
            scrambled.setAutoDraw(False)
        
        # *subliminal* updates
        if frameN >= 166 and subliminal.status == NOT_STARTED:
            # keep track of start time/frame for later
            subliminal.tStart = t
            subliminal.frameNStart = frameN  # exact frame index
            subliminal.setAutoDraw(True)
        if subliminal.status == STARTED and frameN >= (subliminal.frameNStart + 1):
            subliminal.setAutoDraw(False)
        
        # *neutral* updates
        if frameN >= 167 and neutral.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutral.tStart = t
            neutral.frameNStart = frameN  # exact frame index
            neutral.setAutoDraw(True)
        if neutral.status == STARTED and frameN >= (neutral.frameNStart + 6):
            neutral.setAutoDraw(False)
        
        # *text_2* updates
        if frameN >= 413 and text_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_2.tStart = t
            text_2.frameNStart = frameN  # exact frame index
            text_2.setAutoDraw(True)
        if text_2.status == STARTED and frameN >= (text_2.frameNStart + 180):
            text_2.setAutoDraw(False)
        
        # *key_resp_2* updates
        if frameN >= 413 and key_resp_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_2.tStart = t
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_2.status == STARTED and frameN >= (key_resp_2.frameNStart + 180):
            key_resp_2.status = STOPPED
        if key_resp_2.status == STARTED:
            theseKeys = event.getKeys(keyList=['i', 'o'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                key_resp_2.rt = key_resp_2.clock.getTime()
                # was this 'correct'?
                if (key_resp_2.keys == str(Correct)) or (key_resp_2.keys == Correct):
                    key_resp_2.corr = 1
                else:
                    key_resp_2.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys=None
        # was no response the correct answer?!
        if str(Correct).lower() == 'none':
           key_resp_2.corr = 1  # correct non-response
        else:
           key_resp_2.corr = 0  # failed to respond (incorrectly)
    # store data for trialLoop (TrialHandler)
    trialLoop.addData('key_resp_2.keys',key_resp_2.keys)
    trialLoop.addData('key_resp_2.corr', key_resp_2.corr)
    if key_resp_2.keys != None:  # we had a response
        trialLoop.addData('key_resp_2.rt', key_resp_2.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 2 repeats of 'trialLoop'

# get names of stimulus parameters
if trialLoop.trialList in ([], [None], None):
    params = []
else:
    params = trialLoop.trialList[0].keys()
# save data for this loop
trialLoop.saveAsExcel(filename + '.xlsx', sheetName='trialLoop',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
trialLoop.saveAsText(filename + 'trialLoop.csv', delim=',',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# ------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_4 = event.BuilderKeyResponse()
# keep track of which components have finished
endComponents = [text, key_resp_4]
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "end"-------
while continueRoutine:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if t >= 0.0 and text.status == NOT_STARTED:
        # keep track of start time/frame for later
        text.tStart = t
        text.frameNStart = frameN  # exact frame index
        text.setAutoDraw(True)
    
    # *key_resp_4* updates
    if t >= 0.0 and key_resp_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_4.tStart = t
        key_resp_4.frameNStart = frameN  # exact frame index
        key_resp_4.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_4.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_4.keys = theseKeys[-1]  # just the last key pressed
            key_resp_4.rt = key_resp_4.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_4.keys in ['', [], None]:  # No response was made
    key_resp_4.keys=None
thisExp.addData('key_resp_4.keys',key_resp_4.keys)
if key_resp_4.keys != None:  # we had a response
    thisExp.addData('key_resp_4.rt', key_resp_4.rt)
thisExp.nextEntry()
# the Routine "end" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()



# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
