%===========================================
% CONDITION COMPARISON IN TIMELOCK ANALYSIS
% AUTHOR: SANTIAGO MUÑOZ-MOLDES
% DATE: JULY 2019
%===========================================

clear
close all
clc

%% SETUP AND FOLDER CREATION
root_dir = '/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/analysis/eeg/';
cd(root_dir)
addpath('./scripts/')

% adds fieldtrip to the matlab path + the relevant subdirectories
path_ft = '/Users/santiago/Documents/MATLAB/fieldtrip';
addpath(path_ft);
ft_defaults;
ft_hastoolbox('brewermap', 1); % ensure this toolbox for color is on the path

% Participants
everyone = 1:70;
excluded = [6 21 15 25 40 54 60 65 67];  %54 and 60 have very big trial artefacts
included = setdiff(everyone, excluded);

% instructed
grp1 = setdiff([1 4 5 8 9 12 13 16 17 20 21 24 25 28 29 ...
        32 33 36 37 40 41 44 45 48 49 52 53 56 57 60 61 64 65 68 69], excluded);

% uninstructed
grp2 = setdiff(included, grp1);


% load the biosemi 64 channel template that has channel coordinates and
% names
cfg        = [];
cfg.layout = 'biosemi64.lay';
layout = ft_prepare_layout(cfg);

% latencies for each ERP, in seconds

p1   = [0.1 0.14];
n170 = [0.15 0.20];
enp  = [.2 .3];
lpp  = [.4 .6];

%triggers

cs_pos = 2;
cs_neg = 3;
normal = 0;
revers = 1;

%% COMPUTATION OF EVENT-RELATED POTENTIALS AND OF THE GROUP AVERAGE

%Perform the analysis for each group?
%for j=1:2 % For group 1 or group 2
    
    j=1
    
    switch j
        case 1
            subjects = grp1;
        case 2
            subjects = grp2;
    end

   
    % add single subject ERPs in a single cell array
    allerp_pos_norm = cell(1, length(subjects));
    allerp_neg_norm = cell(1, length(subjects));
    allerp_pos_rev  = cell(1, length(subjects));
    allerp_neg_rev  = cell(1, length(subjects));
    
    for i=1:length(subjects)  % INDIVIDUAL AVERAGES
        
        %load clean dataset
        datafile = fullfile(root_dir, 'clean', strcat(num2str(subjects(i)), '.mat'));
        load(datafile);
        
        % options for all conditions
        cfg         = [];
        cfg.channel = {'all'};
        
        % Data is split according to condition and average is created for
        % the participant
        
        % average across chosen trials
        cfg.trials    = find(data_clean.trialinfo(:,2) == cs_pos & data_clean.trialinfo(:,6) == normal);
        erp_pos_norm  = ft_timelockanalysis(cfg, data_clean);
        
        % average across chosen trials
        cfg.trials    = find(data_clean.trialinfo(:,2) == cs_neg & data_clean.trialinfo(:,6) == normal);
        erp_neg_norm  = ft_timelockanalysis(cfg, data_clean);
        
        % average across chosen trials
        cfg.trials    = find(data_clean.trialinfo(:,2) == cs_pos & data_clean.trialinfo(:,6) == revers);
        erp_pos_rev   = ft_timelockanalysis(cfg, data_clean);
        
        % average across chosen trials
        cfg.trials   = find(data_clean.trialinfo(:,2) == cs_neg & data_clean.trialinfo(:,6) == revers);
        erp_neg_rev  = ft_timelockanalysis(cfg, data_clean);
        
        % Average is added to a group cell
        allerp_pos_norm{i} = erp_pos_norm;
        allerp_neg_norm{i} = erp_neg_norm;
        allerp_pos_rev{i}  = erp_pos_rev;
        allerp_neg_rev{i}  = erp_neg_rev;
        
    end
    
    % compute grand average across subjects for each condition
    cfg             = [];
    cfg.latency     = [-.2 .8];
    gaerp_pos_norm  = ft_timelockgrandaverage(cfg, allerp_pos_norm{:});
    
    cfg             = [];
    cfg.latency     = [-.2 .8];
    gaerp_neg_norm  = ft_timelockgrandaverage(cfg, allerp_neg_norm{:});
    
    cfg             = [];
    cfg.latency     = [-.2 .8];
    gaerp_pos_rev   = ft_timelockgrandaverage(cfg, allerp_pos_rev{:});
    
    cfg             = [];
    cfg.latency     = [-.2 .8];
    gaerp_neg_rev   = ft_timelockgrandaverage(cfg, allerp_neg_rev{:});
    
