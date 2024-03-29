#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function, division
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx
import pickle
import numpy, random


# In[2]:


def MIP_IM():
    budget = 25
    m = 10
    for index in range(24):
        with open('../MIP/data/networks_prob/graph_spa_500_'+str(index)+'.pickle', "rb") as f:
            main_graph = pickle.load(f)
    
            samples = []
            for j in range(m):
                G = nx.DiGraph()
                for u in main_graph.nodes():
                    G.add_node(u)
                for u,v in main_graph.edges():
                    if main_graph[u][v]['p']> random.random():
                        G.add_edge(u, v)
                samples.append(G)
                
                
            model = Model('influence_maximization_'+str(index))
            mvars = []
            #active nodes
            avars = []
            #seed nodes
            svars = []
            var_seed_dict = {}
            var_active_dict = {}

            for j in range(len(main_graph.nodes())):
                s = model.addVar(lb=0.0, ub=1.0, vtype=GRB.BINARY)
                svars.append(s)
                var_seed_dict[j] = s

            for sample_index, sample in enumerate(samples):
                for j in range(len(main_graph.nodes())):
                    a = model.addVar(lb=0.0, ub=1.0, vtype=GRB.BINARY)
                    avars.append(a)
                    var_active_dict[(sample_index,j)] = a    

            mvars.append(avars)
            mvars.append(svars)

            obj_expr = quicksum(avars)
            model.setObjective(obj_expr, GRB.MAXIMIZE)
            model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)
            for sample_index, sample in enumerate(samples):
                for i in range(len(main_graph.nodes())):
                    neighbors = sample.in_edges(i) 
                    e = len(neighbors)
                    ai = var_active_dict[(sample_index,i)]
                    si = var_seed_dict[i]
                    neighbors_vars = []
                    for neighbor in neighbors:
                        neighbors_vars.append(var_active_dict[(sample_index,neighbor[0])])
                    expr = (e+1)*ai-si-quicksum(neighbors_vars)
                    model.addConstr(expr, GRB.GREATER_EQUAL, 0)
                    model.addConstr(expr, GRB.LESS_EQUAL, e)
            try:
                model.optimize()
            except e:
                print(e)
                
            with open('../Git/influence_maximization/experiments/im500/results/mip/base10/output_'+str(index)+'.txt', "w") as of:    
                for key,value in var_seed_dict.items():
                    if(value.x > 0):
                        print(key, file = of)


# In[3]:


MIP_IM()


# In[ ]:




