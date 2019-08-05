#!/usr/bin/env python

import os, pickle
import networkx as nx
import random
from os.path import join as ojoin

script_dir = os.path.abspath(os.path.dirname(__file__))
graph_dir = ojoin(script_dir, '..', 'graphs')
sample_dir = script_dir
large_sample_dir = ojoin(script_dir, 'large')

def generate_samples(main_graph, m):
    samples = []
    for j in range(m):
        G = nx.DiGraph()
        for u in main_graph.nodes():
            G.add_node(u)
        for u,v in main_graph.edges():
            if main_graph[u][v]['p']> random.random():
                G.add_edge(u, v)
        samples.append(G)
    return samples

if __name__ == '__main__':
    
    # for each graph, create 10 samples of size 20, and one "large" sample of size 100

    for graph_id in range(24):
        input_graph = ojoin(graph_dir, 'graph_%d.pkl'%graph_id)
        with open(input_graph, "rb") as f:
            graph = pickle.load(f)

        for sample_id in range(10):
            samples = generate_samples(graph, 20)
            sample_file = ojoin(sample_dir, 'g.%d.s.%d.pkl'%(graph_id, sample_id))
            with open(sample_file, 'wb') as f:
                pickle.dump(samples, f)

        samples_large = generate_samples(graph, 100)
        sample_file = ojoin(large_sample_dir, 'g.%d.100.pkl'%graph_id)
        with open(sample_file, 'wb') as f:
            pickle.dump(samples_large, f)


