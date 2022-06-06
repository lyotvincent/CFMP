import subprocess 
import os 
class tgs_quality_control:
    result_dir = None 
    conf = None 
    input_file = None 
    illumina_1 = None
    illumina_2 = None
    output=None
    def __init__(self, result_dir, conf, input_file=None,illumina_1=None,illumina_2=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        self.illumina_1 = illumina_1
        self.illumina_2 = illumina_2
    def nanoplot(self,folder_name):
        print('Begin NanoPlot')
        if 'fastq' not in self.input_file.split('.') and 'fq' not in self.input_file.split('.'):
            print('Please input "*.fastq*" or "*.fq*"...from NanoPlot')
            exit(0)
        nanoplot_conf = self.conf['NanoPlot']
        maxlength = nanoplot_conf['--maxlength']
        minlength = nanoplot_conf['--minlength']
        drop_outliers = nanoplot_conf['--drop_outliers']
        loglength = nanoplot_conf['--loglength']
        barcoded = nanoplot_conf['--barcoded']
        percentqual = nanoplot_conf['--percentqual']
        downsample = nanoplot_conf['--downsample']
        minqual = nanoplot_conf['--minqual']
        readtype = nanoplot_conf['--readtype']
        color = nanoplot_conf['--color']
        formats = nanoplot_conf['--format']
        plot_dot = nanoplot_conf['--plots']['dot']
        plot_kde = nanoplot_conf['--plots']['kde']
        plot_hex = nanoplot_conf['--plots']['hex']
        plot_pauvre = nanoplot_conf['--plots']['pauvre']
        no_N50 = nanoplot_conf['--no-N50']
        N50 = nanoplot_conf['--N50']
        title = nanoplot_conf['--title']
        com = 'NanoPlot --fastq '+self.input_file+' '
        if maxlength:
            com += '--maxlength ' + maxlength + ' '
        if minlength:
            com += '--minlength ' + minlength + ' '
        if drop_outliers:
            com += '--drop_outliers ' + drop_outliers + ' '
        if loglength is True:
            com += '--loglength '
        if barcoded is True:
            com += '--barcoded '
        if percentqual is True:
            com += '--percentqual '
        if downsample:
            com += '--downsample ' + downsample + ' '
        if minqual:
            com += '--minqual ' + minqual + ' '
        
        if readtype:
            com += '--readtype '+ readtype+' '
        if color:
            com += '--color ' + color + ' '
        if formats:
            com += '--format ' + formats + ' '
        if plot_dot or plot_kde or plot_hex or plot_pauvre:
            if plot_dot:
                com += '--plots dot'
            if plot_kde:
                com += ',kde'
            if plot_hex:
                com += ',hex'
            if plot_pauvre:
                com += ',pauvre'
            com += ' '
        if title:
            com += '--title ' + title + ' '
        com += '-o '+os.path.join(os.path.join(self.result_dir,'tgs_quality_control'),folder_name)
        subprocess.run(com,shell=True,check=True)
        
        print('End NanoPlot')
    def nanofilt(self):
        print('Begin NanoFilt')
        nanofilt_conf = self.conf['NanoFilt']
        maxlength = nanofilt_conf['--maxlength']
        length = nanofilt_conf['--length']
        quality = nanofilt_conf['--quality']
        minGC = nanofilt_conf['--minGC']
        maxGC = nanofilt_conf['--maxGC']
        readtype = nanofilt_conf['--readtype']
        com = 'NanoFilt '
        if maxlength:
            com += '--maxlength ' + maxlength + ' '
        if length:
            com += '--length ' + length + ' '
        if quality:
            com += '--quality ' + quality + ' '
        if minGC:
            com += '--minGC ' + minGC + ' '
        if maxGC:
            com += '--maxGC ' + maxGC + ' '
        if readtype:
            com += '--readtype ' + readtype + ' '
        com += self.input_file+' > '+os.path.join(os.path.join(self.result_dir,'tgs_quality_control'),'nanofilt.fastq')
        subprocess.run(com, shell=True, check=True)
        print('End NanoFilt')
    def filtlong(self):
        print('Begin Filtlong')
        filtlong_conf = self.conf['Filtlong']
        target_bases = filtlong_conf['--target_bases']
        keep_percent = filtlong_conf['--keep_percent']
        min_length = filtlong_conf['--min_length']
        min_mean_q = filtlong_conf['--min_mean_q']
        min_window_q = filtlong_conf['--min_window_q']
        length_weight = filtlong_conf['--length_weight']
        mean_q_weight = filtlong_conf['--mean_q_weight']
        window_q_weight = filtlong_conf['--window_q_weight']
        trim = filtlong_conf['--trim']
        split = filtlong_conf['--split']
        window_size = filtlong_conf['--window_size']
        com = 'filtlong '
        if target_bases:
            com += '--target_bases ' + str(target_bases) + ' '
        if keep_percent:
            com += '--keep_percent ' + str(keep_percent) + ' '
        if min_length:
            com += '--min_length ' + str(min_length) + ' '
        if min_mean_q:
            com += '--min_mean_q ' + str(min_mean_q) + ' '
        if min_window_q:
            com += '--min_window_q ' + str(min_window_q) + ' '
        if length_weight:
            com += '--length_weight ' + str(length_weight) + ' '
        if mean_q_weight:
            com += '--mean_q_weight ' + str(mean_q_weight) + ' '
        if window_q_weight:
            com += '--window_q_weight ' + str(window_q_weight) + ' '
        if trim is True:
            com += '--trim '
        if split:
            com += '--split ' + split + ' '
        if window_size:
            com += '--window_size ' + window_size + ' '
        if self.illumina_1:
            com += '--illumina_1 '+illumina_1+' '
        if self.illumina_2:
            com += '--illumina_2 '+illumina_2+' '
        com += self.input_file +' > '+os.path.join(os.path.join(self.result_dir,'tgs_quality_control'),'filtlong.fastq')
        subprocess.run(com, shell=True, check=True)
        print('End Filtlong')
    def porechop(self):
        print('Begin Porechop')
        porechop_conf = self.conf['Porechop']
        barcode_dir = porechop_conf['--barcode_dir']
        barcode_threshold = porechop_conf['--barcode_threshold']
        barcode_diff = porechop_conf['--barcode_diff']
        require_two_barcodes = porechop_conf['--require_two_barcodes']
        untrimmed = porechop_conf['--untrimmed']
        discard_unassigned = porechop_conf['--discard_unassigned']
        adapter_threshold = porechop_conf['--adapter_threshold']
        check_reads = porechop_conf['--check_reads']
        scoring_scheme = porechop_conf['--scoring_scheme']
        end_size = porechop_conf['--end_size']
        min_trim_size = porechop_conf['--min_trim_size']
        extra_end_trim = porechop_conf['--extra_end_trim']
        end_threshold = porechop_conf['--end_threshold']
        no_split = porechop_conf['--no_split']
        discard_middle = porechop_conf['--discard_middle']
        middle_threshold = porechop_conf['--middle_threshold']
        extra_middle_trim_good_side = porechop_conf['--extra_middle_trim_good_side']
        extra_middle_trim_bad_side = porechop_conf['--extra_middle_trim_bad_side']
        min_split_read_size = porechop_conf['--min_split_read_size']
        com = 'porechop -i '+self.input_file+' '
        if barcode_dir:
            com += '--barcode_dir '+barcode_diff+' '
        if barcode_threshold:
            com += '--barcode_threshold '+barcode_threshold+' '
        if barcode_diff:
            com += '--barcode_diff '+barcode_diff+' '
        if require_two_barcodes:
            com += '--require_two_barcodes '
        if untrimmed:
            com += '--untrimmed '
        if discard_unassigned:
            com += '--discard_unassigned '
        if check_reads:
            com += '--check_reads '+check_reads+' '
        if scoring_scheme:
            com += '--scoring_scheme '+scoring_scheme+' '
        if end_size:
            com += '--end_size '+end_size+' '
        if min_trim_size:
            com += '--min_trim_size '+min_trim_size+' '
        if extra_end_trim:
            com += '--extra_end_trim '+extra_end_trim+' '
        if end_threshold:
            com += '--end_threshold '+end_threshold+' '
        if no_split:
            com += '--no_split '
        if discard_middle:
            com += '--discard_middle '
        if extra_middle_trim_good_side:
            com += '--extra_middle_trim_good_side '+extra_middle_trim_good_side+' '
        if extra_middle_trim_bad_side:
            com += '--extra_middle_trim_bad_side '+extra_middle_trim_bad_side+' '
        if min_split_read_size:
            com += '--min_split_read_size '+min_split_read_size+' '
        com += '-o '+os.path.join(os.path.join(self.result_dir,'tgs_quality_control'),'porechop.fastq')
        subprocess.run(com, shell=True, check=True)
        print('End Porechop')
        
    def run(self):
        print('Begin tgs_quality_control')
        if self.conf['NanoPlot']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/tgs_quality_control/nanoplot_before_filtering')
            self.nanoplot('nanoplot_before_filtering')
        quality_filter = None 
        if self.conf['NanoFilt']['enable']:
            self.nanofilt()
            quality_filter = os.path.join(os.path.join(os.path.join(os.path.abspath('.'),self.result_dir),'tgs_quality_control'),'nanofilt.fastq')
        elif self.conf['Filtlong']['enable']:
            self.filtlong()
            quality_filter = os.path.join(os.path.join(os.path.join(os.path.abspath('.'),self.result_dir),'tgs_quality_control'),'filtlong.fastq') 
        else:
            quality_filter = self.input_file
        self.input_file = quality_filter
        if self.conf['Porechop']['enable']:
            self.porechop()
            self.output = os.path.join(os.path.join(self.result_dir,'tgs_quality_control'),'porechop.fastq')
        else:
            self.output = self.input_file
        self.input_file = self.output
        if self.conf['NanoPlot']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/tgs_quality_control/nanoplot_after_filtering')
            self.nanoplot('nanoplot_after_filtering')
        print('End tgs_quality_control')
        