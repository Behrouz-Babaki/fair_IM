from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx

class IMBaseModel(object):

    def __init__(self, graph, samples, time_limit, name):

        self.graph = graph
        self.samples = samples
        self.name = name
        self.time_limit = time_limit

        #active nodes
        self.avars = []
        
        #seed nodes
        self.svars = []
        
        self.var_seed_dict = {}
        self.var_active_dict = {}

        self._initialize()
        self._add_constraints()
        self._add_objective()


    def _initialize(self):        

        self.model = Model(self.name)
        self.model.setParam('OutputFlag', 0)
        self.model.setParam('TimeLimit', self.time_limit)
        
        for j in range(len(self.graph.nodes())):
            s = self.model.addVar(lb=0.0, ub=1.0, vtype=GRB.BINARY)
            self.svars.append(s)
            self.var_seed_dict[j] = s

        for sample_index, sample in enumerate(self.samples):
            for j in range(len(self.graph.nodes())):
                a = self.model.addVar(lb=0.0, ub=1.0, vtype=GRB.BINARY)
                self.avars.append(a)
                self.var_active_dict[(sample_index,j)] = a    

        for sample_index, sample in enumerate(self.samples):
            for i in range(len(self.graph.nodes())):
                neighbors = nx.ancestors(sample, i) 
                e = len(neighbors)
                ai = self.var_active_dict[(sample_index,i)]
                si = self.var_seed_dict[i]
                neighbors_active_vars = []
                neighbors_seed_vars = []
                neighbors_active_vars.append(((e+1), ai))
                neighbors_seed_vars.append(si)
                for neighbor in neighbors:
                    neighbors_active_vars.append(((e+1), self.var_active_dict[(sample_index,neighbor)]))
                    neighbors_seed_vars.append(self.var_seed_dict[neighbor])
                seed_neighbors = quicksum(neighbors_seed_vars)
                self.model.addConstr(ai, GRB.LESS_EQUAL, seed_neighbors)
                self.model.addConstr(seed_neighbors, GRB.LESS_EQUAL, LinExpr(neighbors_active_vars))        
    
    def _add_objective(self):
        pass

    def _add_constraints(self):
        pass

    def solve(self):
        try:
            self.model.optimize()
        except e:
            print(e)        
    
    def save_results(self, log_file, output_file):
        with open(log_file, "w") as of:  
            runtime = self.model.Runtime
            objective_value = self.model.ObjVal
            status = self.model.Status
            print('runtime\t%f'%(runtime), file = of)
            print('objective_value\t%f'%(objective_value), file = of)
            print('status\t%d'%(status), file = of)
            print('sample_size\t%d'%len(self.samples), file = of)
        
        if (self.model.solCount>0):
            with open(output_file, "w") as of:    
                for key,value in self.var_seed_dict.items():
                    if(value.x > 0):
                        print(key, file = of)
