#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
- PsychoPy: Peirce, JW (2007) PsychoPy - Psychophysics software in
Python. J Neurosci Methods, 162(1-2):8-13
- QRS Online Detection : https://github.com/c-labpl/qrs_detector;
DOI: 10.5281/zenodo.826614
- Brener J, Ring C. 2016 Towards a psychophysics of interoceptive processes:
the measurement of heartbeat detection. Phil. Trans. R. Soc. B 371: 20160015.
http://dx.doi.org/10.1098/rstb.2016.0015 :
 -------
 "Of the 6AFC methods, the MCS is the most efficient. A standard implementation
 of this procedure involves 20 trials at each of six R-wave to stimulus
 intervals (R + 0, R + 100, R + 200, R + 300, R + 400 and R + 500 ms). Assuming
 five heart-beat – stimulus pairings on each trial and a 5 s intertrial
 interval, the duration of the entire procedure, including an initial 30-trial
 exteroceptive familiarization task, is approximately 35 min."
"""

#========================
#importing used modules
#========================

from __future__ import division
from psychopy import visual, event, core, gui, data, logging
from pyo import *  # import sound library directly for low latency sound
import glob, os  # for file/folder operations
import serial
import random

#====================================================================
# Start serial port for QRS detection (done separately)
#====================================================================



#====================================================================
# Start Parallel Port
#====================================================================

port = parallel.ParallelPort(address=0xD050)  # Address port in Biosemi Room

# Create function to use shorter trigger commands
def sendTrigger(code):
    port.setData(code)  # sets combination of pins high/low (0-255)
    core.wait(0.002)
    port.setData(0)  # sets all pins low again

sendTrigger(0) # sets all pins low to start
# sendTrigger(254) # Start recording EEG

#==========================================
#store info about the experiment session
#==========================================

expName='6AFC'
expInfo={'participant':'AB', 'session':'000'}
dlg=gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK==False: core.quit()  #user pressed cancel
expInfo['date']=data.getDateStr()  #add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#====================================================================
# Sound
#====================================================================

# Sound server
sound = Server(sr=48000, nchnls=2, buffersize=128, duplex=0, winhost="asio")
sound.verbosity = 0
sound.boot().start()

# Test sound
a = Sine(freq=340, mul=0.2).out(dur=0.2)
core.wait(0.1)
a = Sine(freq=340, mul=0.2).out(dur=0.2)
core.wait(0.1)

#====================================================================
# Setting some static variables that we might want to tweak later on
#====================================================================

intervals = (0, .1, .2, .3, .4, .5)  # Intervals in SECONDS
repetitions = 20  # n of repetitions for each interval
practiceRepetitions = 5 # n of practice trials for each interval
tonesPerTrial = 5  # n of heartbeat-tone pairs per trial
SRI = 1  # Tone-Response interval (in seconds)
ITI = 5  # Intertrial interval (in seconds)
minIBI = .5  # minimum possible inter-beat interval IN SECONDS

#===============================
# Creation of window and stimuli
#===============================

# SCREENS

# win = visual.Window(color='white', units='pix', fullscr=True)#True, allowGUI=False)
win = visual.Window([800, 600], units='pix')  # For testing only

# TEXT

respScreen = visual.TextStim(win,
    text=u"Simultanés (s) or non-simultanés (n)?", color='black', height=15)
instruction_list = []
instr_txt = u" You will hear different series of tones. Please indicate if \
you think the tones are simultaneous or not to your heartbeats."
instr = visual.TextStim(win, text=instr_txt, color='black', height=15)
start_message = visual.TextStim(win, text="Press space to start the experiment.",
    color='black', height=15)
instruction_list.append(instr)
instruction_list.append(start_message)

#======================================================
# Create conditions list and trialhandler to run trials
#======================================================

# Create a list of variable combinations (dictionary)
conditions = [{'interval':interval} for interval in intervals]

# Organise them with the trial handler
trials = data.TrialHandler(conditions, repetitions, method='random',
    extraInfo=expInfo)

practiceTrials = data.TrialHandler(conditions, practiceRepetitions,
    method='random', extraInfo=expInfo)

#============
# INITIALIZE
#============

#=====================
# Instructions screens
#=====================


#============================================
# Practice task (exteroception)
#============================================

for thisTrial in practiceTrials:



#=====================
# Instructions screens
#=====================

for instr, thisInstruction in enumerate(instruction_list):
    instruction_list[instr].draw()
    win.flip()
    keypress= event.waitKeys(keyList=['space', 'escape'])
    if keypress[0] == 'escape': core.quit()


#============================================
# Start main loop that goes through all trials
#============================================

for thisTrial in trials:

    # Add something on screen (Icon?)

    # Play series of tones
    for eachTone in range(tonesPerTrial):

        # Wait period corresponding to minimum possible inter-beat interval
        core.wait(minIBI)
        # Read QRS triggers from serial port
        ser port read
        if ser port read == 'Q':
            # wait for specified interval
            core.wait(thisTrial["interval"])
            # play sound
            a = Sine(freq=340, mul=0.2).out(dur=0.2)

    # Stimuli-response interval
    core.wait(SRI)

    # Ask for response ('Simultaneous (y) / Not Simultaneous (n)')
    respScreen.draw()
    win.flip()
    keypress= event.waitKeys(keyList=['s','n','escape'])
    if keypress[0] == 'escape': core.quit()

    # Add response to trialHandler
    trials.addData('resp', keypress)

    # Present blank screen again
    win.flip()

    # Intertrial interval
    core.wait(ITI)


trials.saveAsWideText(filename+'.csv')

win.close()
core.quit()
