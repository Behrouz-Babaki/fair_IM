#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import product
import os
import json


# In[2]:


job_str = '''#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:40:00
#SBATCH --output=out/o{job_id}.out
#SBATCH --error=out/o{job_id}.out
#SBATCH --job-name=mip.{job_id}

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_MIP.py"
OUTPUTDIR="./results/output"
LOGDIR="./results/log"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER {n_samples} $NETWORKDIR/graph_spa_500_{graph_index}.pickle $OUTPUTDIR/sample_{n_samples}/run_{run_id}/output_{graph_index}.txt $LOGDIR/sample_{n_samples}/run_{run_id}/log_{graph_index}.txt
source deactivate
'''


# In[3]:


graph_index_options = range(20)
run_id_options = range(10)
n_samples_options = [10,100,1000,10000]


# In[4]:


mapping = dict()

job_id = 0
for graph_index, run_id, n_samples in product(graph_index_options, run_id_options, n_samples_options):
    job_id += 1
    option = dict()
    option['graph_index'] = graph_index
    option['job_id'] = job_id
    option['run_id'] = run_id
    option['n_samples'] = n_samples
    outstr = job_str.format(**option)
    mapping[job_id] = option
    with open('../jobscripts/job%d.sh'%job_id, 'w') as f:
        print(outstr, file=f)

num_jobs = job_id

with open('mapping.json', 'w') as f:
    json.dump(mapping, f)


# In[5]:


with open('../submit.sh', 'w') as f:
    print('#!/bin/bash', file=f)
    for i in range(num_jobs):
        job_id = i + 1
        assert(os.path.isfile('../jobscripts/job%d.sh'%job_id))
        print('sbatch jobscripts/job%d.sh'%job_id, file=f)
        

