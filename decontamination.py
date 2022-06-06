import subprocess
import os 
class Decontamination:
    result_dir = None
    conf = None 
    input_file = None 
    input_file_1 = None 
    input_file_2 = None 
    def __init__(self,result_dir,conf,input_file=None,input_file_1=None,input_file_2=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        self.input_file_1 = input_file_1
        self.input_file_2 = input_file_2 
        
    def decontamination_single_end(self):
        print('Begin Decontamination_Single_End')
        if self.conf['contaminant'] != None:
            contaminant = self.conf['contaminant']
            com = 'bowtie2-build ' + contaminant + ' ' + self.result_dir + 'decontamination/contaminant'
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            com = 'bowtie2 '
            com += '-x '+self.result_dir + '/decontamination/contaminant -U '+self.input_file+' -S ' + self.result_dir + '/decontamination/contaminant.sam'
        else:
            contaminant_index = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'hg19'),'hg19')
            com = 'bowtie2 '
            com += '-x '+contaminant_index+' -U '+self.input_file+' -S ' + self.result_dir + '/decontamination/contaminant.sam'
        subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com = 'samtools view -bS ' + self.result_dir + '/decontamination/contaminant.sam > ' + self.result_dir + '/decontamination/contaminant.bam'
        subprocess.run(com, shell=True, check=True)
        com1 = 'samtools view -b -f 4 -F 256 '+ self.result_dir + '/decontamination/contaminant.bam > '+ self.result_dir + '/decontamination/clean_reads.bam'
        com2 = 'samtools sort -n '+ self.result_dir + '/decontamination/clean_reads.bam > '+ self.result_dir + '/decontamination/clean_reads_sorted.bam'
        com3 = 'bedtools bamtofastq -i ' + self.result_dir + '/decontamination/clean_reads_sorted.bam -fq ' + self.result_dir + '/decontamination/clean_reads.fastq'
        subprocess.run(com1, shell=True, check=True)
        subprocess.run(com2, shell=True, check=True)
        subprocess.run(com3, shell=True, check=True)
        print('End Decontamination_Single_End')
    def decontamination_paired_end(self):
        print('Begin Decontamination_Paired_End')
        if self.conf['contaminant'] != None:
            contaminant = self.conf['contaminant']
            com = 'bowtie2-build ' + contaminant + ' ' + self.result_dir + '/decontamination/contaminant'
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            com = 'bowtie2 '
            com += '-x '+self.result_dir + '/decontamination/contaminant -1 '+self.input_file_1+' -2 '+self.input_file_2+' -S ' + self.result_dir + '/decontamination/contaminant.sam'
        else:
            contaminant_index = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'hg19'),'hg19')
            com = 'bowtie2 '
            com += '-x '+contaminant_index+' -1 '+self.input_file_1+' -2 '+self.input_file_2+' -S ' + self.result_dir + '/decontamination/contaminant.sam'
        subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com = 'samtools view -bS ' + self.result_dir + '/decontamination/contaminant.sam > ' + self.result_dir + '/decontamination/contaminant.bam'
        subprocess.run(com, shell=True, check=True)
        com1 = 'samtools view -b -f 12 -F 256 '+ self.result_dir + '/decontamination/contaminant.bam > '+ self.result_dir + '/decontamination/clean_reads.bam'
        com2 = 'samtools sort -n '+ self.result_dir + '/decontamination/clean_reads.bam > '+ self.result_dir + '/decontamination/clean_reads_sorted.bam'
        com3 = 'bedtools bamtofastq -i ' + self.result_dir + '/decontamination/clean_reads_sorted.bam -fq ' + self.result_dir + '/decontamination/clean_reads_1.fastq -fq2 '+self.result_dir + '/decontamination/clean_reads_2.fastq'
        subprocess.run(com1, shell=True, check=True) 
        subprocess.run(com2, shell=True, check=True) 
        subprocess.run(com3, shell=True, check=True) 
        print('End Decontamination_Paired_End')
    def decontamination_tgs(self):
        print('Begin Decontamination_TGS')
        if self.conf['contaminant'] != None:
            contaminant = self.conf['contaminant']
            com = 'minimap2 '+contaminant+' -d '+self.result_dir+'/decontamination/contaminant.min'
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'minimap2 -ax '
            if self.conf['input_type'] == 'Pacbio':
                com += 'map-pb '
            elif self.conf['input_type'] == 'Nanopore':
                com += 'map-ont '
            else:
                print('Error. Please set "input_type" in "decontamination"')
                exit(0)
            com += self.result_dir+'/decontamination/contaminant.min '+self.input_file+' > '+self.result_dir+'/decontamination/contaminant.sam'
        else:
            contaminant_index = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'hg19'),'hg19.min')
            com = 'minimap2 -ax '
            if self.conf['input_type'] == 'Pacbio':
                com += 'map-pb '
            elif self.conf['input_type'] == 'Nanopore':
                com += 'map-ont '
            else:
                print('Error. Please set "input_type" in "decontamination"')
                exit(0)
            com += contaminant_index+' '+self.input_file+' > '+self.result_dir+'/decontamination/contaminant.sam'
        subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com = 'samtools view -bS ' + self.result_dir + '/decontamination/contaminant.sam > ' + self.result_dir + '/decontamination/contaminant.bam'
        subprocess.run(com, shell=True, check=True)
        com1 = 'samtools view -b -f 4 -F 256 '+ self.result_dir + '/decontamination/contaminant.bam > '+ self.result_dir + '/decontamination/clean_reads.bam'
        com2 = 'samtools sort -n '+ self.result_dir + '/decontamination/clean_reads.bam > '+ self.result_dir + '/decontamination/clean_reads_sorted.bam'
        com3 = 'bedtools bamtofastq -i ' + self.result_dir + '/decontamination/clean_reads_sorted.bam -fq ' + self.result_dir + '/decontamination/clean_reads.fastq'
        com4 = 'fq2fa '+self.result_dir + '/decontamination/clean_reads.fastq '+self.result_dir+'/decontamination/clean_reads.fasta'
        #com2 = 'samtools view '+ self.result_dir + '/decontamination/clean_reads.bam |  awk \'{OFS="\t"; print ">"$1"\n"$10}\' - > '+ self.result_dir + '/decontamination/clean_reads.fasta'
        subprocess.run(com1, shell=True, check=True)
        subprocess.run(com2, shell=True, check=True)
        subprocess.run(com3, shell=True, check=True)
        subprocess.run(com4, shell=True, check=True)
        print('End Decontamination_TGS')