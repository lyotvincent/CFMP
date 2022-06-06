library(ggplot2)
args <- commandArgs(T)
data = read.table(args[1], header=T, sep="\t")
dorder = factor(as.integer(rownames(data)), labels=data$TERM)
pic <- ggplot(data, aes(x=TERM, y=Gene_TPM, fill=ONTOLOGY))+geom_bar(stat="identity", position=position_dodge(0.7), width=0.5, aes(x=dorder))+coord_flip()+scale_y_log10(breaks=c(1,10,100,1000))+scale_fill_discrete(name="Ontology")+theme(panel.background=element_rect(fill="transparent", colour=NA))+xlab("Terrm")
ggsave(pic, file=args[2],width=12, height=10)

