import json
from time import sleep
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm


base_url = "https://arxiv.org/list"
categorie = "cs.cl"
years = ["17", "18", "19", "20", "21"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
url = base_url + "/" + categorie + "/" 
crawler_limit = 3

for year in years:
    for month in tqdm(months):
        response = requests.get(url + year + month)
        soup = BeautifulSoup(response.text, "html.parser")

        
        # parse entry number
        start_index = str(soup.find_all("small")).index(" total of ") + len(" total of ")
        end_index = str(soup.find_all("small")).index(" entries")
        num_entry = str(soup.find_all("small"))[start_index: end_index]

        # query all entry
        response = requests.get(url + year + month + f"?show={num_entry}")
        print(url + year + month + f"?show={num_entry}")
        soup = BeautifulSoup(response.text, "html.parser")

        # parse id and title list
        paper_id_list = soup.find_all("a", {"title": "Abstract"})
        paper_title_list = soup.find_all("div", {"class": "list-title mathjax"})

        papers = {}
        for id, title in zip(paper_id_list, paper_title_list):
            papers[id.get_text().replace("arXiv:", "")] = title.get_text().replace("\nTitle: ", "").strip("\n")


        with open(f'../data/arxiv_id2title_{year}{month}.json', 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=4)

        sleep(crawler_limit)