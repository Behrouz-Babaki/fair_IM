#!/bin/bash
#SBATCH --account=def-pesantg
#SBATCH --time=11:59:00
#SBATCH --mem=8000M
#SBATCH --output=out/o2.out
#SBATCH --error=out/o2.out
#SBATCH --job-name=fairim.2

module load singularity/3.1

RESULTDIR=$(readlink -f ./results)
singularity run -C -B $RESULTDIR:/results fairim.sif /influence_maximization/code/fairim/check_fairness.py 2 /results

