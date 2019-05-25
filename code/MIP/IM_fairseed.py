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
    m = 100
    epsilon = 1
    
    attributes = ['gender','age', 'region', 'ethnicity']
  
    for attribute in attributes:
        for index in range(20):
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


                model = Model('fairseed_'+str(index))
                min_value = model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS)

                mvars = []
                #active nodes
                avars = []
                #seed nodes
                svars = []
                var_seed_dict = {}
                var_active_dict = {}
                var_mean_dict = {}

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

                model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)

                obj_expr = quicksum(avars)
                model.setObjective(min_value, GRB.MAXIMIZE)

                for sample_index, sample in enumerate(samples):
                    for i in range(len(main_graph.nodes())):
                        neighbors = sample.in_edges(i) 
                        e = len(neighbors)
                        ai = var_active_dict[(sample_index,i)]
                        si = var_seed_dict[i]
                        if i in  var_mean_dict.keys():
                            var_mean_dict[i]+= ai
                        else:
                            var_mean_dict[i]= ai
                        neighbors_vars = []
                        for neighbor in neighbors:
                            neighbors_vars.append(var_active_dict[(sample_index,neighbor[0])])
                        expr = (e+1)*ai-si-quicksum(neighbors_vars)
                        model.addConstr(expr, GRB.GREATER_EQUAL, 0)
                        model.addConstr(expr, GRB.LESS_EQUAL, e)

                labels = nx.get_node_attributes(main_graph, attribute)
                label_dict = {}
                for i in range(len(main_graph.nodes())):
                    label = labels[i].encode('utf-8')
                    if label in label_dict.keys():
                        label_dict[label].append(i)
                    else:
                        label_dict[label] = [i]     

                for label in label_dict.keys():
                    seed_vars = []
                    label_size = len(label_dict[label])
                    frac = float(label_size)/float(len(main_graph.nodes()))
                    for node in label_dict[label]:
                        seed_vars.append(var_seed_dict[node])
                    label_budget = budget*frac
                    print(label_budget)
                    expr = quicksum(seed_vars)
                    model.addConstr(expr, GRB.LESS_EQUAL, label_budget+ epsilon)
                    model.addConstr(expr, GRB.GREATER_EQUAL, label_budget-epsilon)    
                    

                try:
                    model.optimize()
                except e:
                    print(e)

                with open('../../../../Git/influence_maximization/experiments/im500/results/fairmip/fairseed/base100/'+attribute+'/output_'+str(index)+'.txt', "w") as of:    
                    for key,value in var_seed_dict.items():
                        if(value.x > 0):
                            print(key, file=of)


# In[3]:


MIP_IM()

