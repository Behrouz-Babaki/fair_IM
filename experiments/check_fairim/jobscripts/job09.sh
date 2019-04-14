#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=11:59:00
#SBATCH --mem=8000M
#SBATCH --output=out/o8.out
#SBATCH --error=out/o8.out
#SBATCH --job-name=fairim.8

module load singularity/3.1

RESULTDIR=$(readlink -f ./results)
singularity run -C -B $RESULTDIR:/results fairim.sif /influence_maximization/code/fairim/check_fairness.py 8 /results

