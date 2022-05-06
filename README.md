## 系統簡介
* 這是一個利用論文之間相互引用的關係建立網路，並基於 community detection 與 link prediction 兩種網路演算法，所建立的簡易論文推薦系統。
* 給系統一篇你有興趣的論文，系統會給你幾篇推薦論文。

## 資料爬取
* 爬取 arxiv 指定類別的 paper，將 paper 的 arxiv id 與 title 保存下來。<br>
爬下來的資訊保存在 /data/arxiv_id2title/ 目錄下。
```
python /crawler/get_arxiv_paper.py
```

* 根據 paper 的 arxiv id 至 semantic scholar 爬取它所 reference 的 papers。
* 在這裡會產生三個 json 檔
  * /data/semantic_scholar_id2title.json，這是用來將 semantic scholar id 對應到 title
  * /data/title2semantic_scholar_id.json，這是用來將 title 對應到 semantic scholar id
  * /data/reference.json，這是用來建立 network 的 data，裡面每筆資料的格式為 (first paper id, second paper id)，代表 first paper 有 reference second paper
```
python /crawler/semantic_scholar_search.py
```
## 建立網路
* 利用 /data/reference.json 將每個 reference 關係當作是無項圖的一條邊，建立起一個網路
* 建立網路後，會使用 community detection 演算法將網路切割成一個個 communities
* 這邊會產生兩個 json 檔
  * /data/communities.json，這是用來紀錄每個 community 以下的資訊
    * community 內部的邊 (邊兩端的點皆在同個 community 內)
    * community 所含的點
  * /data/nodes2community.json，這是用來紀錄每個點位於哪個 community
```
python build_network.py
```

## 進行推薦預測
* 給定一篇自己有興趣的 paper 以及希望系統推薦的 paper 數量，讓系統進行推薦預測
* 系統首先偵測該 input paper 位於哪個 community ，接著讓該 community 中的所有 paper 皆與 input paper 利用 link prediction 演算法計算分數
* 將分數排序後，回傳結果
```
python analysis.py
```
