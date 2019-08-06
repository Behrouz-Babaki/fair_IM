#!/usr/bin/env python

from base import IMBaseModel
from gurobipy import Model, GRB, quicksum, LinExpr

class IndividualMaximinModel(IMBaseModel):
    def __init__(self, graph, samples,
        budget, time_limit, name='individual_maximin'):
        
        self.budget = budget
        self.n = len(graph.nodes)
        self.m = len(samples)
        IMBaseModel.__init__(self, graph, samples, time_limit, name)

    def _initialize(self):
        IMBaseModel._initialize(self)
        self.d = []
        for _ in range(self.n):
            self.d.append(self.model.addVar(lb=0.0, ub=self.m, vtype=GRB.CONTINUOUS)) 

    def _add_objective(self):
        self.model.setObjective(quicksum(self.d), GRB.MINIMIZE)

    def _add_constraints(self):
        self.model.addConstr(quicksum(self.svars), GRB.EQUAL, self.budget)

        a_sums = [quicksum([self.var_active_dict[(p, i)] for p in range(self.m)])
                    for i in range(self.n)]
        a_total = quicksum(self.avars)

        for i in range(self.n):
            self.model.addConstr(self.n * self.d[i], GRB.GREATER_EQUAL, 
                self.n * a_sums[i] - a_total)
            self.model.addConstr(self.n * self.d[i], GRB.GREATER_EQUAL,
                a_total - self.n * a_sums[i])

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
    
    model = IndividualMaximinModel(graph, samples, 
        args.budget, args.time_limit)
    model.solve()
    model.save_results(args.log_file, args.output_file)
