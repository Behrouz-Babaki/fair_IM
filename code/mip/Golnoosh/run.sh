#!/bin/bash

for graph_id in {0..23};
do
    for sample_id in {0..9};
    do
        ./runner_mip.py \
        ../data/graphs/graph_${graph_id}.pkl \
        ../data/samples/g.${graph_id}.s.${sample_id}.pkl \
        outputs/mip/g.${graph_id}.s.${sample_id}.out \
        outputs/mip/g.${graph_id}.s.${sample_id}.log
        for type in equality equity group_maximin;
        do
            ./runner_${type}.py \
            gender \
            ../data/graphs/graph_${graph_id}.pkl \
            ../data/samples/g.${graph_id}.s.${sample_id}.pkl \
            outputs/${type}/g.${graph_id}.s.${sample_id}.out \
            outputs/${type}/g.${graph_id}.s.${sample_id}.log
        done
    done
done
