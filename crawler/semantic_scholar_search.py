import json
import requests
from time import sleep
from tqdm import tqdm

years = ["17", "18", "19", "20", "21"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
crawler_limit = 3.5

for year in years:
    for month in months:
        with open("../data/arxiv_id2title" + "/" + year + month + ".json", 'r', encoding='utf-8') as f:
            papers = json.load(f)

        semantic_scholar_id2title = {}
        references = {}

        for arxiv_id, title in tqdm(papers.items()):
            url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=references"
            response = requests.get(url)
            response_dict = json.loads(response.text)
            try:
                semantic_scholar_id2title[response_dict["paperId"]] = title
                references[response_dict["paperId"]] = response_dict["references"]
            except:
                print(f"arxiv_id: {arxiv_id} have error when searching on semantic scholar")
            sleep(crawler_limit)

        with open("../data/semantic_scholar_id2title/" + year + month + ".json", 'w', encoding='utf-8') as f:
            json.dump(semantic_scholar_id2title, f, ensure_ascii=False, indent=4)

        with open("../data/reference/" + year + month + ".json", 'w', encoding='utf-8') as f:
            json.dump(references, f, ensure_ascii=False, indent=4)