%end


%% VISUALIZATION OF THE GROUP AVERAGE ERP

%clr = [.902 .6235 0; .3373 .7059 .9137; .3373 .7059 .9137]
   
% plot a sensor layout with the ERP time course at each electrode
cfg            = [];
cfg.layout     = layout;
%cfg.graphcolor = 'r';
cfg.showlabels = 'yes';

figure;
%cfg.graphcolor = clr; % uisetcolor()
ft_multiplotER(cfg, gaerp_pos_norm, gaerp_neg_norm);

figure;
%cfg.graphcolor = [.902 .6235 0; .3373 .7059 .9137]; % uisetcolor()
ft_multiplotER(cfg, gaerp_pos_rev, gaerp_neg_rev);

% plot mean ERP over central electrodes
cfg            = [];
cfg.ylim       = [-5 5];
cfg.channel    = {'Pz'};
cfg.linewidth  = 2;
%cfg.graphcolor = 'r';
figure;
ft_singleplotER(cfg, gaerp_pos_norm, gaerp_neg_norm);
% below are some 'low-level' matlab commands that do some window dressing
% on the figure
set(gca, 'Fontsize', 20);
%title('Mean over PO8');
set(gca,'box','on');
xlabel('time [sec]');
ylabel('amplitude (\muV)');

%% SUBSTRACTIONS

% Substract conditions (normal)
cfg = [];
cfg.operation = 'subtract';
cfg.parameter = 'avg';
gaerp_norm_diff = ft_math(cfg, gaerp_pos_norm, gaerp_neg_norm);

%Plot the difference
cfg            = [];
cfg.layout     = layout;
%cfg.graphcolor = 'r';
figure;
ft_multiplotER(cfg, gaerp_norm_diff);

% Substract conditions (reversed)
cfg = [];
cfg.operation = 'subtract';
cfg.parameter = 'avg';
gaerp_rev_diff = ft_math(cfg, gaerp_pos_rev, gaerp_neg_rev);

%Plot the difference
cfg            = [];
cfg.layout     = layout;
%cfg.graphcolor = 'r';
figure;
ft_multiplotER(cfg, gaerp_rev_diff);


%% SCALP PLOTS OF SUBSTRACTIONS FOR EACH ERP
%Scalp plot of substraction
cfg          = [];
cfg.layout   = layout;
cfg.zlim     = [-5 5];                % same scale for all or remove for free
cfg.marker   = 'on';                  % 'off' 'labels'
cfg.style    = 'both';                % 'straight' 'fill';
%cfg.comment  = 'off';                 % Comment on the figure
cfg.colorbar = 'yes';

figure;
cfg.xlim = p1;
subplot(3,2,1);ft_topoplotER(cfg, gaerp_norm_diff);
title('CS+ vs CS- : normal (p1)')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = p1;
subplot(3,2,2);ft_topoplotER(cfg, gaerp_rev_diff);
title('CS+ vs CS- : reversed (p1)')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = n170;
subplot(3,2,3);ft_topoplotER(cfg, gaerp_norm_diff);
title('CS+ vs CS- : normal (n170)')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = n170;
subplot(3,2,4);ft_topoplotER(cfg, gaerp_rev_diff);
title('CS+ vs CS- : reversed (n170)');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

cfg.xlim = lpp;
subplot(3,2,5);ft_topoplotER(cfg, gaerp_norm_diff);
title('CS+ vs CS- : normal (lpp)')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = lpp;
subplot(3,2,6);ft_topoplotER(cfg, gaerp_rev_diff);
title('CS+ vs CS- : reversed (lpp)')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

