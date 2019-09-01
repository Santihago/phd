#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Code template from perswww.kuleuven.be

# TO DO
# SET HIGHER NUMBER OF TRIALS PER RUN

 """
#========================
#importing used modules
#========================

from psychopy import visual, event, core, gui, data, logging
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']  # pyo...
from psychopy import sound
import glob, os  # for file/folder operations
import numpy as np  # for random number generators
import random

#==========================================
#store info about the experiment session
#==========================================

expName='Intentional binding in mouse movements'
expInfo={'participant':'', 'session':'001'}
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
# Setting some static variables that we might want to tweak later on
#====================================================================

# Design
# NR_COND = 4  # variable not used, just for info
# TOTAL TR = 4 (conditions) x NR_COND_REPETITIONS x nTrialReps = 120?
"""
There are 4 conditions (deviation types) and 3 delay types
Total_tr = 4 (conditions) x NR_COND_REPETITIONS (2) x nTrialReps (15)
"""
NR_COND_REPETITIONS = 2  # multiply the deviation types by this factor
nTrialReps = 15  # Number of trials per deviation type
timelimit = 20  # IN SECONDS
deviation_degrees = (0,5,10,15)  # IN DEGREES

# Stimuli
cursorRad = 5 # radius size in pixels
targetRad = 20 # radius size in pixels

#=========================
# prepare conditions lists
#=========================

deviation_types = (0,1,2,3) # levels of deviation (0 is no deviation)
# sequence_of_dev = (0,1,0,2,3,1,3,2)  # pseudo randomized example
sequence_of_dev = [deviation_types[i//NR_COND_REPETITIONS] for i in range(len(deviation_types)*NR_COND_REPETITIONS)]  # Multiply each value a few times
np.random.shuffle(sequence_of_dev)  # randomizing sequence of deviations

#===============================
# Creation of window and stimuli
#===============================

# win = visual.Window(color='white', units='pix', fullscr=True)#True, allowGUI=False)
win = visual.Window([800, 600], units='pix')
mouse = event.Mouse(visible=True)

# Creation of stimuli
start_zone = visual.Rect(win, pos = (-300, 0), width=8, height=8, fillColor = 'red', opacity = 0.5)
cursor = visual.Circle(win, radius=cursorRad, edges=13, units='pix')
target = visual.Circle(win, radius=targetRad, edges=13, units='pix',
                       lineWidth = 0, fillColor='Red',  pos=(250, 0))
time_up_message = visual.TextStim(win, text="Time is up! Try again.",
    color='red', height=30, bold=True ) # text that overlays image after 30 seconds
start_message = visual.TextStim(win, text="Press space to start the experiment.",
    color='black', height=30)
instr = visual.TextStim(win, text='Allez au point de depart', pos=(0, -.7), opacity=0.5)
IB_title = visual.TextStim(win, text="How much time between click and sound?",
    color='white', height=20 )
IB_input = visual.TextStim(win, text='', color='black', pos=(0, -100), height=30)

#===============================
# Creation of sound tones
#===============================

sound.init(rate=44100, stereo=True, buffer=128)
tone = sound.Sound(value='G', secs=0.2, octave=4, sampleRate=44100, bits=16)
tone_intervals = (0.3, 0.5, 0.7)

#======================================================
#Create conditions list and trialhandler to run trials
#======================================================

#create a list of trials per condition, adding factor info to trial
# for dev in range(sequence_of_dev):  # for each deviation in the sequence
stimList = []
for dev in [sequence_of_dev]:  # for each deviation in the sequence
    stimList.append(
        {'dev':dev} #this is a python 'dictionary'
        )

# method can be ‘random’, ‘sequential’, or ‘fullRandom’
trials = data.TrialHandler(stimList,nReps=nTrialReps, method='sequential', extraInfo=expInfo)

#============
# INITIALIZE
#============

#=====================================================================
# Display instructions and wait for a spacebar to start the experiment
#=====================================================================

start_message.draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
if keypress[0] == 'escape': core.quit()

#==============================================================================================
# initialize 2 clocks: one for timing the flipping of images and one to register response time
#==============================================================================================

exp_clock = core.Clock()  # experiment clock

#============================================
# Start main loop that goes through all trials
#============================================

for thisTrial in trials:
    trial_clock = core.Clock()  # Initializing start time for calculating response time
    win.flip()

    #=========================
    # prepare trial variables
    #=========================

    done = False #trial not done yet
    target_x = np.random.randint(-50,50)
    target.pos =  (target_x, O) # Set for a new position every trial
    # rand tonelengths

    #=============================================
    # trajectory deviation and degrees/rad value
    #=============================================

    if thisTrial['dev']==0:
         deg = deviation_degrees(0)
    elif thisTrial['dev']==1:
         deg = deviation_degrees(1)
    elif thisTrial['dev']==2:
         deg = deviation_degrees(2)
    elif thisTrial['dev']==3:
         deg = deviation_degrees(3)

    a = np.deg2rad(deg)

    #================================
    # wait for mouse in start position
    #================================
    # pos0 : initial position
    # m_old : continuous moving old position
    # pos1 : continuous moving new position
    # pos2 : continuous moving deviated position

    while not cursor.overlaps(start_zone):
        mnew = mouse.getPos()
        cursor.pos = mnew
        cursor.draw()
        start_zone.draw()
        instr.draw()
        win.flip()

    # When mouse goes through start positition calculate x0,y1 (start position)
    pos0=mouse.getPos()

    #=========================
    #start cycling/presenting
    #=========================
    RT_clock = core.Clock()  # Initializing start time for calculating response time
    m_old=mouse.getPos()
    while not done:
        pos1 = mouse.getPos()  # Keep getting the new position
        if (m_old != pos1).all():
            # Start position
            x0 = pos0[0];
            y0 = pos0[1];
            # The new position
            x1 = pos1[0];
            y1 = pos1[1];
            # The modified new position
            x2 = round(np.sqrt((x1-x0)**2+(y1-y0)**2) * np.cos(a + np.arctan2((y1-y0),(x1-x0))) + x0)
            y2 = round(np.sqrt((x1-x0)**2+(y1-y0)**2) * np.sin(a + np.arctan2((y1-y0),(x1-x0))) + y0)
            # Set cursor to modified new position
            cursor.pos = (x2,y2)
            # Set to compare with new for a possible change
            m_old=mouse.getPos()
        cursor.draw()
        target.draw()
        win.flip()

        if RT_clock.getTime() > timelimit and not done:
            rt = timelimit
            acc=0
            respIB = '-1'  # no respIB

            time_up_message.draw()  # Says that participant has to respond
            win.flip()

            keypress= event.waitKeys(keyList=['space', 'escape'])
            if keypress[0] == 'escape': core.quit()
            done=True  # trial is over


        if cursor.overlaps(target):
            rt=RT_clock.getTime() # example
            acc=1 # example

            #
            # # wait interval
            # interval = random.choice(tone_intervals)
            # core.wait(interval)
            # # play sound
            # tone.play()
            #
            # #=============================
            # # Intentional binding  screen
            # #=============================
            # core.wait(2)
            # IB_title.draw()
            # win.flip()
            #
            # # START RESPONSE SCREEN
            # chars = list('0123456789.') # the valid characters
            # respIB = '' # start with an empty answer on each trial
            # pressed_enter = False
            #
            # while not pressed_enter:
            #     response = event.getKeys() # get a list of keys pressed at this instant
            #     if len(response) > 0: # if there was one,
            #         key = response[0] # just convenient shorthand
            #         if key in chars:
            #             respIB = respIB + response[0]
            #         elif key == 'space':
            #             respIB = respIB + ' '
            #         elif key == 'backspace' and len(respIB) > 0:
            #             respIB = respIB[:-1]
            #         elif key == 'return':  # and len(response)>2: # at least 3 numbers
            #             #  trials.addData('Answer', meanText) # save the response
            #             pressed_enter = True # finish this screen
            #
            #
            #     # update the appropriate text stimulus with the current response value:
            #     IB_input.text = respIB
            #     IB_input.draw()
            #     IB_title.draw()
            #     win.flip()

            done=True  # trial is over
        else:
            continue


    #=======================================
    # add/save the data to the trialhandler
    #=======================================

    #add data
    trials.addData('rt',rt)
    trials.addData('acc', acc)
    # trials.addData('respIB', respIB)

    #=======================================
    # allow for a short breaks
    #=======================================

    if trials.thisN%10==0: #every 10 trials inform the participant of the progress (here: percentage done)
         progText= "{0:.0f}% of trials done! You can take a small break.".format(100*(trials.thisN/float(trials.nTotal)))
         print progText #to actually display this on screen you have to use the setText('progText') method of a TextStim


trials.saveAsWideText(filename+'.csv')
trials.saveAsPickle(filename+'trials')

win.close()
core.quit()
