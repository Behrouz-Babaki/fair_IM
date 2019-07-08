#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:100:00
#SBATCH --output=out/o72.out
#SBATCH --error=out/o72.out
#SBATCH --job-name=mip.72

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_Equality.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER region 100 $NETWORKDIR/graph_spa_500_17.pickle $RESULTDIR/output_72.txt $RESULTDIR/log_72.txt
source deactivate

