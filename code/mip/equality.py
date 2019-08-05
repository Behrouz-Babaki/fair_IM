from base import IMBaseModel
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx

class EqualityModel(IMBaseModel):
    def __init__(self, attribute, graph, samples,
        budget, epsilon, 
        time_limit=1800,
        name='im_equality'):

        self.attribute = attribute
        self.budget = budget
        self.epsilon = epsilon
        
        IMBaseModel.__init__(self, graph, samples, time_limit, name)

    def _add_objective(self):
        obj_expr = quicksum(self.avars)
        self.model.setObjective(obj_expr, GRB.MAXIMIZE)

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

        for label in label_dict.keys():
            for sample_index, sample in enumerate(self.samples):
                active_label_vars = []
                label_size = len(label_dict[label])
                frac = float(label_size)/float(len(self.graph.nodes()))
                for node in label_dict[label]:
                    active_label_vars.append(self.var_active_dict[(sample_index,node)])
                actives = []
                for j in range(len(self.graph.nodes())):
                    actives.append((frac,self.var_active_dict[(sample_index,j)]))

                buget_var = self.model.addVar(lb=0.0, ub=len(self.graph.nodes()), vtype=GRB.CONTINUOUS)
                label_budget = LinExpr(actives)
                expr = quicksum(active_label_vars)
                self.model.addConstr(buget_var, GRB.EQUAL, label_budget)
                self.model.addConstr(expr, GRB.LESS_EQUAL, buget_var*(1+ self.epsilon))
                self.model.addConstr(expr, GRB.GREATER_EQUAL, buget_var*(1-self.epsilon)) 

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
    
    model = EqualityModel(args.attribute, graph, samples,
            budget=25, epsilon=0.1)
    model.solve()
    model.save_results(args.log_file, args.output_file)