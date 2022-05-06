import json

with open('papers.json') as f:
    papers = json.load(f)

google_paper_id = "12435779468187099335"
cite_url = f"https://scholar.google.com.tw/scholar?cites={google_paper_id}&as_sdt=2005&sciodt=0,5&hl=zh-TW"


for id, title in papers.items():
