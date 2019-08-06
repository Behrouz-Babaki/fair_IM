#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o47.out
#SBATCH --error=outputs/o47.out
#SBATCH --job-name=balance.47

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                                \
    --graph-file data/graphs/g.22.pkl                            \
    --sample-file data/samples/s1000/g.22.samples.pkl   \
    --output-file results/g.22.s.1000.out               \
    --log-file results/g.22.s.1000.log                  \
    --time-limit 39600

source deactivate

