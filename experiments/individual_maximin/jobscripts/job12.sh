#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o12.out
#SBATCH --error=outputs/o12.out
#SBATCH --job-name=mip.12

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                 data/graphs/g.11.pkl                     data/samples/s1000/g.11.samples.pkl      results/g.11.out                         results/g.11.log

source deactivate

