#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o4.out
#SBATCH --error=outputs/o4.out
#SBATCH --job-name=maximin.4

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                                     \
    --graph-file data/graphs/g.3.pkl                            \
    --sample-file data/samples/s1000/g.3.samples.pkl   \
    --output-file results/g.3.s.1000.out               \
    --log-file results/g.3.s.1000.log                  \
    --time-limit 39600

source deactivate

