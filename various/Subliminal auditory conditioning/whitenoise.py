#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Threat conditioning of tones using a loud white noise

Author: Santiago Munoz
Universite Libre de Bruxelles
smunozmo@ulb.ac.be
"""

#========================
# Importing used modules
#========================

from __future__ import division
from psychopy import monitors, gui, visual, core, data, event, logging
import numpy as np
from numpy.random import random, randint, normal, shuffle, uniform
from math import ceil, floor
import glob, os
from pyo import *

#==========================================
# Store info about the experiment session
#==========================================
#------------------------------
# Experiment session GUI dialog
#------------------------------

#get values from dialog
expName='WhiteNoise'
myDlg = gui.Dlg(title=expName, pos = (860,340))
myDlg.addField(label='participant',initial=0, tip='Participant name or code'),
myDlg.addField(label='age',initial=0, tip='Participant age'),
myDlg.addField(label='sex', choices=('female','male', 'non-binary'))
myDlg.addField(label='session',initial='', choices=['test', 1, 2], tip='Session Nr'),
myDlg.addField(label='screen', choices=(144, 60), tip='Refresh Rate')
myDlg.addField(label='triggers', initial='Yes', choices=['Yes', 'No'], tip='Send Parallel Port Triggers')
dlg_data = myDlg.show()
if myDlg.OK==False: core.quit()  #user pressed cancel

#store values from dialog
expInfo = {
    'participant':dlg_data[0],
    'age':dlg_data[1],
    'sex':dlg_data[2],
    'session':dlg_data[3],
    'screen':dlg_data[4],
    'triggers':dlg_data[5]
    }

expInfo['date']=data.getDateStr()  #add a simple timestamp
expInfo['expName']=expName

#-----------------------
#setup files for saving
#-----------------------

if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#====================================================================
# Setting some static variables that we might want to tweak later on
#====================================================================

#number of repetitions of each condition
nReps = 60

#determine screen's refresh rate
hz = int(expInfo['screen'])

#experiment time durations in seconds
times= {"REST" : 1., "CS" : 5.5, "UCS" : 0.5, "ITI" : 5.}

#adjust times in seconds to frames depending on screen's refresh rate
#choose 'ceil' for rounding up, 'floor' for rounding down (no half frames)
timeInFrames= {  # choose 'ceil' for rounding up, 'floor' for rounding down
        "REST" : int(ceil(hz * times["REST"])),
        "CS" : int(ceil(hz * times["CS"])),
        "UCS" : int(ceil(hz * times["UCS"])),
        "ITI" : int(ceil(hz * times["ITI"])),
        }

#=====================
# Open parallel port
#=====================
# Parallel port drivers need to be installed
# Note: the file inpout32.dll needs to be in the same folder

#triggers can be turned On or Off
if expInfo['triggers']=='Yes': triggers = True
else: triggers = False

if triggers:

    from psychopy import parallel

    port = parallel.ParallelPort(address=0xDEFC) #0xB010 in new Stim PC, 0xDEFC in Personal PC

    #create function to use shorter trigger commands
    def sendTrigger(code):
        port.setData(code)  #sets combination of pins high/low (0-255)
        core.wait(0.002)
        port.setData(0)  #sets all pins low again

    # TRIGGERS:
    triggerList = {
        'iti':10,  # ITI, first screen flip
        'CS-':11,  # fixation cross, first flip
        'CS+':12,  # fixation cross, first flip
        'UCSStart':13,  # fixation cross, first flip
        'resp':20,  # rating click response
        'restStart':100,  # rest Start
        'restEnd':101,  # rest Stop
        'eegStart':254,  # eeg rec start (set in biosemi config file)
        'eegStop':255   # eeg rec stop (set in biosemi config file)
        }

    sendTrigger(0) #sets all pins low to start
    sendTrigger(triggerList["eegStart"]) #start recording EEG

#===============================
# Creation of window and stimuli
#===============================

#-------------------
# Monitor and screen
#-------------------

# Monitor ('iiyama 144 Hz')
widthPix = 1920  #screen width in px
heightPix = 1080  #screen height in px
monitorwidth = 53.1  #monitor width in cm
viewdist = 60.  #viewing distance in cm
monitorname = 'iiyama'
scrn = 0  #0 to use main screen, 1 to use external screen
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
mon.save()

# Initialize window
win = visual.Window(
    monitor=mon,
    size=(widthPix,heightPix),
    color=[0,0,.7255],  #'#B9B9B9' in hex
    colorSpace='hsv',  # !
    units='deg',
    screen=scrn,
    allowGUI=False,
    fullscr=True)

# win = visual.Window([800, 600], color='Gray', units='pix')  # For testing only

#-------
# MOUSE
#-------

mouse = event.Mouse(visible=True, win=win)

#---------------
# TEXT ELEMENTS
#---------------

# Instructions text
instruction_list = []
text_size = .6  #in degrees of visual angle (dva)
text_color = 'black'
text_font = 'Georgia'
restMessage = visual.TextStim(win,
    text=u"""Bienvenue. Nous allons commencer par une période de repos de trois minutes.
