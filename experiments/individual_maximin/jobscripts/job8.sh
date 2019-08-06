#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o8.out
#SBATCH --error=outputs/o8.out
#SBATCH --job-name=mip.8

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                 data/graphs/g.7.pkl                     data/samples/s1000/g.7.samples.pkl      results/g.7.out                         results/g.7.log

source deactivate

