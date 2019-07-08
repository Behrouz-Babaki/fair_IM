#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:70:00
#SBATCH --output=out/o13.out
#SBATCH --error=out/o13.out
#SBATCH --job-name=mip.13

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_group_maxmin.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER gender 1000 $NETWORKDIR/graph_spa_500_3.pickle $RESULTDIR/output_13.txt $RESULTDIR/log_13.txt
source deactivate