Vous ne devrez rien faire de particulier: trouvez simplement une position confortable et
laissez vos pensées divaguer. Evitez autant que possible les mouvements du corps.

Appuyez sur la touche « espace » pour démarrer la période de repos.""",
    color=text_color ,
    height=text_size,
    font=text_font)
OK = visual.TextStim(win,
    text=u"OK!",
    color=text_color ,
    height=text_size,
    font=text_font)
Merci = visual.TextStim(win,
    text=u"Merci!",
    color=text_color ,
    height=text_size,
    font=text_font)
start_message = visual.TextStim(win,
    text=u"""Bienvenue! Merci de participer à cette expérience.\
    Appuyez sur la barre d'espace pour lire les instructions.""",
    color=text_color ,
    height=text_size,
    font=text_font)
run_message = visual.TextStim(win,
    text=u"""Dès que vous appuyerez sur la barre d'espace, nous commencerons \
avec la vraie expérience.
    A vous de jouer!""",
    color=text_color ,
    height=text_size,
    font=text_font)
pause_message = visual.TextStim(win,
    text=u"",
    color=text_color ,
    height=text_size,
    font=text_font)

instruction_list.append(start_message)

#--------
# SOUNDS
#--------

# Create and boot a server
sv = Server(sr=44100, nchnls=2, buffersize=128, duplex=0, winhost="asio")
sv.verbosity = 0
sv.boot()   #initialize audio stream
sv.start()  #activates server processing loop

#frequencies for the sine tones in Hz
if int(expInfo['participant']) % 2 == 0: #even number
    toneFreqs = {"CS-" : 700, "CS+" : 1300}
else:  #odd number
    toneFreqs = {"CS-" : 1300, "CS+" : 700}

#starting volume
# UCS volume: 0.1275 = 95 dB; 0.1 = 91.8 dB
# CS volume: 0.0005 = 40 dB
volumes = {"CS-" : .0001, "CS+" : .0001, "UCS" : .1275}

#list with created sounds
sounds = {
    "CS-": Sine(freq=toneFreqs["CS-"], mul=volumes["CS-"]),
    "CS+": Sine(freq=toneFreqs["CS+"], mul=volumes["CS+"]),
    "UCS": Noise(mul=volumes["UCS"]).mix(2)  #mix(2) for dual-channel
}

#staircase paremeters
volumeRatioStart = 0.812  #volume reduction is done by dividing by this value (corresponds to -3dB decrease in perceived loudness)
volumeRatioChange = 0.05  #value that will be added to volumeRatio to change step size (will never go above 1.0)
volumeRatio = volumeRatioStart   
#running average
running_perf = np.array([])  #running average of performance
window_length = 10  #change vol unit if 3 non-detections in the last 6 trials
perf_threshold = 0.6  #XX% performance

#--------
# IMAGES
#--------

restScreen = visual.ImageStim(win=win,
    image="imgs/landscape-1920x1080.jpg", units="deg", size= (32, 18))

#--------------
# RATING SCALE
#--------------

# Creating my own rating scale for full flexibility.
# I follow guidelines from Matejka 2016: No ticks, 2 labels, dynamic text
# feedback

