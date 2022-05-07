import json
import requests
from time import sleep
from tqdm import tqdm

years = ["19", "20", "21"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
crawler_limit = 3.5

for year in years:
    for month in months:
        references = {}
        with open("../data/arxiv_id2title" + "/" + year + month + ".json", 'r', encoding='utf-8') as f:
            papers = json.load(f)

        for arxiv_id, title in tqdm(papers.items()):
            url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=references"
            response = requests.get(url)
            response_dict = json.loads(response.text)

            try:
                references[response_dict["paperId"]] = {}
                references[response_dict["paperId"]]["title"] = title
                references[response_dict["paperId"]]["references"] = response_dict["references"]
            except:
                print(f"arxiv_id: {arxiv_id} have error when searching on semantic scholar")

            sleep(crawler_limit)
        
        with open(f"../data/semantic_scholar/{year}{month}.json", 'w', encoding='utf-8') as f:
            json.dump(references, f, ensure_ascii=False, indent=4)

        sleep(180)