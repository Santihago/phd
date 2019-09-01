#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version 31/08/2018 1:10pm

"""
This is a script that uses Psychopy to loop through trials in which a face
is shown subliminally (using backward and forward masking),
and then asks the participant for a response.

Author: Santiago Munoz 
Universite Libre de Bruxelles
santimz[at]gmail.com 
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

#===========================
# Experiment session dialog
#===========================

# Get values from dialog
expName='SublFaces'
myDlg = gui.Dlg(title=expName, pos = (860,340))
myDlg.addField(label='participant',initial=0, tip='Participant name or code'),
myDlg.addField(label='age',initial=0, tip='Participant age'),
myDlg.addField(label='sex', choices=('female','male', 'non-binary'))
myDlg.addField(label='session',initial='', choices=['test', 1, 2], tip='Session Nr'),
myDlg.addField(label='screen', choices=(144, 60), tip='Refresh Rate')
myDlg.addField(label='triggers', initial='Yes', choices=['Yes', 'No'], tip='Send Parallel Port Triggers')
dlg_data = myDlg.show()
if myDlg.OK==False: core.quit()  #user pressed cancel

# Store values from dialog
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

#=====================
# Start parallel port
#=====================
# Parallel port drivers need to be installed
# Note: the file inpout32.dll needs to be in the same folder

# Triggers can be turned On or Off
if expInfo['triggers']=='Yes': triggers = True
else: triggers = False

if triggers:

    from psychopy import parallel

    port = parallel.ParallelPort(address=0xDEFC) # 0x0D50  # Address port 

    #Create function to use shorter trigger commands
    def sendTrigger(code):
        port.setData(code)  # sets combination of pins high/low (0-255)
        core.wait(0.002)
        port.setData(0)  # sets all pins low again

    # TRIGGERS:
    triggerList = {
        'faceDurShort': 2,
        'faceDurLong': 3,
        'iti':10,  # ITI, first screen flip
        'fixcross':11,  # fixation cross, first flip
        'face':12,  # target face, first flip
        'neutral':13, #  target face neutral, first flip
        'disgust':14, #  target face disgust, first flip
        'mask':15,  # start of mask, first flip
        'maskEnd':16,  # end of mask/start of blank 
        'resp':20,  # rating click response
        'restStart':100,  # rest Start
        'restEnd':101,  # rest Stop
        'eegStart':254,  # eeg rec start (set in biosemi config file)
        'eegStop':255   # eeg rec stop (set in biosemi config file)
        }

    sendTrigger(0) # sets all pins low to start
    sendTrigger(triggerList["eegStart"]) # Start recording EEG

#==========================================
# Store info about the experiment session
#==========================================

#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#======================
# Monitor and screen
#======================

# Monitor ('iiyama 144 Hz')
widthPix = 1920  # screen width in px
heightPix = 1080  # screen height in px
monitorwidth = 53.1  # monitor width in cm
viewdist = 60.  # viewing distance in cm
monitorname = 'iiyama'
scrn = 0  # 0 to use main screen, 1 to use external screen
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

#====================================================================
# Setting some static variables that we might want to tweak later on
#====================================================================

hz = int(expInfo['screen'])

timeInFrames = {  # choose 'ceil' for rounding up, 'floor' for rounding down
        "REST" : int(ceil(hz * 180.)),
        "FIXCROSS" : int(ceil(hz * .5)),
        "FWD_MASK_DUR" : int(ceil(hz * .25)),  # 250 ms
        "FACE_DUR" : int(ceil(hz * .016)),  # 16 ms (20 ms in 144)
        "BKW_MASK_DUR" : int(ceil(hz * 1.0)),  # 100 ms   OR MORE IN V.2
        "PRE_RESP_DUR" : int(ceil(hz * 2.5)),
        "RESP_DUR" : int(ceil(hz * 3.)),
        }

#===============================
# Creation of window and stimuli
#===============================

# TEXT ELEMENTS

# Instructions text
instruction_list = []
text_size = .6  # in degrees of visual angle (dva)
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
instr_faces = visual.TextStim(win, 
    text=u"""Cette expérience se compose de nombreux essais similaires. \
A chaque essai, deux visages seront presentés l'un à la suite de l'autre,\
 sans intervalle entre les deux.
Le premier, très rapide, sera pratiquement invisible. \
Le second sera visible et aura toujours une expression neutre.
Vous devez deviner quelle était l'expression du premier visage, celui qui\
 était invisible: il peut être soit neutre, soit expressif.

Appuyez sur la barre d'espace pour voir un exemple de visage.
 """, 
    color=text_color , 
    height=text_size,
    font=text_font)
instr_faces_2 = visual.TextStim(win, 
    text=u"""Le premier etait-il neutre ou expressif? Si vous n'avez \
pas pu voir le premier visage, c'est normal!
Appuyez sur la barre d'espace pour revoir un exemple.
 """, 
    color=text_color , 
    height=text_size,
    font=text_font)
instr_rating = visual.TextStim(win, 
    text=u"""
Vous répondrez sur une échelle horizontale, au moyen de la souris.







- Si vous pensez que le visage caché était 'neutre', rapprochez votre \
souris de l'emoji a l'expression neutre.
- Si vous pensez qu'il était 'expressif', rapprochez votre souris de \
l'emoji expressif.
- Si vous ne savez pas, cliquez au milieu (?).

Vous pouvez utiliser toute la longueur de l'échelle, selon votre \
certitude: approchez vous de l'emoji si vous êtes sûrs!

Cliquez sur l'échelle pour continuer.
 """, 
    color=text_color , 
    height=text_size,
    font=text_font,
    pos=(0,-3.5))
run_message = visual.TextStim(win, 
    text=u"""Voilà! Pendant l'expérience, les visages seront suivis \
de l'échelle, et vous devrez donc deviner quel était le visage chaché.
Même s'ils paraissent invisibles, il est parfois possible de les deviner.
A la fin, nous vous donnerons un score de précision de vos réponses!

    Dès que vous appuyerez sur la barre d'espace, nous commencerons \
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
results = visual.TextStim(win, 
    text=u"",
    color=text_color , 
    height=text_size,
    font=text_font)

instruction_list.append(start_message)
instruction_list.append(instr_faces)
instruction_list.append(instr_faces_2)
instruction_list.append(instr_rating)
instruction_list.append(run_message)

# IMAGES

# Allen et al 2015 report 2.41 x 4.9 DVA faces (ratio of 0.49)
# The face image files are 331x448 (ratio of 0.73), or 255x360 without margins (ratio of 0.70)
# Image height is calculated as 6.09 DVA when adding margins
# Width is calculated as ratio (.73) of the height
face_height = 6.09 # face image height in dva
ratio = .73
imgSz = [face_height*ratio, face_height] # Corresponds to 2.41 x 4.9 DVA faces + margins
# dictionnary with images
stimList = {  
    "fixcross" : visual.TextStim(win, text="+", height = .7, color = "black"),
    "scrambled" : visual.ImageStim(win, image="imgs/noise_face1_image2.jpg", size = imgSz),
    "neutral_1" : visual.ImageStim(win, image="imgs/SHINEd_neutral_face1_image2.jpg", size = imgSz),
    "neutral_2" : visual.ImageStim(win, image="imgs/SHINEd_neutral_face2_image2.jpg", size = imgSz),
    "neutral_3" : visual.ImageStim(win, image="imgs/SHINEd_neutral_face3_image2.jpg", size = imgSz),
    "neutral_4" : visual.ImageStim(win, image="imgs/SHINEd_neutral_face4_image2.jpg", size = imgSz),
    "disgust_1" : visual.ImageStim(win, image="imgs/SHINEd_disgust_face1_image2.jpg", size = imgSz),
    "disgust_2" : visual.ImageStim(win, image="imgs/SHINEd_disgust_face2_image2.jpg", size = imgSz),
    "disgust_3" : visual.ImageStim(win, image="imgs/SHINEd_disgust_face3_image2.jpg", size = imgSz),
    "disgust_4" : visual.ImageStim(win, image="imgs/SHINEd_disgust_face4_image2.jpg", size = imgSz)
}

restScreen = visual.ImageStim(win=win,
    image="imgs/landscape-1920x1080.jpg", units="deg", size= (32, 18))

# RATING SCALE

posNeut = -1
posDisg = 1

ratingScale = visual.RatingScale(win, 
    name = 'rating',
    low=0,
    high=100,
    pos=(0,0),
    tickMarks = [0,50,100],
    labels = [' ','?',' '],
    marker = 'slider',
    textSize = 0.7,
    textColor = 'black',
    #maxTime = 0,
    singleClick=True,
    mouseOnly = True,
    showAccept = False,
    showValue = True,  # Ignored if singleClick
    stretch = 0.6
    )

# Emoji faces for rating scale 
neutralPaint = visual.ImageStim(win, 
    image="imgs/emoji-neutral.png", 
    size = [1.75, 1.75], 
    pos = (6*posNeut,-.65))
disgustPaint = visual.ImageStim(win, 
    image="imgs/emoji-confounded.png", 
    size = [1.75, 1.75], 
    pos = (6*posDisg,-.65))

#======================================================
# Create conditions list and trialhandler to run trials
#======================================================

maskLabels = ["neutral_1", "neutral_2", "neutral_3", "neutral_4"]
disgLabels = ["disgust_1", "disgust_2", "disgust_3", "disgust_4"]
mergedLabels = disgLabels + maskLabels # (8 imgs)

faceDurations = [2,3] # ONLY FOR PILOT IN 144 Hz

trialList = []
for dur in faceDurations:# ONLY FOR PILOT IN 144 Hz
    for face in mergedLabels:  # first variable
        for mask in maskLabels:  # second variable
            trialList.append(
            {"target":face, "mask":mask, "dur":dur}
            )

# Organize trials
trials = data.TrialHandler(trialList, 2, method = 'random', extraInfo=expInfo)

#================================
# Function for presenting a face 
#================================

# Leave 4 seconds before and after face. (time needed for 3 beats if 45 BPM)
# before face: 0.2 + ITI(3.4-3.9) + fixcross(0.5) + forward mask(0.1) = 4-4.5 seconds
# after face: backward mask + postTime + blank  = 4 seconds 

def showFace(face1, face2, preTimeWin=(3.2, 3.7), postTimeWin=(.5,.5), sendTriggers=triggers, faceDur=2): # faceDur ONLY FOR PILOT IN 144 Hz
    # For face1 and face2: strings e.g. "neutral_1", "disgust_2" or thisTrial['target']
    # Optional: 
    # - sendTriggers: boolean, whether parallel port triggers are sent (default from exp settings)
    # - preTimeWin: tuple with min and max time in seconds, blank screen
    # - postTimeWin: tuple with min and max time in seconds, blank screen

    win.flip()
    # Hide mouse
    event.Mouse(visible=False)
    
    # Get target face category
    if face1 in maskLabels: category = 'neutral'
    elif face1 in disgLabels: category = 'disgust'

    # Face Dur category (ONLY FOR PILOT)
    core.wait(.1)
    if sendTriggers:
        if faceDur ==2: sendTrigger(triggerList["faceDurShort"])
        elif faceDur ==3: sendTrigger(triggerList["faceDurLong"])
    core.wait(.1)

    # Variable time blank screen
    iti = uniform(*preTimeWin)  # Get random float between two numbers (* expands the tuple)
    itiFrames = int(iti * hz)  # convert to frames, make integer
    if sendTriggers: win.callOnFlip(sendTrigger, triggerList["iti"])
    for thisFrame in range(itiFrames):
        win.flip()
        
    # Fixation cross
    if sendTriggers: win.callOnFlip(sendTrigger, triggerList["fixcross"])
    for thisFrame in range(timeInFrames["FIXCROSS"]):
        stimList["fixcross"].draw()
        win.flip()
        
    # Forward mask
    for thisFrame in range(timeInFrames["FWD_MASK_DUR"]):
        stimList["scrambled"].draw()
        win.flip()
        
    # Face stimulus
    if sendTriggers: win.callOnFlip(sendTrigger, triggerList[category])
    for thisFrame in range(faceDur):  #(timeInFrames["FACE_DUR"]): # ONLY FOR PILOT IN 144 Hz
        stimList[face1].draw()
        win.flip()
        
    # Backward mask
    if sendTriggers: win.callOnFlip(sendTrigger, triggerList["mask"])
    for thisFrame in range(timeInFrames["BKW_MASK_DUR"]):
        stimList[face2].draw()
        win.flip()
        
    # Blank
    postTime = uniform(*postTimeWin)
    postTimeFrames = int(postTime * hz)
    if sendTriggers: win.callOnFlip(sendTrigger, triggerList["maskEnd"])
    for thisFrame in range(postTimeFrames):
        win.flip()
        
    return category