#------------- You can adjust these
scale_max = 100 #maximum rating in the rating scale (int)
rs_max = 7  #scale upper limit in degrees of visual angle
rs_col = '#373F51'  #charcoal color
rs_txt_col = rs_col
rs_txt_size = .7
labelsYPos = -1
dynTxtYPos = 1
_rs_min = (-1 * rs_max)
labelsXPos = [x * rs_max for x in [-1, 1]]
labels = ["0 %", "100 %"]

#------------- No need to adjust these
dyn_txt = visual.TextStim(win, text=u"", height=rs_txt_size, color = rs_txt_col)
#scale stimuli: horizontal bar, labels, ticks/bands
rs_stims = []
rs_stims += [visual.Rect(win, width=rs_max*2, height=.1, fillColor = rs_col,
             lineColor = rs_col)]
for nr, thisXPos in enumerate(labelsXPos):  #text
    rs_stims += [visual.TextStim(win, text=labels[nr], height=rs_txt_size,
                 pos = [thisXPos, labelsYPos], color = rs_txt_col)]
#moving slider
rs_slider = visual.Rect(win, width=.25, height=1., fillColor = rs_col,
                        lineColor = rs_col)
                        
#initialize some variables
ratings_allTrials = []  #all ratings matrix



#======================================================
# Create conditions list and trialhandler to run trials
#======================================================

trialTypes = ["CS-", "CS+"]

trialList = []
for trialType in trialTypes:
    trialList.append({"trialType": trialType, "toneFreq": toneFreqs[trialType]})

#organize trials
trials = data.TrialHandler(trialList, nReps, method = 'random', extraInfo=expInfo)

#============
# INITIALIZE
#============
#------------------
# Resting period
#------------------

#message before rest
restMessage.draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
if keypress[0] == 'escape': core.quit()

#start rest period
if triggers: sendTrigger(triggerList["restStart"])
for thisFrame in range(timeInFrames["REST"]):
    restScreen.draw() #landscape picture
    win.flip()
core.wait(.5)
if triggers: sendTrigger(triggerList["restEnd"])

#show 'OK!' message
OK.draw()
win.flip()
core.wait(1)

#----------------------------------
# Instructions screens and training
#----------------------------------

run_message.draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
if keypress[0] == 'escape': core.quit()

#============================================
# Start main loop that goes through all trials
#============================================

