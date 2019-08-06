#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o13.out
#SBATCH --error=outputs/o13.out
#SBATCH --job-name=mip.13

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                 data/graphs/g.12.pkl                     data/samples/s1000/g.12.samples.pkl      results/g.12.out                         results/g.12.log

source deactivate

