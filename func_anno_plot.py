import pandas as pd 
import numpy as np
import re
def process_geneid(geneid):
    return geneid.split('|')[0]
def othersid2geneid(geneid_list, othersid_list, others_head):
    l1 = geneid_list
    l2 = othersid_list
    n = len(l1)
    for i in range(n):
        others_ids = str(l2[i]).strip().split(',')
        k = len(others_ids)
        if k!=1:
            l2[i] = others_ids[0]
            for j in range(1,k):
                l1.append(l1[i])
                l2.append(others_ids[j])
    return pd.DataFrame({'query_name':l1, others_head:l2}, columns=['query_name', others_head]) 
def GO_anno_plot(go_anno_df, geneid2tpm,go_anno_out, go_level2_out):
    goid2geneid = othersid2geneid(go_anno_df['query_name'].tolist(),go_anno_df['GOs'].tolist(), 'GO_ID')
    goid2geneid.columns = ['Gene_ID', 'GO_ID']
    geneid2tpm.columns = ['Gene_ID', 'Gene_TPM']
    go_info = pd.read_table(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'godb.txt'))
    go_info.columns = ['GO_ID', 'DEFINITION', 'ONTOLOGY', 'TERM']
    goid2geneid['Gene_ID'] = goid2geneid.apply(lambda x: process_geneid(x['Gene_ID']), axis=1)
    geneid2tpm['Gene_ID'] = geneid2tpm.apply(lambda x: process_geneid(x['Gene_ID']), axis=1)
    f1 = pd.merge(goid2geneid, geneid2tpm, on='Gene_ID',how='left')
    f2 = pd.merge(f1, go_info, on='GO_ID', how='left') 
    f2.to_csv(go_anno_out, index=None, sep='\t')
    go_level2 = pd.read_table(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'go_level2'),header=None)
    go_level2.columns = ['GO_ID']
    f3 = pd.merge(f1, go_level2, on='GO_ID', how='inner')
    df = f3.groupby('GO_ID',as_index=False).agg('sum')
    df2 = go_info[['GO_ID','ONTOLOGY', 'TERM']].drop_duplicates()
    df3 = pd.merge(df, df2, on='GO_ID', how='left')
    df3.sort_values(['ONTOLOGY',"Gene_TPM"],ascending=[False, True],inplace=True)
    df3.to_csv(go_level2_out, index=None, sep="\t")
def GO_anno_plot2(go_anno_df, geneid2tpm,go_anno_out, go_level2_out):
    goid2geneid = othersid2geneid(go_anno_df['query_name'].tolist(),go_anno_df['GOs'].tolist(), 'GO_ID')
    goid2geneid.columns = ['Gene_ID', 'GO_ID']
    geneid2tpm.columns = ['Gene_ID', 'Gene_TPM']
    go_info = pd.read_table(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'godb.txt'))
    go_info.columns = ['GO_ID', 'DEFINITION', 'ONTOLOGY', 'TERM']
    f1 = pd.merge(goid2geneid, geneid2tpm, on='Gene_ID',how='left')
    f2 = pd.merge(f1, go_info, on='GO_ID', how='left') 
    f2.to_csv(go_anno_out, index=None, sep='\t')
    go_level2 = pd.read_table(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'go_level2'),header=None)
    go_level2.columns = ['GO_ID']
    f3 = pd.merge(f1, go_level2, on='GO_ID', how='inner')
    df = f3.groupby('GO_ID',as_index=False).agg('sum')
    df2 = go_info[['GO_ID','ONTOLOGY', 'TERM']].drop_duplicates()
    df3 = pd.merge(df, df2, on='GO_ID', how='left')
    df3.sort_values(['ONTOLOGY',"Gene_TPM"],ascending=[False, True],inplace=True)
    df3.to_csv(go_level2_out, index=None, sep="\t")
def process_pathway_id(pathid_anno, level3_id):
    pathid_anno_l = pathid_anno.strip().split('map')[0].split(',')[:-1]
    pathway_l3 = []
    for i in pathid_anno_l:
        if i[2:] in level3_id:
            pathway_l3.append(i[2:])     
    return ','.join(pathway_l3)
