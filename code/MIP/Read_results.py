#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


labels = ['gender']#, 'age', 'ethnicity', 'region']
methods = ['celf', 'imm', 'simpath', 'tim', 'mip/base1000', 'fairmip/fairseed/base100','fairgap/random','fairgap/greedy','fairgap/Gonzalez','fairgap/naive-myopic','fairgap/myopic', 'fairmip/maxmin/base100', 'fairim/maximin','fairim/dc','fairmip/mean/base100']
coverage = []
coverage_std = []
gini = []
gini_std = []
kld_m = []
kld_m_std = []
kld_f = []
kld_f_std = []
for label in labels:
    for method in methods:
        result = pd.read_csv('/Users/golnoosh/Projects/Golnoosh/Fair_IM/Git/influence_maximization/experiments/im500/results/evaluator/'+label+'/'+method+'.txt', sep = '\t')
        coverage.append(np.mean(result['Coverage_all']))
        coverage_std.append(np.std(result['Coverage_all']))
        gini.append(np.mean(result['Gini_all']))
        gini_std.append(np.std(result['Gini_all']))
        kld_m.append(np.mean(result['KLD_male']))
        kld_m_std.append(np.std(result['KLD_male']))
        kld_f.append(np.mean(result['KLD_female']))
        kld_f_std.append(np.std(result['KLD_female']))
    


# In[3]:


result


# In[4]:


import matplotlib
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
plt.xticks(rotation=90)
plt.bar(methods[0:5], coverage[0:5])


# In[5]:


fig, ax = plt.subplots()
ax.bar(methods, coverage, yerr=coverage_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Coverage')
ax.set_xticks(methods)
plt.xticks(rotation=90)


#ax.set_xlabel('IM methods')
ax.set_title('Gender')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()


# In[6]:


cost = [1-(x / coverage[0]) for x in coverage]
fig, ax = plt.subplots()
ax.bar(methods, cost, yerr=coverage_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Cost of Fairness')
ax.set_xticks(methods)
plt.xticks(rotation=90)

#ax.set_xlabel('IM methods')
ax.set_title('Gender')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()


# In[7]:


fig, ax = plt.subplots()
ax.bar(methods, gini, yerr=gini_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Gini index')
ax.set_xticks(methods)
plt.xticks(rotation=90)
#ax.set_xlabel('IM methods')
ax.set_title('Gender')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()


# In[8]:


fig, ax = plt.subplots()
ax.bar(methods, kld_f, yerr=kld_f_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('KLD female')
ax.set_xticks(methods)
plt.xticks(rotation=90)

#ax.set_xlabel('IM methods')
ax.set_title('Gender')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()


# In[9]:


fig, ax = plt.subplots()
ax.bar(methods, kld_m, yerr=kld_m_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('KLD male')
ax.set_xticks(methods)
plt.xticks(rotation=90)
#ax.set_xlabel('IM methods')
ax.set_title('Gender')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()

