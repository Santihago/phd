%=================================
% GRAND AVERAGE TIMELOCK ANALYSIS
% AUTHOR: SANTIAGO MUÑOZ-MOLDES
% DATE: JULY 2019
%=================================

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
ft_hastoolbox('brewermap', 1);         % ensure this toolbox is on the path

% Participants
% Participants
everyone = 1:70;
excluded = [6 21 15 25 40 54 60 65 67];  %54 and 60 have very big trial artefacts
included = setdiff(everyone, excluded);  % change script if need to use 'included'
subjects = included; %1:70;

% load the biosemi 64 channel template that has channel coordinates and
% names
cfg        = [];
cfg.layout = 'biosemi64.lay';
layout = ft_prepare_layout(cfg);
    
% latencies for each ERP, in seconds

p1   = [0.1 0.14];
n170 = [0.14 0.21];
enp  = [.3 .4];
lpp  = [.4 .6];

%% COMPUTATION OF EVENT-RELATED POTENTIALS AND OF THE GROUP AVERAGE
for i=1:length(subjects)

    datafile = fullfile(root_dir, 'clean', strcat(num2str(subjects(i)), '.mat'));
    load(datafile);
    
    % average across trials
    cfg         = [];
    cfg.channel = {'all'};
    erp         = ft_timelockanalysis(cfg, data_clean);
    
    save(fullfile(root_dir, 'erp', num2str(subjects(i))), 'erp')
end

% load single subject ERPs in a single cell array
allerp = cell(1, length(subjects));
for i=1:length(subjects)
    datafile = fullfile(root_dir, 'erp', strcat(num2str(subjects(i)), '.mat'));
    load(datafile);
    allerp{i} = erp;
end

% compute grand average across subjects
cfg         = [];
cfg.latency = [-.2 .8];
gaerp       = ft_timelockgrandaverage(cfg, allerp{:});


%% VISUALIZATION OF THE GROUP AVERAGE ERP

% plot a sensor layout with the ERP time course at each electrode
cfg            = [];
cfg.layout     = layout;
cfg.graphcolor = 'r';
cfg.showcomment = 'no';

figure;
ft_multiplotER(cfg, gaerp);

% Plot topography of the P1, N170 and LPP components

cfg          = [];
cfg.layout   = layout;
%cfg.zlim     = [-5 5];    % same scale for all or remove for free
cfg.marker   = 'on';      % 'off' or 'labels'
cfg.style    = 'both';    % 'straight' 'fill';
%cfg.comment  = 'off';    % Comment on the figure
cfg.colorbar = 'yes';
cfg.showcomment = 'no';

figure;
cfg.xlim = p1;
cfg.zlim     = [-7 7];
subplot(3,1,1);ft_topoplotER(cfg, gaerp);
title('P1 topography')
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV')

cfg.xlim = n170;
cfg.zlim     = [-3 3];
subplot(3,1,2);ft_topoplotER(cfg, gaerp);
title('N170/VPP topography');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

cfg.xlim = lpp;
cfg.zlim     = [-3 3];
subplot(3,1,3);ft_topoplotER(cfg, gaerp);
title('LPP topography');
c = colorbar;
c.LineWidth = 1;
c.FontSize = 18;
title(c,'\muV');

%change the colormap
colormap(flipud(brewermap(129,'RdBu'))) % change the colormap

%% % plot mean ERP

cfg            = [];
%cfg.ylim       = [-1 1];
cfg.channel    = {'PO8'};
cfg.linewidth  = 2;
cfg.graphcolor = 'r';
figure;
ft_singleplotER(cfg, gaerp);
% % use the rectangle to indicate the time range used later
% rectangle('Position',[p1(1) -5 (p1(2)-p1(1)) 15],'FaceColor',[0 .5 .5 .3]);
% rectangle('Position',[n170(1) -5 (n170(2)-n170(1)) 15],'FaceColor',[.5 .5 .5 .3]);
% rectangle('Position',[lpp(1) -5 (lpp(2)-lpp(1)) 	15],'FaceColor',[0 0 .5 .3]);
% hold on;
% below are some 'low-level' matlab commands that do some window dressing
% on the figure
set(gca, 'Fontsize', 20);
%title('Mean over PO8');
set(gca,'box','on');
xlabel('time [sec]');
ylabel('amplitude (\muV)');

%% plot mean P1 over Oz ERP with SE 

% compute grand average over subjects but keep individual representations
% in the output
cfg                = [];
cfg.latency        = [-.2 .8];
cfg.keepindividual = 'yes';
gaerpind = ft_timelockgrandaverage(cfg, allerp{:});

% and average over channels
cfg             = [];
cfg.channel     = {'POz'};
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
% use the rectangle to indicate the time range used later
rectangle('Position',[lpp(1) -2 (lpp(2)-lpp(1)) 8],'FaceColor',[0.93 .93 .93 .3]);
%rectangle('Position',[n170(1) -8 (n170(2)-n170(1)) 16],'FaceColor',[0.93 .93 .93 .3]);
%rectangle('Position',[p1(1) -8 (p1(2)-p1(1)) 16],'FaceColor',[0.93 .93 .93 .3]);
%hl = line([0 0], get(gca, 'ylim'));
%hl.Color = 'k';
hl = line(x,y);
set(hp, 'facecolor', [1 0.8 0.8], 'edgecolor', 'none');  % [1 0.8 0.8]
set(hl, 'color', 'r','linewidth',2);
set(gca,'FontSize',20);
title ('Mean and SE over POz');
set(gca,'box','on');
xlabel('time [sec]');
ylabel('amplitude (\muV)');
ylim([-2 4])
%rectangle('Position',[n170(1) -5 (n170(2)-n170(1)) 15],'FaceColor',[.5 .5 .5 .3]);
%rectangle('Position',[lpp(1) -5 (lpp(2)-lpp(1)) 	15],'FaceColor',[0 0 .5 .3]);

%okabe_orange = 0.9020 0.6235 0
%uisetcolor()
