import subprocess 
import os 
class tgs_assembly:
    result_dir = None 
    conf = None 
    input_file = None 
    output = None
    def __init__(self,result_dir,conf,input_file):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        if os.path.isdir(os.path.join(self.result_dir,'tgs_assembly')) is False:
            os.mkdir(os.path.join(self.result_dir,'tgs_assembly'))
    def canu(self):
        print('Begin Canu')
        canu_conf = self.conf['canu']
        command_line = 'canu -p canu_assembly_result -d '+self.result_dir+'/tgs_assembly/canu_output/ '
        if canu_conf['genomeSize'] != None:
            command_line += 'genomeSize='+str(canu_conf['genomeSize'])+' '
        else:
            command_line += 'genomeSize=4.8m '
        if canu_conf['minReadLength'] != None:
            command_line += 'minReadLength='+str(int(canu_conf['minReadLength']))+' '
        if canu_conf['minOverlapLength'] != None:
            command_line += 'minOverlapLength='+str(int(canu_conf['minOverlapLength']))+' '
        command_line+='stopOnLowCoverage=1 '
        if canu_conf['-pacbio-raw'] != None:
            command_line += '-pacbio-raw '
        elif canu_conf['-pacbio-corrected'] != None:
            command_line += '-pacbio-corrected '
        elif canu_conf['-nanopore-raw'] != None:
            command_line += '-nanopore-raw '
        elif canu_conf['-nanopore-corrected'] != None:
            command_line += '-nanopore-corrected '
        else:
            print('Error. Please set one of "-pacbio-raw","-pacbio-corrected","-nanopore-raw","-nanopore-corrected" True in Canu')
            exit(0)
        command_line += self.input_file 
        subprocess.run(command_line, shell=True, check=True)
        print('End Canu')
    def Flye(self):
        print('Begin Flye')
        flye_conf = self.conf['Flye']
        inputtype = flye_conf['--input_type']
        genomesize = flye_conf['--genome-size']
        iterations = flye_conf['--iterations']
        minoverlap = flye_conf['--min-overlap']
        asmcoverage = flye_conf['--asm-coverage']
        hifierror = flye_conf['--hifi-error']
        meta = flye_conf['--meta']
        plasmid = flye_conf['--plasmids']
        trestle = flye_conf['--trestle']
        polishtarget = flye_conf['--polish-target']
        keephaplotypes = flye_conf['--keep-haplotypes']
        if inputtype is None:
            print('Error. Please set "--input_type" in Flye')
            exit(0)
        com = 'flye '
        if inputtype:
            com += inputtype + ' '
        com += self.input_file+' -o '+os.path.join(self.result_dir,'tgs_assembly')+' '
        if genomesize:
            com += '--genome-size '+genomesize+' '
        if iterations:
            com += '--iterations '+iterations+' '
        if minoverlap:
            com += '--min-overlap '+minoverlap+' '
        if asmcoverage:
            com += '--asm-coverage '+asmcoverage+' '
        if hifierror:
            com += '--hifi-error '+hifierror+' '
        if trestle:
            com += '--trestle '
        if meta:
            com += '--meta ' 
        if plasmid:
            com += '--plasmid ' 
        if polishtarget:
            com += '--polish-target ' 
        if keephaplotypes:
            com += '--keep-haplotypes ' 
        com += '--meta '
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        print('End Flye')
    
    def SMARTdenovo(self):
        print('Begin SMARTdenovo')
        smartdenovo_conf = self.conf['SMARTdenovo']
        smartdenovop = smartdenovo_conf['-p']
        smartdenovoe = smartdenovo_conf['-e']
        smartdenovok = smartdenovo_conf['-k']
        smartdenovoJ = smartdenovo_conf['-J']
        smartdenovoc = smartdenovo_conf['-c']
        com = 'smartdenovo.pl '
        if smartdenovop:
            com += '-p '+os.path.join(os.path.join(self.result_dir,'tgs_assembly'),smartdenovop)+' '
            os.mkdir(os.path.join(os.path.join(self.result_dir,'tgs_assembly'),smartdenovop))
        if smartdenovoe:
            com += '-e '+smartdenovoe+' '
        if smartdenovok:
            com += '-k '+smartdenovok+' '
        if smartdenovoJ:
            com += '-J '+smartdenovoJ+' '
        if smartdenovoc == 0:
            com += '-c '+smartdenovoc+' '
        else:
            com += '-c 1 '
        com += self.input_file+' > '+os.path.join(os.path.join(self.result_dir,'tgs_assembly'),'smartdenovo.mak')
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        subprocess.run('make -f '+os.path.join(os.path.join(self.result_dir,'tgs_assembly'),'smartdenovo.mak'), shell=True, check=True,encoding='utf-8')
    
        
    def assembly_assessment(self, input_file):
        print('Begin QUAST')
        subprocess.run('quast.py '+input_file+' -o '+self.result_dir+'/tgs_assembly/quast_out', shell=True, check=True)
        print('End QUAST')
    def run(self):
        print('begin tgs_assembly')
        if self.conf['canu']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/tgs_assembly/canu_output')
            self.canu()
            self.output = self.result_dir+'/tgs_assembly/canu_output/canu_assembly_result.contigs.fasta'
        elif self.conf['Flye']['enable']:   
            self.Flye()
            self.output = os.path.join(os.path.join(self.result_dir,'tgs_assembly'),'assembly.fasta')
        elif self.conf['SMARTdenovo']['enable']:
            self.SMARTdenovo()
            smartdenovop = self.conf['SMARTdenovo']['-p']
            com = 'mv '+os.path.join(os.path.join(self.result_dir,'tgs_assembly'),smartdenovop+'.dmo.cns')+' '+os.path.join(os.path.join(self.result_dir,'tgs_assembly'),smartdenovop+'.dmo.cns.fa')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            self.output = os.path.join(os.path.join(self.result_dir,'tgs_assembly'),smartdenovop+'.dmo.cns.fa')
        else:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/tgs_assembly/canu_output')
            self.canu()
            self.output = self.result_dir+'/tgs_assembly/canu_output/canu_assembly_result.contigs.fasta'
        self.assembly_assessment(self.output)
        print('end tgs_assembly')