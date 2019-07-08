#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:70:00
#SBATCH --output=out/o19.out
#SBATCH --error=out/o19.out
#SBATCH --job-name=mip.19

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_group_maxmin.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER ethnicity 1000 $NETWORKDIR/graph_spa_500_4.pickle $RESULTDIR/output_19.txt $RESULTDIR/log_19.txt
source deactivate

