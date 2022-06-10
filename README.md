# CFMP
CFMP is an automatic metagenomic analysis pipeline supporting short-read and long-read sequencing data. It contains quality control, host-DNA removal, assembly, species and functional annotation, and each step is op-tional and can be customized for specific needs.

## Install 

### From github

1. Download program first:```git clone https://github.com/lyotvincent/CFMP.git```
2. Install external tools:  
2.1. Install miniconda from *https://docs.conda.io/en/latest/miniconda.html* or anaconda from *https://www.anaconda.com/products/individual*  
2.2. Create python3.7 environment (because QUAST depends on python3.7) ```conda create -n env_name python=3.7```   
2.3. Install external tools by running a shell script ```sh install_dependencies.sh```  
3. Build Kraken2 database: create kraken2 database folder ```mkdir softwares/kraken2_db``` && then run ```kraken2-build --standard --db softwares/kraken2_db```.
4. Download Krona taxonomy: change directory to softwares/krona/ ```cd softwares/krona/``` && then run ```./updateTaxonomy.sh taxonomy/```.  
5. Download hg19 database and build index: change directory to hg19 ```cd hg19```&& then run ```python download_hg19.py```.   
6. Download MetaOthello database index: change directory to softwares/metaOthello-master ```cd softwares/metaOthello-master``` && then run ```python download_metaOthello_index.py```.  
7. Download eggnog-mapper database: run ```download_eggnog_data.py```.  

## External tools
These software/tools respectively support part of the entire pipeline. If you want to use all the functions of the pipeline, all these software in the table should be installed.
The ✔ in 'conda' column means that the software cound install by conda.
|software|conda|download link|
|----|----|----|
|FastQC|✔|<http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>|
|fastp|✔|<https://github.com/OpenGene/fastp>|
|trimmomatic|✔|<https://github.com/timflutre/trimmomatic>|
|cutadapt|✔|<https://github.com/marcelm/cutadapt>|
|bowtie2|✔|<https://github.com/BenLangmead/bowtie2>|
|samtools|✔|<https://github.com/samtools/samtools>|
|minimap2|✔|<https://github.com/lh3/minimap2>|
|megahit|✔|<https://github.com/voutcn/megahit>|
|spades|✔|<https://github.com/ablab/spades>|
|idba|✔|<https://github.com/loneknightpy/idba>|
|QUAST|✔|<https://github.com/ablab/quast>|
|Kraken2|✔|<https://github.com/DerrickWood/kraken2>|
|Bracken|✔|<https://github.com/jenniferlu717/Bracken>|
|MetaPhlan3|✔|<https://github.com/biobakery/MetaPhlAn>|
|prodigal|✔|<https://github.com/hyattpd/Prodigal>|
|salmon|✔|<https://github.com/COMBINE-lab/salmon>|
|BLAST|✔|<https://blast.ncbi.nlm.nih.gov/Blast.cgi>|
|eggnog-mapper|✔|<https://github.com/eggnogdb/eggnog-mapper>|
|NanoPlot|✔|<https://github.com/wdecoster/NanoPlot>|
|NanoFilt|✔|<https://github.com/wdecoster/nanofilt>|
|Porechop|✔|<https://github.com/rrwick/Porechop>|
|Canu|✔|<https://github.com/marbl/canu>|
