#!/bin/bash

BINARY="../../../code/tim/tim"
DDIR="../data/tim/graph_spa_500"
ODIR="../results/tim"
BUDGET=25

for i in {0..19};
do
    DATASET_DIR="${DDIR}_${i}"
    OUTPUT_FILE="${ODIR}/output_${i}.txt"
    ${BINARY} -dataset ${DATASET_DIR} -k ${BUDGET} -model IC -epsilon 0.1 -outfile ${OUTPUT_FILE}     
done
