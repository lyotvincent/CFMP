import subprocess
import os 
class Gene_Predition:
    result_dir = None
    conf = None 
    contig_file = None
    assembly_reads_file = None 
    assembly_reads_file_1 = None 
    assembly_reads_file_2 = None 
    output = None
    gene_quant = None 
    def __init__(self,result_dir,conf,contig_file=None,assembly_reads_file=None,assembly_reads_file_1=None,assembly_reads_file_2=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.contig_file = contig_file
        self.assembly_reads_file = assembly_reads_file
        self.assembly_reads_file_1 = assembly_reads_file_1
        self.assembly_reads_file_2 = assembly_reads_file_2
    def prodigal(self):
        print('Begin Prodigal')
        prodigal_conf = self.conf['prodigal']
        c = prodigal_conf['-c']
        m = prodigal_conf['-m']
        n = prodigal_conf['-n']
        s = prodigal_conf['-s']
        t = prodigal_conf['-t']
        f = prodigal_conf['-f']
        g = prodigal_conf['-g']
        p = prodigal_conf['-p']
        com = 'prodigal -i '+ self.contig_file+' -a '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_protein.fasta'+' '
        if c:
            com += '-c '
        com += '-d '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_nucleotide.fasta'+' '
        if f:
            com += '-f '+f+' '
        if g:
            com += '-g '+g+' '
        if m:
            com += '-m '
        if n:
            com += '-n '
        if p:
            com += '-p '+p+' '
        if s:
            com += '-s '
        if t:
            com += '-t '
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'cd-hit'),'cd-hit-est')+' -i ' + os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_nucleotide.fasta' + ' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_nucleotide_cdhit.fasta'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'cd-hit'),'cd-hit')+' -i ' + os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_protein.fasta' + ' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_protein_cdhit.fasta'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = 'salmon index -t ' + os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_nucleotide_cdhit.fasta' +' -i '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/gene_index'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = 'salmon quant -i '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/gene_index'+' -l IU --meta '
        if self.assembly_reads_file_1 and self.assembly_reads_file_2:
            com += '-1 '+self.assembly_reads_file_1+' -2 '+self.assembly_reads_file_2+' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/gene_quant'
        else:
            com += '-r '+self.assembly_reads_file+' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/gene_quant'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        print('End Prodigal')
    def metagenemark(self):
        print('Begin MetaGeneMark')
        path_to_metagenemark_v1_mod=os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'MetaGeneMark_linux_64'),'mgm'),'MetaGeneMark_v1.mod')
        metagenemark_conf = self.conf['metagenemark']
        f = metagenemark_conf['-f']
        K = metagenemark_conf['-K']
        r = metagenemark_conf['-r']
        c = metagenemark_conf['-c']
        s = metagenemark_conf['-s']
        p = metagenemark_conf['-p']
        e = metagenemark_conf['-e']
        g = metagenemark_conf['-g']
        com = os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'MetaGeneMark_linux_64'),'mgm'),'gmhmmp')+' '
        if r:
            com += '-r '
        if s:
            com += '-s '+s+' '
        if p:
            com += '-p '+p+' '
        if e:
            com += '-e '+e+' '
        if c:
            com += '-c '
        if g:
            com += '-g '+g+' '
        com += '-m '+path_to_metagenemark_v1_mod +' '+self.contig_file+' '
        if f:
            com += '-f '+f+' '
        com += '-A '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_protein.fasta'+' '
        com += '-D '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_nucleotide.fasta'+' '
        if K:
            com += '-K '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_RBS.fasta'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'cd-hit'),'cd-hit-est')+' -i ' + os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_nucleotide.fasta' + ' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_nucleotide_cdhit.fasta'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'cd-hit'),'cd-hit')+' -i ' + os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_protein.fasta' + ' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_protein_cdhit.fasta'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = 'salmon index -t ' + os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_nucleotide_cdhit.fasta' +' -i '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/gene_index'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        com = 'salmon quant -i '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/gene_index'+' -l IU --meta '
        if self.assembly_reads_file_1 and self.assembly_reads_file_2:
            com += '-1 '+self.assembly_reads_file_1+' -2 '+self.assembly_reads_file_2+' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/gene_quant'
        else:
            com += '-r '+self.assembly_reads_file+' -o '+os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/gene_quant'
        subprocess.run(com, shell=True, check=True, encoding='utf-8')
        print('End MetaGeneMark')
    def run(self):
        print('Begin Gene_Predition')
        if self.conf['prodigal']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out')
            self.prodigal()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_protein_cdhit.fasta'
            self.gene_quant = os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/gene_quant'
        elif self.conf['metagenemark']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out')
            self.metagenemark()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/metagenemark_protein_cdhit.fasta'
            self.gene_quant = os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/metagenemark_out/gene_quant'
        else:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out')
            self.prodigal()
            self.output = os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/prodigal_protein_cdhit.fasta'
            self.gene_quant = os.path.abspath('.')+'/'+self.result_dir+'/gene_predition/prodigal_out/gene_quant'
        print('End Gene_Predition')