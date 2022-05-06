# social-media-analytics-project

###########目錄結構
├── crawler                           // 爬蟲程式
│   ├── get_arxiv_paper.py            // 爬 arxiv 的 paper
│   ├── semantic_scholar_search.py    // 根據 arxiv paper id 到 semantic scholar 爬 paper 的reference
│
├── data
│   ├── arxiv_id2title                // 存放 arxiv 每月的 paper
│       ├── 1701.json 
│       ├── ...
│       ├── 2112.json
│   ├── communities.json
│   ├── nodes2community.json
│   ├── reference.json
│   ├── semantic_scholar_id2title.json
│   ├── title2semantic_scholar_id.json
