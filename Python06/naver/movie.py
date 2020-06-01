# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import flask_cors

from flask import Flask, render_template
app = Flask(__name__)
flask_cors.CORS(app)

# url mapping
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/crawling')
def crawling():
    # naver movie list를 crawling
    raw = requests.get("https://movie.naver.com/movie/running/current.nhn",
                   headers = {"User-Agent" : "Mozilla/5.0"})
    html = BeautifulSoup(raw.text, 'html.parser')
    
    # crawling된 데이터를 list에 담고
    # dictionary에 {title:제목, star:별점} 담기
    movies = html.select("dl.lst_dsc")
    
    result = list()
    for movie in movies:
        
        tmp = dict()
        tmp['title'] = movie.select_one("dt.tit a").text
        tmp['star'] = movie.select_one("a span.num").text
        result.append(tmp)
        
    res_dict = {'movies':result}
    
    api = json.dumps(res_dict, ensure_ascii=False)
    
    return api



if __name__ == '__main__':
    app.run('localhost', port='8585')