# -*- coding: utf-8 -*-
from konlpy.tag import Komoran
from collections import Counter
from konlpy import utils
import csv
#import json

# 크롤링 한 json 열기
# json 파일명은 extract에서 년월일.json으로 만들어짐
news = utils.read_txt('templates/2020529.json', encoding='ANSI')

okt = Komoran()
noun = okt.nouns(news)

# 명사의 글자가 하나인 것은 제외
# '올해'도 명사라고 합니다 ≒ 금년(今年)
for i,v in enumerate(noun):
    if len(v)<2:
        noun.pop(i)

count = Counter(noun)

# 명사 빈도 상위 10개
noun_list = count.most_common(10)
for v in noun_list:
    print(v)
    
# txt 파일로 저장
#with open("templates/rank.txt",'w',encoding='utf-8') as f:
#    for v in noun_list:
#        f.write(" ".join(map(str,v)))
#        f.write("\n")

# csv 파일로 저장
with open("templates/rank.csv","w",newline='',encoding='utf-8') as f:
    csvw = csv.writer(f)
    for v in noun_list:
        csvw.writerow(v)

# json 파일로 저장
#with open("templates/rank.json",'w',encoding='utf-8') as f :
#    json.dump(noun_list, f, ensure_ascii=False, sort_keys=False)