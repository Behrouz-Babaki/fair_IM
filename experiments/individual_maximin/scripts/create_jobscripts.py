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
#SBATCH --job-name=maximin.{job_id}

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                                     \\
    --graph_file data/graphs/g.{graph_id}.pkl                            \\
    --sample_file data/samples/s{sample_size}/g.{graph_id}.samples.pkl   \\
    --output_file results/g.{graph_id}.s.{sample_size}.out               \\
    --log_file results/g.{graph_id}.s.{sample_size}.log                  \\
    --time_limit 39600

source deactivate
'''

mapping = dict()

job_id = 0
for graph_id in range(24):
    job_id += 1
    option = dict()
    option['graph_id'] = graph_id
    option['job_id'] = job_id
    option['sample_size'] = 1000
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
