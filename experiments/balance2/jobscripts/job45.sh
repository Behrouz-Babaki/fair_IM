#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o45.out
#SBATCH --error=outputs/o45.out
#SBATCH --job-name=mip.balance.45

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                   data/graphs/g.20.pkl                       data/samples/s1000/g.20.pkl       results/g.20.s.1000.out           results/g.20.s.1000.log

source deactivate

