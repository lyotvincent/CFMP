import os 
import sys 
import time 
import json 
import yaml 
import subprocess
import ngs_pipeline 
import tgs_pipeline 
import preprocessing 
import configuration_reader 
def main():
	argv = sys.argv 
	print(str(argv)) 
	if "-V" in argv or "-v" in argv or '-version' in argv or '--version' in argv:
		print("CFMP version: 0.1") 
		exit(0) 
	if len(argv) == 1 or '-h' in argv or '-help' in argv or '--h' in argv or '--help' in argv:
		print_help()
		exit(0)
	input_file = None 
	conf_file_path = None
	db = None 
	outdir = None
	blastp = None
	diamond = None 
	if '-f' in argv:
		input_file = argv[argv.index('-f')+1] 
	else:
		print('Please input -f to annotate')
		exit(0)
	if '-conf_file_path' in argv:
		conf_file_path = argv[argv.index('-conf_file_path')+1]
	else:
		print('Please input configuration file path.')
		exit(0)
	if '-o' in argv:
		outdir = argv[argv.index('-o')+1]
		if not os.path.exists(outdir):
			os.makedirs(outdir)
	else:
		print('Please input -o to set the output_dir')
		exit(0)
	if '-blastp' in argv and '-diamond' in argv:
		print('Please input -blastp or -diamond only one, dont input them at the same time.')
		exit(0)
	elif not '-blastp' in argv and not '-diamond' in argv:
		print('Please input -blastp or -diamond only one')
		exit(0)
	if '-func_fasta' in argv and '-db' in argv:
		print('Please input -func_fasta or -db only one, dont input them at the same time.')
		exit(0)
	elif not '-func_fasta' in argv and not '-db' in argv:
		print('Please input -func_fasta or -db only one')
		exit(0)
	conf = configuration_reader.ConfigurationReader(conf_file_path)
	blastp_conf = conf['blastp']
	blastpevalue = blastp_conf['-evalue'] 
	blastpwordsize = blastp_conf['-word_size'] 
	blastpgapopen = blastp_conf['-gapopen'] 
	blastpgapextend = blastp_conf['-gapextend'] 
	blastpcompbasedstats = blastp_conf['-comp_based_stats']
	blastpseg = blastp_conf['-seg']
	blastpqcov_hsp_perc = blastp_conf['-qcov_hsp_perc'] 
	blastpmaxhsps = blastp_conf['-max_hsps'] 
	blastpcullinglimit = blastp_conf['-culling_limit'] 
	blastpbesthitoverhang = blastp_conf['-best_hit_overhang'] 
	blastpbesthitscoreedge = blastp_conf['-best_hit_score_edge'] 
	blastpmaxtargetseqs = blastp_conf['-max_target_seqs']
	blastpxdropungap = blastp_conf['-xdrop_ungap'] 
	blastpxdropgap = blastp_conf['-xdrop_gap']
	blastpxdropgapfinal = blastp_conf['-xdrop_gap_final']
	blastpwindowsize = blastp_conf['-window_size'] 
	blastpungapped = blastp_conf['-ungapped']
	diamond_conf = conf['diamond']
	diamondmaxtargetseqs = diamond_conf['--max-target-seqs'] 
	diamondtop = diamond_conf['--top'] 
	diamondrangeculling = diamond_conf['--range-culling'] 
	diamondevalue = diamond_conf['--evalue'] 
	diamondminscore = diamond_conf['--min-score'] 
	diamondid = diamond_conf['--id'] 
	diamondquerycover = diamond_conf['--query-cover']
	diamondsubjectcover = diamond_conf['--subject-cover'] 
	diamondsensitive = diamond_conf['--sensitive'] 
	diamondmoresensitive = diamond_conf['--more-sensitive'] 
	diamondblocksize = diamond_conf['--block-size'] 
	diamondindexchunks = diamond_conf['--index-chunks']
	diamondgapopen = diamond_conf['--gapopen'] 
	diamondgapextend = diamond_conf['--gapextend'] 
	diamondmatrix = diamond_conf['--matrix'] 
	diamondcompbasedstats = diamond_conf['--comp-based-stats'] 
	diamondmasking = diamond_conf['--masking'] 
	diamondnoselfhits = diamond_conf['--no-self-hits'] 
	diamondsalltitles = diamond_conf['--salltitles'] 
	diamondsallseqid = diamond_conf['--sallseqid']
	diamondalgo = diamond_conf['--algo'] 
	diamondbin = diamond_conf['--bin'] 
	diamondminorf = diamond_conf['--min-orf'] 
	diamondfreqsd = diamond_conf['--freq-sd'] 
	diamondid2 = diamond_conf['--id2'] 
	diamondwindow = diamond_conf['--window'] 
	diamondxdrop = diamond_conf['--xdrop'] 
	diamondungappedscore = diamond_conf['--ungapped-score'] 
	diamondband = diamond_conf['--band']
	diamondshapes = diamond_conf['--shapes'] 
	diamondshapemask = diamond_conf['--shape-mask']
	diamondcullingoverlap = diamond_conf['--culling-overlap']
	diamondrangecover = diamond_conf['--range-cover'] 
	diamondnoautoappend = diamond_conf['--no-auto-append']
	diamondstopmatchscore = diamond_conf['--stop-match-score'] 
	diamondtantanminMaskProb = diamond_conf['--tantan-minMaskProb']
	diamonddaa = diamond_conf['--daa']
	diamondforwardonly = diamond_conf['--forwardonly'] 
	diamondseq = diamond_conf['--seq']
	if '-db' in argv:
		db = argv[argv.index('-db')+1]
		com = ''
		if '-blastp' in argv:
			com += 'blastp '
			if blastpevalue:
				com += '-evalue '+blastpevalue+' '
			if blastpwordsize:
				com += '-word_size '+blastpwordsize+' '
			if blastpgapopen:
				com += '-gapopen ' + blastpgapopen+' '
			if blastpgapextend:
				com += '-gapextend '+ blastpgapextend + ' '
			if blastpcompbasedstats:
				com += '-comp_based_stats ' + blastpcompbasedstats + ' '
			com += '-outfmt 6 '
			if blastpseg:
				com += '-seg '+blastpseg+' '
			if blastpqcov_hsp_perc:
				com += '-qcov_hsp_perc ' + blastpqcov_hsp_perc + ' '
			if blastpmaxhsps:
				com += '-max_hsps '+ blastpmaxhsps + ' '
			if blastpcullinglimit:
				com += '-culling_limit '+ blastpcullinglimit + ' '
			if blastpbesthitoverhang:
				com += '-best_hit_overhang ' + blastpbesthitoverhang + ' '
			if blastpbesthitscoreedge:
				com += '-best_hit_score_edge ' + blastpbesthitscoreedge + ' '
			if blastpmaxtargetseqs:
				com += '-max_target_seqs ' + blastpmaxtargetseqs + ' '
			if blastpxdropungap:
				com += '-xdrop_ungap ' + blastpxdropungap + ' '
			if blastpxdropgap:
				com += '-xdrop_gap ' + blastpxdropgap + ' '
			if blastpxdropgapfinal:
				com += '-xdrop_gap_final ' + blastpxdropgapfinal + ' '
			if blastpwindowsize:
				com += '-window_size ' + blastpwindowsize + ' '
			if blastpungapped:
				com += '-ungapped ' + blastpungapped + ' '
			com += '-query '+input_file+' -db ' +db+' -out '+os.path.join(outdir,'anno_align.result')+' '
			subprocess.run(com, shell=True, check=True,encoding='utf-8')
		if '-diamond' in argv:
			com += 'diamond blastp --outfmt 6 '
			if diamondmaxtargetseqs:
				com += '--max-target-seqs '+diamondmaxtargetseqs+' '
			if diamondtop:
				com += '--top ' + diamondtop+' '
			if diamondrangeculling:
				com += '--range-culling '+ diamondrangeculling + ' '
			if diamondevalue:
				com += '--evalue ' + diamondevalue + ' '
			if diamondminscore:
				com += '--min-score ' + diamondminscore + ' '
			if diamondid:
				com += '--id ' +diamondid+' '
			if diamondquerycover:
				com += '--query-cover ' + diamondquerycover + ' '
			if diamondsubjectcover:
				com += '--subject-cover ' + diamondsubjectcover + ' '
			if diamondsensitive is True:
				com += '--sensitive ' 
			if diamondmoresensitive is True:
				com += '--more-sensitive '
			if diamondblocksize:
				com += '--block-size '+ diamondblocksize + ' '
			if diamondindexchunks:
				com += '--index-chunks ' + diamondindexchunks + ' '
			if diamondgapopen:
				com += '--gapopen ' + diamondgapopen + ' '
			if diamondgapextend:
				com += '--gapextend ' + diamondgapextend + ' '
			if diamondmatrix:
				com += '--matrix ' + diamondmatrix + ' '
			if diamondcompbasedstats:
				com += '--comp-based-stats ' + diamondcompbasedstats + ' '
			if diamondmasking is True:
				com += '--masking ' 
			if diamondnoselfhits is True:
				com += '--no-self-hits ' 
			if diamondsalltitles is True:
				com += '--salltitles ' 
			if diamondsallseqid is True:
				com += '--sallseqid ' 
			if diamondalgo:
				com += '--algo ' + diamondalgo + ' '
			if diamondbin:
				com += '--bin ' + diamondbin + ' '
			if diamondminorf:
				com += '--min-orf '+ diamondminorf + ' '
			if diamondfreqsd:
				com += '--freq-sd '+ diamondfreqsd + ' '
			if diamondid2:
				com += '--id2 ' + diamondid2 + ' '
			if diamondwindow:
				com += '--window ' + diamondwindow + ' '
			if diamondxdrop:
				com += '--xdrop ' + diamondxdrop + ' '
			if diamondungappedscore:
				com += '--ungapped-score ' + diamondungappedscore + ' '
			if diamondband:
				com += '--band ' + diamondband + ' '
			if diamondshapes:
				com += '--shapes ' + diamondshapes + ' '
			if diamondshapemask:
				com += '--shape-mask ' + diamondshapemask + ' '
			if diamondcullingoverlap:
				com += '--culling-overlap ' + diamondcullingoverlap + ' '
			if diamondrangecover:
				com += '--range-cover ' + diamondrangecover+' '
			if diamondnoautoappend is True:
				com += '--no-auto-append '
			if diamondstopmatchscore:
				com += '--stop-match-score ' + diamondstopmatchscore + ' '
			if diamondtantanminMaskProb:
				com += '--tantan-minMaskProb ' + diamondtantanminMaskProb + ' '
			if diamonddaa is True:
				com += '--daa '
			if diamondforwardonly is True:
				com += '--forwardonly '
			if diamondseq:
				com += '--seq ' + diamondseq + ' '
			com += '--query '+self.protein+' --out '+os.path.join(outdir,'anno_align.result')+' --db '+db
			subprocess.run(com, shell=True, check=True, encoding='utf-8')
	if '-func_fasta' in argv:
		func_fasta = argv[argv.index('-func_fasta')+1]
		com = ''
		if '-blastp' in argv:
			com += 'makeblastdb -in '+ func_fasta +' -dbtype prot -input_type fasta -out '+os.path.join(outdir,'func_anno')
			subprocess.run(com, shell=True, check=True, encoding='utf-8')
			com = 'blastp '
			if blastpevalue:
				com += '-evalue '+blastpevalue+' '
			if blastpwordsize:
				com += '-word_size '+blastpwordsize+' '
			if blastpgapopen:
				com += '-gapopen ' + blastpgapopen+' '
			if blastpgapextend:
				com += '-gapextend '+ blastpgapextend + ' '
			if blastpcompbasedstats:
				com += '-comp_based_stats ' + blastpcompbasedstats + ' '
			com += '-outfmt 6 '
			if blastpseg:
				com += '-seg '+blastpseg+' '
			if blastpqcov_hsp_perc:
				com += '-qcov_hsp_perc ' + blastpqcov_hsp_perc + ' '
			if blastpmaxhsps:
				com += '-max_hsps '+ blastpmaxhsps + ' '
			if blastpcullinglimit:
				com += '-culling_limit '+ blastpcullinglimit + ' '
			if blastpbesthitoverhang:
				com += '-best_hit_overhang ' + blastpbesthitoverhang + ' '
			if blastpbesthitscoreedge:
				com += '-best_hit_score_edge ' + blastpbesthitscoreedge + ' '
			if blastpmaxtargetseqs:
				com += '-max_target_seqs ' + blastpmaxtargetseqs + ' '
			if blastpxdropungap:
				com += '-xdrop_ungap ' + blastpxdropungap + ' '
			if blastpxdropgap:
				com += '-xdrop_gap ' + blastpxdropgap + ' '
			if blastpxdropgapfinal:
				com += '-xdrop_gap_final ' + blastpxdropgapfinal + ' '
			if blastpwindowsize:
				com += '-window_size ' + blastpwindowsize + ' '
			if blastpungapped:
				com += '-ungapped ' + blastpungapped + ' '
			com += '-query '+input_file+' -db ' +os.path.join(outdir,'func_anno')+' -out '+os.path.join(outdir,'anno_align.result')+' '
			subprocess.run(com, shell=True, check=True,encoding='utf-8')
		if '-diamond' in argv:
			com += 'diamond makedb --in '+func_fasta+' --db '+os.path.join(outdir,'func_anno')
			subprocess.run(com, shell=True, check=True, encoding='utf-8')
			com += 'diamond blastp --outfmt 6 '
			if diamondmaxtargetseqs:
				com += '--max-target-seqs '+diamondmaxtargetseqs+' '
			if diamondtop:
				com += '--top ' + diamondtop+' '
			if diamondrangeculling:
				com += '--range-culling '+ diamondrangeculling + ' '
			if diamondevalue:
				com += '--evalue ' + diamondevalue + ' '
			if diamondminscore:
				com += '--min-score ' + diamondminscore + ' '
			if diamondid:
				com += '--id ' +diamondid+' '
			if diamondquerycover:
				com += '--query-cover ' + diamondquerycover + ' '
			if diamondsubjectcover:
				com += '--subject-cover ' + diamondsubjectcover + ' '
			if diamondsensitive is True:
				com += '--sensitive ' 
			if diamondmoresensitive is True:
				com += '--more-sensitive '
			if diamondblocksize:
				com += '--block-size '+ diamondblocksize + ' '
			if diamondindexchunks:
				com += '--index-chunks ' + diamondindexchunks + ' '
			if diamondgapopen:
				com += '--gapopen ' + diamondgapopen + ' '
			if diamondgapextend:
				com += '--gapextend ' + diamondgapextend + ' '
			if diamondmatrix:
				com += '--matrix ' + diamondmatrix + ' '
			if diamondcompbasedstats:
				com += '--comp-based-stats ' + diamondcompbasedstats + ' '
			if diamondmasking is True:
				com += '--masking ' 
			if diamondnoselfhits is True:
				com += '--no-self-hits ' 
			if diamondsalltitles is True:
				com += '--salltitles ' 
			if diamondsallseqid is True:
				com += '--sallseqid ' 
			if diamondalgo:
				com += '--algo ' + diamondalgo + ' '
			if diamondbin:
				com += '--bin ' + diamondbin + ' '
			if diamondminorf:
				com += '--min-orf '+ diamondminorf + ' '
			if diamondfreqsd:
				com += '--freq-sd '+ diamondfreqsd + ' '
			if diamondid2:
				com += '--id2 ' + diamondid2 + ' '
			if diamondwindow:
				com += '--window ' + diamondwindow + ' '
			if diamondxdrop:
				com += '--xdrop ' + diamondxdrop + ' '
			if diamondungappedscore:
				com += '--ungapped-score ' + diamondungappedscore + ' '
			if diamondband:
				com += '--band ' + diamondband + ' '
			if diamondshapes:
				com += '--shapes ' + diamondshapes + ' '
			if diamondshapemask:
				com += '--shape-mask ' + diamondshapemask + ' '
			if diamondcullingoverlap:
				com += '--culling-overlap ' + diamondcullingoverlap + ' '
			if diamondrangecover:
				com += '--range-cover ' + diamondrangecover+' '
			if diamondnoautoappend is True:
				com += '--no-auto-append '
			if diamondstopmatchscore:
				com += '--stop-match-score ' + diamondstopmatchscore + ' '
			if diamondtantanminMaskProb:
				com += '--tantan-minMaskProb ' + diamondtantanminMaskProb + ' '
			if diamonddaa is True:
				com += '--daa '
			if diamondforwardonly is True:
				com += '--forwardonly '
			if diamondseq:
				com += '--seq ' + diamondseq + ' '
			com += '--query '+self.protein+' --out '+os.path.join(outdir,'anno_align.result')+' --db '+db
			subprocess.run(com, shell=True, check=True, encoding='utf-8')
def print_help():
	print('help:')
	print('-f the protein file to annotate function, generatd by CFMP gene_prediction or user\'s own protein file') 
	print('-db the functional protein database index that have built')
	print('-func_fasta the functional database of amino acid sequences in fasta')
	print('-blastp build index by blastp or provided blastp index')
	print('-diamond build index by diamond or provided diamond index')
	print('-o out directory name') 
	print('-conf_file_path configuration file for CFMP pipeline which is in xlsx format and only the configures of blastp or diamond are valid') 
	print('-h or -help or --h or --help look help') 

if __name__ == '__main__':
	main() 