%change the colormap
ft_hastoolbox('brewermap', 1);         % ensure this toolbox is on the path
colormap(flipud(brewermap(257,'RdBu'))) % change the colormap

%% DIFFERENCE OF DIFFERENCES

% Substract conditions (reversed)
cfg = [];
cfg.operation = 'subtract';
cfg.parameter = 'avg';
gaerp_diff_diff = ft_math(cfg, gaerp_norm_diff, gaerp_rev_diff);

%Plot the difference
cfg            = [];
cfg.layout     = layout;
%cfg.graphcolor = 'r';
figure;
ft_multiplotER(cfg, gaerp_diff_diff);


%Scalp plot of diff of diff
cfg          = [];
cfg.layout   = layout;
cfg.zlim     = [-2 2];                % same scale for all or remove for free
cfg.marker   = 'on';                  % 'off' 'labels'
cfg.style    = 'fill';                % 'straight' 'fill';
%cfg.comment  = 'off';                 % Comment on the figure
cfg.colorbar = 'yes';
%cfg.renderer = 'zbuffer';

figure;
cfg.xlim = p1;
subplot(2,2,1);ft_topoplotER(cfg, gaerp_diff_diff);
title('P1 topography')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = n170;
subplot(2,2,2);ft_topoplotER(cfg, gaerp_diff_diff);
title('N170 topography');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

cfg.xlim = lpp;
subplot(2,2,3);ft_topoplotER(cfg, gaerp_diff_diff);
title('LPP topography')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = enp;
subplot(2,2,4);ft_topoplotER(cfg, gaerp_diff_diff);
title('Other topography');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

%change the colormap
colormap(flipud(brewermap(64,'RdBu'))) % change the colormap

%% plot mean ERP with SE

% compute grand average over subjects but keep individual representations
% in the output
cfg                = [];
cfg.latency        = [-.2 .8];
cfg.keepindividual = 'yes';
gaerpind = ft_timelockgrandaverage(cfg, allerp{:});

% and average over channels
cfg             = [];
cfg.channel     = {'PO8'};
%cfg.avgoverchan = 'yes';
gaerpind = ft_selectdata(cfg, gaerpind);

x = gaerpind.time'; % x-axis def
y = mean(squeeze(gaerpind.individual),1)'; % y-axis def
e = std(squeeze(gaerpind.individual),1)';  % std
se = e/sqrt(length(subjects));  % std
low = y - se;% lower bound
high = y + se;% upper bound
figure;
hp = patch([x; x(end:-1:1); x(1)], [low; high(end:-1:1); low(1)], 'r');
hold on;
hl = line(x,y);
set(hp, 'facecolor', [1 0.8 0.8], 'edgecolor', 'none');
set(hl, 'color', 'r','linewidth',2);
set(gca,'FontSize',20);
title ('Mean and SE over PO8');
set(gca,'box','on');
xlabel('time [sec]');
ylabel('amplitude (\muV)');


% Plot topography of the N1 and N170 components

cfg          = [];
cfg.layout   = layout;
cfg.zlim     = [-5 5];                % same scale for all or remove for free
cfg.marker   = 'on';                  % 'off' 'labels'
cfg.style    = 'fill';                % 'straight' 'fill';
%cfg.comment  = 'off';                 % Comment on the figure
cfg.colorbar = 'yes';
%cfg.renderer = 'zbuffer';

figure;
cfg.xlim = p1;
subplot(2,2,1);ft_topoplotER(cfg, gaerp);
title('P1 topography')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = n170;
subplot(2,2,2);ft_topoplotER(cfg, gaerp);
title('N170 topography');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

cfg.xlim = lpp;
subplot(2,2,3);ft_topoplotER(cfg, gaerp);
title('LPP topography')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = enp;
subplot(2,2,4);ft_topoplotER(cfg, gaerp);
title('Other topography');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

%change the colormap
ft_hastoolbox('brewermap', 1);         % ensure this toolbox is on the path
colormap(flipud(brewermap(64,'RdBu'))) % change the colormap

