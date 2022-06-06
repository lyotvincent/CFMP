import subprocess
import os 
class TaxonomyAnnotation:
    result_dir = None 
    conf = None 
    input_file = None 
    input_file_1 = None 
    input_file_2 = None 
    path_to_kraken2_db = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'kraken2_db')
    def __init__(self,result_dir,conf,input_file=None,input_file_1=None,input_file_2=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        self.input_file_1 = input_file_1
        self.input_file_2 = input_file_2 
    def get_deep_data(self,dir):
        result = [] 
        data = os.listdir(dir)
        for i in data:
            i = os.path.join(dir,i) 
            result.append(i)
        return result 
    def metaothello_single_end(self):
        print('Begin MetaOthello_single_end') 
        metaothello_software_dir=os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'metaOthello-master')
        metaothello_conf = self.conf['MetaOthello']
        path_to_bacterial_referenceSeqFastaFile = metaothello_conf['path_to_bacterial_referenceSeqFastaFile']
        bacterial_reference_seq_associated_taxonomy_info_file = metaothello_conf['bacterial_reference_seq_associated_taxonomy_info_file']
        db_kmer_length = metaothello_conf['db_kmer_length']
        kmer_length = metaothello_conf['kmer_length']
        com = ''
        if  path_to_bacterial_referenceSeqFastaFile and bacterial_reference_seq_associated_taxonomy_info_file:
            files = self.get_deep_data(path_to_bacterial_referenceSeqFastaFile)
            for file in files:
                i = file.split('.')[-2]
                com += 'jellyfish count -o '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out'+' '+i+'.jf -m ' 
                if db_kmer_length:
                    com += db_kmer_length+' '
                else:
                    com += '6 '
                com += '-s 1G -C '+os.path.join(path_to_bacterial_referenceSeqFastaFile,file)
                subprocess.run(com,shell=True,check=True)
                com = 'jellyfish dump -t -c -o '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/kmer_filedir/'+i+'.Kmer'+' '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/'+i+'.jf'
                subprocess.run(com,shell=True,check=True) 
            com = metaothello_software_dir+'/build/build '+bacterial_reference_seq_associated_taxonomy_info_file+' '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/kmer_filedir'+' Kmer'
            if db_kmer_length:
                com += db_kmer_length+' '
            else:
                com += '6 '
            com += os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/taxo.index'+' '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out'
            subprocess.run(com,shell=True,check=True) 
        com = metaothello_software_dir+'/classifier/classifier '
        if path_to_bacterial_referenceSeqFastaFile and bacterial_reference_seq_associated_taxonomy_info_file:
            com += os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/taxo.index'+' '
        else:
            com += metaothello_software_dir+'/bacterial_'+kmer_length+'mer_L12.index ' 
        if self.input_file.endswith('.gz'):
            subprocess.run('gunzip -c '+self.input_file+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out',self.input_file.rsplit('.',1)[0]),shell=True,check=True) 
            self.input_file=os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out',self.input_file.rsplit('.',1)[0])
        com1 = com+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out'+' '+kmer_length+' '
        if 'fastq' in self.input_file.split('.') or 'fq' in self.input_file.split('.'):
            com1+='fq '
        else:
            com1+='fa '
        com1 += 'SE '
        if path_to_bacterial_referenceSeqFastaFile and bacterial_reference_seq_associated_taxonomy_info_file:
            com1 += bacterial_reference_seq_associated_taxonomy_info_file+' '
        else:
            com1 += metaothello_software_dir+'/classifier/bacterial_speciesId2taxoInfo.txt '
        com1 += metaothello_software_dir+'/classifier/names.dmp.scientific '+self.input_file
        subprocess.run(com1, shell=True,check=True) 
        com1 = 'cut -f 1,2 '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_assignment.txt')+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_input2krona')
        subprocess.run(com1, shell=True,check=True) 
        com1 = 'ktImportTaxonomy '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_input2krona')+' -o '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','metaothello2krona.html')
        subprocess.run(com1,shell=True,check=True) 
        com1 = metaothello_software_dir+'/classifier/getTaxoReadCount '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_assignment.txt')+' '+os.path.join(os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxoInfo'),'species.txt')+' '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','species.count')
        subprocess.run(com1,shell=True,check=True)
        com1 = 'cut -f 2,3 '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','species.count')+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','species.count')
        subprocess.run(com1,shell=True,check=True) 
        print('End MetaOthello_single_end')
    def metaothello_paired_end(self):
        print('Begin MetaOthello_paired_end') 
        metaothello_software_dir=os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'metaOthello-master')
        metaothello_conf = self.conf['MetaOthello']
        path_to_bacterial_referenceSeqFastaFile = metaothello_conf['path_to_bacterial_referenceSeqFastaFile']
        bacterial_reference_seq_associated_taxonomy_info_file = metaothello_conf['bacterial_reference_seq_associated_taxonomy_info_file']
        db_kmer_length = metaothello_conf['db_kmer_length']
        kmer_length = metaothello_conf['kmer_length']
        com = ''
        if  path_to_bacterial_referenceSeqFastaFile and bacterial_reference_seq_associated_taxonomy_info_file:
            files = self.get_deep_data(path_to_bacterial_referenceSeqFastaFile)
            for file in files:
                i = file.split('.')[-2]
                com += 'jellyfish count -o '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out'+' '+i+'.jf -m ' 
                if db_kmer_length:
                    com += db_kmer_length+' '
                else:
                    com += '6 '
                com += '-s 1G -C '+os.path.join(path_to_bacterial_referenceSeqFastaFile,file)
                subprocess.run(com,shell=True,check=True)
                com = 'jellyfish dump -t -c -o '+os.path.join(os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','kmer_filedir'),i+'.Kmer')+' '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out',i+'.jf')
                subprocess.run(com,shell=True,check=True) 
            com = metaothello_software_dir+'/build/build '+bacterial_reference_seq_associated_taxonomy_info_file+' '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','kmer_filedir')+' Kmer'
            if db_kmer_length:
                com += db_kmer_length+' '
            else:
                com += '6 '
            com += os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/taxo.index'+' '+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out'
            subprocess.run(com,shell=True,check=True) 
        com = metaothello_software_dir+'/classifier/classifier '
        if path_to_bacterial_referenceSeqFastaFile and bacterial_reference_seq_associated_taxonomy_info_file:
            com += os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out/taxo.index'+' '
        else:
            com += metaothello_software_dir+'/bacterial_'+kmer_length+'mer_L12.index ' 
        if self.input_file_1.endswith('.gz'):
            subprocess.run('gunzip -c '+self.input_file_1+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out',self.input_file_1.rsplit('.',1)[0]),shell=True,check=True) 
            self.input_file_1=os.path.join(self.result_dir,self.input_file_1.rsplit('.',1)[0])
        if self.input_file_2.endswith('.gz'):
            subprocess.run('gunzip -c '+self.input_file_2+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out',self.input_file_2.rsplit('.',1)[0]),shell=True,check=True) 
            self.input_file_2=os.path.join(self.result_dir,self.input_file_2.rsplit('.',1)[0])
        com1 = com+os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out'+' '+kmer_length+' '
        if 'fastq' in self.input_file_1.split('.') or 'fq' in self.input_file_1.split('.'):
            com1+='fq '
        else:
            com1+='fa '
        com1 += 'PE '
        if path_to_bacterial_referenceSeqFastaFile and bacterial_reference_seq_associated_taxonomy_info_file:
            com1 += bacterial_reference_seq_associated_taxonomy_info_file+' '
        else:
            com1 += metaothello_software_dir+'/classifier/bacterial_speciesId2taxoInfo.txt '
        com1 += metaothello_software_dir+'/classifier/names.dmp.scientific '+self.input_file_1+' '+self.input_file_2
        subprocess.run(com1, shell=True,check=True) 
        com1 = 'cut -f 1,2 '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_assignment.txt')+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_input2krona')
        subprocess.run(com1, shell=True,check=True) 
        com1 = 'ktImportTaxonomy '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_input2krona')+' -o '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','metaothello2krona.html')
        subprocess.run(com1,shell=True,check=True) 
        com1 = metaothello_software_dir+'/classifier/getTaxoReadCount '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxo_assignment.txt')+' '+os.path.join(os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','taxoInfo'),'species.txt')+' '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','species.count')
        subprocess.run(com1,shell=True,check=True)
        com1 = 'cut -f 2,3 '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','species.count')+' > '+os.path.join(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out','species.count')
        subprocess.run(com1,shell=True,check=True) 
        print('End MetaOthello_paired_end') 
    def kraken2_single_end(self):
        print('Begin Kraken2_single_end')
        kraken2_conf = self.conf['Kraken2']
        quick = kraken2_conf['--quick']
        gzip_compressed = kraken2_conf['--gzip-compressed']
        bzip2_compressed = kraken2_conf['--bzip2-compressed']
        use_mpa_style = kraken2_conf['--use-mpa-style']
        use_names = kraken2_conf['--use-names']
        minimum_hit_groups = kraken2_conf['--minimum-hit-groups']
        confidence = kraken2_conf['--confidence']
        minimum_base_quality = kraken2_conf['--minimum-base-quality']
        com = 'kraken2 -db '+self.path_to_kraken2_db+' '
        if quick:
            com += '--quick '
        if gzip_compressed:
            com += '--gzip_compressed '
        if bzip2_compressed:
            com += '--bzip2_compressed '
        if use_mpa_style:
            com += '--use_mpa_style '
        if use_names:
            com += '--use_names '
        if minimum_hit_groups:
            com += '--minimum-hit-groups '+minimum_hit_groups+' '
        if confidence:
            com += '--confidence '+confidence+' '
        if minimum_base_quality:
            com += '--minimum-base-quality '+ minimum-base-quality+' '
        com += '--report '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_report.txt')+' '+self.input_file+' > '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_result.txt')
        subprocess.run(com,shell=True,check=True) 
        com2 = 'bracken -d '+self.path_to_kraken2_db+' -i '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_report.txt')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2_bracken.output')+' -w '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_bracken.report')+' -r 150 -l S'
        subprocess.run(com2, shell=True, check=True,encoding='utf-8')
        com2 = 'kreport2mpa.py -r '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_bracken.report')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2_bracken.taxon.abundance')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com2 = 'kreport2krona.py -r '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_report.txt')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2krona')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com2 = 'ktImportText '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2krona')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2krona.html')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print('End Kraken2_single_end')
    def kraken2_paired_end(self):
        print('Begin Kraken2_paired_end')
        kraken2_conf = self.conf['Kraken2']
        quick = kraken2_conf['--quick']
        gzip_compressed = kraken2_conf['--gzip-compressed']
        bzip2_compressed = kraken2_conf['--bzip2-compressed']
        use_mpa_style = kraken2_conf['--use-mpa-style']
        use_names = kraken2_conf['--use-names']
        minimum_hit_groups = kraken2_conf['--minimum-hit-groups']
        confidence = kraken2_conf['--confidence']
        minimum_base_quality = kraken2_conf['--minimum-base-quality']
        com = 'kraken2 -db '+self.path_to_kraken2_db+' '
        if quick:
            com += '--quick '
        if gzip_compressed:
            com += '--gzip_compressed '
        if bzip2_compressed:
            com += '--bzip2_compressed '
        if use_mpa_style:
            com += '--use_mpa_style '
        if use_names:
            com += '--use_names '
        if minimum_hit_groups:
            com += '--minimum-hit-groups '+minimum_hit_groups+' '
        if confidence:
            com += '--confidence '+confidence+' '
        if minimum_base_quality:
            com += '--minimum-base-quality '+ minimum-base-quality+' '
        com += '--report '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_report.txt')+' --paired '+self.input_file_1+' '+self.input_file_2+' > '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_result.txt')
        subprocess.run(com,shell=True,check=True) 
        com2 = 'bracken -d '+self.path_to_kraken2_db+' -i '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_report.txt')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2_bracken.output')+' -w '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_bracken.report')+' -r 150 -l S'
        subprocess.run(com2, shell=True, check=True,encoding='utf-8')
        com2 = 'kreport2mpa.py -r '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_bracken.report')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2_bracken.taxon.abundance')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com2 = 'kreport2krona.py -r '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'kraken2_out'),'kraken2_report.txt')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2krona')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com2 = 'ktImportText '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2krona')+' -o '+os.path.join(os.path.join(os.path.join(self.result_dir, 'taxonomy'),'kraken2_out'),'kraken2krona.html')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print('End Kraken2_paired_end')
    def process_metaphlan2_line(self,curr_str):
        split_str = curr_str.strip().split('\t')
        out = []
        out.append(split_str[2])
        taxo = split_str[0].split('|')
        out = out+taxo
        return '\t'.join(str(i) for i in out)
    def metaphlan2krona(self,input_file,output_file):
        in_file = open(input_file,'r')
        out_file = open(output_file,'w')
        for line in in_file:
            if line.startswith('#'):
                continue 
            krona_line = self.process_metaphlan2_line(line)
            out_file.write(krona_line+'\n')
        in_file.close() 
        out_file.close() 
    def metaphlan2_single_end(self):
        print('Begin MetaPhlan2_Single_End')
        metaphlan2_conf = self.conf['MetaPhlAn2']
        input_type = metaphlan2_conf['--input_type']
        bt2_ps = metaphlan2_conf['--bt2_ps']
        tax_lev = metaphlan2_conf['--tax_lev']
        min_cu_len = metaphlan2_conf['--min_cu_len']
        min_alignment_len = metaphlan2_conf['--min_alignment_len']
        ignore_viruses = metaphlan2_conf['--ignore_viruses']
        ignore_eukaryotes = metaphlan2_conf['--ignore_eukaryotes']
        ignore_bacteria = metaphlan2_conf['--ignore_bacteria']
        ignore_archaea = metaphlan2_conf['--ignore_archaea']
        avoid_disqm = metaphlan2_conf['--avoid_disqm']
        no_map = metaphlan2_conf['--no_map']
        stat_q = metaphlan2_conf['--stat_q']
        ignore_markers = metaphlan2_conf['--ignore_markers']
        stat = metaphlan2_conf['--stat']
        t = metaphlan2_conf['-t']
        nreads = metaphlan2_conf['--nreads']
        pres_th = metaphlan2_conf['--pres_th']
        clade = metaphlan2_conf['--clade']
        min_ab = metaphlan2_conf['--min_ab']
        read_min_len = metaphlan2_conf['--read_min_len']
        if input_type is None:
            print('Please set metaphlan2_conf "--input_type"')
            exit(0)
        com = 'metaphlan --input_type '+input_type+' '
        if bt2_ps:
            com += '--bt2_ps '+bt2_ps+' '
        if tax_lev:
            com += '--tax_lev '+tax_lev+' ' 
        if min_cu_len:
            com += '--min_cu_len '+min_cu_len+' '
        if min_alignment_len:
            com += '--min_alignment_len ' + min_alignment_len + ' '
        if ignore_viruses is True:
            com += '--ignore_viruses '
        if ignore_eukaryotes is True:
            com += '--ignore_eukaryotes '
        if ignore_bacteria is True:
            com += '--ignore_bacteria '
        if ignore_archaea is True:
            com += '--ignore_archaea '
        if avoid_disqm is True:
            com += '--avoid_disqm '
        if no_map is True:
            com += '--no_map '
        if stat_q:
            com += '--stat_q ' + stat_q + ' '
        if ignore_markers:
            com += '--ignore_markers ' +ignore_markers+' '
        if stat:
            com += '--stat '+stat+' '
        if t:
            com += '-t '+t+' '
        if nreads:
            com += '--nreads ' + nreads + ' '
        if pres_th:
            com += '--pres_th ' + pres_th + ' '
        if clade:
            com += '--clade ' + clade + ' '
        if min_ab:
            com += '--min_ab ' + min_ab + ' '
        if read_min_len:
            com += '--read_min_len ' + read_min_len + ' '
        if self.input_file.endswith('.gz'):
            subprocess.run('gunzip -c '+self.input_file+' > '+os.path.join(os.path.join(self.result_dir,'metaphlan2_out'),self.input_file.rsplit('.',1)[0]),shell=True,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
            self.input_file = os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),self.input_file.rsplit('.',1)[0])
        com1 = com +self.input_file+' '
        com1 += ' --bowtie2out ' + os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),'metaphlan2_bowtie2.bz2')+' > ' + os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),'metaphlan2_profile.txt')
        subprocess.run(com1, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        self.metaphlan2krona(os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2_profile.txt'), os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2krona'))
        com2 = 'ktImportText '+os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2krona')+' -o '+os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2krona.html')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print('End MetaPhlan2_Single_End')
    def metaphlan2_paired_end(self):
        print('Begin MetaPhlan2_Paired_End')
        metaphlan2_conf = self.conf['MetaPhlAn2']
        input_type = metaphlan2_conf['--input_type']
        bt2_ps = metaphlan2_conf['--bt2_ps']
        tax_lev = metaphlan2_conf['--tax_lev']
        min_cu_len = metaphlan2_conf['--min_cu_len']
        min_alignment_len = metaphlan2_conf['--min_alignment_len']
        ignore_viruses = metaphlan2_conf['--ignore_viruses']
        ignore_eukaryotes = metaphlan2_conf['--ignore_eukaryotes']
        ignore_bacteria = metaphlan2_conf['--ignore_bacteria']
        ignore_archaea = metaphlan2_conf['--ignore_archaea']
        avoid_disqm = metaphlan2_conf['--avoid_disqm']
        no_map = metaphlan2_conf['--no_map']
        stat_q = metaphlan2_conf['--stat_q']
        ignore_markers = metaphlan2_conf['--ignore_markers']
        stat = metaphlan2_conf['--stat']
        t = metaphlan2_conf['-t']
        nreads = metaphlan2_conf['--nreads']
        pres_th = metaphlan2_conf['--pres_th']
        clade = metaphlan2_conf['--clade']
        min_ab = metaphlan2_conf['--min_ab']
        read_min_len = metaphlan2_conf['--read_min_len']
        if input_type is None:
            print('Please set metaphlan2_conf "--input_type"')
            exit(0)
        com = 'metaphlan --input_type '+input_type+' '
        if bt2_ps:
            com += '--bt2_ps '+bt2_ps+' '
        if tax_lev:
            com += '--tax_lev '+tax_lev+' ' 
        if min_cu_len:
            com += '--min_cu_len '+min_cu_len+' '
        if min_alignment_len:
            com += '--min_alignment_len ' + min_alignment_len + ' '
        if ignore_viruses is True:
            com += '--ignore_viruses '
        if ignore_eukaryotes is True:
            com += '--ignore_eukaryotes '
        if ignore_bacteria is True:
            com += '--ignore_bacteria '
        if ignore_archaea is True:
            com += '--ignore_archaea '
        if avoid_disqm is True:
            com += '--avoid_disqm '
        if no_map is True:
            com += '--no_map '
        if stat_q:
            com += '--stat_q ' + stat_q + ' '
        if ignore_markers:
            com += '--ignore_markers ' +ignore_markers+' '
        if stat:
            com += '--stat '+stat+' '
        if t:
            com += '-t '+t+' '
        if nreads:
            com += '--nreads ' + nreads + ' '
        if pres_th:
            com += '--pres_th ' + pres_th + ' '
        if clade:
            com += '--clade ' + clade + ' '
        if min_ab:
            com += '--min_ab ' + min_ab + ' '
        if read_min_len:
            com += '--read_min_len ' + read_min_len + ' '
        if self.input_file_1.endswith('.gz'):
            subprocess.run('gunzip -c '+self.input_file_1+' > '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),self.input_file_1.rsplit('.',1)[0]),shell=True,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
            self.input_file_1 = os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),self.input_file_1.rsplit('.',1)[0])
        if self.input_file_2.endswith('.gz'):
            subprocess.run('gunzip -c '+self.input_file_2+' > '+os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),self.input_file_2.rsplit('.',1)[0]),shell=True,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
            self.input_file_2 = os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),self.input_file_2.rsplit('.',1)[0])
        subprocess.run('cat '+self.input_file_1+' '+self.input_file_2+' > '+os.path.join(os.path.join(result_dir,'metaphlan2_out'),'metaphlan2_input'), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        com1 = com +os.path.join(os.path.join(result_dir,'metaphlan2_out'),'metaphlan2_input')+' '
        com1 += ' --bowtie2out ' + os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),'metaphlan2_bowtie2.bz2')+' > ' + os.path.join(os.path.join(os.path.join(self.result_dir,'taxonomy'),'metaphlan2_out'),'metaphlan2_profile.txt')
        subprocess.run(com1, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        self.metaphlan2krona(os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2_profile.txt'), os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2krona'))
        com2 = 'ktImportText '+os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2krona')+' -o '+os.path.join(os.path.join(self.result_dir, 'metaphlan2_out'),'metaphlan2krona.html')
        subprocess.run(com2, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print('End MetaPhlan2_Paired_End')
    def run_single(self):
        print('Begin Taxonomy - single end reads')
        if self.conf['Kraken2']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/kraken2_out')
            self.kraken2_single_end()
        elif self.conf['MetaOthello']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out')
            self.metaothello_single_end()
        elif self.conf['MetaPhlAn2']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaphlan2_out')
            self.metaphlan2_single_end()
        else:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/kraken2_out')
            self.kraken2_single_end()
        print('End Taxonomy - single end reads')
    def run_paired(self):
        print('Begin Taxonomy - paired end reads')
        if self.conf['Kraken2']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/kraken2_out')
            self.kraken2_paired_end()
        elif self.conf['MetaOthello']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaothello_out')
            self.metaothello_paired_end()
        elif self.conf['MetaPhlAn2']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/metaphlan2_out')
            self.metaphlan2_paired_end()
        else:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/taxonomy/kraken2_out')
            self.kraken2_paired_end()
        print('End Taxonomy - paired end reads')