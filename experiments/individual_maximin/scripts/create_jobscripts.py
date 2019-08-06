#!/usr/bin/env python
# coding: utf-8

import os
import json
from itertools import product


job_str = '''#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o{job_id}.out
#SBATCH --error=outputs/o{job_id}.out
#SBATCH --job-name=mip.{job_id}

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py               \
    data/graphs/g.{graph_id}.pkl                   \
    data/samples/s{sample_size}/g.{graph_id}.pkl   \
    results/g.{graph_id}.s.{sample_size}.out       \
    results/g.{graph_id}.s.{sample_size}.log

source deactivate
'''

mapping = dict()

graph_ids = range(24)
sample_sizes = (100, 1000)

job_id = 0
for sample_size, graph_id in product(sample_sizes, graph_ids):
    job_id += 1
    option = dict()
    option['graph_id'] = graph_id
    option['job_id'] = job_id
    option['sample_size'] = sample_size
    outstr = job_str.format(**option)
    mapping[job_id] = option
    with open('../jobscripts/job%d.sh'%job_id, 'w') as f:
        print(outstr, file=f)

num_jobs = job_id

with open('mapping.json', 'w') as f:
    json.dump(mapping, f)


with open('../submit.sh', 'w') as f:
    print('#!/bin/bash', file=f)
    for i in range(num_jobs):
        job_id = i + 1
        assert(os.path.isfile('../jobscripts/job%d.sh'%job_id))
        print('sbatch jobscripts/job%d.sh'%job_id, file=f)
