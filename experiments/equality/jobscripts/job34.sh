#!/bin/bash
#SBATCH --account=def-gendrea1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:100:00
#SBATCH --output=out/o34.out
#SBATCH --error=out/o34.out
#SBATCH --job-name=mip.34

module use /scinet/niagara/software/commercial/modules
module load gurobi/8.1.1
module load anaconda3/5.2.0
source activate myenv

RUNNER="../../code/MIP/Runner_Equality.py"
RESULTDIR="./results"
NETWORKDIR="../../code/MIP/data/networks_prob"

$RUNNER age 100 $NETWORKDIR/graph_spa_500_8.pickle $RESULTDIR/output_34.txt $RESULTDIR/log_34.txt
source deactivate

