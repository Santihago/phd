#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# NOTE: Change to Helvetica, Add Instructions, check output

"""
Using PsychoPy Package: Peirce, JW (2007) PsychoPy - Psychophysics software in
Python. J Neurosci Methods, 162(1-2):8-13
Code snippets from:
- http://osdoc.cogsci.nl/3.1/tutorials/advanced/
- https://stackoverflow.com/questions/28964556/psychopy-builder-expt-how-to-add-live-updating-text-on-screen
- http://gestaltrevision.be/wiki/python/coding

"""
#========================
#importing used modules
#========================

from psychopy import visual, event, core, gui, data, logging
from psychopy import prefs
import glob, os  # for file/folder operations
import numpy as np
import pandas as pd # for loading csv files
import random
import codecs # for loading text with correct decoding (for accents)
import myfunctions as pers

#==========================================
#store info about the experiment session
#==========================================

expName='Attentional Blink'
expInfo = {'subject':'', 'age':'', 'gender':['homme','femme']}
if not gui.DlgFromDict(expInfo, order=['subject', 'age', 'gender']).OK:
    core.quit()
expInfo['date']=data.getDateStr()  #add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['subject'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#====================================================================
# Setting some static variables that we might want to tweak later on
#====================================================================

var = pers.L()
# The presentation time of each stimulus (in frames)
var.letter_dur = 3  # In nr of frames (50 ms)
# The inter-stimulus interval (in frames)
var.isi = 4  # In nr of frames (66 ms)
# The maximum lag, i.e. the number of letters that follow T1.
var.max_lag = 4
# We load a list of words (utf-8 or 16 for french accents) for distractors / T1
fileFillers = 'words_fillers.txt'
words = codecs.open(fileFillers, 'r', encoding ='utf-16').readlines()
words = [x.replace("\r\n","") for x in words]  # Remove \r\n symbols

#===============================
# Creation of window and stimuli
#===============================

txtColor = 'black'
backgroundColor = '#c1c1c1'  # light gray
Tcolor = 'green'  # color of target

win = visual.Window(color=backgroundColor, units='pix', fullscr=True)
# win = visual.Window([800, 600], color=backgroundColor, units='pix')

# Creation of stimuli
instr_1 = visual.TextStim(win,
    text=u"""
    Durant cette tâche qui durera une quinzaine de minutes au total, 120 séries d’items vous seront présentées.
    Chacune des séries sera composée de quelques dizaines de mots en Français (des noms communs) qui défileront très rapidement au centre de votre écran.
    Ces mots seront tous de couleur noire, sauf 2 d’entre eux, qui seront de couleur verte.

    Votre tâche: repérer ces deux mots de couleur verte et les restituer dans l’ordre à la fin de chaque série.
    Appuyez sur « espace » pour continuer les instructions.""",
	color=txtColor,
	height=22)
instr_2 = visual.TextStim(win,
    text=u"""
    Pour chacun des deux mots repérés, un message sur l’écran vous invitera à indiquer votre réponse, selon deux modalités que vous devrez toutes les deux utiliser:

    - vous rapporterez le mot oralement
    - vous entrerez sur le clavier la première lettre du mot correspondant

    Si vous n’avez pas pu repérer un des mots en vert, vous direz « pas vu » et taperez sur le clavier « 0 » (le chiffre zéro).
    Si ce sont les deux mots en vert qui vous ont échappé, vous direz donc « pas vu-pas vu » et taperez sur le clavier « 0 » deux fois. 

    Appuyez sur la touche « espace » du clavier pour continuer.""",
	color=txtColor,
	height=22)
practiceMessage = visual.TextStim(win,
    text=u"A vous de jouer ! Nous allons commencer par quelques essais d'entraînement. Appuyez sur la touche « espace » quand vous êtes prêt(e).",
    color=txtColor,
    height=22)
taskMessage = visual.TextStim(win,
    text=u"Nous allons maintenant commencer la vraie tâche. Appuyez sur la touche « espace » quand vous êtes prêt(e).",
    color=txtColor,
	height=22)
startMessage = visual.TextStim(win,
    text=u"Appuyez sur la touche « espace » pour démarrer le prochain essai.",
    color=txtColor,
	height=22)

resp1_title = visual.TextStim(win,
    text=u"Introduisez l'initiale du premier mot vert, et appuyez ensuite sur « Enter »:",
    color=txtColor,
    height=20)
resp2_title = visual.TextStim(win,
    text=u"Introduisez l'initiale du second mot vert, et appuyez ensuite sur « Enter »:",
    color=txtColor,
    height=20)
resp1_input = visual.TextStim(win,
    text='',
    color=txtColor,
    pos=(0, -60),
    height=25)
