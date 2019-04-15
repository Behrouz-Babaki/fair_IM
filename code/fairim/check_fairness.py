#!/usr/bin/env python

import networkx as nx
import numpy as np
import pickle
from utils import greedy
from icm import sample_live_icm, make_multilinear_objective_samples_group, make_multilinear_gradient_group
from algorithms import algo, maxmin_algo, make_normalized, indicator
import math
import argparse
import os
import time
import functools

print = functools.partial(print, flush=True)

def multi_to_set(f, n = None):
    '''
    Takes as input a function defined on indicator vectors of sets, and returns
    a version of the function which directly accepts sets
    '''
    global g
    if n == None:
        n = len(g)
    def f_set(S):
        return f(indicator(S, n))
    return f_set

def valoracle_to_single(f, i):
    def f_single(x):
        return f(x, 1000)[i]
    return f_single


def run(graph_filename, budget, attribute, output_filename):
    global g
    print('Budget: {}'.format(budget))

    #whether fair influence share is calculated by forming a subgraph consisting
    #only of nodes in a given subgroup -- leave this to True for the setting in
    #the paper
    succession = True

    #what method to use to solve the inner maxmin LP. This can be either 'md' to
    #use stochastic saddlepoint mirror descent, or 'gurobi' to solve the LP explicitly
    #the the gurobi solver (requires an installation and license).
    #MD is better asymptotically for large networks but may require many iterations
    #and is typically slower than gurobi for small/medium sized problems. You can
    #tune the stepsize/batch size/number of iterations for MD by editing algorithms.py
    solver = 'md'

    g = pickle.load(open(graph_filename, 'rb'))
    g = nx.convert_node_labels_to_integers(g, label_attribute='pid')

    #assign a unique numeric value for nodes who left the attribute blank
    nvalues = len(np.unique([g.node[v][attribute] for v in g.nodes()]))
    group_size = np.zeros(nvalues)

    live_graphs = sample_live_icm(g, 1000)

    group_indicator = np.ones((len(g.nodes()), 1))

    val_oracle = make_multilinear_objective_samples_group(live_graphs, group_indicator,  list(g.nodes()), list(g.nodes()), np.ones(len(g)))
    grad_oracle = make_multilinear_gradient_group(live_graphs, group_indicator,  list(g.nodes()), list(g.nodes()), np.ones(len(g)))

    def f_multi(x):
        return val_oracle(x, 1000).sum()


    #f_multi = make_multilinear_objective_samples(live_graphs, list(g.nodes()), list(g.nodes()), np.ones(len(g)))
    f_set = multi_to_set(f_multi)

    #find overall optimal solution
    print('running the greedy algorithm')
    start = time.time()
    S, obj = greedy(list(range(len(g))), budget, f_set)
    duration = time.time() - start
    print('finished running the greedy algorithm in %g seconds'%duration)

    #all values taken by this attribute
    values = np.unique([g.node[v][attribute] for v in g.nodes()])

    values = np.unique([g.node[v][attribute] for v in g.nodes()])
    nodes_attr = {}
    for vidx, val in enumerate(values):
        nodes_attr[val] = [v for v in g.nodes() if g.node[v][attribute] == val]
        group_size[vidx] = len(nodes_attr[val])

    opt_succession = {}
    if succession:
        for vidx, val in enumerate(values):
            h = nx.subgraph(g, nodes_attr[val])
            h = nx.convert_node_labels_to_integers(h)
            live_graphs_h = sample_live_icm(h, 1000)
            group_indicator = np.ones((len(h.nodes()), 1))
            val_oracle = multi_to_set(valoracle_to_single(make_multilinear_objective_samples_group(live_graphs_h, group_indicator,  list(h.nodes()), list(h.nodes()), np.ones(len(h))), 0), len(h))
            S_succession, opt_succession[val] = greedy(list(h.nodes()), math.ceil(len(nodes_attr[val])/len(g) * budget), val_oracle)

    group_indicator = np.zeros((len(g.nodes()), len(values)))
    for val_idx, val in enumerate(values):
        group_indicator[nodes_attr[val], val_idx] = 1



    val_oracle = make_multilinear_objective_samples_group(live_graphs, group_indicator,  list(g.nodes()), list(g.nodes()), np.ones(len(g)))
    grad_oracle = make_multilinear_gradient_group(live_graphs, group_indicator,  list(g.nodes()), list(g.nodes()), np.ones(len(g)))


    #build an objective function for each subgroup
    f_attr = {}
    f_multi_attr = {}
    for vidx, val in enumerate(values):
        nodes_attr[val] = [v for v in g.nodes() if g.node[v][attribute] == val]
        f_multi_attr[val] = valoracle_to_single(val_oracle, vidx)
        f_attr[val] = multi_to_set(f_multi_attr[val])


    #get the best seed set for nodes of each subgroup
    S_attr = {}
    opt_attr = {}
    if not succession:
        for val in values:
            S_attr[val], opt_attr[val] = greedy(list(range(len(g))), int(len(nodes_attr[val])/len(g) * budget), f_attr[val])
    if succession:
        opt_attr = opt_succession

    threshold = 5
    targets = [opt_attr[val] for val in values]
    targets = np.array(targets)

    #run the constrained fair algorithm
    print('running the constrained fair algorithm')
    start = time.time()
    fair_x = algo(grad_oracle, val_oracle, threshold, budget, group_indicator, np.array(targets), 100, solver)[1:]
    fair_x = fair_x.mean(axis=0)
    duration = time.time() - start
    print('finished running the constrained fair algorithm in %g seconds'%duration)

    #run the minimax algorithm
    print('running the minimax algorithm')
    start = time.time()
    grad_oracle_normalized = make_normalized(grad_oracle, group_size)
    val_oracle_normalized = make_normalized(val_oracle, group_size)
    minmax_x = maxmin_algo(grad_oracle_normalized, val_oracle_normalized, threshold, budget, group_indicator, 20, 10, 0.05, solver)
    minmax_x = minmax_x.mean(axis=0)
    duration = time.time() - start
    print('finished running the minimax algorithm in %g seconds'%duration)

    xg = np.zeros(len(fair_x))
    xg[list(S)] = 1
    
    results = dict(greedy=xg, fair=fair_x, minmax=minmax_x)
    pickle.dump(results, open(output_filename, 'wb'))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('graph_filename')
    parser.add_argument('output_filename')
    parser.add_argument('--attribute', default='gender',
                        choices=['region', 'ethnicity', 'age', 'gender', 'status'])
    parser.add_argument('--budget', type=int, default=15)
    args = parser.parse_args()

    if not os.path.isfile(args.graph_filename):
        print('ERROR opening %s'%args.graph_filename)
        exit(1)
    
    try:
        f = open(args.output_filename, 'wb')
        f.close()
        os.remove(args.output_filename)
    except:
        print('ERROR writing to %s'%args.output_filename)
        exit(1)

    run(args.graph_filename, args.budget, args.attribute, args.output_filename)
