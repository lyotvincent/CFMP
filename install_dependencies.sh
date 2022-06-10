#!/bin/sh
set -e

conda install -y fastqc
conda install -y fastp
conda install -y trimmomatic
conda install -y cutadapt
conda install -y bowtie2
conda install -y samtools
conda install -y minimap2
conda install -y megahit
conda install -y spades
conda install -y idba
conda install -y quast
conda install -y kraken2
conda install -y bracken
conda install -y metaphlan
conda install -y prodigal
conda install -y salmon
conda install -y blast
conda install -y eggnog-mapper
conda install -y nanoplot
conda install -y nanofilt
conda install -y porechop
conda install -y canu
conda install -y racon


exit 0