resp2_input = visual.TextStim(win,
    text='',
    color=txtColor,
    pos=(0, -60),
    height=25)
feedback = visual.TextStim(win,
    text='',
    color=txtColor,
    height=20 )
MERCI = visual.TextStim(win, 
    text=u"Merci!",
    color='green', 
	height=22) 
	

instructions = []
instructions.extend([instr_1, instr_2])

optoSquare = visual.Rect(win, # for timing testing
    units='pix',
    width = 100,
    height = 100,
    fillColor = 'black')

#======================================================
#Create conditions list and trialhandler to run trials
#======================================================

"""
Conditions:
2 x 2 Design – Arousal of T2 (low/high) x SOA (232ms/464ms)
30 trials per conditions = 120 total trials.
We have a list of 60 words as T2 that is repeated twice.
It is loaded from an external file that provides for each trial:
- lag (1 or 3) => changed to 2 or 4
- T2 type ('n' for neutral or 'a' for arousal)
- word (the whole word)
"""
nTrialReps = 1  # No repetitions, just 1 full list
nPractice = 4  # Nr practice trials

#import trialstypes from excel of csv file
# In the file 4 first trials are only for training
trialList=data.importConditions('trialList-124.csv')

# method can be ‘random’, ‘sequential’, or ‘fullRandom’
trials = data.TrialHandler(trialList,nReps=nTrialReps, method='sequential', extraInfo=expInfo)
# Under a random order, the next row will be selected at random
# (without replacement); it can only be selected again after all the other rows
# have also been selected. nReps determines how many repeats will be performed
# (for all conditions).

trials.data.addDataType('respT1')
trials.data.addDataType('respT2')	


#============
# INITIALIZE
#============

#=====================================================================
# Display instructions for the task
#=====================================================================

for ins, thisInstruction in enumerate(instructions):
    instructions[ins].draw()
    win.flip()
    keypress= event.waitKeys(keyList=['space', 'escape'])
    if keypress[0] == 'escape': core.quit()

#============================================
# Start main loop that goes through all trials
#============================================

