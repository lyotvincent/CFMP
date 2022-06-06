import subprocess
import os

class Assembly:

    result_dir = None
    conf = None
    input_file = None
    input_file_1 = None
    input_file_2 = None
    input_file_12 = None
    output = None
    def __init__(self, result_dir, conf, input_file=None, input_file_1=None, input_file_2=None, input_file_12=None):
        self.result_dir = result_dir
        self.conf = conf
        self.input_file = input_file
        self.input_file_1 = input_file_1
        self.input_file_2 = input_file_2
        self.input_file_12 = input_file_12

    def megahit_single(self):
        print("begin megahit_single_end")
        megahit_conf = self.conf['megahit']
        command_line = 'megahit '
        if megahit_conf['--min-count'] != None:
            command_line += '--min-count %s ' % int(megahit_conf['--min-count'])
        if megahit_conf['--k-list'] != None:
            command_line += '--k-list '+str(megahit_conf['--k-list'])+' '
        if megahit_conf['--no-mercy'] != None:
            command_line += '--no-mercy '
        if megahit_conf['--bubble-level'] != None:
            command_line += '--bubble-level %s ' % int(megahit_conf['--bubble-level'])
        if megahit_conf['--merge-level'] != None:
            command_line += '--merge-level '+str(megahit_conf['--merge-level'])+' '
        if megahit_conf['--prune-level'] != None:
            command_line += '--prune-level %s ' % int(megahit_conf['--prune-level'])
        if megahit_conf['--prune-depth'] != None:
            command_line += '--prune-depth %s ' % int(megahit_conf['--prune-depth'])
        if megahit_conf['--low-local-ratio'] != None:
            command_line += '--low-local-ratio '+str(megahit_conf['--low-local-ratio'])+' '
        if megahit_conf['--max-tip-len'] != None:
            command_line += '--max-tip-len %s ' % int(megahit_conf['--max-tip-len'])
        if megahit_conf['--no-local'] != None:
            command_line += '--no-local '
        if megahit_conf['--kmin-1pass'] != None:
            command_line += '--kmin-1pass '
        if megahit_conf['-m'] != None:
            command_line += '-m '+str(megahit_conf['-m'])+' '
        if megahit_conf['--mem-flag'] != None:
            command_line += '--mem-flag %s ' % int(megahit_conf['--mem-flag'])
        if megahit_conf['-t'] != None:
            command_line += '-t %s ' % int(megahit_conf['-t'])
        if megahit_conf['--no-hw-accel'] != None:
            command_line += '--no-hw-accel '
        if megahit_conf['--min-contig-len'] != None:
            command_line += '--min-contig-len %s ' % int(megahit_conf['--min-contig-len'])
        command_line += '-r '+self.input_file+' -o '+self.result_dir+'/assembly/megahit_out'
        subprocess.run(command_line, shell=True, check=True, encoding=True)
        print("end megahit_single_end")
    
    def megahit_paired(self):
        print("begin megahit_paired_end")
        megahit_conf = self.conf['megahit']
        command_line = 'megahit '
        if megahit_conf['--min-count'] != None:
            command_line += '--min-count %s ' % int(megahit_conf['--min-count'])
        if megahit_conf['--k-list'] != None:
            command_line += '--k-list '+str(megahit_conf['--k-list'])+' '
        if megahit_conf['--no-mercy'] != None:
            command_line += '--no-mercy '
        if megahit_conf['--bubble-level'] != None:
            command_line += '--bubble-level %s ' % int(megahit_conf['--bubble-level'])
        if megahit_conf['--merge-level'] != None:
            command_line += '--merge-level '+str(megahit_conf['--merge-level'])+' '
        if megahit_conf['--prune-level'] != None:
            command_line += '--prune-level %s ' % int(megahit_conf['--prune-level'])
        if megahit_conf['--prune-depth'] != None:
            command_line += '--prune-depth %s ' % int(megahit_conf['--prune-depth'])
        if megahit_conf['--low-local-ratio'] != None:
            command_line += '--low-local-ratio '+str(megahit_conf['--low-local-ratio'])+' '
        if megahit_conf['--max-tip-len'] != None:
            command_line += '--max-tip-len %s ' % int(megahit_conf['--max-tip-len'])
        if megahit_conf['--no-local'] != None:
            command_line += '--no-local '
        if megahit_conf['--kmin-1pass'] != None:
            command_line += '--kmin-1pass '
        if megahit_conf['-m'] != None:
            command_line += '-m '+str(megahit_conf['-m'])+' '
        if megahit_conf['--mem-flag'] != None:
            command_line += '--mem-flag %s ' % int(megahit_conf['--mem-flag'])
        if megahit_conf['-t'] != None:
            command_line += '-t %s ' % int(megahit_conf['-t'])
        if megahit_conf['--no-hw-accel'] != None:
            command_line += '--no-hw-accel '
        if megahit_conf['--min-contig-len'] != None:
            command_line += '--min-contig-len %s ' % int(megahit_conf['--min-contig-len'])
        command_line += '-1 '+self.input_file_1+' -2 '+self.input_file_2+' -o '+self.result_dir+'/assembly/megahit_out'
        subprocess.run(command_line, shell=True, check=True)
        print("end megahit_paired_end")

    def megahit_interleaved(self):
        print("begin megahit_interleaved")
        megahit_conf = self.conf['megahit']
        command_line = 'megahit '
        if megahit_conf['--min-count'] != None:
            command_line += '--min-count '+str(megahit_conf['--min-count'])+' '
        if megahit_conf['--k-list'] != None:
            command_line += '--k-list '+str(megahit_conf['--k-list'])+' '
        if megahit_conf['--no-mercy'] != None:
            command_line += '--no-mercy '
        if megahit_conf['--bubble-level'] != None:
            command_line += '--bubble-level '+str(megahit_conf['--bubble-level'])+' '
        if megahit_conf['--merge-level'] != None:
            command_line += '--merge-level '+str(megahit_conf['--merge-level'])+' '
        if megahit_conf['--prune-level'] != None:
            command_line += '--prune-level '+str(megahit_conf['--prune-level'])+' '
        if megahit_conf['--prune-depth'] != None:
            command_line += '--prune-depth '+str(megahit_conf['--prune-depth'])+' '
        if megahit_conf['--low-local-ratio'] != None:
            command_line += '--low-local-ratio '+str(megahit_conf['--low-local-ratio'])+' '
        if megahit_conf['--max-tip-len'] != None:
            command_line += '--max-tip-len '+str(megahit_conf['--max-tip-len'])+' '
        if megahit_conf['--no-local'] != None:
            command_line += '--no-local '
        if megahit_conf['--kmin-1pass'] != None:
            command_line += '--kmin-1pass '
        if megahit_conf['-m'] != None:
            command_line += '-m '+str(megahit_conf['-m'])+' '
        if megahit_conf['--mem-flag'] != None:
            command_line += '--mem-flag '+str(megahit_conf['--mem-flag'])+' '
        if megahit_conf['-t'] != None:
            command_line += '-t '+str(megahit_conf['-t'])+' '
        if megahit_conf['--no-hw-accel'] != None:
            command_line += '--no-hw-accel '
        if megahit_conf['--min-contig-len'] != None:
            command_line += '--min-contig-len '+str(megahit_conf['--min-contig-len'])+' '
        command_line += '-12 '+self.input_file_12+' -o '+self.result_dir+'/megahit_out'
        subprocess.run(command_line, shell=True, check=True)
        print("end megahit_interleaved")

    def spades_single(self):
        print("begin spades_single_end")
        spades_conf = self.conf['spades']
        command_line = 'spades.py -s '+self.input_file+' '
        if spades_conf['--iontorrent'] != None:
            command_line += '--iontorrent '
        if spades_conf['-t'] != None:
            command_line += '-t %s ' % int(spades_conf['-t'])
        if spades_conf['-m'] != None:
            command_line += '-m %s ' % int(spades_conf['-m'])
        if spades_conf['-k'] != None:
            command_line += '-k '+str(spades_conf['-k'])+' '
        if spades_conf['--cov-cutoff'] != None:
            command_line += '--cov-cutoff '+str(spades_conf['--cov-cutoff'])+' '
        if spades_conf['--phred-offset'] != None:
            command_line += '--phred-offset '+str(spades_conf['--phred-offset'])+' '
        command_line += '-o '+self.result_dir+'/assembly/spades_out/'
        subprocess.run(command_line, shell=True, check=True)
        print("end spades_single_end")
    
    def spades_interlaced(self):
        print("begin spades_interlaced")
        spades_conf = self.conf['spades']
        command_line = 'spades.py -12 '+self.input_file_12+' '
        if spades_conf['--iontorrent'] != None:
            command_line += '--iontorrent '
        if spades_conf['-t'] != None:
            command_line += '-t %s ' % int(spades_conf['-t'])
        if spades_conf['-m'] != None:
            command_line += '-m %s ' % int(spades_conf['-m'])
        if spades_conf['-k'] != None:
            command_line += '-k '+str(spades_conf['-k'])+' '
        if spades_conf['--cov-cutoff'] != None:
            command_line += '--cov-cutoff '+str(spades_conf['--cov-cutoff'])+' '
        if spades_conf['--phred-offset'] != None:
            command_line += '--phred-offset '+str(spades_conf['--phred-offset'])+' '
        command_line += '-o '+self.result_dir+'/assembly/spades_out/'
        subprocess.run(command_line, shell=True, check=True)
        print("end spades_interlaced")

    def idba_single(self):
        print('begin idba_single_end')
        idba_conf = self.conf['idba-ud']
        command_line = 'idba_ud '
        if idba_conf['-r']:
            command_line += '-r '
        elif idba_conf['--read_level_2']:
            command_line += "--read_level_2 "
        elif idba_conf['--read_level_3']:
            command_line += '--read_level_3 '
        elif idba_conf['--read_level_4']:
            command_line += '--read_level_4 '
        elif idba_conf['--read_level_5']:
            command_line += '--read_level_5 '
        elif idba_conf['-l']:
            command_line += '-l '
        else:
            command_line += '-r '
        com1 = 'fq2fa '+self.input_file + ' '+os.path.join(os.path.join(os.path.join(self.result_dir,'assembly'),'idba_ud_out'),'idba_input_file.fasta')
        subprocess.run(com1, shell=True, check=True)
        command_line += os.path.join(os.path.join(os.path.join(self.result_dir,'assembly'),'idba_ud_out'),'idba_input_file.fasta')+' '
        if idba_conf['--mink'] != None:
            command_line += "--mink "+idba_conf['--mink']+' '
        if idba_conf['--maxk'] != None:
            command_line += "--maxk "+str(idba_conf['--maxk'])+' '
        if idba_conf['--step'] != None:
            command_line += "--step "+idba_conf['--step']+' ' 
        if idba_conf['--prefix'] != None:
            command_line += "--prefix "+idba_conf['--prefix']+' '
        if idba_conf['--min_count'] != None:
            command_line += "--min_count "+idba_conf['--min_count']+' '
        if idba_conf['--min_support'] != None:
            command_line += "--min_support "+idba_conf['--min_support']+' '
        if idba_conf['--seed_kmer'] != None:
            command_line += "--seed_kmer "+idba_conf['--seed_kmer']+' '
        if idba_conf['--min_contig'] != None:
            command_line += "--min_contig "+idba_conf['--min_contig']+' '
        if idba_conf['--similar'] != None:
            command_line += "--similar "+idba_conf['--similar']+' '
        if idba_conf['--max_mismatch'] != None:
            command_line += "--max_mismatch "+idba_conf['--max_mismatch']+' '
        if idba_conf['--min_pairs'] != None:
            command_line += "--min_pairs "+idba_conf['--min_pairs']+' '
        if idba_conf['--no_coverage']:
            command_line += "--no_coverage "
        if idba_conf['--no_correct']:
            command_line += "--no_correct "
        if idba_conf['--pre_correction']:
            command_line += "--pre_correction "
        command_line += ' -o '+ os.path.join(os.path.join(self.result_dir,'assembly'),'idba_ud_out')
        subprocess.run(command_line, shell=True, check=True)
       
        print('end idba_single_end')
    
    def idba_paired(self):
        print('begin idba_paired_end')
        idba_conf = self.conf['idba-ud']
        command_line = 'idba_ud '
        if idba_conf['-r']:
            command_line += '-r '
        elif idba_conf['--read_level_2']:
            command_line += "--read_level_2 "
        elif idba_conf['--read_level_3']:
            command_line += '--read_level_3 '
        elif idba_conf['--read_level_4']:
            command_line += '--read_level_4 '
        elif idba_conf['--read_level_5']:
            command_line += '--read_level_5 '
        elif idba_conf['-l']:
            command_line += '-l '
        else:
            command_line += '-r '
        com1 = 'fq2fa --merge '+self.input_file_1 + ' '+self.input_file_2+' '+os.path.join(os.path.join(os.path.join(self.result_dir,'assembly'),'idba_ud_out'),'idba_input_file.fasta')
        subprocess.run(com1, shell=True, check=True)
        command_line += os.path.join(os.path.join(os.path.join(self.result_dir,'assembly'),'idba_ud_out'),'idba_input_file.fasta')
        if idba_conf['--mink'] != None:
            command_line += "--mink "+idba_conf['--mink']+' '
        if idba_conf['--maxk'] != None:
            command_line += "--maxk "+idba_conf['--maxk']+' '
        if idba_conf['--step'] != None:
            command_line += "--step "+idba_conf['--step']+' ' 
        if idba_conf['--prefix'] != None:
            command_line += "--prefix "+idba_conf['--prefix']+' '
        if idba_conf['--min_count'] != None:
            command_line += "--min_count "+idba_conf['--min_count']+' '
        if idba_conf['--min_support'] != None:
            command_line += "--min_support "+idba_conf['--min_support']+' '
        if idba_conf['--seed_kmer'] != None:
            command_line += "--seed_kmer "+idba_conf['--seed_kmer']+' '
        if idba_conf['--min_contig'] != None:
            command_line += "--min_contig "+idba_conf['--min_contig']+' '
        if idba_conf['--similar'] != None:
            command_line += "--similar "+idba_conf['--similar']+' '
        if idba_conf['--max_mismatch'] != None:
            command_line += "--max_mismatch "+idba_conf['--max_mismatch']+' '
        if idba_conf['--min_pairs'] != None:
            command_line += "--min_pairs "+idba_conf['--min_pairs']+' '
        if idba_conf['--no_coverage']:
            command_line += "--no_coverage "
        if idba_conf['--no_correct']:
            command_line += "--no_correct "
        if idba_conf['--pre_correction']:
            command_line += "--pre_correction "
        command_line += ' -o '+ os.path.join(os.path.join(self.result_dir,'assembly'),'idba_ud_out')
        subprocess.run(command_line, shell=True, check=True)
        print('end idba_paired_end')
    
    def assembly_assessment(self, input_file):
        print('Begin QUAST')
        subprocess.run('quast.py '+input_file+' -o '+self.result_dir+'/assembly/quast_out', shell=True, check=True)
        print('End QUAST')
    def run_single(self):
        print('Begin Assembly for Single-end reads')
        if self.conf['megahit']['enable']:
            self.megahit_single()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/megahit_out/final.contigs.fa'
            
        elif self.conf['spades']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly/spades_out')
            self.spades_single()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/spades_out/contigs.fasta'
        elif self.conf['idba-ud']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly/idba_ud_out')
            self.idba_single()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/idba_ud_out/contig.fa'
        else:
            self.output = self.input_file
        self.assembly_assessment(self.output)
        print('End Assembly for Single-end reads')
    def run_paired(self):
        print('Begin Assembly for Paired-end reads')
        if self.conf['megahit']['enable']:
            self.megahit_paired()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/megahit_out/final.contigs.fa'
        elif self.conf['spades']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly/spades_out')
            self.spades_paired()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/spades_out/contigs.fasta'
        elif self.conf['idba-ud']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly/idba_ud_out')
            self.idba_paired()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/idba_ud_out/contig.fa'
        else:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly/idba_ud_out')
            self.idba_paired()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/assembly/idba_ud_out/contig.fa'
        self.assembly_assessment(self.output)
        print('End Assembly for Paired-end reads')
