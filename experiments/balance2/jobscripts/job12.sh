#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o12.out
#SBATCH --error=outputs/o12.out
#SBATCH --job-name=balance.12

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                                \
    --graph-file data/graphs/g.11.pkl                            \
    --sample-file data/samples/s100/g.11.samples.pkl   \
    --output-file results/g.11.s.100.out               \
    --log-file results/g.11.s.100.log                  \
    --time-limit 39600

source deactivate

