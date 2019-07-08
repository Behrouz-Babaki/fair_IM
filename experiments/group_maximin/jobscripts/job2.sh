#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:70:00
#SBATCH --output=out/o2.out
#SBATCH --error=out/o2.out
#SBATCH --job-name=mip.2

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_group_maxmin.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER age 1000 $NETWORKDIR/graph_spa_500_0.pickle $RESULTDIR/output_2.txt $RESULTDIR/log_2.txt
source deactivate

