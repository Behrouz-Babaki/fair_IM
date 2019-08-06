#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o31.out
#SBATCH --error=outputs/o31.out
#SBATCH --job-name=balance.31

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                                \
    --graph_file data/graphs/g.6.pkl                            \
    --sample_file data/samples/s1000/g.6.samples.pkl   \
    --output_file results/g.6.s.1000.out               \
    --log_file results/g.6.s.1000.log                  \
    --time_limit 39600

source deactivate

