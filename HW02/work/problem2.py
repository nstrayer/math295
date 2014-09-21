# # HW2 Problem 2

import numpy as np
import pandas as pd
import os 
import matplotlib.pyplot as plt
casesFileNames = os.listdir("data/cases") #We're gonna need the names of the files. 


diseases = ["measles", "Whooping+Cough+[pertussis]", "scarlet+fever", 
            "diphtheria", "influenza", "mumps", "rubella", 
            "Chickenpox+[varicella]"]

diseasesNames = ["measles", "Whooping Cough", "scarlet fever", 
                "diphtheria", "influenza", "mumps", "rubella", 
                "Chickenpox"]

def sumByYearOfDisease(currentDisease):
    files = [file for file in casesFileNames if currentDisease in file]
    listOfDataframes = [pd.read_csv("data/cases/" + fileName) for fileName in files]
    bigDataframe = pd.concat(listOfDataframes)
    bigDataframe = bigDataframe.groupby(["year"])
    cleanedDataframe = bigDataframe.aggregate(np.sum).drop(["week"],1)
    cleanedDataframe["disease"] = currentDisease
    return cleanedDataframe


plt.rcParams['font.family'] = 'sans-serif'
steelBlue = "#4682b4"
niceRed   = "#ff6347"
allDiseasesByYear = []
fig = plt.figure(figsize=(18,10))
fig.suptitle("The impact of Diseases in the U.S. (by year)", fontsize=18, fontweight='bold')
for i in range(len(diseases)):
    try:
        data = sumByYearOfDisease(diseases[i])
        currentFigure = fig.add_subplot(2,4,i+1)
        currentFigure.plot([year for year in data.index],[number for number in data["number"]],niceRed,marker='.')
        ax = pd.rolling_mean(data["number"],6).plot(linewidth=4, color=steelBlue)
        ax.set_xlabel("")
        ax.set_xlim([1900,2020])
        if i == 0:                               # We only need one axis-label and legend
            ax.set_ylabel( "Number of Infected" )
        if i == 3:
            plt.legend(["Real Data", "Moving Average"])
        currentFigure.set_title(diseasesNames[i].capitalize())
        plt.xticks(rotation=70)
        allDiseasesByYear.append(data)
    except: 
        print diseases[i]
        
fig.savefig("diseaseCasesByYear.pdf")
