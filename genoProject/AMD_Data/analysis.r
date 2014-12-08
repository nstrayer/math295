setwd("/Users/Nick/fall14/math295/genoProject/AMD_Data")

#Load the csv generated in cleaning.r
#chr1 = read.csv("genome_chr1.csv")
chr1 = read.csv("genome_full.csv")

SNP_Names = names(chr1)[5:length(chr1)]
head(SNP_Names)
#All is working, now let's loop through this. 

pvals = NULL
for (name in SNP_Names){
  cur_snp = chr1[[name]]
  chi2    = chisq.test(table(cur_snp, chr1$"phenotype"))
  pvals   = c(pvals, chi2$p.value)
}


fileDataframe = data.frame(SNP_Names, -log10(pvals))
names(fileDataframe) = c("SNP", "PVal")

write.csv(fileDataframe, "d3Viz/full_Data.csv")

#write.csv(fileDataframe, "chr1_Data.csv")

plot(-log10(pvals))

