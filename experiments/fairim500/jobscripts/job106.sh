#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=11:59:00
#SBATCH --mem=8000M
#SBATCH --output=out/o106.out
#SBATCH --error=out/o106.out
#SBATCH --job-name=fairim.region.21

module load singularity/3.1

RESULTDIR=$(readlink -f ./results)
singularity run -C -B $RESULTDIR:/results \
                      fairim.sif          \
                      /influence_maximization/code/fairim/check_fairness.py \
                      /influence_maximization/code/fairim/networks/graph_spa_500_21.pickle \
                      /results/result_region_21.pkl      \
                      --attribute region

