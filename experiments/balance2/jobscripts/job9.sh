#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o9.out
#SBATCH --error=outputs/o9.out
#SBATCH --job-name=balance.9

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                                \
    --graph_file data/graphs/g.8.pkl                            \
    --sample_file data/samples/s100/g.8.samples.pkl   \
    --output_file results/g.8.s.100.out               \
    --log_file results/g.8.s.100.log                  \
    --time_limit 39600

source deactivate

