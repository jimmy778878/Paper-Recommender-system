import json
import networkx as nx
import numpy as np

def predict(title: str, top_n: int = 10):
    with open("data/network_info/title2semantic_scholar_id.json", "r", encoding='utf-8') as f:
        title2paper_id = json.load(f)
    query_paper_id = title2paper_id[title]

    with open("data/network_info/nodes2community.json", "r", encoding='utf-8') as f:
        nodes2community = json.load(f)
    community_id = nodes2community[query_paper_id]
    print(community_id)
    with open("data/network_info/communities.json", "r", encoding='utf-8') as f:
        communities = json.load(f)

    graph = nx.Graph()
    for edge in communities[community_id]["edges"]:
        graph.add_edge(edge[0], edge[1])
    
    query_edges = [(query_paper_id, other_paper) for other_paper 
        in communities[community_id]["member"]]

    jc_preds = nx.jaccard_coefficient(graph, query_edges)
    aa_preds = nx.adamic_adar_index(graph, query_edges)

    mixed_preds = {}
    for preds in [jc_preds, aa_preds]:
        for _, other_paper_id, score in preds:
            if other_paper_id not in mixed_preds.keys(): 
                mixed_preds[other_paper_id] = score
            else:
                mixed_preds[other_paper_id] += score

    mixed_preds = {k: v for k, v in sorted(mixed_preds.items(), key=lambda item: item[1], reverse=True)}
    mixed_preds_id = list(mixed_preds.keys())[:top_n]
    mixed_preds_score = list(mixed_preds.values())[:top_n]
    with open("data/network_info/semantic_scholar_id2title.json", "r", encoding='utf-8') as f:
        paper_id2title = json.load(f)
    mixed_preds_title = [paper_id2title[id] for id in mixed_preds_id]
    return mixed_preds_title, mixed_preds_score


if __name__ == "__main__":
    title = "Masked Language Model Scoring"
    top_n = 10
    title, score = predict(title, top_n)
    for title, score in zip(title, score):
        print(score, title)