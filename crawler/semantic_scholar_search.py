import json
import ast
import requests
from time import sleep
from bs4 import BeautifulSoup
from tqdm import tqdm

with open('arxiv_id2title.json') as f:
    papers = json.load(f)


semantic_scholar_id2title = {}
references = {}
crawler_limit = 3
for arxiv_id, title in tqdm(papers.items()):
    url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=references"
    response = requests.get(url)
    response_dict = json.loads(response.text)
    semantic_scholar_id2title[response_dict["paperId"]] = title
    references[response_dict["paperId"]] = response_dict["references"]
    
    sleep(crawler_limit)

with open('semantic_scholar_id2title.json', 'w', encoding='utf-8') as f:
    json.dump(semantic_scholar_id2title, f, ensure_ascii=False, indent=4)

with open('references.json', 'w', encoding='utf-8') as f:
    json.dump(references, f, ensure_ascii=False, indent=4)