#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o16.out
#SBATCH --error=outputs/o16.out
#SBATCH --job-name=balance.16

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                                \
    --graph-file data/graphs/g.15.pkl                            \
    --sample-file data/samples/s100/g.15.samples.pkl   \
    --output-file results/g.15.s.100.out               \
    --log-file results/g.15.s.100.log                  \
    --time-limit 39600

source deactivate

