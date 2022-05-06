import json
import networkx as nx
import networkx.algorithms.community as nx_comm

with open("data/reference.json", "r", encoding='utf-8') as f:
    edges = json.load(f)

graph = nx.Graph()

print("building network ...")
for i, edge in enumerate(edges):
    graph.add_edge(edge[0], edge[1])
print("build network finish.")


print("runing community partition algorithm ...")
communities = nx_comm.louvain_communities(graph, seed=487)
print("community partition algorithm finish.")


communities_info = {}
nodes2community = {}
for community_id, community in enumerate(communities):

    community_edges = set()
    for node_i in community:
        neighbors = graph.neighbors(node_i)
        for node_j in neighbors:
            if node_j in community:
                community_edges.add(
                    (node_i, node_j) if node_i < node_j else (node_j, node_i)
                )
        nodes2community[node_i] = str(community_id)

    communities_info[community_id] = {
        "edges": list(community_edges),
        "member": list(community)
    }

with open("data/communities.json", 'w', encoding='utf-8') as f:
    json.dump(communities_info, f, ensure_ascii=False, indent=4)
with open("data/nodes2community.json", 'w', encoding='utf-8') as f:
    json.dump(nodes2community, f, ensure_ascii=False, indent=4)