#!/usr/bin/env python

from base import IMBaseModel
from gurobipy import Model, GRB, quicksum, LinExpr

class IndividualMaximinModel(IMBaseModel):
    def __init__(self, graph, samples, budget, time_limit,
        name='individual_maximin'):
        
        self.budget = budget
        self.n = len(graph.nodes)
        self.m = len(samples)
        IMBaseModel.__init__(self, graph, samples, time_limit, name)

    def _initialize(self):
        IMBaseModel._initialize(self)
        self.min_influence = self.model.addVar(lb=0.0, ub=self.m, vtype=GRB.CONTINUOUS)

    def _add_objective(self):
        self.model.setObjective(self.min_influence, GRB.MAXIMIZE)


    def _add_constraints(self):
        self.model.addConstr(quicksum(self.svars), GRB.LESS_EQUAL, self.budget)

        for i in range(self.n):
            expr = quicksum([self.var_active_dict[(p, i)] for p in range(self.m)])
            self.model.addConstr(self.min_influence, GRB.LESS_EQUAL, expr)

if __name__ == '__main__':

    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--graph-file', required=True)
    parser.add_argument('--sample-file', required=True)
    parser.add_argument('--output-file', required=True)
    parser.add_argument('--log-file', required=True)
    parser.add_argument('--budget', type=int, default=25)
    parser.add_argument('--time-limit', type=int, default=1800)
    args = parser.parse_args()

    with open(args.graph_file, 'rb') as f:
        graph = pickle.load(f)

    with open(args.sample_file, 'rb') as f:
        samples = pickle.load(f)
    
    model = IndividualMaximinModel(graph, samples, args.budget, args.time_limit)
    model.solve()
    model.save_results(args.log_file, args.output_file)
