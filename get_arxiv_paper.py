import json
import requests
import json
from bs4 import BeautifulSoup

base_url = "https://arxiv.org/list"
categorie = "cs.cl"
time = "1801"
url = base_url + "/" + categorie + "/" + time

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


paper_id_list = soup.find_all("a", {"title": "Abstract"})
paper_title_list = soup.find_all("div", {"class": "list-title mathjax"})

papers = {}
for id, title in zip(paper_id_list, paper_title_list):
	papers[id.get_text().replace("arXiv:", "")] = title.get_text().replace("\nTitle: ", "").strip("\n")


with open('arxiv_id2title.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, ensure_ascii=False, indent=4)