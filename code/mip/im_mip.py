from base import IMBaseModel
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx

class IMMip(IMBaseModel):

    def __init__(self, graph, samples, budget, 
        time_limit=1800,
        name='influence_maximization'):
        
        self.budget = budget
        IMBaseModel.__init__(self, graph, samples, time_limit, name)

    def _add_constraints(self):
        self.model.addConstr(quicksum(self.svars), GRB.LESS_EQUAL, self.budget)

    def _add_objective(self):
        obj_expr = quicksum(self.avars)
        self.model.setObjective(obj_expr, GRB.MAXIMIZE)

if __name__ == '__main__':

    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input_graph')
    parser.add_argument('sample_file')
    parser.add_argument('output_file')
    parser.add_argument('log_file')
    args = parser.parse_args()

    with open(args.input_graph, 'rb') as f:
        graph = pickle.load(f)

    with open(args.sample_file, 'rb') as f:
        samples = pickle.load(f)
    
    model = IMMip(graph, samples, budget=25)
    model.solve()
    model.save_results(args.log_file, args.output_file)