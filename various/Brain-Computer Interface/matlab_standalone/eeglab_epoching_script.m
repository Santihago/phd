%% 1.0 Epoch data with EEGLAB
% Because I'm unable to read the triggers of a Biosemi file with Fieldtrip
cd /Users/Main/Documents/eeglab
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;

bdffilename = '/Users/Main/Downloads/evan_real_feet_movement/evan_imaginery_feet_movement.bdf';
setfilename = 'NAMEIS.set';

% 1.1 Import file
% File > Import > .BDF
EEG = pop_biosig(bdffilename);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 

% 1.2 Downgrade to 512 Hz
EEG = pop_resample( EEG, 512);

% 1.3 Epoch data {events}, [time points]
EEG = pop_epoch( EEG, {  '30'  '92'  }, [-3         3.1], 'epochinfo', 'yes');
EEG = eeg_checkset( EEG );

% 1.4 Add comments
comments = 'This is a comment';
EEG = pop_editset(EEG, 'setname', 'Here the title', 'subject', '1', ...
    'condition', '1', 'session', [1], 'comments', strvcat(comments));
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

eeglab redraw

% 1.5 Save file
EEG = pop_saveset( EEG, 'filename',setfilename,'filepath','/Users/Main/Desktop/');
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

clear ALLCOM
clear EEG
clear comments
clear CURRENTSTUDY
clear eeglabUpdater
clear PLUGINLIST
clear STUDY

