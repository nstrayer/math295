import matplotlib.pyplot as plt
import numpy as np
import pymc as pm
import collections


data = np.loadtxt("data/txtdata.csv")
n = len(data)

plt.bar(np.arange(n), data, color="#00dd2f", ec='none')
plt.xlabel("Day")
plt.ylabel("Number of texts received")
plt.title("Texts received over time.")
plt.xlim(0, n);

plt.savefig("texts_recieved.png")

# Build the three prior probability distributions
# using PyMC objects
alpha = 1.0 / data.mean()

phi_1    = pm.Uniform("phi_1",-100, 0)
phi_2    = pm.Uniform("phi_2",   0,20)
lambda_1 = pm.Exponential("lambda_1", alpha)
lambda_2 = pm.Exponential("lambda_2", alpha)

tau = pm.DiscreteUniform("tau", lower=0, upper=n)

#a function that is given our split point(tau) and returns a vector out of lambdas on either side of it.
@pm.deterministic
def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
    out = np.zeros(n)
    out[:tau] = lambda_1  # lambda before tau is lambda1
    out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
    return out

#Make a poisson variable for the texting rates
observation = pm.Poisson("obs", lambda_, value=data, observed=True)
#construct the whole model:
model = pm.Model([observation, lambda_1, lambda_2, tau])

mcmc = pm.MCMC(model) #set up MCMC

#Tell it how to work for each side of tau
mcmc.use_step_method(pm.Metropolis, lambda_1)
mcmc.use_step_method(pm.Metropolis, lambda_2)

mcmc.sample(100000, 30000, 2) #actually perform MCMC, first we will do 10,000 samples, removing first 1000
lambda_1_samples = mcmc.trace('lambda_1')[:]
lambda_2_samples = mcmc.trace('lambda_2')[:]
tau_samples      = mcmc.trace('tau')[:]


#Lambda1 plot
ax = plt.subplot(311)
plt.hist(lambda_1_samples, histtype='stepfilled', bins=151, alpha=0.85,
         label="posterior of $\lambda_1$", color="#A60628", normed=True)
plt.legend(loc="upper right", frameon=False);
plt.title(r"Posterior distributions of the parameters", fontsize=18);
plt.xlim([15, 30])
plt.xlabel("$\lambda_1$ value");

#Lambda2 plot
ax = plt.subplot(312)
#ax.set_autoscaley_on(False)
plt.hist(lambda_2_samples, histtype='stepfilled', bins=151, alpha=0.85,
         label="posterior of $\lambda_2$", color="#7A68A6", normed=True)
plt.legend(loc="upper right", frameon=False);
plt.xlim([15, 30])
plt.xlabel("$\lambda_2$ value", fontsize=14);
plt.ylabel("Probability");

#Tau plot
plt.subplot(313)
T,Nt = zip(*sorted( collections.Counter(tau_samples).items() ))
T = [t-0.4 for t in T] # shift bar locations
Pt = [1.0*n/sum(Nt) for n in Nt]
plt.bar(T,Pt, color="#00dd2f", label=r"posterior of $\tau$");
plt.xticks(np.arange(n));

plt.legend(loc="upper right", frameon=False);
plt.ylim([0, .75]);
plt.xlim([35, len(data) - 20]);
plt.xlabel(r"$\tau$ (in days)");

plt.savefig("bigPlot.png")
