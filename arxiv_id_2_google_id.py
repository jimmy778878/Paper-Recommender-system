import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

with open('arxiv_id2title.json') as f:
    papers = json.load(f)


data = {}
for arxiv_id in tqdm(papers.keys()):
    url = f"https://scholar.google.com/scholar_lookup?arxiv_id={arxiv_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    google_info = soup.select(f"a[href=\"https://arxiv.org/abs/{arxiv_id}\"]")
    google_info = str(google_info)

    start_index, end_index = 0, 0
    try:
        start_index = google_info.index("&amp;d=")
        end_index = google_info.index("&amp;ei")
    except:
        pass

    google_id = google_info[start_index + len("&amp;d="): end_index]
    data[arxiv_id] = google_id

with open('arxiv_id2google_id.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)