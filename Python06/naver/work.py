# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd

teacher_text=[]
name_text=[]
result={}

url = 'https://www.iei.or.kr'
raw = requests.get('https://www.iei.or.kr/intro/teacher.kh')
soup = BeautifulSoup(raw.text, 'html.parser')

#강사 이름 추출
name = soup.select('div.intro_txt > p.intro_name')
for name_list in name:
    name_text.append(name_list.text)

#강사 사진의 주소 추출
teacher = soup.select('div.intro_thum > img')
for teacher_list in teacher:
    teacher_text.append(url + teacher_list.get('src'))

result = {"name":name_text,"img":teacher_text}

df = pd.DataFrame(result)
df.to_json('teacher.json', orient='table', force_ascii = False)