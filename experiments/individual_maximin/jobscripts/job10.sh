#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o10.out
#SBATCH --error=outputs/o10.out
#SBATCH --job-name=mip.10

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                   data/graphs/g.9.pkl                       data/samples/s100/g.9.pkl       results/g.9.s.100.out           results/g.9.s.100.log

source deactivate

