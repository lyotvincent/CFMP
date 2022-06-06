import preprocessing 
import decontamination 
import ngs_assembly 
import gene_predition
import function_anno
import taxonomy
import os 
import pandas as pd
class NextGenerationSequencing:
    def __init__(self,result_dir,conf,input_file=None,input_file_1=None,input_file_2=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        self.input_file_1 = input_file_1
        self.input_file_2 = input_file_2 
    def run_single(self):
        print('Begin NGS_Pipeline')
        preprocessing_output = self.input_file
        if self.conf['preprocessing']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing')
            
            preprocessing_obj = preprocessing.Preprocessing(self.result_dir,self.conf,input_file=self.input_file)
            if self.conf['preprocessing']['fastqc']['enable']:
                os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing/fastqc_before_filtering')
                preprocessing_obj.fastqc_single_end('fastqc_before_filtering')
            if self.conf['preprocessing']['fastp']['enable']:
                preprocessing_obj.fastp_single_end()
                preprocessing_output = self.result_dir+'/preprocessing/fastp_output.fastq'
            else:
                if self.conf['preprocessing']['cutadapt']['enable']:
                    preprocessing_obj.cutadapt_single_end()
                    preprocessing_output = self.result_dir+'/preprocessing/cutadapt_output.fastq'
                    if self.conf['preprocessing']['fastqc']['enable']:
                        preprocessing_obj.input_file = preprocessing_output
                        os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing/fastqc_after_cutadapt_filtering')
                        preprocessing_obj.fastqc_single_end('fastqc_after_cutadapt_filtering')
                if self.conf['preprocessing']['trimmomatic']['enable']:
                    if self.conf['preprocessing']['cutadapt']['enable']:
                        preprocessing_obj.input_file = self.result_dir+'/preprocessing/cutadapt_output.fastq'
                    preprocessing_obj.trimmomatic_single_end()
                    preprocessing_output = self.result_dir+'/preprocessing/trimmomatic_output.fastq'
                    if self.conf['preprocessing']['fastqc']['enable']:
                        preprocessing_obj.input_file = preprocessing_output 
                        os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing/fastqc_after_trimmomatic_filtering')
                        preprocessing_obj.fastqc_single_end('fastqc_after_trimmomatic_filtering')
                
            temp_file = open(os.path.abspath('.')+'/'+self.result_dir+'/Summary_of_results.html','a+')
            temp_file.write('<ul>\n')
            temp_file.write('<li>preprocessing result is in %s</li>\n' % './preprocessing')
            temp_file.write('<li><a href="%s">click to report</a></li>\n' % ('./preprocessing/'))
            temp_file.write('</ul>\n')
            temp_file.close() 
       
        decontamination_output = preprocessing_output
        if self.conf['decontamination']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/decontamination')
            decontamination_obj = decontamination.Decontamination(self.result_dir,self.conf['decontamination'],input_file=preprocessing_output)
            decontamination_obj.decontamination_single_end()
            decontamination_output = os.path.abspath('.')+'/'+self.result_dir+'/decontamination/clean_reads.fastq'
        
        assembly_output = decontamination_output 
        if self.conf['assembly']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly')
            assembly_obj = ngs_assembly.Assembly(self.result_dir,self.conf['assembly'],input_file=decontamination_output)
            assembly_obj.run_single()
            assembly_output = assembly_obj.output
        gene_predition_output = assembly_output 
        gene_quant = None 
        if self.conf['gene_predition']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/gene_predition')
            gene_predition_obj = gene_predition.Gene_Predition(self.result_dir,self.conf['gene_predition'],contig_file=assembly_output,assembly_reads_file=decontamination_output)
            gene_predition_obj.run()
            gene_predition_output = gene_predition_obj.output 
            gene_quant = gene_predition_obj.gene_quant
        
        if self.conf['functional_annotation']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/function_annotation')
            gene_tpm=None
            if gene_quant:
                gene_tpm = pd.read_table(os.path.join(gene_quant,'quant.sf'))[['Name', 'TPM']]
            function_anno_obj = function_anno.Function_Annotation(self.result_dir,self.conf['functional_annotation'],gene_predition_output,gene_tpm)
            function_anno_obj.run()
        if self.conf['Species_Annotation']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy')
            species_annotation_obj = taxonomy.TaxonomyAnnotation(self.result_dir,self.conf['Species_Annotation'],input_file=decontamination_output)
            species_annotation_obj.run_single()
        print('End NGS Pipeline')
    def run_paired(self):
        print('Begin NGS Pipeline')
        preprocessing_output_1 = self.input_file_1
        preprocessing_output_2 = self.input_file_2
        if self.conf['preprocessing']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing')
            preprocessing_obj = preprocessing.Preprocessing(self.result_dir,self.conf,input_file_1=self.input_file_1,input_file_2=self.input_file_2)
            if self.conf['preprocessing']['fastqc']['enable']:
                os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing/fastqc_before_filtering')
                preprocessing_obj.fastqc_paired_end('fastqc_before_filtering')
            
            if self.conf['preprocessing']['fastp']['enable']:
                preprocessing_obj.fastp_paired_end()
                preprocessing_output_1 = self.result_dir+'/preprocessing/fastp_output_1.fastq'
                preprocessing_output_2 = self.result_dir+'/preprocessing/fastp_output_2.fastq'
            else:
                if self.conf['preprocessing']['cutadapt']['enable']:
                    preprocessing_obj.cutadapt_paired_end()
                    preprocessing_output_1 = self.result_dir+'/preprocessing/cutadapt_output_1.fastq'
                    preprocessing_output_2 = self.result_dir+'/preprocessing/cutadapt_output_2.fastq'
                    if self.conf['preprocessing']['fastqc']['enable']:
                        preprocessing_obj.input_file_1 = preprocessing_output_1
                        preprocessing_obj.input_file_2 = preprocessing_output_2
                        os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing/fastqc_after_cutadapt_filtering')
                        preprocessing_obj.fastqc_paired_end('fastqc_after_cutadapt_filtering')
                elif self.conf['preprocessing']['trimmomatic']['enable']:
                    if self.conf['preprocessing']['cutadapt']['enable']:
                        preprocessing_obj.input_file_1 = self.result_dir+'/preprocessing/cutadapt_output_1.fastq'
                        preprocessing_obj.input_file_2 = self.result_dir+'/preprocessing/cutadapt_output_2.fastq'
                    preprocessing_obj.trimmomatic_paired_end() 
                    preprocessing_output_1 = self.result_dir+'/preprocessing/paired_output_1.fastq'
                    preprocessing_output_2 = self.result_dir+'/preprocessing/paired_output_2.fastq'
                    if self.conf['preprocessing']['fastqc']['enable']:
                        preprocessing_obj.input_file_1 = preprocessing_output_1
                        preprocessing_obj.input_file_2 = preprocessing_output_2
                        os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/preprocessing/fastqc_after_trimmomatic_filtering')
                        preprocessing_obj.fastqc_paired_end('fastqc_after_trimmomatic_filtering')
                else:
                    preprocessing_output_1 = self.input_file_1
                    preprocessing_output_2 = self.input_file_2
            temp_file = open(os.path.abspath('.')+'/'+self.result_dir+'/Summary_of_results.html','a+')
            temp_file.write('<ul>\n')
            temp_file.write('<li>preprocessing result is in %s</li>\n' % './preprocessing')
            temp_file.write('<li><a href="%s">click to report</a></li>\n' % './preprocessing/')
            temp_file.write('</ul>\n')
            temp_file.close() 
        else:
            preprocessing_output_1 = self.input_file_1
            preprocessing_output_2 = self.input_file_2 
        print('preprocessing_output_1='+str(preprocessing_output_1))
        print('preprocessing_output_2='+str(preprocessing_output_2))
        decontamination_output_1 = preprocessing_output_1
        decontamination_output_2 = preprocessing_output_2
        if self.conf['decontamination']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/decontamination')
            decontamination_obj = decontamination.Decontamination(self.result_dir,self.conf['decontamination'],input_file_1=preprocessing_output_1,input_file_2=preprocessing_output_2)
            decontamination_obj.decontamination_paired_end()
            decontamination_output_1 = os.path.abspath('.')+'/'+self.result_dir+'/decontamination/clean_reads_1.fastq'
            decontamination_output_2 = os.path.abspath('.')+'/'+self.result_dir+'/decontamination/clean_reads_2.fastq'
        assembly_output = None 
        if self.conf['assembly']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/assembly')
            assembly_obj = ngs_assembly.Assembly(self.result_dir,self.conf['assembly'],input_file_1=decontamination_output_1,input_file_2=decontamination_output_2)
            assembly_obj.run_paired()
            assembly_output = assembly_obj.output
        gene_predition_output = assembly_output 
        gene_quant = None 
        if self.conf['gene_predition']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/gene_predition')
            gene_predition_obj = gene_predition.Gene_Predition(self.result_dir,self.conf['gene_predition'],contig_file=assembly_output,assembly_reads_file_1=decontamination_output_1,assembly_reads_file_2=decontamination_output_2)
            gene_predition_obj.run()
            gene_predition_output = gene_predition_obj.output 
            gene_quant = gene_predition_obj.gene_quant
        
        if self.conf['functional_annotation']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/function_annotation')
            if gene_quant:
                gene_tpm = pd.read_table(os.path.join(gene_quant,'quant.sf'))[['Name', 'TPM']]
                function_anno_obj = function_anno.Function_Annotation(self.result_dir,self.conf['functional_annotation'],gene_predition_output,gene_tpm)
                function_anno_obj.run()
        if self.conf['Species_Annotation']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy')
            species_annotation_obj = taxonomy.TaxonomyAnnotation(self.result_dir,self.conf['Species_Annotation'],input_file_1=decontamination_output_1,input_file_2=decontamination_output_2)
            species_annotation_obj.run_paired()
        print('End NGS Pipeline')