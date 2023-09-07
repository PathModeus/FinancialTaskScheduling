# import networkx as nx
# import matplotlib.pyplot as plt



# G = parse.construct_graph_from_json("smallComplex.json")
# nx.draw(G,with_labels=True)
# plt.savefig("smallComplex.png")
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

from collections import defaultdict
import numpy as np
from multiprocessing.managers import BaseManager, DictProxy

#MyManager.register('defaultdict', defaultdict, DictProxy)

from IDA import * 
from display import *
import sys
from multiprocessing import Pool
import time
G = Tree("/home/aymanelotfi/st7-graph-optimization/data/given_graphs/smallComplex.json",5)
sys.setrecursionlimit(100000)
tasks = G.tasks 
sum =0
for task in tasks.values() :
    sum += task.time

upper_bound=sum
assert (size>1),"At least two processes are needed for this MPI architecture"
def search(node):
    sorted_children = sorted(G.children(node),key=lambda u:u.g+G.h(u))
    for u in sorted_children:
        if u.g > upper_bound:
            continue
        if G.is_terminal(u):
            return u
        return search(u)
    return None
answer = None
sorted_children = sorted(G.children(G.root),key=lambda u:u.g+G.h(u))
ans_list = []
if rank == 0:
    while True:
        comm.recv(ans_list) 
        
else:
    for i in range((len(sorted_children)-rank)//(size-1)+1):    
        answer = search(sorted_children[i*(size-1)+rank-1])
        comm.Send(answer,dest=0)


if rank == 0:
    print("total sum is :",sum)
    start = time.time()
    end = time.time() - start
    print('\n\n\n',end,'\n\n\n')
    sol = None
    for ans in ans_list:
        if ans is not None:
            if sol is None:
                sol = ans
            elif ans.g < sol.g:
                sol = ans
    #answer = search(G.root)

    if sol is not None :
        #print("solution gives : ",sol.hist)
        showChronogram(list(sol.hist))
