#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o15.out
#SBATCH --error=outputs/o15.out
#SBATCH --job-name=mip.balance.15

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                      data/graphs/g.14.pkl                               data/samples/s100/g.14.samples.pkl       results/g.14.s.100.out                   results/g.14.s.100.log

source deactivate

