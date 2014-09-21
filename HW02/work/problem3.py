
# # HW2 Problem 3
# ---
# What I am going to do to end up with a "predictability measure" is to take the difference between every successive measure. I.e. |measure_i - measure_i-1|. This will then be plotted. If the plot is flat then it means that the series is predictable. Basic analysis can be run on this new data such as std-dev. 

import numpy as np
import scipy.stats as sp
import pandas as pd
import os 
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    test = bigDataframe.aggregate(np.sum).drop(["week"],1)
    test["disease"] = currentDisease
    return test

def predictabilityIndex(diseaseCounts):
    differenceList = []
    for i in range(len(diseaseCounts) - 1): #len - 1 to avoid running off the end of the list.
        change = abs(diseaseCounts[i] - diseaseCounts[i+1])
        differenceList.append(change)
        
    return differenceList

def findLinearFitLine(changeAmount_list):
    xCoords = range(len(changeAmount_list))
    slope, intercept, rVal, pVal, stdDev = sp.linregress(xCoords, changeAmount_list)
    
    def linearized(x_val):
        y_linear = slope*x_val + intercept 
        return y_linear
    
    linearFitLine = [linearized(x) for x in xCoords]
    
    return rVal, pVal, linearFitLine



plt.rcParams['font.family'] = 'sans-serif'
steelBlue = "#4682b4"
niceRed   = "#ff6347"
allDiseasesByYear = []
fig = plt.figure(figsize=(18,10))
fig.suptitle("Amount of change in disease prevalence", fontsize=18, fontweight='bold')
for i in range(len(diseases)):
    try:
        data = sumByYearOfDisease(diseases[i])
        currentFigure = fig.add_subplot(2,4,i+1)
        diseaseCounts_list = list(data["number"])
        amountOfChange = predictabilityIndex(diseaseCounts_list)
        currentFigure.plot(amountOfChange,niceRed,marker='.')
        # Now that we have the change plotted, move on to the linear fit line: 
        rVal, pVal, linearFitLine = findLinearFitLine(amountOfChange)
        plt.plot(linearFitLine,steelBlue)
        # Some plot cleaning: 
        currentFigure.set_title(diseasesNames[i].capitalize() + " r-val =" + str(round(rVal,3)))
        plt.xticks(rotation=70)
        currentFigure.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: ('%.0f')%(y*1e-3)))
        plt.ylim([0, max(amountOfChange)])
        if i == 0:                               # We only need one axis-label and legend
            plt.ylabel( "Change in number of Infected (in thousands)" )
        if i == 3:
            plt.legend(["Change", "linear fit line"])
        
    except: 
        print "We got errors!"
        print diseases[i]
        
fig.savefig("figures/problem3Output.pdf")





