from mpi4py import MPI


from collections import defaultdict
import numpy as np


from IDA import * 
#from display import *
from display import showChronogram
import sys
import csv
from multiprocessing import Pool
import time

# Open the file
path = "given_graphs/smallRandom.json"

G = Tree(f"./data/{path}",5)
sys.setrecursionlimit(100000)


# Making the calculation of the upper bound
tasks = G.tasks
sum =0
for task in tasks.values() :
    sum += task.time
percentage = 0.1
# Initializing the MPI interface and objects
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
# sz = 1
# double_size =  MPI.DOUBLE.Get_size()
# if rank == 0:
#     nbbytes = sz*double_size
# else:
#     nbbytes = 0
# win = MPI.Win.Allocate_shared(nbbytes,sz,comm=comm)
# buf,sz = win.Shared_query(0)
# upper_bound = np.ndarray(buffer=buf,dtype='d',shape=(sz,))
# upper_bound[0] = sum
# Verifying the number of processes
if size <= 1:
    raise ValueError("At least two processes are needed for this MPI architecture")
upper_bound = sum 
# Declaring the function 'search' to search for the solution
def search(node):
    sorted_children = sorted(G.children(node),key=lambda u:u.g+G.h(u))
    sorted_children = sorted_children[:max(int(len(sorted_children)*percentage),1)]
    for u in sorted_children:
        if u.g > upper_bound[0]:
            continue
        if G.is_terminal(u):
            upper_bound[0] = min(upper_bound[0],u.g)
            return u
        return search(u)
    return None


sorted_children = sorted(G.children(G.root),key=lambda u:u.g+G.h(u))
total_answers = []
process_answers = []


if rank == 0:
    # If the process is the mainly one (rank=0), it will wait
    # the calculations of the other processes.
    time_benchmarks = {}

    start = time.perf_counter()
    time_benchmarks["after building tree"] = time.perf_counter()
    for id in range(1,size):
        total_answers.append(comm.recv(source=id))
        
else:

    # If the process is not the mainly one (rank!=0), it will search
    # for possible solutions of the problem.


    for i in range((len(sorted_children)-rank)//(size-1)+1):    
        node_answer = search(sorted_children[i*(size-1)+rank-1])
        process_answers.append(node_answer)
    comm.send(process_answers,dest=0)

# After receive the answers of all processes, the mainly process
# will find the best solution.

if rank==0:
    solution = None
    for process_answers in total_answers:
        for node_answer in process_answers:
            if node_answer is None:
                continue
            else:
                if solution is None:
                    solution = node_answer
                elif node_answer.g < solution.g:
                    solution = node_answer
    time_benchmarks["end"] = time.perf_counter()
    showChronogram(list(solution.hist))
    with open('C:\\Users\\Vikos\\st7-graph-optimization\\data\\performance.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([path] + [v - start for v in (time_benchmarks.values())])
    
                







