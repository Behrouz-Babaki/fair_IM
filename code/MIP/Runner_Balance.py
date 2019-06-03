#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function, division
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx
import pickle
import numpy, random
import argparse


# In[2]:


def OPT(model_name, main_graph, samples, budget ,m):
    model = Model(model_name)
    mvars = []
    #active nodes
    avars = []
    #seed nodes
    svars = []
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

    mvars.append(avars)
    mvars.append(svars)

    obj_expr = quicksum(avars)
    model.setObjective(obj_expr, GRB.MAXIMIZE)
    model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)

    for sample_index, sample in enumerate(samples):
        for i in main_graph.nodes():
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
    try:
        model.optimize()
    except e:
        print(e)       
            
    objective = model.ObjVal     
    return objective


# In[3]:


def Mont_Carlo_Samplig(main_graph, m):
    samples = []
    for j in range(m):
        G = nx.DiGraph()
        for u in main_graph.nodes():
            G.add_node(u)
        for u,v in main_graph.edges():
            if main_graph[u][v]['p']> random.random():
                G.add_edge(u, v)
        samples.append(G)
    return samples


# In[4]:


def stage_1_MIP(main_graph, budget ,m, index):
    model_name = 'Balance_stage_2_'+str(index)
    samples = Mont_Carlo_Samplig(main_graph, m)
    objective_val = OPT(model_name, main_graph, samples, budget ,m)
    return objective_val 


# In[5]:


def MIP_IM(m, input_graph, output_file, log_file):
    budget = 25
    with open(input_graph, "rb") as f:
        main_graph = pickle.load(f)
        index = random.randint(0,100)
        objective_val = stage_1_MIP(main_graph, budget ,m, index)
        stage_2_MIP(main_graph, objective_val,  budget ,m, index, output_file, log_file, input_graph)


# In[6]:


def stage_2_MIP(main_graph, objective_val, budget ,m, index, output_file, log_file, input_graph):
    delta = 0.8
    samples =  Mont_Carlo_Samplig(main_graph, m)
    model_name = 'Balance_stage_2'+str(index)
    model = Model(model_name)
    model.setParam('OutputFlag', 0)
    model.setParam('TimeLimit', 3600)
        
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
            
            
    size_graph = float(1)/ float(len(main_graph.nodes()))
    mean_vars = []
    for ai in avars:
        mean_vars.append((size_graph,ai))
    mean_exp = LinExpr(mean_vars)

    model.addConstr(quicksum(svars), GRB.LESS_EQUAL, budget)

    for i in main_graph.nodes():
        avgai = []
        for sample_index, sample in enumerate(samples):
            if (sample.has_node(i)):
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
            di = model.addVar(lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS)
            dvars.append(di)
            avg_exp = quicksum(avgai)
            model.addConstr(di, GRB.GREATER_EQUAL, avg_exp - mean_exp)
            model.addConstr(di, GRB.GREATER_EQUAL, mean_exp - avg_exp)
            
    model.addConstr(quicksum(avars), GRB.GREATER_EQUAL, objective_val* delta)
    obj_expr = quicksum(dvars)         
    model.setObjective(obj_expr, GRB.MINIMIZE)
    
    try:
        model.optimize()
    except e:
        print(e) 
        
        
    objective_value = -1
        
    if (model.solCount>0):
        objective_value = model.ObjVal
        with open(output_file, "w") as of:    
            for key,value in var_seed_dict.items():
                if(value.x > 0):
                    print(key, file = of)

    with open(log_file, "w") as of:  
        runtime = model.Runtime
        status = model.Status
        print('runtime\t%f'%(runtime), file = of)
        print('objective_value\t%f'%(objective_value), file = of)
        print('status\t%d'%(status), file = of)
        print('sample_size\t%d'%(m), file = of)
        print('input_graph\t%s'%(input_graph), file = of)


# In[7]:


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('sample_size', type=int)
    parser.add_argument('input_graph', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('log_file', type=str)
    args = parser.parse_args()

    MIP_IM(args.sample_size, args.input_graph, args.output_file, args.log_file)