for thisTrial in trials:

    #===================================
    # Practice or real task message
    #===================================

    if trials.thisN  == 0:  # practice
        practiceMessage.draw()
        win.flip()
        keypress= event.waitKeys(keyList=['space', 'escape'])
        if keypress[0] == 'escape': core.quit()
    if trials.thisN  == 4:  # real task
        taskMessage.draw()
        win.flip()
        keypress= event.waitKeys(keyList=['space', 'escape'])
        if keypress[0] == 'escape': core.quit()

    #============================
    # Prepare trial, load images
    #============================

    # The position of T1 is random between 8 and 25. Note that the first position is
    # 0, so the position indicates the number of preceding stimuli.
    var.T1_pos = random.randint(8, 25)  # Same as Kiel et al. 2006
    # The length of the stream is the position of T1 + the maximum lag + 1. We need
    # to add 1, because we count starting at 0, so the length of a list is always
    # 1 larger than its maximum index.
    var.stream_len = var.T1_pos + var.max_lag + 5 # ()+1) # NOTE: Not clear how many in Kiel2006
    # Randomly sample a `stream_len` number of letters
    stream_list = random.sample(words, var.stream_len)
    # Set lag for this trial (Nr of words between T1 and T2)
    var.lag = thisTrial['lag'] #ater
    # Add T2 to the stim list
    var.T2_pos = var.T1_pos + var.lag
    # Replace the word for T1 and T2 from a pre-made list
    stream_list[var.T1_pos] = thisTrial['wordT1']
    stream_list[var.T2_pos] = thisTrial['wordT2']

    # Convert text stim to images (Create an empty list for the canvas objects.)
    imgstream_list = []
    # Loop through all letters in `stim_list`. `enumerate()` is a convenient
    # function that automatically returns (index, item) tuples. In our case, the
    # index (`i`) reflects the position in the RSVP stream. This Python trick, in
    # which you assign a single value to two variables, is called tuple unpacking.
    for j, stim in enumerate(stream_list):
        if j == var.T1_pos or j == var.T2_pos:
            color = Tcolor
        else:
            color = txtColor
        # All stimuli require an psychopy.visual.Window object to be passed as first
        # argument. In OpenSesame, this object is available as `win`.
        imgstim= visual.TextStim(win,
                                 text=stim,
                                 color=color,
                                 height=40, # 0.82 degree vertical visual angle as in Kiel et al
                                 font='helvetica' # as in Kiel et al
                                 )
        imgstream_list.append(imgstim)

    # We set the identity of T1 as an experimental variable, because it has been
    # randomly determined in the script
    # Extract T1 word from the list
    #var.T1 = stream_list[var.T1_pos] # NOTE important for me to save later! DATA ANALYSIS!

    #=================
    # Run RSVP images
    #=================

    # Start trial message
    startMessage.draw()
    win.flip()
    keypress= event.waitKeys(keyList=['space', 'escape'])
    if keypress[0] == 'escape': core.quit()
    win.flip()
    core.wait(1.2)

    # Start RSVP stream
    #l_letter_time = [] #NOTE: for testing timing
    #l_blank_time = [] #NOTE: for testing timing

    for textstim in imgstream_list:
        # Show text for 50 ms = 3 frames on 60Hz monitor

        #t0 = core.getTime() #NOTE: for testing timing
        for frame in range(var.letter_dur):
            textstim.draw()
            #optoSquare.draw()
            win.flip()
       # t1 = core.getTime() - t0 #NOTE: for testing timing
       # l_letter_time.append(t1) #NOTE: for testing timing

        # Blank screen for 66 ms = 4 frames on 60Hz monitor
       # t2 = core.getTime() #NOTE: for testing timing
        for frame in range(var.isi):
            win.flip() # OBS: no drawing in this loop. Just a blank screen.
      #  t3 = core.getTime() - t2 #NOTE: for testing timing
       # l_blank_time.append(t3) #NOTE: for testing timing

    #NOTE: for testing timing
   # a_letter_dur = np.array(l_letter_time)
    #a_blank_dur = np.array(l_blank_time)

    #mean_letter_dur = a_letter_dur.mean()
    #std_letter_dur = a_letter_dur.std()
    #mean_blank_dur = a_blank_dur.mean()
    #std_blank_dur = a_blank_dur.std()
    #print 'Mean Letter:', mean_letter_dur
    #print 'STD Letter:', std_letter_dur
    #print 'Mean Blank:', mean_blank_dur
    #print 'STD Blank:', std_blank_dur

    #print(a_letter_time)
    #print(a_blank_time)

    #==============
    # Response 1
    #==============

    chars = list('abcdefghijklmnopqrstuvwxyz0') # the valid characters
    resp1 = '' # start with an empty answer on each trial
    pressed_enter = False

    while not pressed_enter:
        response = event.getKeys() # get a list of keys pressed at this instant
        if len(response) > 0: # if there was one,
            key = response[0] # just convenient shorthand
            if key in chars:
                resp1 = resp1 + response[0]
            elif key == 'space':
                resp1 = resp1 + ' '
            elif key == 'backspace' and len(resp1) > 0:
                resp1 = resp1[:-1]
            elif key == 'return':  # and len(response)>2: # at least 3 numbers
                #  trials.addData('Answer', meanText) # save the response
                pressed_enter = True # finish this screen
            elif key == 'escape':
                core.quit()

        # update the appropriate text stimulus with the current response value:
        resp1_input.text = resp1
        resp1_input.draw()
        resp1_title.draw()
        win.flip()

    #==============
    # Response 2
    #==============

    resp2 = '' # start with an empty answer on each trial
    pressed_enter = False

    while not pressed_enter:
        response = event.getKeys() # get a list of keys pressed at this instant
        if len(response) > 0: # if there was one,
            key = response[0] # just convenient shorthand
            if key in chars:
                resp2 = resp2 + response[0]
            elif key == 'space':
                resp2 = resp2 + ' '
            elif key == 'backspace' and len(resp2) > 0:
                resp2 = resp2[:-1]
            elif key == 'return':  # and len(response)>2: # at least 3 numbers
                pressed_enter = True # finish this screen
            elif key == 'escape':
                core.quit()

        # update the appropriate text stimulus with the current response value:
        resp2_input.text = resp2
        resp2_input.draw()
        resp2_title.draw()
        win.flip()

    #=======================================
    # add/save the data to the trialhandler
    #=======================================

    trials.addData('respT1', resp1)
    trials.addData('respT2', resp2)

    #trials.saveAsWideText(filename+'.csv', encoding='utf-8')
    #core.wait(.5)
    
    #===========================
    # allow for a short breaks
    #===========================

    if (trials.thisN-nPractice)%12==0 and trials.thisN is not nPractice: #every 12 trials inform the participant of the progress (here: percentage done)
          progText= u"{0:.0f}% des essais complétés!".format(100*(trials.thisN/float(trials.nTotal)))
          feedback.setText(progText)
          feedback.draw()
          win.flip()
          keypress= event.waitKeys(keyList=['space'])


# save data
trials.saveAsWideText(filename+'.csv', encoding='utf-8')
core.wait(.5)

# Show end message
MERCI.draw()
win.flip()
core.wait(1)

# close nicely
win.close()
core.quit()

