import os 
import pandas as pd 
import tgs_quality_control
import tgs_assembly
import polish
import decontamination
class ThirdGenerationSequencing:
    def __init__(self,result_dir,conf,input_file=None,pacbio=None,nanopore=None,input_file_1=None,input_file_2=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        self.pacbio = pacbio
        self.nanopore = nanopore
        self.input_file_1 = input_file_1
        self.input_file_2 = input_file_2 
    def run(self):
        print('Begin TGS Pipeline')
        preprocessing_output = self.input_file 
        if self.conf['tgs_quality_control']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/tgs_quality_control')
            tgs_quality_control_obj = tgs_quality_control.tgs_quality_control(self.result_dir,self.conf['tgs_quality_control'],input_file=self.input_file,illumina_1=self.input_file_1,illumina_2=self.input_file_2)
            tgs_quality_control_obj.run()
            preprocessing_output = tgs_quality_control_obj.output
        decontamination_output = preprocessing_output
        if self.conf['decontamination']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/decontamination')
            decontamination_obj = decontamination.Decontamination(self.result_dir,self.conf['decontamination'],input_file=preprocessing_output)
            decontamination_obj.decontamination_tgs()
            decontamination_output = os.path.abspath('.')+'/'+self.result_dir+'/decontamination/clean_reads.fasta'
        assembly_output = decontamination_output
        if self.conf['assembly']['enable']:
            tgs_assembly_obj = tgs_assembly.tgs_assembly(self.result_dir,self.conf['assembly'],input_file=preprocessing_output)
            tgs_assembly_obj.run()
            assembly_output = tgs_assembly_obj.output 
        polish_output = assembly_output
        if self.conf['Polish']['enable']:
            polish_obj = polish.polish(self.result_dir,self.conf['Polish'],assembly_output,illumina_1=self.input_file_1,illumina_2=self.input_file_2,nanopore=self.nanopore,pacbio=self.pacbio)
            polish_obj.run()
            polish_output = polish_obj.output 
        
        gene_predition_output = polish_output
        gene_quant = None
        if self.conf['gene_predition']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/gene_predition')
            gene_predition_obj = gene_predition.Gene_Predition(self.result_dir,self.conf['gene_predition'],contig_file=assembly_output,assembly_reads_file=decontamination_output)
            gene_predition_obj.run()
            gene_predition_output = gene_predition_obj.output 
            gene_quant = gene_predition_obj.gene_quant
        
        if self.conf['functional_annotation']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/functional_annotation')
            
            if gene_quant:
                gene_tpm = pd.read_table(os.path.join(gene_quant,'quant.sf'))[['Name', 'TPM']]
                function_anno_obj = function_anno.Function_Annotation(self.result_dir,self.conf['functional_annotation'],gene_predition_output,gene_tpm)
                function_anno_obj.run()
        if self.conf['Species_Annotation']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy')
            species_annotation_obj = taxonomy.TaxonomyAnnotation(self.result_dir,self.conf['Species_Annotation'],input_file=decontamination_output)
            species_annotation_obj.run_single()
        print('End TGS Pipeline')
                
                    