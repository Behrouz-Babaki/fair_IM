#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=11:59:00
#SBATCH --mem=8000M
#SBATCH --output=out/o27.out
#SBATCH --error=out/o27.out
#SBATCH --job-name=fairim.ethnicity.5

module load singularity/3.1

RESULTDIR=$(readlink -f ./results)
singularity run -C -B $RESULTDIR:/results \
                      fairim.sif          \
                      /influence_maximization/code/fairim/check_fairness.py \
                      /influence_maximization/code/fairim/networks/graph_spa_500_5.pickle \
                      /results/result_ethnicity_5.pkl      \
                      --attribute ethnicity

