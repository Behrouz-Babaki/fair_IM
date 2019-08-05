from base import IMBaseModel
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx

class GroupMaximinModel(IMBaseModel):
    def __init__(self, attribute, graph, samples,
        budget, epsilon, 
        time_limit=1800,
        name='group_maximin'):
        
        self.attribute = attribute
        self.budget = budget
        self.epsilon = epsilon        
        
        IMBaseModel.__init__(self, graph, samples, time_limit, name)

    def _initialize(self):
        IMBaseModel._initialize(self)
        self.min_value = self.model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS)

    def _add_objective(self):
        self.model.setObjective(self.min_value, GRB.MAXIMIZE)

    def _add_constraints(self):
        
        self.model.addConstr(quicksum(self.svars), GRB.LESS_EQUAL, self.budget)

        labels = nx.get_node_attributes(self.graph, self.attribute)
        label_dict = {}
        for i in range(len(self.graph.nodes())):
            label = labels[i].encode('utf-8')
            if label in label_dict.keys():
                label_dict[label].append(i)
            else:
                label_dict[label] = [i]     

        var_mean_dict = {}
        for sample_index, sample in enumerate(self.samples):
            for i in range(len(self.graph.nodes())):
                ai = self.var_active_dict[(sample_index,i)]
                if i in  var_mean_dict.keys():
                    var_mean_dict[i]+= ai
                else:
                    var_mean_dict[i]= ai

        mean_label_dict = {}
        for label in label_dict.keys():
            for node in label_dict[label]:
                if label in mean_label_dict.keys():
                    mean_label_dict[label].append(var_mean_dict[node])
                else:
                    mean_label_dict[label]= [var_mean_dict[node]]
            label_size = len(label_dict[label])
            expr = quicksum(mean_label_dict[label])
            self.model.addConstr(expr, GRB.GREATER_EQUAL, label_size * len(self.samples) * self.min_value)

if __name__ == '__main__':

    import pickle
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('attribute')
    parser.add_argument('input_graph')
    parser.add_argument('sample_file')
    parser.add_argument('output_file')
    parser.add_argument('log_file')
    args = parser.parse_args()

    with open(args.input_graph, 'rb') as f:
        graph = pickle.load(f)

    with open(args.sample_file, 'rb') as f:
        samples = pickle.load(f)
    
    model = GroupMaximinModel(args.attribute, graph, samples, 
        budget=25, epsilon=0.1)
    model.solve()
    model.save_results(args.log_file, args.output_file)