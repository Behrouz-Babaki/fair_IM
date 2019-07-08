#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:120:00
#SBATCH --output=out/o33.out
#SBATCH --error=out/o33.out
#SBATCH --job-name=mip.33

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_group_maxmin.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER gender 100 $NETWORKDIR/graph_spa_500_8.pickle $RESULTDIR/output_33.txt $RESULTDIR/log_33.txt
source deactivate

