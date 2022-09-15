#!/usr/bin/env Rscript

library("edgeR")
library(ggplot2)
library(reshape2)
library(RColorBrewer)
library(plotly)
library(htmlwidgets)

theme_set(
  theme_classic() +
    theme(legend.position = "top")
  )

selectGenes <- function(counts, min.samples, min.count=10){
  
 	
  lib.size <- colSums(counts)
  MedianLibSize <- median(lib.size)
  CPM.Cutoff <- min.count / MedianLibSize*1e6
  CPM <- edgeR::cpm(counts,lib.size=lib.size)
  CPM
  #min.samples <- round(N * ncol(counts))
 
  f1 <- genefilter::kOverA(min.samples, CPM.Cutoff)
  flist <- genefilter::filterfun(f1)
  keep <- genefilter::genefilter(CPM, flist)
 
  ## the same as:
  #keep <- apply(CPM, 1, function(x, n = min.samples){
  #  t = sum(x >= CPM.Cutoff) >= n
  #  t
  #})
 
  return(keep)
}


args = commandArgs(trailingOnly=TRUE)
length(args)
if (length(args)==0){
  input="/home/user/testInput"
  output="/home/user/testOutput"
  norma="TMM"
  sampcount=4
  numsamp=5
  selectNumb=30
}

itera=seq(1,length(args))
print(args)
print(itera)
skip=F
for (i in itera){
	if (skip){
		skip=F
		next}
	cat(args[i], args[i+1],"\n")
	
	if (args[i]=="--input" || args[i]=="-i"){
		input <- as.character(args[i+1])
		skip=T}
		
	else if (args[i]=="--output" || args[i]=="-o"){
		output <- as.character(args[i+1])
		skip=T}
		
	else if (args[i]=="--normalization" || args[i]=="-n"){
		norma <- as.character(args[i+1])
		skip=T}
		
	else if (args[i]=="--sampcount" || args[i]=="-c"){
		sampcount <- as.integer(args[i+1])
		skip=T}
		
	else if (args[i]=="--numsamp" || args[i]=="-s"){
		numsamp <- as.integer(args[i+1])
		skip=T}
	
	else if (args[i]=="--topcount" || args[i]=="-t"){
	  selectNumb <- as.integer(args[i+1])
	  skip=T}
		
	else {
		cat(paste("\nError, the argument (", args[i], ") don't exist in the script edgeR.R\n\n", sep=""))
		stopifnot(F)}
}



#### Create EdgeR data ####
cat("\n\n### Create EdgeR data ###\n")
data <- read.table(input, header=TRUE, skip=2)
group <- read.table(input, skip=0, nrows=1)
cols <-seq(7,ncol(data),1)
x <- data.frame(data[1:(dim(data)[1]),cols])
row.names(x) <- data$Geneid
idx <- which(rowSums(x)==0)
d <- DGEList(counts=x ,group=factor(group))
row.names(d$counts) <- data$featureID
head(x)
head(data)
group
d

#### Filter low count reads ####
cat("\n\n### Filter low count reads ###\n")

cat("Number of different transcript identified with the mapping of RNA-seq of all", dim(d)[2], "samples:\t",dim(d)[1],"\n")
#dim(d)[1]
cat("Samples with associated group, number of mapped reads (lib.size), and the factor of normalisation:\n")
d$samples
#png(paste(output,"/librarySize_preFLEG.png",sep=""))
#par(oma=c(6,0,0,0))
#barplot(d$samples$lib.size, names=colnames(d), las=2)
#dev.off()


gd <- ggplot(d$samples, aes(x=colnames(d), y=d$samples$lib.size, fill=d$samples$group))
gd <- gd + geom_col()+labs(x="", y="Library Size", fill="group") +
  geom_text(aes(label = d$samples$lib.size), hjust = 1.2, color = "white", angle=90) +
  theme(axis.text.x = element_text(angle=45, hjust=1, vjust=0.9))
ggsave(paste(output,"/librarySize_preFLEG.png",sep=""),gd, height= 5, width=  5, dpi=1200)

#keepd <- rowSums(cpm(d)>sampcount)>=numsamp
keepd <- selectGenes(d$counts, min.samples=numsamp, min.count=sampcount)
d <- d[keepd,]
cat("Number of different transcript identified with the mapping of RNA-seq of all", dim(d)[2], "samples:\t",dim(d)[1],"\n")
dim(d)
d$samples$lib.size <- colSums(d$counts)
d$sample

gd <- ggplot(d$samples, aes(x=colnames(d), y=d$samples$lib.size, fill=d$samples$group))
gd <- gd + geom_col()+labs(x="", y="Library Size", fill="group") +
  geom_text(aes(label = d$samples$lib.size), hjust = 1.2, color = "white", angle=90) +
  theme(axis.text.x = element_text(angle=45, hjust=1, vjust=0.9))
ggsave(paste(output,"/librarySize_postFLEG.png",sep=""),gd, height= 5, width=  5, dpi=1200)


#### Multi-Dimensionnal Scaling ####
cat("\n\n### Multi-Dimensionnal Scaling ###\n")
d<- calcNormFactors(d, method=norma)
#d
head(d, 10)

distance <- dist(t(d$counts))
distance
fit <- cmdscale(distance,eig=TRUE, k=2)
fit
fitPoint <- as.data.frame(fit$points)
fitPoint <- merge(fitPoint, d$samples, by=0)
row.names(fitPoint) <- fitPoint$Row.names
subset(fitPoint, select=-c(Row.names))
write.csv(fitPoint, paste(output,'MultiDimScaling.csv',sep="/"))