#============
# INITIALIZE
#============
#==================================
# Instructions screens and training
#==================================

# Message before rest
restMessage.draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
if keypress[0] == 'escape': core.quit()

# Start rest period
sendTrigger(triggerList["restStart"])
for thisFrame in range(timeInFrames["REST"]):
    restScreen.draw() # landscape picture
    win.flip()
core.wait(.5)
sendTrigger(triggerList["restEnd"])

# Show 'OK!' message
OK.draw()
win.flip()
core.wait(1)

# TASK INSTRUCTIONS

for instr, thisInstruction in enumerate(instruction_list[0:2]):
    instruction_list[instr].draw()
    win.flip()
    keypress= event.waitKeys(keyList=['space', 'escape'])
    if keypress[0] == 'escape': core.quit()
# Face example
event.Mouse(visible=False)
showFace("neutral_1", "neutral_3", preTimeWin=(.5,.5), sendTriggers=False)
# Text
instruction_list[2].draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
# Face example again
showFace("disgust_2", "neutral_2", preTimeWin=(.5,.5), sendTriggers=False)
# Rating Scale example
event.Mouse(visible=True)
testScale = visual.RatingScale(win, low=0, high=100, pos=(0,0),
    tickMarks = [0,50,100], labels = [' ','?',' '], marker = 'slider',
    textSize = 0.7, textColor = 'black', singleClick=True, mouseOnly = True,
    showAccept = False, showValue = True, stretch = 0.6)
event.clearEvents()
while testScale.noResponse:
    instruction_list[3].draw()
    neutralPaint.draw()  # Draw other item next to scale
    disgustPaint.draw() 
    testScale.draw()
    win.flip()
    if event.getKeys(['escape']): core.quit()
# Text
instruction_list[4].draw()
win.flip()
keypress= event.waitKeys(keyList=['space', 'escape'])
if keypress[0] == 'escape': core.quit()

#============================================
# Start main loop that goes through all trials
#============================================

for thisTrial in trials:

    #=========
    # Stimuli
    #=========

    # Face function
    cat = showFace(thisTrial['target'], thisTrial['mask'], faceDur=thisTrial['dur'])

    # Period before response
    for thisFrame in range(timeInFrames["PRE_RESP_DUR"]):
        win.flip()

    #==========
    # Response
    #==========
    
    # Rating Scale
    event.Mouse(visible=True)
    ratingScale.reset()  # reset between repeated uses of the same scale
    event.clearEvents()
    rating = None
    decisionTime = None
    for thisFrame in range(timeInFrames["RESP_DUR"]): 
        if ratingScale.noResponse:
            neutralPaint.draw()  # Draw other item next to scale
            disgustPaint.draw()
            ratingScale.draw()
            win.flip()
            if event.getKeys(['escape']): core.quit()
        elif not ratingScale.noResponse:  # Response
            rating = ratingScale.getRating()  # !!  returns value if not clicked
            decisionTime = ratingScale.getRT()
            if triggers: sendTrigger(triggerList["resp"])
            break

    ratingScale.noResponse = False
    
    #==================================
    # Add the data to the trialHandler
    #==================================

    # Add response to trialHandler
    trials.addData('category', cat)
    trials.addData('faceDur', thisTrial['dur'])
    trials.addData('rating', rating)
    trials.addData('ratingRT', decisionTime)

    # Present blank screen again
    win.flip()

    #========================
    # Allow for short breaks
    #========================

    if trials.thisN%32==0 and trials.thisN is not 0: # inform participant of the progress
        progText=u"{0:.0f}% des essais complétés!".format(100*((trials.thisN)/float(trials.nTotal)))
        pause_message.setText(progText)
        pause_message.draw()
        win.flip()
        keypress= event.waitKeys(keyList=['space', 'escape'])
        if keypress[0] == 'escape': core.quit()

#================
# Save and close
#================

# Stop Biosemi EEG recording
if triggers: sendTrigger(triggerList["eegStop"])

# Save response data
trials.saveAsWideText(filename+'.csv')

#=======
# Close
#=======

# Show 'Merci!' message
Merci.draw()
win.flip()
core.wait(2)

win.close()
core.quit()