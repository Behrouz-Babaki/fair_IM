#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function, division
from gurobipy import Model, GRB, quicksum, LinExpr
import networkx as nx
import pickle
import numpy, random
import argparse
from MIP_DC import Mont_Carlo_Samplig, stage_1_MIP, induce_sub_graphs


# In[2]:


def MIP_IM(attribute, m, input_graph, output_file, log_file):
    budget = 25
    with open(input_graph, "rb") as f:
        main_graph = pickle.load(f)
        labels = nx.get_node_attributes(main_graph, attribute)
        label_dict = {}
        for i in range(len(main_graph.nodes())):
            label = labels[i].encode('utf-8')
            if label in label_dict.keys():
                label_dict[label].append(i)
            else:
                label_dict[label] = [i] 
        index = random.randint(0,100)
        opt_dict = stage_1_MIP(main_graph, label_dict, budget ,m, index)
        stage_2_MIP(main_graph, opt_dict, attribute, label_dict, budget ,m, index, output_file, log_file, input_graph)


# In[3]:


def stage_2_MIP(main_graph, opt_dict, attribute, label_dict, budget ,m, index, output_file, log_file, input_graph):
    samples =  Mont_Carlo_Samplig(main_graph, m)
    model_name = 'DC_stage_2'+str(attribute)+'_'+str(index)
    model = Model(model_name)
    model.setParam('OutputFlag', 0)
    model.setParam('TimeLimit', 3600)
        
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
            
    for label,node_labels in label_dict.items():
        label_vars = []
        for sample_index, sample in enumerate(samples): 
            for node in node_labels:
                label_vars.append(var_active_dict[(sample_index,neighbor)])
        expr = quicksum(label_vars)
        model.addConstr(expr, GRB.GREATER_EQUAL , opt_dict[label])    
    
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


# In[4]:


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('attribute', type=str)
    parser.add_argument('sample_size', type=int)
    parser.add_argument('input_graph', type=str)
    parser.add_argument('output_file', type=str)
    parser.add_argument('log_file', type=str)
    args = parser.parse_args()

    MIP_IM(args.attribute, args.sample_size, args.input_graph, args.output_file, args.log_file)

