import json

years = ["17"]#, "18", "19", "20", "21"]
months = ["01"]#, "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

edges = []
for year in years:
    for month in months:
        with open("data/reference/" + year + month + ".json", "r", encoding='utf-8') as f:
            data = json.load(f)

            for paper_id, referenced_papers in data.items():
                for referenced_paper in referenced_papers:
                    if referenced_paper["paperId"] != None:
                        edges.append([paper_id, referenced_paper["paperId"]])

with open("data/edges.json", 'w', encoding='utf-8') as f:
    json.dump(edges, f, ensure_ascii=False, indent=4)
