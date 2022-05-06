import json
import requests
from time import sleep
from tqdm import tqdm

years = ["17", "18", "19", "20", "21"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
crawler_limit = 3.5

semantic_scholar_id2title = {}
references = []
for year in years:
    for month in months:
        with open("../data/arxiv_id2title" + "/" + year + month + ".json", 'r', encoding='utf-8') as f:
            papers = json.load(f)

        for arxiv_id, title in tqdm(papers.items()):
            url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=references"
            response = requests.get(url)
            response_dict = json.loads(response.text)

            try:
                semantic_scholar_id2title[response_dict["paperId"]] = title
                for referenced_paper in response_dict["references"]:
                    if referenced_paper["paperId"] != None:
                        semantic_scholar_id2title[referenced_paper["paperId"]] = \
                            referenced_paper["title"]
                        references.append([response_dict["paperId"], referenced_paper["paperId"]])
            except:
                print(f"arxiv_id: {arxiv_id} have error when searching on semantic scholar")

            sleep(crawler_limit)

with open("../data/semantic_scholar_id2title.json", 'w', encoding='utf-8') as f:
    json.dump(semantic_scholar_id2title, f, ensure_ascii=False, indent=4)

title2semantic_scholar_id = {}
for id, title in semantic_scholar_id2title.items():
    title2semantic_scholar_id[title] = id
with open("../data/title2semantic_scholar_id.json", 'w', encoding='utf-8') as f:
    json.dump(title2semantic_scholar_id, f, ensure_ascii=False, indent=4)

with open("../data/reference.json", 'w', encoding='utf-8') as f:
    json.dump(references, f, ensure_ascii=False, indent=4)