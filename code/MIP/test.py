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
m = 100
for j in range(m):
    G = nx.DiGraph()
    for u in main_graph.nodes():
        G.add_node(u)
    for u,v in main_graph.edges():
        if main_graph[u][v]['p']> random.random():
            G.add_edge(u, v)
    samples.append(G)


# In[3]:


labels = nx.get_node_attributes(main_graph, 'gender')
label_dict = {}
for i in range(len(main_graph.nodes())):
    label = labels[i].encode('utf-8')
    if label in label_dict.keys():
        label_dict[label].append(i)
    else:
        label_dict[label] = [i]


# In[4]:


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


# In[5]:


budget = 25
model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)


# In[6]:


obj_expr = quicksum(avars)
model.setObjective(min_value, GRB.MAXIMIZE)


# In[7]:


for sample_index, sample in enumerate(samples):
    for i in range(len(main_graph.nodes())):
        reachable = sample.in_edges(i)
        #reachable = nx.descendants(sample, i)
        e = len(reachable)
        ai = var_active_dict[(sample_index,i)]
        si = var_seed_dict[i]
        if i in  var_mean_dict.keys():
            var_mean_dict[i]+= ai
        else:
            var_mean_dict[i]= ai
        child_active_vars = []
        child_seed_vars = []
        
        
        
        for child in reachable:
            child = child[0]
            child_active_vars.append(var_active_dict[(sample_index,child)])
            child_seed_vars.append(var_seed_dict[child])
            model.addConstr(ai, GRB.GREATER_EQUAL, var_active_dict[(sample_index,child)])
        #model.addConstr(ai * e  , GRB.GREATER_EQUAL, quicksum(child_seed_vars))    
        #model.addConstr(ai  , GRB.LESS_EQUAL, quicksum(var_seed_dict))       
            #model.addConstr(ai, GRB.GREATER_EQUAL, var_active_dict[(sample_index,neighbor[0])])
        expr = (e+1)*ai-si-quicksum(child_active_vars)
        model.addConstr(expr, GRB.GREATER_EQUAL, 0)
        model.addConstr(expr, GRB.LESS_EQUAL, e)
        
        #model.addConstr(ai, GRB.LESS_EQUAL, si)
        #model.addConstr(ai, GRB.LESS_EQUAL, 1)
        #model.addConstr(ai, GRB.GREATER_EQUAL, 0)
        #model.addConstr(ai, GRB.LESS_EQUAL, quicksum(neighbors_active_vars)+quicksum(neighbors_seed_vars))
        
        
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


# In[8]:


try:
    model.optimize()
except e:
    print(e)


# In[9]:


for key,value in var_seed_dict.items():
    if(value.x > 0):
        print(key)


# In[10]:


optimal = (model.Status == GRB.OPTIMAL)
optimal


# In[11]:


objective = model.ObjVal
objective


# In[12]:


objective/(500*m)


# In[ ]:




