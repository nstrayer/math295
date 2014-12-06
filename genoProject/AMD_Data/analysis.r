setwd("/Users/Nick/fall14/math295/genoProject/AMD_Data")
chrom1_raw  = data.frame(read.table("amd_chr1.out.ped"))

#Let's break up the object into the conditions and the SNPs
SNPs = chrom1_raw[,7:length(chrom1_raw)]
SNPs[SNPs == TRUE] = "T" #There are some weird values where T alleles are represented as TRUE. This fixes that. 

place = 1
combinedSnps = matrix(0,146,length(SNPs)/2)
for (i in seq(1,length(SNPs),2)){
  combinedSnps[,place] = paste(SNPs[,i], SNPs[,i+1],sep = "")
  place = place + 1
}

#Assemble the data into a big and clean(er) dataframe
chrom1 = cbind(chrom1_raw[,0:6],data.frame(combinedSnps)) 

#These are standard for sequencing data
names(chrom1)[0:6] = c("family_ID", "individual_ID", "father_ID", "mother_ID", "sex", "phenotype") 

#We can throw out the family_ID as it is simply sequential, in addition mother and father id values as they are all simply zeros. 
chrom1 = chrom1[,!(names(chrom1) %in% c("family_ID", "mother_ID", "father_ID"))]

#The form of .map files is chromosome, marker ID, genetic location and physical location. We are only interested in marker ID
#Because R likes to give weird datatypes when selecting out of a dataframe we have to specifiy we want this in a vector of strings.
SNP_Names = as.character(read.table("amd_chr1.out.map")[,2])

#Now that we have the names let's put them into the SNP column names of the big dataframe:
names(chrom1)[4:length(chrom1)] = SNP_Names

rm(SNP_Names,SNPs,combinedSnps,chrom1_raw) #Do some housecleaning. 

#Let's change the phenotype column to true if they are a case (2), false if they are a control(1)
chrom1$phenotype = chrom1$phenotype == 2

#Currently the missing data is represented as 00, this is not great for R, let's change it to NA.
chrom1[chrom1 == "00"] = NA
#It should be noted that 00 will remain a factor for the r objects, something that potentially will be problematic later.
