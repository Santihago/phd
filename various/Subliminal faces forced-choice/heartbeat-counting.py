#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.84.2),
    on Mon May  8 15:29:50 2017
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
expName = 'Exp.battements'  # from the Builder filename that created this script
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
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "consg"
consgClock = core.Clock()
appuyer = visual.TextStim(win=win, name='appuyer',
    text="Dans cette tache, vous allez devoir compter vos propres battements. Vous devrez realiser cet exercice sans toucher votre pouls et sans utiliser d'autres indicateurs directs.\nSi vous n'arrivez pas a identifier vos battements, continuez a compter sur base de ce que vous supposez etre votre rythme cardiaque.\n\n\nAppuyez sur espace pour continuer.",
    font='Arial',
    pos=(0, 0), height=20, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);
# Load heart Arduino class
import heart_santi

# Start monitor (COM4)
Monitor = heart_santi.Heart_Monitor()



# Initialize components for Routine "consigne"
consigneClock = core.Clock()
Start = visual.TextStim(win=win, name='Start',
    text="Vous devez commencer a compter des que vous appuyez sur la barre d'espace. Vous devrez vous arretez des que l'experimentateur vous le dira.\n\nAppuyez sur espace des que vous etes pret(e).",
    font='Arial',
    pos=[0, 0], height=20, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "deux"
deuxClock = core.Clock()

blocNr = visual.TextStim(win=win, name='blocNr',
    text='default text',
    font='Arial',
    pos=(200, -200), height=15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
title = visual.TextStim(win=win, name='title',
    text='Block number (0-1-2-3-4):',
    font='Arial',
    pos=(-75, -200), height=15, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0);

polygon = visual.Rect(
    win=win, name='polygon',
    width=(50, 50)[0], height=(50, 50)[1],
    ori=0, pos=(-250, 200),
    lineWidth=1, lineColor=[1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-4.0, interpolate=True)
polygon_2 = visual.Rect(
    win=win, name='polygon_2',
    width=(50, 50)[0], height=(50, 50)[1],
    ori=0, pos=(-250, 200),
    lineWidth=1, lineColor=[1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-5.0, interpolate=True)
polygon_3 = visual.Rect(
    win=win, name='polygon_3',
    width=(50, 50)[0], height=(50, 50)[1],
    ori=0, pos=[-250,200],
    lineWidth=1, lineColor=[1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-6.0, interpolate=True)
polygon_4 = visual.Rect(
    win=win, name='polygon_4',
    width=(50, 50)[0], height=(50, 50)[1],
    ori=0, pos=(-250, 200),
    lineWidth=1, lineColor=[1.000,-1.000,-1.000], lineColorSpace='rgb',
    fillColor=[1.000,-1.000,-1.000], fillColorSpace='rgb',
    opacity=1, depth=-7.0, interpolate=True)

# Initialize components for Routine "response"
responseClock = core.Clock()
instr = visual.TextStim(win=win, name='instr',
    text='Ecrivez le nombre de battements que vous avez pu compter et appuyez ensuite sur Espace.',
    font='Arial',
    pos=[0, 0], height=20, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0);

# Initialize components for Routine "fin"
finClock = core.Clock()
end = visual.TextStim(win=win, name='end',
    text=u'Termin\xe9 ! ',
    font='Arial',
    pos=(0, 0), height=30, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "consg"-------
t = 0
consgClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
resp = event.BuilderKeyResponse()

# keep track of which components have finished
consgComponents = [appuyer, resp]
for thisComponent in consgComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "consg"-------
while continueRoutine:
    # get current time
    t = consgClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *appuyer* updates
    if t >= 0.0 and appuyer.status == NOT_STARTED:
        # keep track of start time/frame for later
        appuyer.tStart = t
        appuyer.frameNStart = frameN  # exact frame index
        appuyer.setAutoDraw(True)
    
    # *resp* updates
    if t >= 0.0 and resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        resp.tStart = t
        resp.frameNStart = frameN  # exact frame index
        resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            if resp.keys == []:  # then this was the first keypress
                resp.keys = theseKeys[0]  # just the first key pressed
                resp.rt = resp.clock.getTime()
                # a response ends the routine
                continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in consgComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "consg"-------
for thisComponent in consgComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if resp.keys in ['', [], None]:  # No response was made
    resp.keys=None
thisExp.addData('resp.keys',resp.keys)
if resp.keys != None:  # we had a response
    thisExp.addData('resp.rt', resp.rt)
thisExp.nextEntry()

# the Routine "consg" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
myblockloop = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='myblockloop')
thisExp.addLoop(myblockloop)  # add the loop to the experiment
thisMyblockloop = myblockloop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisMyblockloop.rgb)
if thisMyblockloop != None:
    for paramName in thisMyblockloop.keys():
        exec(paramName + '= thisMyblockloop.' + paramName)

for thisMyblockloop in myblockloop:
    currentLoop = myblockloop
    # abbreviate parameter names if possible (e.g. rgb = thisMyblockloop.rgb)
    if thisMyblockloop != None:
        for paramName in thisMyblockloop.keys():
            exec(paramName + '= thisMyblockloop.' + paramName)
    
    # ------Prepare to start Routine "consigne"-------
    t = 0
    consigneClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    start_key = event.BuilderKeyResponse()
    # keep track of which components have finished
    consigneComponents = [Start, start_key]
    for thisComponent in consigneComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "consigne"-------
    while continueRoutine:
        # get current time
        t = consigneClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *Start* updates
        if t >= 0.0 and Start.status == NOT_STARTED:
            # keep track of start time/frame for later
            Start.tStart = t
            Start.frameNStart = frameN  # exact frame index
            Start.setAutoDraw(True)
        
        # *start_key* updates
        if t >= 0.0 and start_key.status == NOT_STARTED:
            # keep track of start time/frame for later
            start_key.tStart = t
            start_key.frameNStart = frameN  # exact frame index
            start_key.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if start_key.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in consigneComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "consigne"-------
    for thisComponent in consigneComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "consigne" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "deux"-------
    t = 0
    deuxClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # Determine the block number and the number of target beats
    blNumber = myblockloop.thisN
    print(blNumber)
    if blNumber == 0:  # 0 indexed!!
        targetBeats = 150
    elif blNumber == 1:
        targetBeats = 120
    elif blNumber == 2:  # Stethoscope
        targetBeats = 140
    elif blNumber == 3:
        targetBeats = 130
    elif blNumber == 4:
        targetBeats = 100
    
    
    # Add trial info
    myblockloop.addData("targetBeats", targetBeats)
    blocNr.setText(blNumber)
    
    # keep track of which components have finished
    deuxComponents = [blocNr, title, polygon, polygon_2, polygon_3, polygon_4]
    for thisComponent in deuxComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "deux"-------
    while continueRoutine:
        # get current time
        t = deuxClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *blocNr* updates
        if t >= 0.0 and blocNr.status == NOT_STARTED:
            # keep track of start time/frame for later
            blocNr.tStart = t
            blocNr.frameNStart = frameN  # exact frame index
            blocNr.setAutoDraw(True)
        
        # *title* updates
        if t >= 0.0 and title.status == NOT_STARTED:
            # keep track of start time/frame for later
            title.tStart = t
            title.frameNStart = frameN  # exact frame index
            title.setAutoDraw(True)
        # Check Arduino each frame to see if heart beat
        Monitor.listen_for_beat()
        
        # Restart beat counts 
        if t == 1.5:
            Monitor.RR_intervals = [()]
        
        # Keep track of beats and stop routine if target achieved
        if t >= 1.5:
            Beats = Monitor.counting()
            print(Beats)
            if Beats >= targetBeats:
                Monitor.RR_intervals = [()]
                continueRoutine = False
        
        # *polygon* updates
        if t >= 1.5 and polygon.status == NOT_STARTED:
            # keep track of start time/frame for later
            polygon.tStart = t
            polygon.frameNStart = frameN  # exact frame index
            polygon.setAutoDraw(True)
        frameRemains = 1.5 + 3.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if polygon.status == STARTED and t >= frameRemains:
            polygon.setAutoDraw(False)
        
        # *polygon_2* updates
        if t >= 30 and polygon_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            polygon_2.tStart = t
            polygon_2.frameNStart = frameN  # exact frame index
            polygon_2.setAutoDraw(True)
        frameRemains = 30 + 3.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if polygon_2.status == STARTED and t >= frameRemains:
            polygon_2.setAutoDraw(False)
        
        # *polygon_3* updates
        if t >= 60 and polygon_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            polygon_3.tStart = t
            polygon_3.frameNStart = frameN  # exact frame index
            polygon_3.setAutoDraw(True)
        frameRemains = 60 + 3.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if polygon_3.status == STARTED and t >= frameRemains:
            polygon_3.setAutoDraw(False)
        
        # *polygon_4* updates
        if t >= 90 and polygon_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            polygon_4.tStart = t
            polygon_4.frameNStart = frameN  # exact frame index
            polygon_4.setAutoDraw(True)
        frameRemains = 90 + 3.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if polygon_4.status == STARTED and t >= frameRemains:
            polygon_4.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in deuxComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "deux"-------
    for thisComponent in deuxComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    # the Routine "deux" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "response"-------
    t = 0
    responseClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    battementsComptes = event.BuilderKeyResponse()
    spaceOK = event.BuilderKeyResponse()
    # keep track of which components have finished
    responseComponents = [battementsComptes, spaceOK, instr]
    for thisComponent in responseComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "response"-------
    while continueRoutine:
        # get current time
        t = responseClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *battementsComptes* updates
        if t >= 0.0 and battementsComptes.status == NOT_STARTED:
            # keep track of start time/frame for later
            battementsComptes.tStart = t
            battementsComptes.frameNStart = frameN  # exact frame index
            battementsComptes.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(battementsComptes.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if battementsComptes.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                battementsComptes.keys.extend(theseKeys)  # storing all keys
                battementsComptes.rt.append(battementsComptes.clock.getTime())
        
        # *spaceOK* updates
        if t >= 4 and spaceOK.status == NOT_STARTED:
            # keep track of start time/frame for later
            spaceOK.tStart = t
            spaceOK.frameNStart = frameN  # exact frame index
            spaceOK.status = STARTED
            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')
        if spaceOK.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False
        
        # *instr* updates
        if t >= 0.0 and instr.status == NOT_STARTED:
            # keep track of start time/frame for later
            instr.tStart = t
            instr.frameNStart = frameN  # exact frame index
            instr.setAutoDraw(True)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "response"-------
    for thisComponent in responseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if battementsComptes.keys in ['', [], None]:  # No response was made
        battementsComptes.keys=None
    myblockloop.addData('battementsComptes.keys',battementsComptes.keys)
    if battementsComptes.keys != None:  # we had a response
        myblockloop.addData('battementsComptes.rt', battementsComptes.rt)
    # the Routine "response" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'myblockloop'

# get names of stimulus parameters
if myblockloop.trialList in ([], [None], None):
    params = []
else:
    params = myblockloop.trialList[0].keys()
# save data for this loop
myblockloop.saveAsExcel(filename + '.xlsx', sheetName='myblockloop',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
myblockloop.saveAsText(filename + 'myblockloop.csv', delim=',',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# ------Prepare to start Routine "fin"-------
t = 0
finClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(2.000000)
# update component parameters for each repeat
# keep track of which components have finished
finComponents = [end]
for thisComponent in finComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "fin"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = finClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end* updates
    if t >= 0.0 and end.status == NOT_STARTED:
        # keep track of start time/frame for later
        end.tStart = t
        end.frameNStart = frameN  # exact frame index
        end.setAutoDraw(True)
    frameRemains = 0.0 + 2- win.monitorFramePeriod * 0.75  # most of one frame period left
    if end.status == STARTED and t >= frameRemains:
        end.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in finComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "fin"-------
for thisComponent in finComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)



# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
