import json
import networkx as nx
import numpy as np

def predict(title: str, top_n: int = 10):
    with open("data/title2semantic_scholar_id.json", "r", encoding='utf-8') as f:
        title2paper_id = json.load(f)
    query_paper_id = title2paper_id[title]

    with open("data/nodes2community.json", "r", encoding='utf-8') as f:
        nodes2community = json.load(f)
    community_id = nodes2community[query_paper_id]

    with open("data/communities.json", "r", encoding='utf-8') as f:
        communities = json.load(f)

    graph = nx.Graph()
    for edge in communities[community_id]["edges"]:
        graph.add_edge(edge[0], edge[1])
    
    preds = nx.jaccard_coefficient(
        graph,
        [(query_paper_id, other_paper) for other_paper 
        in communities[community_id]["member"]]
    )

    preds = {other_paper_id: score for _, other_paper_id, score in preds}
    preds = {k: v for k, v in sorted(preds.items(), key=lambda item: item[1])}
    preds = list(preds.keys())[:top_n]
    with open("data/semantic_scholar_id2title.json", "r", encoding='utf-8') as f:
        paper_id2title = json.load(f)
    return [paper_id2title[pred] for pred in preds]


if __name__ == "__main__":
    title = "Deep learning for computational biology"
    top_n = 10
    recommends = predict(title, top_n)
    for recommend in recommends:
        print(recommend)