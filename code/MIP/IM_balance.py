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
    for index in range(1):
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
                
                
            model = Model('balance_'+str(index))
            #active nodes
            avars = []
            #seed nodes
            svars = []
            #distance
            dvars = []
            var_seed_dict = {}
            var_active_dict = {}

            for j in main_graph.nodes():
                s = model.addVar(lb=0.0, ub=1.0, vtype=GRB.BINARY)
                svars.append(s)
                var_seed_dict[j] = s

            for sample_index, sample in enumerate(samples):
                for j in main_graph.nodes():
                    a = model.addVar(lb=0.0, ub=1.0, vtype=GRB.BINARY)
                    avars.append(a)
                    var_active_dict[(sample_index,j)] = a    

            
            
            model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)

            
            size_graph = float(1)/ float(len(main_graph.nodes()))
            mean_vars = []
            for ai in avars:
                mean_vars.append((size_graph,ai))
            mean_exp = LinExpr(mean_vars)
            
            for i in main_graph.nodes():
                avgai = []
                for sample_index, sample in enumerate(samples):
                    neighbors = nx.ancestors(sample, i) 
                    e = len(neighbors)
                    ai = var_active_dict[(sample_index,i)]
                    avgai.append(ai)
                    si = var_seed_dict[i]
                    neighbors_active_vars = []
                    neighbors_seed_vars = []
                    neighbors_active_vars.append(((e+1), ai))
                    neighbors_seed_vars.append(si)
                    for neighbor in neighbors:
                        neighbors_active_vars.append(((e+1), var_active_dict[(sample_index,neighbor)]))
                        neighbors_seed_vars.append(var_seed_dict[neighbor])
                    seed_neighbors = quicksum(neighbors_seed_vars)
                    model.addConstr(ai, GRB.LESS_EQUAL, seed_neighbors)
                    model.addConstr(seed_neighbors, GRB.LESS_EQUAL, LinExpr(neighbors_active_vars))
                di = model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS)
                dvars.append(di)
                avg_exp = quicksum(avgai)
                model.addConstr(di, GRB.GREATER_EQUAL, avg_exp - mean_exp)
                model.addConstr(di, GRB.GREATER_EQUAL, mean_exp - avg_exp)
                    
            
            model.addConstr(quicksum(avars), GRB.GREATER_EQUAL, 1000)
            obj_expr = quicksum(dvars)         
            model.setObjective(obj_expr, GRB.MINIMIZE)
           
                
            try:
                model.optimize()
            except e:
                print(e)
                
            '''
            with open('../Git/influence_maximization/experiments/im500/results/fairmip/balance/base1000/output_'+str(index)+'.txt', "w") as of:    
                for key,value in var_seed_dict.items():
                    if(value.x > 0):
                        print(key, file = of)
            '''
            for key,value in var_seed_dict.items():
                if(value.x > 0):
                    print(key)


# In[3]:


MIP_IM()

