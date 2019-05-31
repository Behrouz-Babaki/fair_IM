#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function, division
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx
import pickle
import numpy, random


# In[2]:


with open('../MIP/data/networks_prob/graph_spa_500_0.pickle', "rb") as f:
    main_graph = pickle.load(f)
    
samples = []
m = 10
for j in range(m):
    G = nx.DiGraph()
    for u in main_graph.nodes():
        G.add_node(u)
    for u,v in main_graph.edges():
        if main_graph[u][v]['p']> random.random():
            G.add_edge(u, v)
    samples.append(G)


# In[3]:


model = Model('IM')
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


# In[4]:


budget = 25
model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)


# In[5]:


obj_expr = quicksum(avars)
model.setObjective(obj_expr, GRB.MAXIMIZE)


# In[6]:


attributes = ['gender']#,'age', 'region', 'ethnicity']
epsilon = 0.1  
for attribute in attributes:
    for sample_index, sample in enumerate(samples):
        for i in range(len(main_graph.nodes())):
            neighbors = nx.ancestors(sample, i) 
            e = len(neighbors)
            ai = var_active_dict[(sample_index,i)]
            si = var_seed_dict[i]
            if i in  var_mean_dict.keys():
                var_mean_dict[i]+= ai
            else:
                var_mean_dict[i]= ai
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

    labels = nx.get_node_attributes(main_graph, attribute)
    label_dict = {}
    for i in range(len(main_graph.nodes())):
        label = labels[i].encode('utf-8')
        if label in label_dict.keys():
            label_dict[label].append(i)
        else:
            label_dict[label] = [i] 

    for label in label_dict.keys():
        active_label_vars = []
        label_size = len(label_dict[label])
        frac = float(label_size)/float(len(main_graph.nodes()))
        epsilon_plus_active = []
        epsilon_minus_active = []
        for avar in avars:
            epsilon_plus_active.append((frac+epsilon, avar))
            epsilon_minus_active.append((frac-epsilon, avar))
        for sample_index, sample in enumerate(samples):
            for node in label_dict[label]:
                active_label_vars.append(var_active_dict[(sample_index, node)])
            
        lin_exr_plus = LinExpr(epsilon_plus_active)
        lin_exr_minus = LinExpr(epsilon_minus_active)
        expr = quicksum(active_label_vars)      
        model.addConstr(expr, GRB.LESS_EQUAL, lin_exr_plus)
        model.addConstr(expr, GRB.LESS_EQUAL, lin_exr_minus)  


# In[7]:


try:
    model.optimize()
except e:
    print(e)


# In[8]:


for key,value in var_seed_dict.items():
    if(value.x > 0):
        print(key)


# In[9]:


optimal = (model.Status == GRB.OPTIMAL)
optimal


# In[10]:


objective = model.ObjVal
objective


# In[11]:


objective/(500*m)


# In[ ]:




