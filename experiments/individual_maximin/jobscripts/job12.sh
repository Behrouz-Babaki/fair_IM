#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=11:59:00
#SBATCH --output=outputs/o12.out
#SBATCH --error=outputs/o12.out
#SBATCH --job-name=maximin.12

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate im-env

../../code/mip/individual_maximin.py                                     \
    --graph_file data/graphs/g.11.pkl                            \
    --sample_file data/samples/s1000/g.11.samples.pkl   \
    --output_file results/g.11.s.1000.out               \
    --log_file results/g.11.s.1000.log                  \
    --time_limit 39600

source deactivate

