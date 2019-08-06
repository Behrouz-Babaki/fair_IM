#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o18.out
#SBATCH --error=outputs/o18.out
#SBATCH --job-name=mip.18

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                   data/graphs/g.17.pkl                       data/samples/s100/g.17.pkl       results/g.17.s.100.out           results/g.17.s.100.log

source deactivate

