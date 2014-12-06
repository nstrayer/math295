setwd("/Users/Nick/fall14/math295/genoProject/AMD_Data")
chrom1_raw  = data.frame(read.table("amd.out_.ped"))      #The whole genome
#chrom1_raw  = data.frame(read.table("amd_chr1.out.ped")) #Just chromosome 1

#Let's break up the object into the conditions and the SNPs
SNPs = chrom1_raw[,7:length(chrom1_raw)]

#---------------------------------------------------------------------------------------------------------
# Exploration of r replace functions using runtime analysis
# There are some weird values where T alleles are represented as TRUE. This fixes that. 
#---------------------------------------------------------------------------------------------------------
#SNPs[SNPs == TRUE] = "T" 
#This code is increadibly slow. There must be a faster way, 16x10^6 datapoints isn't even that large
#Let's do some runtime analysis courtesy of the beautiful system.time() function. 

#Attempt number 1: 
firstReplace = function(dataFrame, find, replaceWith){
  dataFrame[dataFrame == find] = replaceWith
  return(dataFrame)
}
first_method = system.time( firstReplace(SNPs, TRUE, "T" ))
# user  system elapsed 
# 422.609 114.023 544.427 Oh gosh, let's not do that. 

#Attempt number 2: 
lapply_method = system.time(as.data.frame(lapply  (SNPs, function(x){replace(x, x = TRUE,"T")}) ))
#This one doesn't work at all. Oh well.

#R seems to have much better algorithms in place for dealing with matrices, so let's utilize them. 
#Attempt number 3: 
fastReplace = function(dataFrame, find, replaceWith){
  temp_matrix = as.matrix(dataFrame)
  temp_matrix[temp_matrix == find] = replaceWith
  return(as.data.frame(temp_matrix))
}
makeMatrix_method = system.time(fastReplace(SNPs, TRUE, "T" ))
# user  system elapsed 
# 51.642   0.758  52.977 That's better. 

#Using the third method
SNPs = fastReplace(SNPs, TRUE, "T" )

#---------------------------------------------------------------------------------------------------------
# More cleaning
# Looking at the data we see that we have a single letter (e.g. "C" or "G") in each slot. This is not how 
# the data should be. Each letter resprsents an allele and two alleles make a genotype, so let's merge the
# successive columns into their respective genotypes...
#---------------------------------------------------------------------------------------------------------

#make a holder for merged snps
combinedSnps = matrix(0,146,length(SNPs)/2)
#                       146 individuals were sequenced

#Counter for walking through the new matrix holder in the upcoming loop. 
place = 1 

#To the loops!
for (i in seq(1,length(SNPs),2)){
  combinedSnps[,place] = paste(SNPs[,i], SNPs[,i+1],sep = "")
  place = place + 1
}

#Assemble the data into a big and clean(er) dataframe
chrom1 = cbind(  chrom1_raw[,0:6]   ,   data.frame(combinedSnps)) 
#                non-genotype cols           cleaned cols

#---------------------------------------------------------------------------------------------------------
# Variable labeling:
# So the data is getting to look pretty nice. However we can quickly notice something, the column titles
# are basically giberish. Luckly the format that this data came to us from is rather standard and we can 
# fix this. 
#---------------------------------------------------------------------------------------------------------

#quickly let's check what we have so far: 
chrom1[1:5,1:20]

#... V5 V6 X1 X2 ... ew, Let's fix this. 

#These are standard for .ped files. 
names(chrom1)[0:6] = c("family_ID", "individual_ID", "father_ID", "mother_ID", "sex", "phenotype") 

#We can throw out the family_ID as it is simply sequential, in addition mother and father id values as they are all simply zeros. 
chrom1 = chrom1[,!(names(chrom1) %in% c("family_ID", "mother_ID", "father_ID"))]

#The columns of .map files are chromosome, marker ID, genetic location and physical location. We are only interested in marker ID.
#Because R likes to give weird datatypes when selecting out of a dataframe we have to specifiy we want this in a vector of strings.
SNP_Names = as.character(read.table("amd.out_.map")[,2])      #Whole genome
#SNP_Names = as.character(read.table("amd_chr1.out.map")[,2]) #First chromosome

#Now that we have the names let's put them into the SNP column names of the big dataframe:
names(chrom1)[4:length(chrom1)] = SNP_Names

#What does it look like now?: 
chrom1[1:5,1:10]
#nice. 

rm(SNP_Names,SNPs,combinedSnps,chrom1_raw,i, place) #Some quick housecleaning. 

#---------------------------------------------------------------------------------------------------------
# Making sense of what we have:
# We have a pretty clean(ish) looking dataset now. But what do the different columns actually mean?
#---------------------------------------------------------------------------------------------------------
#focusing on one individual. 
chrom1[1,1:10]
#    individual_ID sex phenotype rs950122 rs1496555 rs1338382 rs10492936 rs10489589 rs10489588 rs1109251
# 1      55113000    1         2       CG        GG        TT         GG         CC         AA        AA
#ID is self explanatory, what are sex and phenotype though? 

chrom1[1:10,"sex"]
#So we have variables 1 and 2 here. Looking at the paper we see that 1 = male, 2 = female. Good to know. 

chrom1[10:20,"phenotype"]
#Lots of 1s and 2s again here. Turns out 2 is case(has macular degeneration), 1 is control(doesnt). 
#This is rather un-intuitive. 

chrom1$phenotype = chrom1$phenotype == 2 #2/case is TRUE
chrom1[10:20,"phenotype"]
#[1]  TRUE  TRUE  TRUE  TRUE  TRUE  TRUE FALSE  TRUE  TRUE  TRUE  TRUE 
# Sweet looks good to me. 

#---------------------------------------------------------------------------------------------------------
# Missing data!:
# Different sequencing technologies, or processing software report missing data in different ways. This is
# annoying, but what is data science without some more cleaning? 
# R uses NA for missing data, let's make sure this data works like that. 
#---------------------------------------------------------------------------------------------------------

#By scanning through a couple of SNPs and running summarys we find that our data has 00 for it's missing values:
summary(chrom1$rs2455122)
# 00  CC  GC  GG 
#  1 115  28   2 

#Well that wont do. Let's use our fast replace function to fix all of these points. 
chrom1 = fastReplace(chrom1, "00", NA )

#So fast, let's check and see if it worked:
#  CC   GC   GG NA's 
# 115   28    2    1 
#Nice. 

