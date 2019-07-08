#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:120:00
#SBATCH --output=out/o65.out
#SBATCH --error=out/o65.out
#SBATCH --job-name=mip.65

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_group_maxmin.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER gender 100 $NETWORKDIR/graph_spa_500_16.pickle $RESULTDIR/output_65.txt $RESULTDIR/log_65.txt
source deactivate

