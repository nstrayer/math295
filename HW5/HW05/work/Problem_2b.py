# This is the code for problem 2b on homework 5 for Data Science 2
# This script should take a while to run and at the end spit out two files:
# "2b.png" is a plot of the results of the MCMC run. It is four panes of
# distributions respresenting the posteriors of the 4 variables in out model.
# "sigmoid.png" is a plot of the sigmoid that represents model of the rate of
# change.
import matplotlib.pyplot as plt
import numpy as np
import pymc as pm
import collections


data = np.loadtxt("data/txtdata.csv")
n = len(data)

# Build the three prior probability distributions using PyMC objects
alpha = 1.0 / data.mean()

phi_1    = pm.Normal("phi_1", -40, 1.0/5**2, value = 0)
phi_2    = pm.Normal("phi_2",   1.5,1.0/0.6**2, value = 0)
lambda_1 = pm.Exponential("lambda_1", alpha)
lambda_2 = pm.Exponential("lambda_2", alpha)
tau      = pm.DiscreteUniform("tau", lower=0, upper=n)

@pm.deterministic
def lambda_(lambda_1=lambda_1, lambda_2=lambda_2, phi_1=phi_1, phi_2=phi_2):
    out    = np.zeros(n)
    times  = np.arange(1,n+1)* 1.00
    L_1    = lambda_1    #From this rate (Lambda)
    L_2    = lambda_2    #To this rate
    L_D    = L_2 - L_1   #Difference between those rates
    out    = L_D / (1.0 + np.exp( -(phi_1 + phi_2*times) )) + L_1

    return out


#Make a poisson variable for the texting rates
observation = pm.Poisson("obs", lambda_, value=data, observed=True)
#construct the whole model:
model = pm.Model([observation, lambda_1, lambda_2, tau])

mcmc = pm.MCMC(model) #set up MCMC

#Tell it how to work for each side of tau
mcmc.use_step_method(pm.AdaptiveMetropolis, lambda_1)
mcmc.use_step_method(pm.AdaptiveMetropolis, lambda_2)

mcmc.sample(100000, 20000, 2) #actually perform MCMC
lambda_1_samples = mcmc.trace('lambda_1')[:,None]
lambda_2_samples = mcmc.trace('lambda_2')[:,None]
phi_1_samples    = mcmc.trace('phi_1')[:,None]
phi_2_samples    = mcmc.trace('phi_2')[:,None]

ax = plt.subplot(411)
plt.hist(lambda_1_samples, histtype='stepfilled', bins=151, alpha=0.85,
         label="$\lambda_1$", color="#7b3294", normed=True)
plt.legend(loc="upper right", frameon=False,fontsize=18);
plt.title(r"Posterior distributions", fontsize=22);
plt.xlim([15, 30])
plt.xlabel("$\lambda_1$ value");

ax = plt.subplot(412)
plt.hist(lambda_2_samples, histtype='stepfilled', bins=151, alpha=0.85,
         label="$\lambda_2$", color="#a6dba0", normed=True)
plt.legend(loc="upper right", frameon=False,fontsize=18);
plt.xlim([15, 30])
plt.xlabel("$\lambda_2$ value", fontsize=14);
plt.ylabel("Probability");

ax = plt.subplot(413)
plt.hist(phi_1_samples, histtype='stepfilled', bins=151, alpha=0.85,
         label="$\phi_1$", color="#c2a5cf", normed=True)
plt.legend(loc="upper right", frameon=False,fontsize=18);
#plt.xlim([15, 30])
plt.xlabel("$\phi_1$ value", fontsize=14);
plt.ylabel("Probability");

ax = plt.subplot(414)
plt.hist(phi_2_samples, histtype='stepfilled', bins=151, alpha=0.85,
         label="$\phi_2$", color="#008837", normed=True)
plt.legend(loc="upper right", frameon=False,fontsize=18);
#plt.xlim([15, 30])
plt.xlabel("$\phi_2$ value", fontsize=14);
plt.ylabel("Probability");


plt.legend(loc="upper right", frameon=False,fontsize=18);

plt.savefig("2b.png")


from scipy.stats.mstats import mquantiles

def logistic(x,lambda_1,lambda_2,phi2,phi1=0): #redefine the logistic model for plotting of the curve
    p = 1.0/(1.0 + np.exp(-(np.dot(phi2,x)+phi1)))
    return (lambda_2-lambda_1)*p + lambda_1

t   = np.linspace(0, 74,150)[:,None]
p_t = logistic(t.T, lambda_1_samples,lambda_2_samples, phi_2_samples, phi_1_samples)

mean_prob_t = p_t.mean(axis=0)

qs = mquantiles(p_t, [0.025, 0.975], axis=0)

plt.figure(2)
plt.fill_between(t[:,0],*qs, alpha = 0.7, color = "#7A68A6")
plt.plot(t[:,0], qs[0], label="95% CI", color = "#7A68A6", alpha = 0.7)
plt.plot(t, mean_prob_t,lw=1, ls='--', color = "k", label = 'average posterior \n num texts')
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.xlabel('day', fontsize = 16)
plt.ylabel('number of texts', fontsize = 18)
plt.xlim(0,74)
#plt.scatter(np.arange(n), data, color="#00dd2f")
plt.title('Message Rate by Day',fontsize = 18)
plt.savefig("sigmoid.png")
