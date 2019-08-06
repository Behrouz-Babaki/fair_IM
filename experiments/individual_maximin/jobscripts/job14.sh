#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o14.out
#SBATCH --error=outputs/o14.out
#SBATCH --job-name=mip.14

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                   data/graphs/g.13.pkl                       data/samples/s100/g.13.pkl       results/g.13.s.100.out           results/g.13.s.100.log

source deactivate

