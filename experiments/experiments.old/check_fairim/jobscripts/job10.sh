#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=11:59:00
#SBATCH --mem=8000M
#SBATCH --output=out/o9.out
#SBATCH --error=out/o9.out
#SBATCH --job-name=fairim.9

module load singularity/3.1

RESULTDIR=$(readlink -f ./results)
singularity run -C -B $RESULTDIR:/results fairim.sif /influence_maximization/code/fairim/check_fairness.py 9 /results

