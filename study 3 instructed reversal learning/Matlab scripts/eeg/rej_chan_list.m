rej_chan = {
    {'EEG' '-F6'  '-F8'  '-FT8'} %1
    {'EEG' '-FT8' '-T8'  '-FT7'} %2
    {'EEG' '-AF7' '-AF8' '-Fp1' '-Fp2' '-Fpz'} %3
    {'EEG' '-Oz'  '-T8'  '-Fp2'} %4
    {'EEG' '-AF8'} %5
    {'EEG' '-Fp2' '-FT8' '-T7'} %6
    {'EEG' '-FT7' '-T7'  'Fp2' 'FC5' } %7
    {'EEG' '-T7'  '-TP7' '-T8'} %8
    {'EEG' '-Oz'  '-POz' '-PO4' } %9
    {'EEG' '-AF8' } %10
    
    {'EEG' '-Fp1' '-Fp2'} %11
    {'EEG' '-Fpz' '-Fp2' '-Fp1' '-AF7'} %12
    {'EEG' '-AF4' '-Fp1'} %13 probably need to be interpolated Af4
    {'EEG' '-FT8' '-F5'  '-F8' '-TP7'} %14
    {'EEG' '-AF7' '-FC5' '-Iz' '-FT8'} %15
    {'EEG' '-AF8' '-FT8' '-Fp2' } %16
    {'EEG' '-T7'  '-FT8' '-TP8' '-CP5' } %17
    {'EEG' '-Fp2' '-FT7' } %18
    {'EEG' '-PO7' '-F6' } %19
    {'EEG' '-AF7' '-FT7' '-AF8' '-Fp2' } %20
    
    {'EEG' '-Fp1' '-FT7' '-T7' } %21
    {'EEG' '-AF7' '-AF7' '-TP7'  '-AF3'} %22
    {'EEG' '-T7'  '-F5'  '-FT7' } %23
    {'EEG' '-T7'  '-AF7' '-AF8' '-T8' '-Fp2' } %24
    {'EEG' '-AF8' '-FC3' '-AF7' '-F7' '-FT7' '-FC4' '-AF4'} %25
    {'EEG' '-Fp1' '-AF3' '-F3' } %26
    {'EEG' '-FC2' '-FT8' '-AF7' '-AF4' '-TP7' } %27   % interpolate FC2 FT8
    {'EEG' '-F1'  '-POz' '-P1' '-FT7' '-F6' } %28    % interpolate F1
    {'EEG' '-Fp1' '-AF7' '-Fpz' '-Fp2' '-AF8' '-Iz'} %29
    {'EEG' '-AF8' '-FC4' '-P7' '-FC5'} %30
    
    {'EEG' '-AF8' '-F7'}  %31
    {'EEG' '-FC4'}  %32
    {'EEG' '-FC4'}  %33
    {'EEG' '-Fp2'}  %34
    {'EEG'}  %35
    {'EEG' '-F4' '-FC4' '-FC6' '-F6' '-AF4' '-AF8' '-F8'}  %36
    {'EEG'}  %37  
    {'EEG'  '-F7' '-AF7' '-AF4' '-T7' '-T8' '-F8' '-AF8' '-FT8' '-FT7'}  %38
    {'EEG' '-AF3' '-AF4' '-AF7' '-AFz' '-F2' '-CP5'}  %39
    {'EEG'}  %40
    
    {'EEG'}  %41 % P8 bad....
    {'EEG' '-Oz'  '-Fpz'  '-Fp2'}  %42
    {'EEG' '-FT7' '-T8'   '-T7'}  %43
    {'EEG' '-TP8'}  %44
    {'EEG' '-T8'  '-T7'   '-F3'}  %45
    {'EEG' '-FCz'}  %46
    {'EEG' '-TP8' '-FC3'}  %47
    {'EEG'}  %48
    {'EEG'}  %49
    {'EEG' '-F6' '-FT7' '-C1' '-P3' '-Fpz' '-F8' '-C2'}  %50
    
    {'EEG'}  %51
    {'EEG' '-CP2' '-Pz' '-AFz' '-TP8'}  %52
    {'EEG'}  %53
    {'EEG' '-AF7' '-F7'   '-FT7' '-AF8' '-Fpz' '-Fp2' '-T7'}  %54 many bad looking trials
    {'EEG'}  %55
    {'EEG' '-F7'  '-AF8'  '-F8'}  %56
    {'EEG' '-P10'}  %57 interpolate P10
    {'EEG'}  %58
    {'EEG' '-F4'}  %59
    {'EEG' '-FC5' '-P9'  '-F6' '-C6'}  %60
    
    {'EEG' '-TP7'}  %61
    {'EEG' '-T7'  '-AF7'  '-F4'}  %62
    {'EEG' '-T8'}  %63
    {'EEG'}  %64
    {'EEG'}  %65 
    {'EEG'}  %66
    {'EEG'}  %67
    {'EEG'}  %68
    {'EEG'}  %69
    {'EEG' '-PO7' '-CP4'}  %70
    
    };

save('/Users/santiago/Dropbox/MyScience/MyPhD/MyPhD-projects/ALR/analysis/eeg/scripts/rej_chan', 'rej_chan')