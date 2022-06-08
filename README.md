# CFMP
CFMP is an automatic metagenomic analysis pipeline supporting short-read and long-read sequencing data. It contains quality control, host-DNA removal, assembly, species and functional annotation, and each step is op-tional and can be customized for specific needs.

## Install 

### From github

1. Download program first:```git clone https://github.com/lyotvincent/CFMP.git```
2. Install external tools:  
2.1. Install miniconda from *https://docs.conda.io/en/latest/miniconda.html* or anaconda from *https://www.anaconda.com/products/individual*  
2.2. Create python3.7 environment (because QUAST depends on python3.7) ```conda create -n env_name python=3.7```   
2.3. Install external tools by running a shell script ```sh install_dependencies.sh```  
3. Download hg19 database and build index: change directory to hg19 ```cd hg19```&& then run ```python download_hg19.py```.   
4. Build Kraken2 database:  
5. Download MetaOthello database index:  
