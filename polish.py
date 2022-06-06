import subprocess
import os 
class polish:
    result_dir = None 
    conf = None 
    input_file = None 
    illumina_1 = None 
    illumina_2 = None
    nanopore = None 
    pacbio = None 
    output = None
    def __init__(self,result_dir,conf,input_file=None,illumina_1=None,illumina_2=None,nanopore=None,pacbio=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.input_file = input_file
        self.illumina_1 = illumina_1
        self.illumina_2 = illumina_2
        self.nanopore = nanopore
        self.pacbio = pacbio
        if os.path.isdir(os.path.join(self.result_dir,'polish_result')) is False:
            os.mkdir(os.path.join(self.result_dir,'polish_result'))
    def pilon(self):
        print('Begin Pilon')
        path_to_pilon_jar = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'pilon-1.23.jar')
        pilon_conf = self.conf['Pilon']
        pilonoutput =pilon_conf['--output'] 
        changes =pilon_conf['--changes'] 
        vcf =pilon_conf['--vcf'] 
        vcfqe =pilon_conf['--vcfqe'] 
        tracks =pilon_conf['--tracks'] 
        vatiant =pilon_conf['--variant'] 
        chunksize =pilon_conf['--chunksize'] 
        diploid =pilon_conf['--diploid'] 
        snps =pilon_conf['--fix']['snps'] 
        indels =pilon_conf['--fix']['indels']
        gaps =pilon_conf['--fix']['gaps'] 
        local =pilon_conf['--fix']['local'] 
        fixall =pilon_conf['--fix']['all'] 
        bases =pilon_conf['--fix']['bases'] 
        none =pilon_conf['--fix']['none'] 
        amb =pilon_conf['--fix']['amb'] 
        breaks =pilon_conf['--fix']['breaks']
        circles =pilon_conf['--fix']['circles']
        novel =pilon_conf['--fix']['novel'] 
        dumpreads =pilon_conf['--dumpreads'] 
        duplicates =pilon_conf['--duplicates'] 
        iupac =pilon_conf['--iupac'] 
        nonpf =pilon_conf['--nonpf'] 
        targets =pilon_conf['--targets'] 
        defaultqual =pilon_conf['--defaultqual'] 
        flank =pilon_conf['--flank']
        gapmargin =pilon_conf['--gapmargin'] 
        pilonK =pilon_conf['--K'] 
        mindepth =pilon_conf['--mindepth'] 
        mingap =pilon_conf['--mingap'] 
        minmq =pilon_conf['--minmq'] 
        minqual =pilon_conf['--minqual'] 
        nostrays =pilon_conf['--nostrays'] 
        
        if self.illumina_1 or self.illumina_2:
            com = 'bwa index '+self.input_file
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            com = 'bwa mem -t 10 '+self.input_file+' '
            if self.illumina_1:
                com += self.illumina_1+' '
            if self.illumina_2:
                com += self.illumina_2+' '
            com += '| samtools sort -@ 10 -O bam -o '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_ngs.bam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'samtools index ' + os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_ngs.bam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'java -Xmx32G -jar '+ path_to_pilon_jar + ' --genome '+self.input_file
            if illumina_1 and illumina_2:
                com += ' --frags '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_ngs.bam')+' '
            else:
                com += ' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_ngs.bam')+' '
            if pilonoutput:
                com += '--output '+pilonoutput+'_ngs '
            else:
                com += '--output '+'pilon_by_ngs'
            com += '--outdir '+os.path.join(self.result_dir,'polish_result') + ' '
            if changes:
                com += '--changes '
            if vcf:
                com += '--vcf '
            if vcfqe:
                com += '--vcfqe '
            if tracks:
                com += '--tracks '
            if vatiant:
                com += '--vatiant '
            if chunksize:
                com += '--chunksize '+chunksize+' '
            if diploid:
                com += '--diploid ' 
            com += '--fix '
            if snps:
                com += 'snps,'
            if indels:
                com += 'indels,'
            if gaps:
                com += 'gaps,'
            if local:
                com += 'local,'
            if fixall:
                com += 'all,'
            if bases:
                com += 'bases,'
            if none:
                com += 'none,'
            if amb:
                com += 'amb,'
            if breaks:
                com += 'breaks,'
            if circles:
                com += 'circles,'
            if novel:
                com += 'novel,'
            com = com[0,-1]+' '
            if dumpreads:
                com += '--dumpreads '
            if duplicates:
                com += '--duplicates '
            if iupac:
                com += '--iupac '
            if nonpf:
                com += '--nonpf '
            if targets:
                com += '--targets '+targets+' '
            if defaultqual:
                com += '--defaultqual '+defaultqual+' '
            if flank:
                com += '--flank '+flank+' '
            if gapmargin:
                com += '--gapmargin '+gapmargin+' '
            if pilonK:
                com += '--K '+pilonK+' '
            if mindepth:
                com += '--mindepth '+mindepth+' '
            if mingap:
                com += '--mingap '+mingap+' '
            if minmq:
                com += '--minmq '+minmq+' ' 
            if minqual:
                com += '--minqual '+minqual+' '
            
            com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_ngs.log')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
        if self.pacbio:
            com = 'minimap2 '+self.input_file+' -d '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'minimap2 -ax map-pb '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')+' '+self.pacbio+' > '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'samtools sort -@ 10 -O bam -o ' + os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.bam')+' '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'samtools index ' + os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.bam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            
            com = 'java -Xmx32G -jar '+ path_to_pilon_jar + ' --genome '
            if self.illumina_1 or self.illumina_2:
                if pilonoutput:
                    com += os.path.join(os.path.join(self.result_dir,'polish_result'),pilonoutput+'_ngs')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.bam')+' '
                    com += '--output '+pilonoutput+'_ngs_pacbio '
                else:
                    com += os.path.join(os.path.join(self.result_dir,'polish_result'),'pilon_by_ngs')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.bam')+' '
                    com += '--output pilon_by_ngs_pacbio '
            else:
                com += self.input_file+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.bam')+' '
                if pilonoutput:
                    com += '--output '+pilonoutput+'_pacbio '
                else:
                    com += '--output pilon_by_pacbio '
            com += '--outdir '+os.path.join(self.result_dir,'polish_result') + ' '
            if changes:
                com += '--changes '
            if vcf:
                com += '--vcf '
            if vcfqe:
                com += '--vcfqe '
            if tracks:
                com += '--tracks '
            if vatiant:
                com += '--vatiant '
            if chunksize:
                com += '--chunksize '+chunksize+' '
            if diploid:
                com += '--diploid ' 
            com += '--fix '
            if snps:
                com += 'snps,'
            if indels:
                com += 'indels,'
            if gaps:
                com += 'gaps,'
            if local:
                com += 'local,'
            if fixall:
                com += 'all,'
            if bases:
                com += 'bases,'
            if none:
                com += 'none,'
            if amb:
                com += 'amb,'
            if breaks:
                com += 'breaks,'
            if circles:
                com += 'circles,'
            if novel:
                com += 'novel,'
            com = com.rsplit(',')[0]+' '
            if dumpreads:
                com += '--dumpreads '
            if duplicates:
                com += '--duplicates '
            if iupac:
                com += '--iupac '
            if nonpf:
                com += '--nonpf '
            if targets:
                com += '--targets '+targets+' '
            if defaultqual:
                com += '--defaultqual '+defaultqual+' '
            if flank:
                com += '--flank '+flank+' '
            if gapmargin:
                com += '--gapmargin '+gapmargin+' '
            if pilonK:
                com += '--K '+pilonK+' '
            if mindepth:
                com += '--mindepth '+mindepth+' '
            if mingap:
                com += '--mingap '+mingap+' '
            if minmq:
                com += '--minmq '+minmq+' ' 
            if minqual:
                com += '--minqual '+minqual+' '
            if nostrays:
                com += '--nostrays '
            com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_pacbio.log')
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if self.nanopore:
            com = 'minimap2 '+self.input_file+' -d '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'minimap2 -ax map-ont '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')+' '+self.nanopore+' > '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'samtools sort -@ 10 -O bam -o ' + os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'samtools index ' + os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            
            com = 'java -Xmx32G -jar '+ path_to_pilon_jar + ' --genome '
            if self.pacbio:
                if self.illumina_1 or self.illumina_2:
                    if pilonoutput:
                        com += os.path.join(os.path.join(self.result_dir,'polish_result'),pilonoutput+'_ngs_pacbio')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                        com += '--output '+pilonoutput+'_ngs_pacbio_nanopore '
                        self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), pilonoutput+'_ngs_pacbio_nanopore.fasta')
                    else:
                        com += os.path.join(os.path.join(self.result_dir,'polish_result'),'pilon_by_ngs_pacbio')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                        com += '--output pilon_by_ngs_pacbio_nanopore '
                        self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_by_ngs_pacbio_nanopore.fasta')
                else:
                    if pilonoutput:
                        com += os.path.join(os.path.join(self.result_dir,'polish_result'),pilonoutput+'_pacbio')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                        com += '--output '+pilonoutput+'_pacbio_nanopore '
                        self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), pilonoutput+'_pacbio_nanopore.fasta')
                    else:
                        com += os.path.join(os.path.join(self.result_dir,'polish_result'),'pilon_by_pacbio')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                        com += '--output pilon_by_pacbio_nanopore '
                        self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_by_pacbio_nanopore.fasta')
            elif self.illumina_1 or self.illumina_2:
                if pilonoutput:
                    com += os.path.join(os.path.join(self.result_dir,'polish_result'),pilonoutput+'_ngs')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                    com += '--output '+pilonoutput+'_ngs_nanopore '
                    self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), pilonoutput+'_ngs_nanopore.fasta')
                else:
                    com += os.path.join(os.path.join(self.result_dir,'polish_result'),'pilon_by_ngs')+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                    com += '--output pilon_by_ngs_nanopore '
                    self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_by_ngs_nanopore.fasta')
            else:
                com += self.input_file+' --unpaired '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.bam')+' '
                if pilonoutput:
                    com += '--output '+pilonoutput+'_nanopore '
                    self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), pilonoutput+'_nanopore.fasta')
                else:
                    com += '--output pilon_by_nanopore '
                    self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_by_nanopore.fasta')
            com += '--outdir '+os.path.join(self.result_dir,'polish_result') + ' '
            if changes:
                com += '--changes '
            if vcf:
                com += '--vcf '
            if vcfqe:
                com += '--vcfqe '
            if tracks:
                com += '--tracks '
            if vatiant:
                com += '--vatiant '
            if chunksize:
                com += '--chunksize '+chunksize+' '
            if diploid:
                com += '--diploid ' 
            com += '--fix '
            if snps:
                com += 'snps,'
            if indels:
                com += 'indels,'
            if gaps:
                com += 'gaps,'
            if local:
                com += 'local,'
            if fixall:
                com += 'all,'
            if bases:
                com += 'bases,'
            if none:
                com += 'none,'
            if amb:
                com += 'amb,'
            if breaks:
                com += 'breaks,'
            if circles:
                com += 'circles,'
            if novel:
                com += 'novel,'
            com = com[0:-1]+' '
            if dumpreads:
                com += '--dumpreads '
            if duplicates:
                com += '--duplicates '
            if iupac:
                com += '--iupac '
            if nonpf:
                com += '--nonpf '
            if targets:
                com += '--targets '+targets+' '
            if defaultqual:
                com += '--defaultqual '+defaultqual+' '
            if flank:
                com += '--flank '+flank+' '
            if gapmargin:
                com += '--gapmargin '+gapmargin+' '
            if pilonK:
                com += '--K '+pilonK+' '
            if mindepth:
                com += '--mindepth '+mindepth+' '
            if mingap:
                com += '--mingap '+mingap+' '
            if minmq:
                com += '--minmq '+minmq+' ' 
            if minqual:
                com += '--minqual '+minqual+' '
            if nostrays:
                com += '--nostrays '
            com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'pilon_nanopore.log')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
        print('End Pilon')
    def racon(self):
        print('Begin Racon')
        racon_conf = self.conf['Racon']
        raconu = racon_conf['-u'] 
        raconw = racon_conf['-w'] 
        raconq = racon_conf['-q'] 
        racone = racon_conf['-e'] 
        notrimming = racon_conf['--no-trimming'] 
        raconm = racon_conf['-m'] 
        raconx = racon_conf['-x'] 
        racong = racon_conf['-g']
        if self.illumina_1 or self.illumina_2:
            com1 = 'cat '
            com = 'bwa index '+self.input_file
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'bwa mem -t 10 '+self.input_file
            if self.illumina_1:
                com1 += self.illumina_1+' '
                com += self.illumina_1+' '
            if self.illumina_2:
                com1 += self.illumina_2+' '
                com += self.illumina_2+' '
            com1 += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'),'racon_input_ngs')
            subprocess.run(com1, shell=True, check=True, encoding='utf-8')
            com += '| samtools sort -@ 10 -O sam -o '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_ngs.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'racon '+os.path.join(os.path.join(self.result_dir,'polish_result'),'racon_input_ngs')+' '
            com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_ngs.sam')+' '+self.input_file
            if raconu:
                com += '-u ' 
            if raconw:
                com += '-w '+raconw+' '
            if raconq:
                com += '-q '+raconq+' '
            if racone:
                com += '-e '+racone+' '
            if notrimming:
                com += '--no-trimming '
            if raconm:
                com += '-m '+raconm+' '
            if raconx:
                com += '-x '+raconx+' '
            if racong:
                com += '-g '+racong+' '
            com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs.fasta')
            self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs.fasta')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
        if self.pacbio:
            com = 'minimap2 '+self.input_file+ ' -d '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'minimap2 -ax map-pb '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')+' '+self.pacbio+' > '+os.path.join(os.path.join(self.result_dir,'polish_result'),'racon_pacbio.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'racon ' +self.pacbio+' '
            com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_pacbio.sam')+' '
            if self.illumina_1 or self.illumina_2:
                com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs.fasta')+' '
            else:
                com += self.input_file+' '
            if raconu:
                com += '-u ' 
            if raconw:
                com += '-w '+raconw+' '
            if raconq:
                com += '-q '+raconq+' '
            if racone:
                com += '-e '+racone+' '
            if notrimming:
                com += '--no-trimming '
            if raconm:
                com += '-m '+raconm+' '
            if raconx:
                com += '-x '+raconx+' '
            if racong:
                com += '-g '+racong+' '
            if self.illumina_1 or self.illumina_2:
                com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_pacbio.fasta')
                self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_pacbio.fasta')
            else:
                com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_pacbio.fasta')
                self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_pacbio.fasta')
            try:
                return_info=subprocess.Popen(com, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                for next_line in return_info.stdout:
                    print(next_line.decode("utf-8", "ignore"))
                returncode = return_info.wait()
                if returncode:
                    raise subprocess.CalledProcessError(returncode, return_info)
            except Exception as e:
                print(e)
                exit()
        if self.nanopore:
            com = 'minimap2 '+self.input_file+ ' -d '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'minimap2 -ax map-ont '+os.path.join(os.path.join(self.result_dir,'polish_result'),os.path.basename(self.input_file)+'.index')+' '+self.nanopore+' > '+os.path.join(os.path.join(self.result_dir,'polish_result'),'racon_nanopore.sam')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
            com = 'racon ' +self.nanopore+' '
            com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_nanopore.sam')+' '
            if self.pacbio:
                if self.illumina_1 or self.illumina_2:
                    com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_pacbio.fasta')+' '
                else:
                    com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_pacbio.fasta')+' '
            elif self.illumina_1 or self.illumina_2:
                com += os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs.fasta')+' '
            else:
                com += self.input_file+' '
            if raconu:
                com += '-u ' 
            if raconw:
                com += '-w '+raconw+' '
            if raconq:
                com += '-q '+raconq+' '
            if racone:
                com += '-e '+racone+' '
            if notrimming:
                com += '--no-trimming '
            if raconm:
                com += '-m '+raconm+' '
            if raconx:
                com += '-x '+raconx+' '
            if racong:
                com += '-g '+racong+' '
            if self.pacbio:
                if self.illumina_1 or self.illumina_2:
                    com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_pacbio_nanopore.fasta')+' '
                    self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_pacbio_nanopore.fasta')
                else:
                    com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_pacbio_nanopore.fasta')+' '
                    self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_pacbio_nanopore.fasta')
            elif self.illumina_1 or self.illumina_2:
                com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_nanopore.fasta')+' '
                self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_ngs_nanopore.fasta')
            else:
                com += '> '+os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_nanopore.fasta')
                self.output = os.path.join(os.path.join(self.result_dir,'polish_result'), 'racon_by_nanopore.fasta')
            subprocess.run(com, shell=True, check=True, encoding='utf-8')
    def run(self):
        print('Begin Polish')
        if self.conf['Pilon']['enable']:
            self.pilon()
        elif self.conf['Racon']['enable']:
            self.racon()
        else:
            self.racon()
        print('End Polish')
            