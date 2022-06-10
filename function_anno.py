import subprocess 
import os 
import pandas as pd 
import func_anno_plot
class Function_Annotation:
    path_to_Rscripts = os.path.join(os.path.dirname(os.path.realpath(__file__)),'R_scripts')
    result_dir = None 
    conf = None 
    protein = None 
    tpm = None 
    def __init__(self,result_dir,conf,protein=None,tpm=None):
        self.result_dir = result_dir
        self.conf = conf 
        self.protein = protein 
        self.tpm = tpm 
    def emapper(self):
        print('Begin emapper.py')
        emapper_conf = self.conf['emapper.py']
        emappermatrix = emapper_conf['--matrix'] 
        emappergapopen = emapper_conf['--gapopen'] 
        emappergapextend = emapper_conf['--gapextend'] 
        emapperquerycover = emapper_conf['--query-cover'] 
        emappersubjectcover = emapper_conf['--subject-cover'] 
        emapperseedorthologevalue = emapper_conf['--seed_ortholog_evalue'] 
        emapperseedorthologscore = emapper_conf['--seed_ortholog_score'] 
        emappertargettaxa = emapper_conf['--target_taxa']
        emapperpredictoutputformat = emapper_conf['--predict_output_format'] 
        emappercpu = emapper_conf['--cpu']
        com = 'emapper.py -i '+self.protein+' -m diamond --output '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/emapper_anno'+' '
        if emappermatrix:
            com += '--matrix '+emappermatrix+' '
        if emappergapopen:
            com += '--gapopen '+emappergapopen+' '
        if emapperquerycover:
            com += '--query-cover '+emapperquerycover+' '
        if emappersubjectcover:
            com += '--subject-cover '+emappersubjectcover+' '
        if emapperseedorthologevalue:
            com += '--seed_ortholog_evalue '+emapperseedorthologevalue+' '
        if emapperseedorthologscore:
            com += '--seed_ortholog_score '+emapperseedorthologscore+' '
        if emappertargettaxa:
            com += '--target_taxa '+emappertargettaxa+' '
        if emapperpredictoutputformat:
            com += '--predict_output_format '+emapperpredictoutputformat+' '
        if emappercpu:
            com+='--cpu '+str(int(emappercpu))+' '
        subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if self.tpm is not None:
            com = 'cat '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/emapper_anno.emapper.annotations'+'| sed "1,3d" | sed "1s/#//" | sed "/^#/d" > '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/emapper_anno.emapper.annotations2plot'
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            eggnog_anno_all = pd.read_table(os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/emapper_anno.emapper.annotations2plot')
            gene_tpm = self.tpm
            if 'metagenemark' in self.protein or 'MetaGeneMark' in self.protein:
                func_anno_plot.GO_anno_plot(eggnog_anno_all[['query_name', 'GOs']].dropna(axis=0, how='any').drop_duplicates(), gene_tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/go_anno', os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/go_level2_plot_anno')
                com = 'Rscript '+os.path.join(self.path_to_Rscripts, 'go_anno_plot.R')+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/go_level2_plot_anno'+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/GO_level2_anno_plot.pdf'
                subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
                func_anno_plot.kegg_anno_plot(eggnog_anno_all[['query_name','KEGG_Pathway']].dropna(axis=0, how='any').drop_duplicates(),gene_tpm,os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/kegg_pathway_plot_anno')
                com = 'Rscript '+os.path.join(self.path_to_Rscripts, 'kegg_anno_plot.R')+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/kegg_pathway_plot_anno'+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/kegg_pathway_plot_anno.pdf'
                subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
                func_anno_plot.CAZy_plot_anno(eggnog_anno_all[['query_name','CAZy']].dropna(axis=0, how='any').drop_duplicates(), gene_tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/cazy_anno_plot')
                com = 'Rscript '+os.path.join(self.path_to_Rscripts,'cazy_anno_plot.R')+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/cazy_anno_plot'+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/cazy_anno_plot.pdf'
                subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
            else:
                func_anno_plot.GO_anno_plot2(eggnog_anno_all[['query_name', 'GOs']].dropna(axis=0, how='any').drop_duplicates(), gene_tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/go_anno',os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/go_level2_plot_anno')
                com = 'Rscript '+os.path.join(self.path_to_Rscripts, 'go_anno_plot.R')+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/go_level2_plot_anno'+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/GO_level2_anno_plot.pdf'
                subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding='utf-8')
                func_anno_plot.kegg_anno_plot2(eggnog_anno_all[['query_name','KEGG_Pathway']].dropna(axis=0, how='any').drop_duplicates(),gene_tpm,os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/kegg_pathway_plot_anno')
                com = 'Rscript '+os.path.join(self.path_to_Rscripts, 'kegg_anno_plot.R')+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/kegg_pathway_plot_anno'+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/kegg_pathway_plot_anno.pdf'
                subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
                func_anno_plot.CAZy_plot_anno2(eggnog_anno_all[['query_name','CAZy']].dropna(axis=0, how='any').drop_duplicates(), gene_tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/cazy_anno_plot')
                com = 'Rscript '+os.path.join(self.path_to_Rscripts,'cazy_anno_plot.R')+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/cazy_anno_plot'+' '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out/cazy_anno_plot.pdf'
                subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding='utf-8')
        print('End emapper.py')
    def AnnoByBlastp(self):
        print('Begin Annotation by Blastp')
        PHI_Anno_enable = self.conf['PHI_Annotation']['enable']
        VFDB_Anno_enable = self.conf['VFDB_Annotation']['enable']
        CARD_Anno_enable = self.conf['CARD_Annotation']['enable']
        TCDB_Anno_enable = self.conf['TCDB_Annotation']['enable']
        phi_plot_top = self.conf['PHI_Annotation']['plot_for_top_k']
        vfdb_plot_top = self.conf['VFDB_Annotation']['plot_for_top_k']
        card_plot_top = self.conf['CARD_Annotation']['plot_for_top_k']
        tcdb_plot_top = self.conf['TCDB_Annotation']['plot_for_top_k']
        blastp_conf = self.conf['blastp']
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
        if PHI_Anno_enable:
            com += '-query '+self.protein+' -db '+os.path.join(os.path.join(path_func_db,'PHI'),'PHIDB')+' -out '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/PHI_anno'+' '
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            phi_blast=os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/PHI_anno'
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.PHI_anno_plot(phi_blast, self.tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/phi_anno_result', os.path.join(os.path.join(self.result_dir,'function_annotation'),'phi_anno_plot'), phi_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'phi_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.PHI_anno_plot2(phi_blast, self.tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/phi_anno_result', os.path.join(os.path.join(self.result_dir,'function_annotation'),'phi_anno_plot'), phi_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'phi_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if TCDB_Anno_enable:
            com += '-query '+self.protein+' -db '+os.path.join(os.path.join(path_func_db,'TCDB'),'TCDB')+' -out '+os.path.join(os.path.join(self.result_dir, 'function_annotation'),'TCDB_anno')+' '
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            tcdb_blast=os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno')
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.TCDB_anno_plot(tcdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_plot'), tcdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'tcdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.TCDB_anno_plot2(tcdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_plot'), tcdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'tcdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if VFDB_Anno_enable:
            com += '-query '+self.protein+' -db '+os.path.join(os.path.join(path_func_db,'VFDB'),'VFDB_prot')+' -out '+os.path.join(os.path.join(self.result_dir, 'function_annotation'),'VFDB_anno')+' '
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            vfdb_blast=os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno')
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.VFDB_anno_plot(vfdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_plot'), vfdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'vfdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.VFDB_anno_plot2(vfdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_plot'), vfdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'vfdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if CARD_Anno_enable:
            com += '-query '+self.protein+' -db '+os.path.join(os.path.join(os.path.join(path_func_db,'CARD'),'localDB'),'card_anno')+' -out '+os.path.join(os.path.join(self.result_dir, 'function_annotation'),'CARD_anno')+' '
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            card_blast=os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno')
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.CARD_anno_plot(card_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_plot'), card_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'card_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.CARD_anno_plot2(card_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_plot'), card_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'card_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print('End Annotation by Blastp')
    def AnnoByDiamond(self):
        print('Begin Annotation by Diamond')
        PHI_Anno_enable = self.conf['PHI_Annotation']['enable']
        VFDB_Anno_enable = self.conf['VFDB_Annotation']['enable']
        CARD_Anno_enable = self.conf['CARD_Annotation']['enable']
        TCDB_Anno_enable = self.conf['TCDB_Annotation']['enable']
        phi_plot_top = self.conf['PHI_Annotation']['plot_for_top_k']
        vfdb_plot_top = self.conf['VFDB_Annotation']['plot_for_top_k']
        card_plot_top = self.conf['CARD_Annotation']['plot_for_top_k']
        tcdb_plot_top = self.conf['TCDB_Annotation']['plot_for_top_k']
        diamond_conf = self.conf['diamond']
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
        com = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'softwares'),'diamond')+' blastp --outfmt 6 '
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
        if PHI_Anno_enable:
            com += '--query '+self.protein+' --out '+os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/PHI_anno'+' --db '+os.path.join(os.path.join(path_func_db,'PHI'),'PHIDB')
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            phi_blast=os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/PHI_anno'
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.PHI_anno_plot(phi_blast, self.tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/phi_anno_result', os.path.join(os.path.join(self.result_dir,'function_annotation'),'phi_anno_plot'), phi_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'phi_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.PHI_anno_plot2(phi_blast, self.tpm, os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/phi_anno_result', os.path.join(os.path.join(self.result_dir,'function_annotation'),'phi_anno_plot'), phi_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'phi_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'phi_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if TCDB_Anno_enable:
            com += '--query '+self.protein+' --out '+os.path.join(os.path.join(self.result_dir, 'function_annotation'),'TCDB_anno')+' --db '+os.path.join(os.path.join(path_func_db,'TCDB'),'TCDB')
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            tcdb_blast=os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno')
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.TCDB_anno_plot(tcdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_plot'), tcdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'tcdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.TCDB_anno_plot2(tcdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'TCDB_anno_plot'), tcdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'tcdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'TCDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if VFDB_Anno_enable:
            com += '--query '+self.protein+' --out '+os.path.join(os.path.join(self.result_dir, 'function_annotation'),'VFDB_anno')+' --db '+os.path.join(os.path.join(path_func_db,'VFDB'),'VFDB_prot')
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            vfdb_blast=os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno')
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.VFDB_anno_plot(vfdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_plot'), vfdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'vfdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.VFDB_anno_plot2(vfdb_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'VFDB_anno_plot'), vfdb_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'vfdb_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'VFDB_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if CARD_Anno_enable:
            com += '--query '+self.protein+' --out '+os.path.join(os.path.join(self.result_dir, 'function_annotation'),'CARD_anno')+' --db '+os.path.join(os.path.join(os.path.join(path_func_db,'CARD'),'localDB'),'card_anno')
            subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            card_blast=os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno')
            if self.tpm is not None:
                if self.protein.search('metagenemark') or self.protein.search('MetaGeneMark'):
                    func_anno_plot.CARD_anno_plot(card_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_plot'), card_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'card_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
                else:
                    func_anno_plot.CARD_anno_plot2(card_blast, self.tpm, os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_result'), os.path.join(os.path.join(self.result_dir,'function_annotation'),'CARD_anno_plot'), card_plot_top)
                    com = 'Rscript '+os.path.join(self.path_to_Rscripts,'card_anno_plot.R')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot')+' '+os.path.join(os.path.join(self.result_dir,'function_annotation'), 'CARD_anno_plot.pdf')
                    subprocess.run(com, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        print('End Annotation by Diamond')
    def run(self):
        print('Begin Functional Annotation')
        if self.conf['emapper.py']['enable']:
            os.mkdir(os.path.abspath('.')+'/'+self.result_dir+'/function_annotation/emapper_out')
            self.emapper()
        elif self.conf['blastp']['enable']:
            self.AnnoByBlastp()
        elif self.conf['diamond']['enable']:
            self.AnnoByDiamond()
        print('End Functional Annotation')