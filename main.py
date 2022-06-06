import os 
import sys 
import time 
import json 
import yaml 
import ngs_pipeline 
import tgs_pipeline 
import preprocessing 
import configuration_reader 
def main():
    time_note2 = time.time()
    time_note = time.process_time() 
    argv = sys.argv 
    print(str(argv)) 
    if "-V" in argv or "-v" in argv or '-version' in argv or '--version' in argv:
        print("CFMP version: 0.1") 
        exit(0) 
    if len(argv) == 1 or '-h' in argv or '-help' in argv or '--h' in argv or '--help' in argv:
        print_help()
        exit(0)
    input_file = None 
    input_file_1 = None 
    input_file_2 = None
    ngs = None 
    tgs = None 
    pacbio = None 
    nanopore = None
    mode = None
    if '-ngs' in argv and not '-tgs' in argv:
        ngs = 1 
        if '-f' in argv and not '-1' in argv and not '-2' in argv:
            input_file = argv[argv.index('-f')+1] 
            mode = 1 
        elif '-1' in argv and '-2' in argv and not '-f' in argv:
            input_file_1 = argv[argv.index('-1')+1] 
            input_file_2 = argv[argv.index('-2')+1] 
            mode = 2 
        else:
            print('Please input -f or -1 and -2. And dont input -f, -1 and -2 at the same time.') 
            exit(0) 
    elif '-tgs' in argv and not '-ngs' in argv:
        tgs = 1 
        if '-f' in argv:
            input_file = argv[argv.index('-f')+1] 
        else:
            print('Please input -f as input_file for -tgs')
            exit()
        if '-pacbio' in argv:
            pacbio = argv[argv.index('-pacbio')+1]
        
        if '-nanopore' in argv:
            nanopore = argv[argv.index('-nanopore')+1]
    else:
        print('please choose -ngs or -tgs') 
        print_help()
        exit(0)
    
    if '-conf_file_path' in argv:
        conf_file_path = argv[argv.index('-conf_file_path')+1] 
    else:
        print('Please input configuration file path.') 
        exit(0) 
    conf = configuration_reader.ConfigurationReader(conf_file_path).run() 
    
    if '-o' in argv:
        result_dir = argv[argv.index('-o')+1]+'_'
    else:
        result_dir = '' 
    start_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()) 
    result_dir += 'result_'+start_time 
    print('result_dir='+os.path.abspath('.')+'/'+result_dir) 
    if not os.path.exists(os.path.abspath('.')+'/'+result_dir):
        os.mkdir(os.path.abspath('.')+'/'+result_dir) 
    temp_file = open(os.path.abspath('.')+'/'+result_dir+'/Summary_of_results.html','w') 
    temp_file.close() 
    if ngs == 1:
        if mode == 1:
            ngs = ngs_pipeline.NextGenerationSequencing(result_dir,conf['ngs_pipeline'],input_file=input_file) 
            ngs.run_single() 
        elif mode == 2:
            ngs = ngs_pipeline.NextGenerationSequencing(result_dir,conf['ngs_pipeline'],input_file_1=input_file_1,input_file_2=input_file_2) 
            ngs.run_paired() 
    if tgs == 1:
        print('tgs')
        tgs = tgs_pipeline.ThirdGenerationSequencing(result_dir,conf['tgs_pipeline'],input_file=input_file,pacbio=pacbio,nanopore=nanopore,input_file_1=input_file_1,input_file_2=input_file_2) 
        tgs.run() 
    print('starttime='+start_time) 
    print('endtime='+time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())) 
    print('process_time='+str(time.time()-time_note2)) 
    print('End') 
    temp_file = open(os.path.abspath('.')+'/'+result_dir+'/Summary_of_results.html','a+') 
    temp_file.write('<ul>\n') 
    temp_file.write('<li>starttime= %s' % start_time)
    temp_file.write('<li>endtime= %s' % time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime()))
    temp_file.write('<li>process_time %s</li>\n' % (time.process_time()-time_note)) 
    temp_file.write('<li>time %s</li>\n' % (time.time()-time_note2)) 
    temp_file.write('</ul>\n') 
    temp_file.close() 
def print_help():
    print('help:')
    print('-f input single end file when -ngs or input pacbio/nanopore file when -tgs') 
    print('-1 and -2 input paired end files when -ngs or input illumina_1 and illumina_2 for polish when -tgs') 
    print('-pacbio input pacbio file for polish when -tgs')
    print('-nanopore input nanopore file for polish when -tgs')
    print('-o out directory name') 
    print('-ngs make pipeline run for next-generation sequencing data (short reads)') 
    print('-tgs make pipeline run for third-generation sequencing data (long reads)') 
    print('-conf_file_path configuration file for CFMP pipeline which is in xlsx format') 
    print('-h or -help or --h or --help look help') 

if __name__ == '__main__':
    main() 