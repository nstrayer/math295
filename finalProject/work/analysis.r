setwd("/Users/Nick/fall14/math295/finalProject/data")

#Load the csv generated in cleaning.r
chr1 = read.csv("genome_chr1.csv")
#chr1 = read.csv("genome_full.csv")

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

#write.csv(fileDataframe, "../d3Viz/full_Data.csv")

write.csv(fileDataframe, "../d3Viz/chr1_Data.csv")

plot(-log10(pvals))

#What is that weird line doing there? 
#Let's see if we can figure it out.
#Going into the interactive plotter we can see that all of those SNPs have a pvalue of ~1.4067e-4
#A randomly chosen one is rs10494429

weirdSNP = chr1$"rs10494429"
summary(weirdSNP)
# AA 
# 146 Hmm, where are the other genotypes. Let's look at a few more. 

#rs10489304
summary(chr1$"rs10489304")
# TT 
# 146 Looks like a trend to me. Let's exclude all of the SNPs with only a single genotype and see what the 
# Plot looks like. 

#Let's make a function to make our lives easier later on.

makeData = function(genoData){
  SNP_Names = names(genoData)[5:length(genoData)]
  pvals     = NULL
  usedSnps  = NULL #We're not using all of the SNPs this time so we need to make a list of used SNPs for plotting.
  
  for (name in SNP_Names){
    cur_snp = factor(genoData[[name]]) #Factor needs to be added here for when we split by gender. R remembers that it had a particular
                                       #genotype and include it in the summary table even if you removed it from the vector, factor fixes this.
    if (length(unique(cur_snp)) > 2){
      chi2     = chisq.test(table(cur_snp, genoData$"phenotype"))
      pvals    = c(pvals, chi2$p.value)
      usedSnps = c(usedSnps, name)
    }
  }
  fileDataframe = data.frame(usedSnps, -log10(pvals))
  names(fileDataframe) = c("SNP", "PVal")
  return(fileDataframe)
}

fixed_chr1 = makeData(chr1)

#Fix this to be length of resulting df.
#print(length(SNP_Names) - length(usedSnps))
# [1] 659 cool cool. 

#make a file:
write.csv(fixed_chr1, "../d3Viz/fixed_chr1_Data.csv")
#To the interactive plotter!


#Let's check for gender biases. The paper did not do this:

males   = makeData(chr1[chr1$sex == 1,])
write.csv(males, "../d3Viz/males_Data.csv")

#It didn't work, oh no. What is going on? There are some NA's. Upon inspection its for SNPs that are monogenomic for a gender. Add a factor
#command to the makeData function to deal with this. It would be interesting to look at how many snps are monogenomic by gender. 

#ahh now it's working: 
#rs6719 and rs1329428 seem to be male oriented, but not really that much at all. 

females = makeData(chr1[chr1$sex == 2,])
write.csv(females, "../d3Viz/females_Data.csv")

#rs1418632, rs4845835 seem to be heavily female oriented. This is interesting. Also seem to be in LD, test. rs342818 as well but not ld

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# One of the main benefits of using D3 is to help rapidly visualize differences between datasets using animations. This cuts down on the amount of conveluted loops
# and other coding you have to do and allows for a more phisical understanding of data. Just like the datasets that all have the same values but different shapes. 
# The problem is browsers can't handle transitions on 9k+ points, and even if it could we would have a very hard time parsing it ourselves. Because of this I want to 
# make a function that will take the big ouput from my makeData function and bring it down to the largest say, 100 x^2 values. This then when put into the 
# visualization will allow the user to quickly visualize which SNPs have differeing results by the stratifications. 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

makeSmaller = function(dataset, size){
  values = sort(dataset$PVal)
  cutoff = values[length(values) - size]
  
  newSnps  = NULL
  newPVals = NULL
  
  for (i in 1:length(values)){
    if (dataset[i,]$PVal > cutoff){
      newSnps  = c(newSnps,  toString(dataset[i,][["SNP"]])) #Why oh why does it take this to just get the string out of the dataframe?
      newPVals = c(newPVals, dataset[i,]$PVal)
    }
  }
  smallerData = data.frame(newSnps, newPVals)
  names(smallerData) = c("SNP", "PVal")
  return(smallerData)
}

males_small = makeSmaller(males,100)
write.csv(males_small, "../d3Viz/males_small_Data.csv")
#good it's working. 

females_small = makeSmaller(females,100)
write.csv(females_small, "../d3Viz/females_small_Data.csv")

#Going to the d3 viz and typing in the file names and boom, works like a charm. 
#Now that we have a list of some interesting looking SNPs let's dive further in and look at LD.



