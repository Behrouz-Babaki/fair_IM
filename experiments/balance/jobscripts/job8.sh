#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:100:00
#SBATCH --output=out/o8.out
#SBATCH --error=out/o8.out
#SBATCH --job-name=mip.8

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_Balance.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER 100 $NETWORKDIR/graph_spa_500_7.pickle $RESULTDIR/output_8.txt $RESULTDIR/log_8.txt
source deactivate