def level3tolevel2(level3_ids,level2_3_df):
    level3_ids = level3_ids.strip().split(',')
    l2_list = []
    for i in level3_ids:
        l2_id = level2_3_df[level2_3_df['level3_pathway_id']==i]['level2_pathway_id'].tolist()
        if len(l2_id)==0:
            return np.nan
        if l2_id[0] not in l2_list:
            l2_list.append(l2_id[0])
    return ','.join(l2_list)
def kegg_anno_plot(kegg_pathway_anno,gene2tpm,kegg_pathway_anno_out):
    pathway_anno = kegg_pathway_anno
    kegg_pathway = pd.read_table(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'KEGG_pathway_ko_uniq.txt'),dtype={'level1_pathway_id':str,'level2_pathway_id':str,'level3_pathway_id':str})
    pathway_anno['KEGG_Pathway'] = pathway_anno.apply(lambda x: process_pathway_id(x['KEGG_Pathway'],kegg_pathway['level3_pathway_id'].drop_duplicates().tolist()),axis=1)
    l3id2l2id = kegg_pathway[['level2_pathway_id','level3_pathway_id']].drop_duplicates()
    l2id2l1id = kegg_pathway[['level1_pathway_id','level2_pathway_id']].drop_duplicates()
    pathway_anno['level2_pathway_id'] = pathway_anno.apply(lambda x: level3tolevel2(x['KEGG_Pathway'], l3id2l2id),axis=1)
    pathway_anno = pathway_anno[['query_name', 'level2_pathway_id']]
    pathway_anno = othersid2geneid(pathway_anno['query_name'].tolist(),pathway_anno['level2_pathway_id'].tolist(),'level2_pathway_id')
    pathway_anno = pathway_anno.dropna(axis=0, how='any')
    pathway_anno.columns = ['Gene_ID','level2_pathway_id']
    gene2tpm.columns = ['Gene_ID', 'Gene_TPM']
    pathway_anno['Gene_ID'] = pathway_anno.apply(lambda x: process_geneid(x['Gene_ID']), axis=1)
    gene2tpm['Gene_ID'] = gene2tpm.apply(lambda x: process_geneid(x['Gene_ID']), axis=1) 
    pathway_anno = pd.merge(pathway_anno, gene2tpm, on='Gene_ID', how='left')
    pathway_anno = pathway_anno.groupby('level2_pathway_id',as_index=False).agg('sum')
    pathway_anno = pd.merge(pathway_anno, l2id2l1id, on='level2_pathway_id', how='left') 
    level2_all = kegg_pathway[['level2_pathway_id', 'level2_pathway_name']].drop_duplicates()
    pathway_anno = pd.merge(pathway_anno, level2_all, on='level2_pathway_id', how='left')
    level1_all = kegg_pathway[['level1_pathway_id', 'level1_pathway_name']].drop_duplicates()
    pathway_anno = pd.merge(pathway_anno, level1_all, on='level1_pathway_id', how='left')
    pathway_anno.sort_values(['level1_pathway_name', 'Gene_TPM'], ascending=[False, True],inplace=True)
    pathway_anno.to_csv(kegg_pathway_anno_out,index=None,sep='\t')
