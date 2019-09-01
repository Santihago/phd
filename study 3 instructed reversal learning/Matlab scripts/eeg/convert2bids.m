clear
close all 
clc

path_ft = '/Users/santiago/Documents/MATLAB/fieldtrip';
addpath(path_ft); 
ft_defaults

% path where data is located
cd('/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/')
path_data     = './data/raw/';
path_destin   = './analysis/eeg/'; if ~exist(path_destin); mkdir(path_destin); end %#ok<*EXIST>

sub = 1:70;

% for one subject the age is unknown
age = [24  19  25  23  23  18  23  22  28  20
       24  23  24  24  21  26  21  22  26  20
       31  22  21  22  22  22  22  20  24  21
       19  19  22  19  19  19  23  20  18  21
       nan 18  19  22  24  38  18  39  nan 19
       24  20  28  nan  18  21  19 20  20  nan
       19  nan 19  22   nan 20  19  45 20 20];
   
sex = {'m' 'f' 'f' 'f' 'm' 'f ' 'f' 'f' 'f' 'f'
       'm' 'f' 'f' 'f' 'f' 'f' 'm' 'f' 'm' 'f'
       'f' 'f' 'f' 'f' 'f' 'f' 'f' 'm' 'f' 'f'
       'm' 'f' 'f' 'f' 'f' 'f' 'f' 'f' 'f' 'f'
       'm' 'f' 'm' 'f' 'f' 'm' 'f' 'm' 'm' 'm'
       'm' 'f' 'm' 'f' 'f' 'm' 'f' 'm' 'm' 'f'
       'f' 'f' 'f' 'm' []  'f' 'm' 'f' 'm' 'm'};  % 22 males
   
  exc = [21 65];  % excluded due to behaviour or requesites
  no_ecg = [23 26];

for subindx=1:length(sub)

  cfg = [];
  cfg.method    = 'copy';  % cfg.method = 'convert';
  cfg.datatype  = 'eeg';

  % specify the input file name
  filename = strcat('EEG_ECG_P', num2str(subindx), '.bdf');
  cfg.dataset  = fullfile(path_data, filename);

  % specify the output directory
  cfg.bidsroot  = 'data/bids';  % top level directory for the BIDS output  % or just 'bids'
  cfg.sub       = num2str(sub(subindx));  % string, subject name

  % specify the information for the participants.tsv file
  % this is optional, you can also pass other pieces of info
  cfg.participant.age = age(subindx);
  cfg.participant.sex = sex{subindx};

  % specify the information for the scans.tsv file
  % this is optional, you can also pass other pieces of info
  %cfg.scans.acq_time = datestr(now, 'yyyy-mm-ddThh:MM:SS'); % according to RFC3339

  % specify some general information that will be added to the eeg.json file
  cfg.InstitutionName             = 'Universite Libre de Bruxelles';
  cfg.InstitutionalDepartmentName = 'Center for Research in Cognition and Neuroscience';
  cfg.InstitutionAddress          = '50 FD Roosevelt, 1050 CP 191, Brussels, Belgium';
  
% You can specify cfg.events.trl as a Nx3 matrix with the trial definition (see
% FT_DEFINETRIAL) or as a MATLAB table. When specified as table, the first three
% columns containing integer values corresponding to the begsample, endsample and
% offset, the additional colums can be of another type and have any name. If you do
% not specify the trial definition, the events will be read from the MEG/EEG/iEEG
% dataset. Events from the trial definition or from the data will be written to
% events.tsv.
%   cfg.events.trl              = trial definition, see also FT_DEFINETRIAL
  
% If you specify cfg.bidsroot, this function will also write the dataset_description.json
% file. You can specify the following fields
%   cfg.dataset_description.writesidecar        = string
   cfg.dataset_description.Name                = 'EEG and ECG during Aversive Revesal Learning';
   cfg.dataset_description.BIDSVersion         = 'BEP006';
%   cfg.dataset_description.License             = string
%   cfg.dataset_description.Authors             = string or cell-array of strings
%   cfg.dataset_description.Acknowledgements    = string
%   cfg.dataset_description.HowToAcknowledge    = string
   cfg.dataset_description.Funding             = 'European Research Council Advanced Grant 340718'; 
%   cfg.dataset_description.ReferencesAndLinks  = string or cell-array of strings
%   cfg.dataset_description.DatasetDOI          = string

% You can specify cfg.presentationfile with the name of a NBS presentation log file,
% which will be aligned with the data based on triggers (MEG/EEG/iEEG) or based on
% the volumes (fMRI). To indicate how triggers (in MEG/EEG/iEEG) or volumes (in fMRI)
% match the presentation events, you should also specify the mapping between them.
% Events from the presentation log file will be written to events.tsv.
%   cfg.presentationfile        = string, optional filename for the presentation log file
%   cfg.trigger.eventtype       = string (default = [])
%   cfg.trigger.eventvalue      = string or number
%   cfg.presentation.eventtype  = string (default = [])
%   cfg.presentation.eventvalue = string or number
%   cfg.presentation.skip       = 'last'/'first'/'none'

  % provide the mnemonic and long description of the task
  cfg.TaskName        = 'Aversive Reversal Learning';
  cfg.TaskDescription = 'Subjects...';
  cfg.Instructions    = ''; % Text of the instructions given to participants before the scan. This is not only important for behavioural or cognitive tasks but also in resting state paradigms (e.g. to distinguish between eyes open and eyes closed).
  
  % other details
  cfg.Manufacturer                = 'Biosemi';
  cfg.ManufacturersModelName      = 'ActiveTwo';
  
  % these are EEG specific
  %cfg.eeg.EEGReference       = 'M1'; % actually I do not know, but let's assume it was left mastoid
  
  % EEG specific fields
  cfg.eeg.SamplingFrequency             = 2048; % Sampling frequency (in Hz) of the EEG recording (e.g. 2400)
  cfg.eeg.EEGChannelCount               = 64; % Number of EEG channels included in the recording (e.g. 128).
  cfg.eeg.EOGChannelCount               = 4; % Number of EOG channels included in the recording (e.g. 2).
  cfg.eeg.ECGChannelCount               = 2; % Number of ECG channels included in the recording (e.g. 1).
  cfg.eeg.EEGReference                  = ''; % Description of the type of reference used (common", "average", "DRL", "bipolar" ).  Any specific electrode used as reference should be indicated as such in the channels.tsv file
  cfg.eeg.TriggerChannelCount           = 1; % Number of channels for digital and analog triggers.
  cfg.eeg.PowerLineFrequency            = 50; % Frequency (in Hz) of the power grid where the EEG is installed (i.e. 50 or 60).
  cfg.eeg.EEGPlacementScheme            = '10-20'; % Placement scheme of the EEG electrodes. Either the name of a placement system (e.g. "10-20", "equidistant", "geodesic") or a list of electrode positions (e.g. "Cz", "Pz").
  cfg.eeg.CapManufacturer               = 'Biosemi'; % name of the cap manufacturer
  cfg.eeg.RecordingType                 = 'continuous'; % "continuous", "epoched"

  data2bids(cfg);

end
