import json
import networkx as nx
import numpy as np
import time

def predict(title: str, top_n: int = 10):

    print(f"==================")
    print("predict")
    now = time.ctime()
    print(f"Start:{now}")

    with open("data/network_info/title2semantic_scholar_id.json", "r", encoding='utf-8') as f:
        title2paper_id = json.load(f)
    query_paper_id = title2paper_id[title]

    with open("data/network_info/nodes2community.json", "r", encoding='utf-8') as f:
        nodes2community = json.load(f)
    community_id = nodes2community[query_paper_id]

    with open("data/network_info/communities.json", "r", encoding='utf-8') as f:
        communities = json.load(f)

    # 根據輸入的 paper 找出它對應的 community，將該 community 建成一個小型 network
    graph = nx.Graph()
    for edge in communities[community_id]["edges"]:
        graph.add_edge(edge[0], edge[1])


    # 在這個小型 network 中執行 edge detection 演算法，計算每個 node 和輸入 node 相連的可能性    
    query_edges = [(query_paper_id, other_paper) for other_paper 
        in communities[community_id]["member"]]
    
    jc_preds = nx.jaccard_coefficient(graph, query_edges)
    aa_preds = nx.adamic_adar_index(graph, query_edges)

    # 將不同演算法預測結果整合
    mixed_preds = {}
    for preds in [jc_preds, aa_preds]:
        for _, other_paper_id, score in preds:
            if other_paper_id not in mixed_preds.keys(): 
                mixed_preds[other_paper_id] = score
            else:
                mixed_preds[other_paper_id] += score

    # 將預測結果排序並輸出
    mixed_preds = {k: v for k, v in sorted(mixed_preds.items(), key=lambda item: item[1], reverse=True)}
    mixed_preds_id = list(mixed_preds.keys())[:top_n]
    mixed_preds_score = list(mixed_preds.values())[:top_n]
    with open("data/network_info/semantic_scholar_id2title.json", "r", encoding='utf-8') as f:
        paper_id2title = json.load(f)
    mixed_preds_title = [paper_id2title[id] for id in mixed_preds_id]
    end = time.ctime()
    print(f"End:{end}")
    print(f"==================")
    return mixed_preds_title, mixed_preds_score

def predict_no_dection(title: str, top_n: int = 10):

    now = time.ctime()
    print(f"Start:{now}")

    with open("data/network_info/edges.json", "r", encoding='utf-8') as f:
        edges = json.load(f)
    
    graph = nx.Graph()
    
    for i, edge in enumerate(edges):
        graph.add_edge(edge[0], edge[1])


    with open("data/network_info/title2semantic_scholar_id.json", "r", encoding='utf-8') as f:
        title2paper_id = json.load(f)
    query_paper_id = title2paper_id[title]


    # 在這個大型 network 中執行 edge detection 演算法，計算每個 node 和輸入 node 相連的可能性
    query_edges = [(query_paper_id, other_paper) for other_paper 
        in graph[query_paper_id]]

    jc_preds = nx.jaccard_coefficient(graph, query_edges)
    aa_preds = nx.adamic_adar_index(graph, query_edges)

    # 將不同演算法預測結果整合
    mixed_preds = {}
    for preds in [jc_preds, aa_preds]:
        for _, other_paper_id, score in preds:
            if other_paper_id not in mixed_preds.keys(): 
                mixed_preds[other_paper_id] = score
            else:
                mixed_preds[other_paper_id] += score

    # 將預測結果排序並輸出
    mixed_preds = {k: v for k, v in sorted(mixed_preds.items(), key=lambda item: item[1], reverse=True)}
    mixed_preds_id = list(mixed_preds.keys())[:top_n]
    mixed_preds_score = list(mixed_preds.values())[:top_n]
    with open("data/network_info/semantic_scholar_id2title.json", "r", encoding='utf-8') as f:
        paper_id2title = json.load(f)
    mixed_preds_title = [paper_id2title[id] for id in mixed_preds_id]
    end = time.ctime()
    print(f"End:{end}")
    print(f"==================")
    return mixed_preds_title, mixed_preds_score

if __name__ == "__main__":
    title = "Masked Language Model Scoring"
    top_n = 10

    titles, scores = predict(title, top_n)
    # for title, score in zip(titles, scores):
    #     print(score, title)

    print("predict_no_dection")
    titles, scores = predict_no_dection(title, top_n)
    # for title, score in zip(titles, scores):
    #     print(score, title)