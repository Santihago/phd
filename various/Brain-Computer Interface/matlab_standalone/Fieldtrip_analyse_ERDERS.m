%% Fieldtrip code for analyse TFR of Motor Imagery

bdffilename = '/Users/Main/Dropbox/Science/My PhD/My PhD Projects/Brussels BCI/v6_ERD_ERS_Analysis/EEG Raw Data/motorimagery3.bdf';
ftpath = '/Users/Main/Documents/fieldtrip';
addpath(ftpath)
cd '/Users/Main/Dropbox/Science/My PhD/My PhD Projects/Brussels BCI/v6_ERD_ERS_Analysis/EEG Raw Data'


% Write down trigger value for our conditions
marker_right = 92;
marker_down = 30;
marker_index = [marker_right marker_down];

% This will perform all steps of analysis for all conditions
for condition = 1:length(marker_index)
    
    %% Pre-processing
    
    marker = marker_index(condition);
    
    % 2.1 Read file and select channels, re-reference
    cfg                     = [];
    cfg.dataset             = bdffilename; % your filename with file extension;
    cfg.trialdef.eventtype  = 'STATUS'; % Status notation maybe
    cfg.trialdef.eventvalue = marker; % your event value (30 down, 92 right, 60 cue stop)
    cfg.trialdef.prestim    = 2; % before stimulation (sec), only use positive value
    cfg.trialdef.poststim   = 4; % after stimulation (sec) , only use positive value
    cfg                     = ft_definetrial(cfg);
    cfg.method              = 'trial';
    data = ft_preprocessing(cfg);
    
    % Remove extra channel
    cfg = [];
    cfg.channel = 1:64;
    data = ft_selectdata(cfg, data);
    
    % Repair biosemi channels labels from A1, A2, B29, to Cz, Fz, etc
    % But channel 65 (status vs. CMNT) and 66 (Scale) do not match
    cfg = [];
    cfg.layout = 'biosemi64.lay';
    layout = ft_prepare_layout(cfg);
    data.label(1:64,1) = layout.label(1:64,1);
    
    % Downsample data
    cfg                    = [];
    cfg.resamplefs         = 512;
    data = ft_resampledata(cfg, data);
    
    save data
    
    %% 3.0 Artifact rejection
    
    % 3.0 Remove bad channels and trials
    cfg                   = [];
    cfg.layout            = 'biosemi64.lay';
    data = ft_rejectvisual(cfg, data);
    
    % Re-reference
    cfg                   = [];
    cfg.reref             = 'yes';
    cfg.refchannel        = 'all';   % for a common average reference
    cfg.refmethod         = 'avg';
    data = ft_preprocessing(cfg, data)
    
    % 3.7 Filtering 
    cfg                  = [];
    cfg.bpfilter         = 'yes';
    cfg.bpfreq           = [1 40];         % Band pass filter
    data_bp  = ft_preprocessing(cfg,data);
    
    
    % 3.1 Visual data inspection (close with 'q')
    cfg                   = [];
    cfg.viewmode          = 'vertical';
    cfg                   = ft_databrowser(cfg,data_bp)
    

    % 3.2 Proceed to reject selected trials
    cfg.artfctdef.reject  = 'complete';
    cleandata = ft_rejectartifact(cfg,data_bp);
    
     
    % 3.3 Using ICA for artifact removal
    cfg                  = [];
    cfg.channel          = 'eeg';                   % Or list them manually
    ic_data = ft_componentanalysis(cfg,cleandata);
    
    save ic_data
    
    % 3.4 Browse 10 components
    cfg                  = [];
    cfg.viewmode         = 'component';
    %cfg.continuous       = 'yes';
    cfg.blocksize        = 10;
    cfg.channels         = [1:9];                 % Number of components
    cfg.layout           = 'biosemi64.lay';
    ft_databrowser(cfg,ic_data);
    
    % 3.5 Select components to reject
    cfg                  = [];
    cfg.component        = [2 ];
    data_iccleaned  = ft_rejectcomponent(cfg, ic_data);
    
    % 3.6 A final visual inspection
    cfg                  = [];
    cfg.viewmode         = 'vertical';
    ft_databrowser(cfg,data_iccleaned);
    
    cfg.artfctdef.remove = 'complete';
    data_manual = ft_rejectartifact(cfg,data_iccleaned);
    
    save data_manual_down
    
    %% References and laplacians
    
    
    % Prepare neighbours for interpolation and Surface Laplacian
    cfg                  = [];
    cfg.method           = 'template';
    cfg.template         = 'biosemi64_neighb.mat';
    cfg.layout           = 'biosemi64.lay';
    cfg.channel          = 'eeg';
    cfg.feedback         = 'yes';
    neighbours = ft_prepare_neighbours(cfg, data);
    
    % Interpolate channels
%     cfg                  = [];
%     cfg.method           = 'nearest';
%     %cfg.template         = 'biosemi64_neighb.mat';
%     cfg.neighbours       = neighbours;
%     cfg.badchannel       = {'AFz', 'Iz'}; % cell-array, see FT_CHANNELSELECTION for details
%     cfg.elec = layout;
%     interp = ft_channelrepair(cfg, data);
    
    
    % 3.9 Surface Laplacian
    
    cfg                  = [];
    cfg.method           = 'hjorth';
    cfg.neighbours       = neighbours;
    cfg.layout           = layout;
    data_laplacian = ft_scalpcurrentdensity(cfg,data_manual);
    
    
    %% 5.0 Time-Frequency Analysis
    
    cfg                  = [];
    cfg.output           = 'pow';
    cfg.channel          = 'eeg';
    cfg.method           = 'mtmconvol';
    cfg.taper            = 'hanning';
    cfg.foi              = 3:1:30;                         % analysis 3 to 30 Hz in steps of 2 Hz
    cfg.t_ftimwin        = ones(length(cfg.foi),1).*0.5;   % length of time window = 0.5 sec
    %cfg.tapsmofrq        = ones(length(cfg.foi),1).* 4.5;
    cfg.toi              = -2:0.001:4;                     % time window "slides" from -0.5 to 1.5 sec in steps of 0.001 sec (50 ms)
    %cfg.layout           = 'biosemi64.lay';
    TFRhann = ft_freqanalysis(cfg, data_laplacian);
    
    
    
    %% Baseline normalization
    
    cfg = [];
    cfg.baseline         = [-1.1 -0.1];
    cfg.baselinetype     = 'relative';
    cfg.parameter        = 'powspctrm'; 
    TFRbaseline = ft_freqbaseline(cfg,TFRhann);
    
    %% Visualisation
    
    cfg = [];
    %cfg.baseline        = [-1 -0.1];
    %cfg.baselinetype    = 'relative';
    cfg.xlim            = [2 4];                     % time
    %cfg.zlim            = [-0.5  3];
    %cfg.ylim            = [15 30];                  % frequencies
    cfg.marker          = 'labels';
    cfg.colorbar        = 'yes';
    cfg.layout          = 'biosemi64.lay';
    figure
    ft_topoplotTFR(cfg, TFRbaseline);
    
    %% Statistics
    
    cfg = [];
    %cfg.variance       = 'yes';
    cfg.channel        = 'eeg';
    cfg.frequency      = [6 30];
    cfg.latency        = 'all';
    freq = ft_freqdescriptives(cfg, TFRhann);
    
end

% yo