def kegg_anno_plot2(kegg_pathway_anno,geneid2tpm,kegg_pathway_anno_out):
    pathway_anno = kegg_pathway_anno
    kegg_pathway = pd.read_table(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'KEGG_pathway_ko_uniq.txt'),dtype={'level1_pathway_id':str,'level2_pathway_id':str,'level3_pathway_id':str})
    pathway_anno['KEGG_Pathway'] = pathway_anno.apply(lambda x: process_pathway_id(x['KEGG_Pathway'],kegg_pathway['level3_pathway_id'].drop_duplicates().tolist()),axis=1)
    l3id2l2id = kegg_pathway[['level2_pathway_id','level3_pathway_id']].drop_duplicates()
    l2id2l1id = kegg_pathway[['level1_pathway_id','level2_pathway_id']].drop_duplicates()
    pathway_anno['level2_pathway_id'] = pathway_anno.apply(lambda x: level3tolevel2(x['KEGG_Pathway'], l3id2l2id),axis=1)
    pathway_anno = pathway_anno[['query_name', 'level2_pathway_id']]
    pathway_anno = othersid2geneid(pathway_anno['query_name'].tolist(),pathway_anno['level2_pathway_id'].tolist(),'level2_pathway_id')
    pathway_anno = pathway_anno.dropna(axis=0, how='any')
    pathway_anno.columns = ['Gene_ID','level2_pathway_id']
    gene2tpm.columns = ['Gene_ID', 'Gene_TPM']
    pathway_anno = pd.merge(pathway_anno, gene2tpm, on='Gene_ID', how='left')
    pathway_anno = pathway_anno.groupby('level2_pathway_id',as_index=False).agg('sum')
    pathway_anno = pd.merge(pathway_anno, l2id2l1id, on='level2_pathway_id', how='left') 
    level2_all = kegg_pathway[['level2_pathway_id', 'level2_pathway_name']].drop_duplicates()
    pathway_anno = pd.merge(pathway_anno, level2_all, on='level2_pathway_id', how='left')
    level1_all = kegg_pathway[['level1_pathway_id', 'level1_pathway_name']].drop_duplicates()
    pathway_anno = pd.merge(pathway_anno, level1_all, on='level1_pathway_id', how='left')
    pathway_anno.sort_values(['level1_pathway_name', 'Gene_TPM'], ascending=[False, True],inplace=True)
    pathway_anno.to_csv(kegg_pathway_anno_out,index=None,sep='\t')
def process_cazy_term(cazy_term):
        terms = cazy_term.strip().split(',')
        relt = []
        for i in terms:
            term = re.sub('[0-9]+','',i)
            if term not in relt:
               relt.append(term)
        return ','.join(relt)
def CAZy_plot_anno(df,gene_tpm,out):
    df['CAZy'] = df.apply(lambda x:process_cazy_term(x['CAZy']), axis=1)
    df = othersid2geneid(df['query_name'].tolist(), df['CAZy'].tolist(),'CAZy')
    df.columns = ['Gene_ID', 'CAZy']
    gene_tpm.columns = ['Gene_ID', 'Gene_TPM']
    df['Gene_ID'] = df.apply(lambda x: x['Gene_ID'].strip().split('|')[0], axis=1)
    gene_tpm['Gene_ID'] = df.apply(lambda x: x['Gene_ID'].strip().split('|')[0], axis=1)
    df = pd.merge(df, gene_tpm, on='Gene_ID', how='left')
    df = df.groupby('CAZy', as_index=False).agg('sum')
    df.to_csv(out, index=None, sep='\t')
def CAZy_plot_anno2(df,gene_tpm,out):
    df['CAZy'] = df.apply(lambda x:process_cazy_term(x['CAZy']), axis=1)
    df = othersid2geneid(df['query_name'].tolist(), df['CAZy'].tolist(),'CAZy')
    df.columns = ['Gene_ID', 'CAZy']
    gene_tpm.columns = ['Gene_ID', 'Gene_TPM']
    df = pd.merge(df, gene_tpm, on='Gene_ID', how='left')
    df = df.groupby('CAZy', as_index=False).agg('sum')
    df.to_csv(out, index=None, sep='\t')
