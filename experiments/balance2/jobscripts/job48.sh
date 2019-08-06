#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o48.out
#SBATCH --error=outputs/o48.out
#SBATCH --job-name=balance.48

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/balance.py                                                \
    --graph_file data/graphs/g.23.pkl                            \
    --sample_file data/samples/s1000/g.23.samples.pkl   \
    --output_file results/g.23.s.1000.out               \
    --log_file results/g.23.s.1000.log                  \
    --time_limit 39600

source deactivate

