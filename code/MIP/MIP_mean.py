#!/usr/bin/env python
# coding: utf-8

# In[4]:


from __future__ import print_function, division
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx
import pickle
import numpy, random


# In[5]:


def MIP_IM():
    attributes = ['age']#, 'gender', 'age', 'region', 'ethnicity']
  
    budget = 25
    m = 100
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

                labels = nx.get_node_attributes(main_graph, attribute)
                label_dict = {}
                for i in range(len(main_graph.nodes())):
                    label = labels[i].encode('utf-8')
                    if label in label_dict.keys():
                        label_dict[label].append(i)
                    else:
                        label_dict[label] = [i] 
                        
                model = Model('mean_'+str(attribute)+'_'+str(index))
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

                obj_expr = quicksum(avars)
                model.setObjective(min_value, GRB.MAXIMIZE)

                model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)

                for sample_index, sample in enumerate(samples):
                    for i in range(len(main_graph.nodes())):
                        neighbors = nx.ancestors(sample, i) 
                        e = len(neighbors)
                        ai = var_active_dict[(sample_index,i)]
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

                mean_label_dict = {}
                for label in label_dict.keys():
                    for node in label_dict[label]:
                        if label in mean_label_dict.keys():
                            mean_label_dict[label]+=var_mean_dict[node]
                        else:
                            mean_label_dict[label]=var_mean_dict[node]
        
        
                for label in label_dict.keys():
                    label_size = len(label_dict[label])
                    model.addConstr(mean_label_dict[label], GRB.GREATER_EQUAL, label_size *m* min_value)

                try:
                    model.optimize()
                except e:
                    print(e)

                with open('../../../../Git/influence_maximization/experiments/im500/results/fairmip/mean/base100/'+attribute+'/output_'+str(index)+'.txt', "w") as of:    
                    for key,value in var_seed_dict.items():
                        if(value.x > 0):
                            print(key, file=of)


# In[ ]:


MIP_IM()


# In[ ]:




