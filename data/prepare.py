import json

years = ["17", "18", "19", "20", "21"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
title2semantic_scholar_id = {}
semantic_scholar_id2title = {}
edges = []

for year in years:
    for month in months:
        with open(f"semantic_scholar/{year}{month}.json", 'r', encoding='utf-8') as f:
            papers = json.load(f)

        for paper_id, paper_info in papers.items():
            title2semantic_scholar_id[paper_info["title"]] = paper_id
            semantic_scholar_id2title[paper_id] = paper_info["title"]

            for referenced_paper in paper_info["references"]:
                if referenced_paper["paperId"] == None: continue

                title2semantic_scholar_id[referenced_paper["title"]] = \
                    referenced_paper["paperId"]
                semantic_scholar_id2title[referenced_paper["paperId"]] = \
                    referenced_paper["title"]
                edges.append([paper_id, referenced_paper["paperId"]])


with open("../data/network_info/title2semantic_scholar_id.json", 'w', encoding='utf-8') as f:
    json.dump(title2semantic_scholar_id, f, ensure_ascii=False, indent=4)

with open("../data/network_info/semantic_scholar_id2title.json", 'w', encoding='utf-8') as f:
    json.dump(semantic_scholar_id2title, f, ensure_ascii=False, indent=4)

with open("../data/network_info/edges.json", 'w', encoding='utf-8') as f:
    json.dump(edges, f, ensure_ascii=False, indent=4)