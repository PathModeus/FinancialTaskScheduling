# import networkx as nx
# import matplotlib.pyplot as plt

# import display
# import IDA
# import parse

# G = parse.construct_graph_from_json("smallComplex.json")
# nx.draw(G,with_labels=True)
# plt.savefig("smallComplex.png")	

from IDA import * 
from display import showChronogram
import sys
import time
import csv

time_benchmarks = {}

start = time.perf_counter()

#just mention which graph you are using in this variable
path = "given_graphs/smallRandom.json"

G = Tree(f"./data/{path}",5)

time_benchmarks["after building tree"] = time.perf_counter()

sys.setrecursionlimit(100000)
tasks = G.tasks 
sum =0

for task in tasks.values() :
     sum += task.time

print("total sum is :",sum)


def search(node,upper_bound=sum):
    #print(node.__repr__())
    sorted_children = sorted(G.children(node),key=lambda u:u.g+G.h(u))
    #print(node.tasks_done_time)
    #print(G.children(node))
    for u in sorted_children:
        if u.g > upper_bound:
            continue
        if G.is_terminal(u):
            return u
        return search(u,upper_bound)
    return None

answer = search(G.root)

time_benchmarks["end"] = time.perf_counter()

if answer is not None :
    

    print("solution gives : ",answer.hist)
    showChronogram(list(answer.hist))
    
    with open('data/performance.csv', mode='a') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([path] + [v - start for v in (time_benchmarks.values())])
