# Aversive Learning Task with Staircase

This repository contains the necessary files to run a behavioural psychology experimental task. The task was modelled after the study of [Knight et al. 2006](DOI), but contains some variations.

Here, the task consists of a conditioning paradigm where one of two stimuli (sine tone) is presented in each trial. One of the tones (CS+) is associated with 100% chance of receiving an aversive outcome (US; a 500ms auditory 92 dB white noise). The other tone (CS-) is not associated to any noise. Crucially, after each tone starts playing, participants use the mouse to rate on a continous scale the the probability (from 0% to 100% in 1% increments) of receiving the loud noise (US). Without the participant's knowledge, after each detection (hit) of the tone the tone's volume is decreased, and after each non-detection (miss), the tone's volume is increased for the next trial using a 1-up-1-down staircase procedure.

The task starts with a volume the participants can hear, but the volume becomes progressively lower until reaching the participant's auditory perceptual threshold. 

## Getting Started

### Prerequisites

The task was developed to run on Python 2.7 using the following packages. It can probably be easily adapted to Python 3. 

* [Python 2.7](https://www.python.org/downloads/release/python-2715/)
* [Psychopy 1.90.1](https://www.github.com/psychopy/psychopy/releases/tag/1.90.1) - free package for running neuroscience, psychology and psychophysics experiments
* [PYO Ajax Sound Studio](https://www.ajaxsoundstudio.com/software/pyo/) - free package for digital signal processing of sound

### Installing

On the Command Prompt or Terminal

```
>>> cd \folderwherescriptislocated\
>>> python nameofscript.py
```

The script will automatically create a `\data\` folder and will output a `.csv` file inside.

### Trigger markers

The script offers the possibility to send markers through the parallel port, marking various moments of each trial e.g. on the ECG or EEG recording. If you use this, the parallel port address might be different in your system and will need to be changed inside the script.

## Authors

* **Santiago Munoz Moldes** - [Github](https://github.com/santihago)

## License

Released under the MIT license – see the [LICENSE.md](LICENSE.md) file for details.
