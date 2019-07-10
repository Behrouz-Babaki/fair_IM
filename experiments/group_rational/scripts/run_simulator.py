#!/usr/bin/env python
# coding: utf-8


import os, subprocess, json, math
from os.path import join as ojoin


DDIR = os.path.abspath(ojoin('..', 'datasets'))
BIN = os.path.abspath(ojoin('..', '..', '..', 'code', 'simulator', 'simulator'))
num_simulations = 1000000


with open('attribute_values.json') as f:
    attribute_values = json.load(f)


def create_simulator_graph(graph_number, attribute, value):
    
    graph_name = 'graph_spa_500_%d'%graph_number
    data_dir = ojoin(DDIR, graph_name, attribute, value) 
    ingraph_file = ojoin(data_dir, 'graph_ic.inf')
    info_file = ojoin(data_dir, 'attribute.txt')
    outgraph_file = ojoin(data_dir, 'sim_graph.txt')
    
    with open(info_file) as f:
        num_nodes = int(f.readline()[2:])
        num_edges = int(f.readline()[2:])
    
    with open(outgraph_file, 'w') as outf:
        print(num_nodes, file=outf)
        print(num_edges, file=outf)
        with open(ingraph_file) as inf:
            for line in inf:
                print(line.strip(), file=outf)


def run_simulator(graph_number, attribute, value):
    graph_name = 'graph_spa_500_%d'%graph_number
    data_dir = ojoin(DDIR, graph_name, attribute, value)
    
    seed_file = ojoin(data_dir, 'tim_output.txt')
    graph_file = ojoin(data_dir, 'sim_graph.txt')
    simulator_output_file = ojoin(data_dir, 'sim_output.txt')


    cmd = [BIN, 
           '--graph-file', graph_file, 
           '--seed-file', seed_file,
           '--output-file', simulator_output_file,
           '--num-simulations', str(num_simulations)]

    out = subprocess.check_output(cmd, text=True)
    return out


for graph_number in range(24):
    for attribute in attribute_values:
        for value in attribute_values[attribute]:
            create_simulator_graph(graph_number, attribute, value)
            _ = run_simulator(graph_number, attribute, value)

