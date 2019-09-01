%===============================
% EXTRACT ERP VALUES
% AUTHOR: SANTIAGO MUÑOZ-MOLDES
% DATE: JULY 2019
%===============================

clear
close all
clc

%% SETUP
root_dir = '/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/analysis/eeg/';
cd(root_dir)
addpath('./scripts/')

% Basic experimental info
subjects = 1:70;
ntrials = 1:80;

% Our ERP info and latencies
erps = 1:3;  % number of ERPs to calculate
p1   = [.1  .14];
n170 = [.14 .21];
lpp  = [.4  .6];

% Create empty table
big_table = zeros((length(subjects)*length(ntrials)*length(erps)), 4);  % long format

tic
for i=1:length(subjects)
    
    disp(strcat('Calculating for subject', {' '}, num2str(i), '...'))
   
    %load
    datafile = fullfile(root_dir, 'clean', strcat(num2str(subjects(i)), '.mat'));
    load(datafile);
   
    for j=1:length(erps) % for each erp
        
        % ELECTRODE AND TIMEPOINTS OF INTEREST
        switch j
            case 1 % P1
                elec    = find(strcmp(data_clean.label, 'Oz')); 
                timesel = find(data_clean.time{1,1} >= p1(1) & data_clean.time{1,1} <= p1(2));
            case 2 % N170
                elec    = find(strcmp(data_clean.label, 'PO8')); 
                timesel = find(data_clean.time{1,1} >= n170(1) & data_clean.time{1,1} <= n170(2));
            case 3 % LPP
                elec    = find(strcmp(data_clean.label, 'POz')); 
                timesel = find(data_clean.time{1,1} >= lpp(1) & data_clean.time{1,1} <= lpp(2));
        end
       
        % SELECT DATA EACH TRIAL
        for k=1:length(ntrials)
            
            % SELECT DATA
            data = data_clean.trial{1,k}(elec, timesel);
            
            % COMPUTATION (peak or average)
            switch j
                case 1 % positive peak
                    value = max(data);
                case 2 % negative peak
                    value = min(data);
                case 3 % average activation
                    value = mean(data); % 'average'
            end
            
            % ADD TO TABLE
            this_pos = (240*(i-1)) + (length(erps)*(k-1)) + j;  % find the row
            big_table(this_pos, 4) = value;
            
            % OTHER INFO
            big_table(this_pos,1) = i; %add IDs
            big_table(this_pos,2) = k; %add trial
            big_table(this_pos,3) = j; %add erp nr
        end

    end
    
end
toc  % Elapsed time is 7 seconds.

% export
csvwrite(strcat(fullfile(root_dir, 'scripts', 'erp_table.csv')), big_table)