for thisTrial in trials:

    #is this trial CS- or CS+?
    cond = thisTrial["trialType"]

    #wait for inter-trial interval
    if triggers: win.callOnFlip(sendTrigger, triggerList["iti"])
    for thisFrame in range(timeInFrames["ITI"]):
        win.flip()

    #--------------
    # Play CS sound
    #--------------

    #set sound
    cs = sounds[cond]  # CS- or CS+

    #set volume for this trial (updated at each trial)
    cs.setMul(volumes[cond])

    #play sound (Start processing and sending samples out)
    # cs.out(dur=times["CS"])
    cs.out()

    #send a trigger at next window flip
    if triggers: win.callOnFlip(sendTrigger, triggerList[cond])
    win.flip()

    #---------------------------
    # Rating Scale during sound
    #---------------------------

    #prepare and reset between repeated uses of the same scale
    event.clearEvents()
    detected = False
    detectedRT = None
    RATING = None
    ratings_thisTrial = []  #continuous rating
    ratings_thisTrial.append(trials.thisN)
    rs_slider.setFillColor('#FEFFFA')
    mouse.setPos([0,0])
    mouse.clickReset()
    #start showing the scale
    for thisFrame in range(timeInFrames["CS"]):
        #draw all components of the rating scale
        for stim in rs_stims:
            stim.draw()
        #set slider and dynamic text position to follow mouse (with limits)
        m_x, m_y = mouse.getPos()
        if m_x < _rs_min: m_x = _rs_min
        if m_x > rs_max: m_x = rs_max
        rs_slider.setPos([m_x, 0])
        rs_slider.draw()
        #re-scale rating value to new range
        RATING = int(((m_x+rs_max)/rs_max)*(scale_max/2))
        dyn_txt.setPos([m_x, dynTxtYPos])
        dyn_txt.setText(str(RATING)+ " %")
        dyn_txt.draw()
        win.flip()
        #listen to keyboard and mouse
        buttons, RT = mouse.getPressed(getTime=True)  #returns 3-item list and time since reset
        if not detected and buttons[0]:  #first click detected
            detected = True
            detectedRT = round(RT[0], 2)
            if triggers: sendTrigger(triggerList["resp"])
            rs_slider.setFillColor('#1A7AF8')
            mouse.clickReset()
        if event.getKeys(['escape']): core.quit()
        #save continuous rating sampled at each frame in a vector
        ratings_thisTrial.append(RATING)

    #stop sound
    cs.stop()

    #blank screen
    win.flip()

    #----------------
    # Play UCS sound
    #----------------

    if cond is "CS+":
        #set sound
        ucs = sounds["UCS"]
        
        #play sound
        ucs.out()
        
        #send trigger at next window flip
        if triggers: win.callOnFlip(sendTrigger, triggerList["UCSStart"])
        win.flip()

    #wait during sound
    for thisFrame in range(timeInFrames["UCS"]):
        win.flip()

    #stop sound
    if cond is "CS+": ucs.stop()

    #======================
    # Some data processing
    #======================

    #add this trial ratings to all trials ratings
    ratings_allTrials.append(ratings_thisTrial)

    #--------------------------------------
    # 1. Calculate running average of perf 
    #--------------------------------------
    
    #add last detection responses to running average
    if len(running_perf)<window_length:  #add new value only
        running_perf = np.concatenate((running_perf[:], [detected]))
    elif len(running_perf)==window_length:  #add a new value and remove first value
        running_perf = np.concatenate((running_perf[1:], [detected]))
    
    #calculate running average of performance
    running_perf_mean = np.count_nonzero(running_perf)/len(running_perf)
    
    goodperformance = running_perf_mean==1.0
    badperformance = running_perf_mean <= perf_threshold
    enoughtrials =  len(running_perf)==window_length
    room4change = (volumeRatio + volumeRatioChange) < 1  #3 decrements of unit
    #if random performance and enough trials
    if badperformance and enoughtrials and room4change:
        #make the steps smaller
        volumeRatio += volumeRatioChange
        running_perf = np.array([])  #restart running average

    #if perfomance is good, return to previous ratios of change
    if goodperformance and enoughtrials and volumeRatio>volumeRatioStart:
        #make the steps bigger
        volumeRatio -= volumeRatioChange
        running_perf = np.array([])  #restart running average
 
    #--------------------------------
    # 2. Modify volume for next trial
    #--------------------------------
    
    if detected:
        volumes[cond] *= volumeRatio
    elif not detected:
        volumes[cond] /= volumeRatio

    #----------------------------------
    # Add the data to the trialHandler
    #----------------------------------

    #add response to trialHandler
    trials.addData('detected', detected)
    trials.addData('detectedRT', detectedRT)
    trials.addData('lastRating', RATING)
    trials.addData('volume', volumes[cond])
    trials.addData('volUnit', volumeRatio)
    trials.addData('averagePerformance', running_perf_mean)


    #========================
    # Allow for short breaks
    #========================

    if trials.thisN%10==0 and trials.thisN is not 0: #inform participant of the progress
        progText=u"{0:.0f}% des essais complétés!".format(100*((trials.thisN)/float(trials.nTotal)))
        pause_message.setText(progText)
        pause_message.draw()
        win.flip()
        keypress= event.waitKeys(keyList=['space', 'escape'])
        if keypress[0] == 'escape': core.quit()

#======
# Save
#======

# Stop Biosemi EEG recording
if triggers: sendTrigger(triggerList["eegStop"])

# Save response data
trials.saveAsWideText(filename+'.csv')

# Save continuous ratings in a file (1 trial per row, 1 sample per column)
# Add trial Nr and participant number

arr = np.array(ratings_allTrials)
np.savetxt(filename+'_ratings.csv', arr, delimiter=",", fmt = '%.0f')

#=======
# Close
#=======

# Show 'Merci!' message
Merci.draw()
win.flip()
core.wait(4)

sv.stop()
win.close()
core.quit()
