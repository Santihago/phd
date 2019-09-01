# heart-feedback

This project consists of multiple Python files for conducting an experiment in psychology. This experiment investigated whether heartbeat feedback training improved detection of subliminally presented disgust faces. 
It was part of a project of psychology master students at Universite Libre de Bruxelles.

The files allow for stimuli presentation, keyboard response recordings, and real-time heartbeat measurements.

## File descriptions

- `heart_santi.py` : a script slightly modified from Joseph Wright (Copyright (c) 2014 Joseph Wright, license: BSD 3 clause) that connects to a plethysmograph (Pulse Sensor ©; www.pulsesensor.com) through an Arduino Uno board to to measure heart beats. Functions from this file are imported into the two other scripts.
- `faces-task.py` : is the main task of the experiment. The script loads a set of images (neutral or disgut face expressions, jpgs not included) that are presented to the participant, and made subliminal through a masking procedure.
- `heartbeat-counting.py` : is the heartbeat counting task. Participants are asked to count their heartbeats in five different trials. The script keeps records heartbeats in real-time. Feedback is delivered on the third trial through a stethoscope held by the participant.
