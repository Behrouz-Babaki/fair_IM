#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o3.out
#SBATCH --error=outputs/o3.out
#SBATCH --job-name=mip.balance.3

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                   data/graphs/g.2.pkl                       data/samples/s100/g.2.pkl       results/g.2.s.100.out           results/g.2.s.100.log

source deactivate

