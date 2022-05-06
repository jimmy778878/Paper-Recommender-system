import json
import matplotlib.pyplot as plt 
import networkx as nx
import networkx.algorithms.community as nx_comm

with open("data/edges.json", "r", encoding='utf-8') as f:
    edges = json.load(f)

graph = nx.Graph()

print("building network ...")
for i, edge in enumerate(edges):
    graph.add_edge(edge[0], edge[1])
print("build network finish ...")


print("runing community partition algorithm")
communities = nx_comm.louvain_communities(graph, seed=487)
