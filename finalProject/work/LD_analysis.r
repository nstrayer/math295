#This script will take the interesting SNPs generated in analysis.r and investigates them further using Linkage Disequilibrium. 
#This is a measure of how likely two SNPs are to change with eachother in different subjects. 
#Coding inspiration for this comes from Professor Richard Singles Lesson on LD: http://www.uvm.edu/~rsingle/stat295/F14/notes/LD-intro2b.R

#Some administrative stuff. 
library(genetics)
setwd("/Users/Nick/fall14/math295/finalProject/data")

#Load the csv generated in cleaning.r
chr1 = read.csv("genome_chr1.csv")

#We're going to attach the dataframe to ease the process of dealing with it, make sure that your global env is clear before doing this to avoid potential contamination. 
attach(chr1)
#this allows the columns of the dataframe to be called without prefacing chr1: e.g.
head(rs380390)
# [1] GG CG GG GG CG GG
# Levels: CC CG GG

#So out interesting SNPs are: rs380390, rs1329428, rs6719, rs1329428, rs342818, rs1418632, rs4845835 

#Significant from the overall run
SNP1 = genotype(rs380390,sep="")   
SNP2 = genotype(rs1329428,sep="")

#Most significant from males
SNP3 = genotype(rs6719,sep="")
SNP4 = genotype(rs1329428,sep="")

#Most significant from females
SNP5 = genotype(rs342818,sep="")
SNP6 = genotype(rs1418632,sep="")
SNP7 = genotype(rs4845835,sep="")

LD(SNP1,SNP2)$"P-value"
# [1] 0 Hmm, so those two SNPs are in heavy LD. This makes sense as they are close to eachother on the genome. This basically means that most likely only one, or more realistically, a SNP
# near them is actually causing the behavior. Good to know. This could be tedious to do all of these combinations. if only there was a better way! Oh, there is. 

#LD Heatmap!!!

#install.packages("LDheatmap")      #UNCOMMENT BEFORE THE FIRST CALL
library(LDheatmap)
All_SNPs = data.frame(SNP1, SNP2, SNP3, SNP4, SNP5, SNP6, SNP7)
Labels = names(All_SNPs)
pdf("../figures/LDHeatmap.pdf")
LDheatmap(All_SNPs, LDmeasure="r", color=heat.colors(20), add.map=F, SNP.name=Labels)
dev.off()
#Note: Make sure to breifly discuss the differences in LD measures and give the equation for D'

#From this we can see that SNP 5 and 3 are very interesting and not in LD strongly with any other SNPs. 
#Let's look at them. 

SNP3_info = summary(SNP3)
SNP5_info = summary(SNP5)

pdf("../figures/distributionPlots.pdf")
par(mfrow=c(2,2))
barplot(SNP3_info$allele.freq[,1], main = "rs6719", xlab = "Alleles") #Bar plot of allele distribution
barplot(SNP5_info$allele.freq[,1], main = "rs342818", xlab = "Alleles") 

barplot(SNP3_info$genotype.freq[,1], xlab = "Genotypes") #genotype distribution 
barplot(SNP5_info$genotype.freq[,1], xlab = "Genotypes") 
dev.off()