def assembly_single_end(input_file, result_dir):
    print("Begin assembly")
    print("input_file="+input_file)
    # result = subprocess.run('megahit -r '+input_file+' -o '+result_dir+'/assembly', shell=True, check=True)
    print("Begin megahit")
    subprocess.run('megahit -r '+input_file+' -o '+result_dir+'/assembly/megahit_out', shell=True, check=True)
    # print("result of megahit:")
    # print(result.stdout)
    print("End megahit")
    print("Begin QUAST")
    subprocess.run('quast.py '+result_dir+'/assembly/megahit_out/final.contigs.fa -o '+result_dir+'/assembly/quast_out', shell=True, check=True)
    print("End QUAST")
    print("End assembly")

def assembly_paired_end(input_file_1, input_file_2, result_dir):
    print("Begin assembly")
    print("input_file="+input_file_1+input_file_2)
    # result = subprocess.run('megahit -r '+input_file+' -o '+result_dir+'/assembly', shell=True, check=True)
    print("Begin megahit")
    subprocess.run('megahit -1 '+input_file_1+' -2 '+input_file_2+' -o '+result_dir+'/assembly/megahit_out', shell=True, check=True)
    # print("result of megahit:")
    # print(result.stdout)
    print("End megahit")
    print("Begin QUAST")
    subprocess.run('quast.py '+result_dir+'/assembly/megahit_out/final.contigs.fa -o '+result_dir+'/assembly/quast_out', shell=True, check=True)
    print("End QUAST")
    print("End assembly")