perc_var=fit$eig/sum(fit$eig)*100
perc_var
length(perc_var)
dimName <- paste("D", seq(length(perc_var)), sep="")
dimFrame <- data.frame(dim=dimName,eig=perc_var)
eigP <- ggplot(dimFrame, aes(x=factor(dim, level=dim) , y=eig))
eigP <- eigP+geom_col(fill="springgreen3",color="springgreen3")+ labs(x="MDS Dimensions", y="Percentage of variance (%)")+ geom_text(aes(label = paste(round(perc_var,2), "%", sep="")), vjust = -1, color = "gray18")
ggsave(paste(output,"/variance_func_dimension.png",sep=""),eigP, height= 7, width=  7, dpi=1200)




#### Estimate Dispersion ####
cat("\n\n### Estimate Dispersion ###\n")
d <- estimateCommonDisp(d, verbose=T)
names(d)

d <- estimateTagwiseDisp(d)
names(d)
head(d, 10)
png(paste(output, "/Dispersion.png", sep=""),width=7, height=7, units="in", res=1200)
plotBCV(d)
dev.off()



png(paste(output, "/Heatmap.png", sep=""),width=7, height=7, units="in", res=1200)
par(oma=c(6,0,0,0))
matrixd = d$pseudo.counts
head(matrixd)
coul <- colorRampPalette(brewer.pal(3, "YlOrRd"))(7)
heatmap(matrixd, col=coul, labRow= FALSE)
dev.off()

png(paste(output, "/DispersionGLM.png", sep=""),width=7, height=7, units="in", res=1200)
design.mat <- model.matrix(~ 0 + d$samples$group)
colnames(design.mat) <- levels(d$samples$group)
dglm <- estimateGLMCommonDisp(d,design.mat)
dglm <- estimateGLMTrendedDisp(dglm,design.mat, method="power")
dglm <- estimateGLMTagwiseDisp(dglm,design.mat)
plotBCV(dglm)
dev.off()

png(paste(output, "/HeatmapGLM.png", sep=""),width=7, height=7, units="in", res=1200)
par(oma=c(6,0,0,0))
matrixDglm = d$pseudo.counts
head(matrixDglm)
heatmap(matrixDglm, col=coul, labRow= FALSE)
dev.off()

head(d$pseudo.counts)
head(dglm$pseudo.counts)
#head(d, 10)
#head(dglm, 10)

#### Differential Expression ####
cat("\n\n### Differential Expression ###\n")
head(d, 10)
result <- exactTest(d)
cat("\n Top Tags:\n")
topTags(result, n=10)
diex <- decideTestsDGE(result, adjust.method="BH", p.value=0.5)
summary(diex)
head(result$table)
result[[1]]["33905_00045",]
result
diex


png(paste(output, "/Fold_func.png", sep=""),width=7, height=7, units="in", res=1200)
FCtags <- rownames(d)[as.logical(diex)]
FCtags
plotSmear(result, de.tags=FCtags)
abline(h = c(-2, 2), col = "blue")
dev.off()
FCresult=result$table[FCtags,]
write.table(FCresult, file=paste(output,'/FoldChange.tsv',sep=""), sep="\t")

selectNumb
if (selectNumb>nrow(FCresult)){
  selectNumb=nrow(FCresult)
}
head(d, 20)
selectD <- d$pseudo.counts[order(FCresult$logFC),][1:selectNumb,]
selectD

selectMatrixD = as.matrix(selectD)
png(paste(output, "/SelectedHeatmap.png", sep=""),width=7, height=7, units="in", res=1200)
par(oma=c(6,0,0,0))
heatmap(selectMatrixD, col=coul)
dev.off()

cat("\n\n")
design.mat
dglm$trended.dispersion
resultglm <- glmFit(dglm, design.mat)
resultglm <- glmLRT(resultglm, contrast=c(1,-1))
topTags(resultglm, n=15)
topTags(resultglm)
deresultglm <- decideTestsDGE(resultglm, adjust.method="BH", p.value = 0.05)
summary(deresultglm)
rownames(dglm)
as.logical(deresultglm)
rownames(resultglm)[as.logical(deresultglm)]
typeof(resultglm$table)

FCglmTags <- rownames(dglm)[as.logical(deresultglm)]
FCglmTags
png(paste(output, "/Fold_funcGLM.png", sep=""),width=7, height=7, units="in", res=1200)
plotSmear(resultglm, de.tags=FCglmTags)
abline(h = c(-2, 2), col = "blue")
dev.off()
FCresultGLM=resultglm$table[FCglmTags,]
FCresultGLM
write.table(FCresultGLM, file=paste(output,'/FoldChangeGLM.tsv',sep=""), sep="\t")

cat("\n\n\n\n")
if (selectNumb>nrow(FCresultGLM)){
  selectNumb=nrow(FCresultGLM)
}
head(dglm, 20)
selectDglm <- dglm$pseudo.counts[order(FCresultGLM$logFC),][1:selectNumb,]
selectDglm

selectMatrixDglm = as.matrix(selectDglm)
png(paste(output, "/SelectedHeatmapGLM.png", sep=""),width=7, height=7, units="in", res=1200)
par(oma=c(6,0,0,0))
heatmap(selectMatrixDglm, col=coul)
dev.off()

