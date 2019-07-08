#!/usr/bin/env python
# coding: utf-8


import json, os, shutil

with open('./mapping.json') as f:
    mapping = json.load(f)
    
attributes = set()
for _, v in mapping.items():
    attributes.add(v['attribute'])
    
print(attributes)


TDIR = os.path.abspath('../tree/')
if not os.path.isdir(TDIR):
    os.mkdir(TDIR)

for d in ('output', 'log'):
    dir1 = os.path.join(TDIR, d)
    if not os.path.isdir(dir1):
        os.mkdir(dir1)
    for a in attributes:
        dir2 = os.path.join(dir1, a)
        if not os.path.isdir(dir2):
            os.mkdir(dir2)


RDIR = os.path.abspath('../results/')

for _, v in mapping.items():
    attribute = v['attribute']
    job_id = v['job_id']
    graph_index = v['graph_index']
    
    logfile_src = os.path.join(RDIR, 'log_%d.txt'%job_id)
    outfile_src = os.path.join(RDIR, 'output_%d.txt'%job_id)
    assert(os.path.isfile(logfile_src))
    assert(os.path.isfile(outfile_src))
    
    logfile_dest = os.path.join(TDIR, 'log', attribute, 'log_%d.txt'%graph_index)
    outfile_dest = os.path.join(TDIR, 'output', attribute, 'output_%d.txt'%graph_index)
    
    shutil.copy2(logfile_src, logfile_dest)
    shutil.copy2(outfile_src, outfile_dest)

