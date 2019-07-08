#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:120:00
#SBATCH --output=out/o46.out
#SBATCH --error=out/o46.out
#SBATCH --job-name=mip.46

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_group_maxmin.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER age 100 $NETWORKDIR/graph_spa_500_11.pickle $RESULTDIR/output_46.txt $RESULTDIR/log_46.txt
source deactivate

