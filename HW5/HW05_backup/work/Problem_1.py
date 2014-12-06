import numpy as np
import matplotlib.pyplot as plt
import random
import scipy, scipy.stats
import pymc as pm

p     = pm.Uniform('p', lower=0, upper=1)                    #set dah priah

#Mk1
Mk1_encounters = 26751
Mk1_kills = 183
Mk1_data = [0]*(Mk1_encounters-Mk1_kills) + [1]*Mk1_kills
Mk1_obs   = pm.Bernoulli("obs", p, value=Mk1_data, observed=True)    #set dah datah
Mk1_model = pm.Model([Mk1_obs, p])                                   #set dah modelh
Mk1_mcmc  = pm.MCMC(Mk1_model)
Mk1_mcmc.sample(50000, 30000, 2)
Mk1_samples = Mk1_mcmc.trace("p")[:]

#Mk2
Mk2_encounters = 27079
Mk2_kills = 222
Mk2_data = [0]*(Mk2_encounters-Mk2_kills) + [1]*Mk2_kills
Mk2_obs   = pm.Bernoulli("obs", p, value=Mk2_data, observed=True)    #set dah datah
Mk2_model = pm.Model([Mk2_obs, p])                                   #set dah modelh
Mk2_mcmc  = pm.MCMC(Mk2_model)
Mk2_mcmc.sample(50000, 30000, 2)
Mk2_samples = Mk2_mcmc.trace("p")[:]
differences = Mk2_samples - Mk1_samples
p_value = scipy.stats.percentileofscore(differences,0)

# plt.hist(Mk1_samples, histtype='stepfilled', bins=100, alpha=0.85,
#          label="Mk1", color="#008837", normed=True, edgecolor="none")
#
# plt.hist(Mk2_samples, histtype='stepfilled', bins=100, alpha=0.85,
#          label="Mk2", color="#c2a5cf", normed=True, edgecolor="none")

plt.hist(differences, histtype='stepfilled', bins=100, alpha=0.85,
         label="differences", color="#7b3294", normed=True, edgecolor="none")


plt.xlabel("Mk1 - Mk2 kill rates"); plt.ylabel("Number of samples observed")
plt.title("Comparing Kill Rates")

# plt.xlabel("Kill rates"); plt.ylabel("Number of samples observed")
# plt.title("Mk1 and Mk2 Kill Rate Distributions")

plt.legend(loc="upper right", frameon=False,fontsize=18);

#plt.savefig("Mk1_Vs_Mk2.png")
plt.savefig("differences.png")

print("The 2.5th percentile is")
print(scipy.stats.scoreatpercentile(differences, 2.5))

print("The 97.5th percentile is")
print(scipy.stats.scoreatpercentile(differences, 97.5))

print(p_value)
