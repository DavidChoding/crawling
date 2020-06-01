# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import flask_cors
import re
import json
from konlpy.tag import Komoran
from collections import Counter
from konlpy import utils

from flask import Flask, render_template

app = Flask(__name__)
flask_cors.CORS(app)

#각 크롤링 결과 저장하기 위한 리스트
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}

#날짜 정제화 함수
def date_cleansing(test):
    try:
        #지난 뉴스
        #머니투데이  10면1단  2018.11.05.  네이버뉴스
        pattern = '\d+.(\d+).(\d+).'  #정규표현식
    
        r = re.compile(pattern)
        match = r.search(test).group(0)  # 2018.11.05
        date_text.append(match)
        
    except AttributeError:
        #최근 뉴스
        #이데일리  1시간 전  네이버뉴스   보내기
        pattern = '\w* (\d\w*)'     #정규표현식
        
        r = re.compile(pattern)
        match = r.search(test).group(1)
        #print(match)
        date_text.append(match)


#내용 정제화 함수
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                       first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)

# url mapping
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/crawling', methods=['GET'])
def crawling():
    
    #os.remove('templates/test.json')
    
    raw = requests.get("https://search.naver.com/search.naver?where=news&query=%EA%B0%9C%EB%B0%9C%EC%9E%90",headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(raw.text, 'html.parser')
        
    #본문요약본
    contents_lists = soup.select('ul.type01 dl')
    for contents_list in contents_lists:
        #print('==='*40)
        #print(contents_list)
        contents_cleansing(contents_list) #본문요약 정제화
        
    #모든 리스트 딕셔너리형태로 저장
    result= { "contents": contents_text }
    
    #resultJSON = json.dumps(result, ensure_ascii=False)
    df = pd.DataFrame(result)
    df.to_json('templates/itnews.json', orient='table', force_ascii = False)
    
    news = utils.read_txt('templates/itnews.json', encoding='ANSI')
    
    okt = Komoran()
    noun = okt.nouns(news)

    for i,v in enumerate(noun):
        if len(v)<2:
            noun.pop(i)

    count = Counter(noun)
    result = list()
    
    for i,v in count.most_common(10):
        insert_data = dict()
        insert_data = ({'tag': [i],'count': [v]})
        result.append(insert_data)
    
    res_dict = {'rank':result}
    api = json.dumps(res_dict, ensure_ascii=False)
    
    return api

if __name__ == '__main__':
    app.run('localhost', port='8585', debug=True)