def PHI_anno_plot(PHI_blast, gene_tpm, result, plotout, top_k):
    phi_blast = pd.read_table(PHI_blast)
    phi_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    phi_blast = phi_blast[['Gene_ID','Subject', 'Evalue']]
    phi_blast=phi_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    phi_blast['Gene_ID'] = phi_blast.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    gene_tpm['Gene_ID'] = gene_tpm.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    phi_blast['Subject'] = phi_blast.apply(lambda x: x['Subject'].split('#')[-1], axis=1)
    l1 = phi_blast['Gene_ID'].tolist()
    l2 = phi_blast['Subject'].tolist()
    n = len(l1)
    for i in range(n):
        Sub_lis = l2[i].split('__')
        k = len(Sub_lis)
        if k>1:
            l2[i] = Sub_lis[0]
            for j in range(1,k):
                l2.append(Sub_lis[j])
                l1.append(l1[i])
    phi_blast = pd.DataFrame({'Gene_ID':l1, 'Subject':l2}, columns=['Gene_ID', 'Subject'])
    phi_anno = pd.merge(phi_blast, gene_tpm, on='Gene_ID', how='left').groupby('Subject',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    phi_anno.to_csv(result,index=None,sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(phi_anno)>top_k:
        phi_anno.head(top_k).to_csv(plotout,index=None,sep='\t')
    else:
        phi_anno.to_csv(plotout, index=None, sep='\t')
def PHI_anno_plot2(PHI_blast, gene_tpm, result, plotout,top_k):
    phi_blast = pd.read_table(PHI_blast)
    phi_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    phi_blast = phi_blast[['Gene_ID','Subject', 'Evalue']]
    phi_blast=phi_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    phi_blast['Subject'] = phi_blast.apply(lambda x: x['Subject'].split('#')[-1], axis=1)
    l1 = phi_blast['Gene_ID'].tolist()
    l2 = phi_blast['Subject'].tolist()
    n = len(l1)
    for i in range(n):
        Sub_lis = l2[i].split('__')
        k = len(Sub_lis)
        if k>1:
            l2[i] = Sub_lis[0]
            for j in range(1,k):
                l2.append(Sub_lis[j])
                l1.append(l1[i])
    phi_blast = pd.DataFrame({'Gene_ID':l1, 'Subject':l2}, columns=['Gene_ID', 'Subject'])
    phi_anno = pd.merge(phi_blast, gene_tpm, on='Gene_ID', how='left').groupby('Subject',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    phi_anno.to_csv(result,index=None,sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(phi_anno)>top_k:
        phi_anno.head(top_k).to_csv(plotout,index=None,sep='\t')
    else:
        phi_anno.to_csv(plotout, index=None, sep='\t')
def VFDB_anno_plot(vfdb_blast, gene_tpm, result, vfdb_anno2plot,top_k):
    vfdb_blast = pd.read_table(vfdb_blast)
    vfdb_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    vfdb_blast = vfdb_blast[['Gene_ID','Subject', 'Evalue']]
    vfdb_blast=vfdb_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    vfdb_blast = vfdb_blast[['Gene_ID', 'Subject']]
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    vfdb_blast['Gene_ID'] = vfdb_blast.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    gene_tpm['Gene_ID'] = gene_tpm.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    vfdb_anno = pd.merge(vfdb_blast, gene_tpm, on='Gene_ID', how='left').groupby('Subject',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    vfdb_anno.to_csv(result, index=None, sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(vfdb_anno)>top_k:
        vfdb_anno.head(top_k).to_csv(vfdb_anno2plot,index=None,sep='\t')
    else:
        vfdb_anno.to_csv(vfdb_anno2plot,index=None,sep='\t')
def VFDB_anno_plot2(vfdb_blast, gene_tpm, result, vfdb_anno2plot,top_k):
    vfdb_blast = pd.read_table(vfdb_blast)
    vfdb_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    vfdb_blast = vfdb_blast[['Gene_ID','Subject', 'Evalue']]
    vfdb_blast=vfdb_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    vfdb_blast = vfdb_blast[['Gene_ID', 'Subject']]
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    vfdb_anno = pd.merge(vfdb_blast, gene_tpm, on='Gene_ID', how='left').groupby('Subject',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    vfdb_anno.to_csv(result, index=None, sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(vfdb_anno)>top_k:
        vfdb_anno.head(top_k).to_csv(vfdb_anno2plot,index=None,sep='\t')
    else:
        vfdb_anno.to_csv(vfdb_anno2plot,index=None,sep='\t')
def TCDB_anno_plot(tcdb_blast, gene_tpm, result, tcdb_anno2plot,top_k):
    tcdb_blast = pd.read_table(tcdb_blast)
    tcdb_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    tcdb_blast = tcdb_blast[['Gene_ID','Subject', 'Evalue']]
    tcdb_blast=tcdb_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    tc2des = pd.read_table(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'TCDB'),'tc2des'))
    tc2des.columns = ['Subject', 'TC']
    tcdb_blast = pd.merge(tcdb_blast, tc2des, on='Subject', how='left')
    tcdb_blast = tcdb_blast[['Gene_ID', 'TC']]
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    tcdb_blast['Gene_ID'] = tcdb_blast.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    gene_tpm['Gene_ID'] = gene_tpm.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    tcdb_anno = pd.merge(tcdb_blast, gene_tpm, on='Gene_ID', how='left').groupby('TC',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    tcdb_anno.to_csv(result, index=None, sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(tcdb_anno)>top_k:
        tcdb_anno.head(top_k).to_csv(tcdb_anno2plot,index=None,sep='\t')
    else:
        tcdb_anno.to_csv(tcdb_anno2plot,index=None,sep='\t')
def TCDB_anno_plot2(tcdb_blast, gene_tpm, result, tcdb_anno2plot,top_k):
    tcdb_blast = pd.read_table(tcdb_blast)
    tcdb_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    tcdb_blast = tcdb_blast[['Gene_ID','Subject', 'Evalue']]
    tcdb_blast=tcdb_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    tc2des = pd.read_table(os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'func_db'),'TCDB'),'tc2des'))
    tc2des.columns = ['Subject', 'TC']
    tcdb_blast = pd.merge(tcdb_blast, tc2des, on='Subject', how='left')
    tcdb_blast = tcdb_blast[['Gene_ID', 'TC']]
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    tcdb_anno = pd.merge(tcdb_blast, gene_tpm, on='Gene_ID', how='left').groupby('TC',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    tcdb_anno.to_csv(result, index=None, sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(tcdb_anno)>top_k:
        tcdb_anno.head(top_k).to_csv(tcdb_anno2plot,index=None,sep='\t')
    else:
        tcdb_anno.to_csv(tcdb_anno2plot,index=None,sep='\t')
def CARD_anno_plot(card_blast, gene_tpm, result, card_anno2plot,top_k):
    card_blast = pd.read_table(card_blast)
    card_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    card_blast = card_blast[['Gene_ID','Subject', 'Evalue']]
    card_blast=card_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    card_blast = card_blast[['Gene_ID', 'Subject']]
    card_blast['Subject'] = card_blast.apply(lambda x:x['Subject'].split('|',2)[2], axis=1)
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    card_blast['Gene_ID'] = card_blast.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    gene_tpm['Gene_ID'] = gene_tpm.apply(lambda x: process_geneid(x['Gene_ID']),axis=1)
    card_anno = pd.merge(card_blast, gene_tpm, on='Gene_ID', how='left').groupby('Subject',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    card_anno.to_csv(result, index=None, sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(card_anno)>top_k:
        card_anno.head(top_k).to_csv(card_anno2plot,index=None,sep='\t')
    else:
        card_anno.to_csv(card_anno2plot,index=None,sep='\t')
def CARD_anno_plot2(card_blast, gene_tpm, result, card_anno2plot, top_k):
    card_blast = pd.read_table(card_blast)
    card_blast.columns = ['Gene_ID','Subject', 'Identity', 'Align_length', 'Mismatches','Gap_opens', 'Q_start', 'Q_end', 'S_start','S_end', 'Evalue', 'Bit_score']
    card_blast = card_blast[['Gene_ID','Subject', 'Evalue']]
    card_blast=card_blast.sort_values(by=['Gene_ID','Evalue']).drop_duplicates(subset='Gene_ID')
    card_blast = card_blast[['Gene_ID', 'Subject']]
    card_blast['Subject'] = card_blast.apply(lambda x:x['Subject'].split('|',2)[2], axis=1)
    gene_tpm = pd.read_table(gene_tpm)[['Name','TPM']].drop_duplicates()
    gene_tpm.columns = ['Gene_ID','Gene_TPM']
    card_anno = pd.merge(card_blast, gene_tpm, on='Gene_ID', how='left').groupby('Subject',as_index=False).agg('sum').sort_values('Gene_TPM', ascending=False)
    card_anno.to_csv(result, index=None, sep='\t')
    if top_k:
        top_k = int(top_k)
    else:
        top_k = 20
    if len(card_anno)>top_k:
        card_anno.head(top_k).to_csv(card_anno2plot,index=None,sep='\t')
    else:
        card_anno.to_csv(card_anno2plot,index=None,sep='\t')
