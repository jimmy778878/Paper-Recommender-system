# !/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from analysis import predict
import networkx
import sys
import json
import string
app = Flask(__name__)

@app.route("/")
def home():
    res = {}
    return render_template('index.html', res=res)

# http://127.0.0.1:5000/search/?key=angiosarcoma


@app.route("/search/", methods=['GET'])
def search():
    key = request.args.get('key')
    
    tmp = key.split('?')
    query = tmp[0]
    topn = int(tmp[1].split('=')[1])

    title, score = predict(query, topn)

    output_papers = []
    for title, score in zip(title, score):
        output_papers.append(title)

    return dictHTML(output_papers)

def dictHTML(papers):
    article = ""

    for title in papers:
        article += "<h4>" + title + "<h4>"

    # return out + "</p>"
    return render_template('article.html', ar=article)


if __name__ == '__main__':
    app.debug = True
    app.run()
