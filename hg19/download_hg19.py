import subprocess
def main():
    subprocess.run('wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz', shell=True, check=True)
    subprocess.run('tar zvfx chromFa.tar.gz', shell=True, check=True)
    subprocess.run('cat *.fa > hg19.fa', shell=True, check=True)
    subprocess.run('bowtie2-build hg19.fa hg19', shell=True, check=True)
    subprocess.run('minimap2 hg19.fa -d hg19.min', shell=True, check=True)
    subprocess.run('rm ch* -f', shell=True, check=True)
if __name__=='__main__':
    main()