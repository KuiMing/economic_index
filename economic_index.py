from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
from glob import glob
import json
import os
import wget

def get_base_year(x):
    try:
        return x[:4]
    except:
        return None
    
def get_index_latest(response, pid):
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all('div', id='content')
    content = content[0].find_all('p')
    year_month = (datetime.strptime(str(content[3]).split(': ')[1].replace('</p>', ''), '%A, %B %d, %Y') - \
    relativedelta(months=1)).strftime("%Y%m")
    cbi = []
    for i in content:
        if i.find('strong'):
            cbi.append(i)

    content = pd.DataFrame({'content':cbi})
    content['content'] = content.content.astype(str)
    content['year_month'] = year_month
    content['base_year'] = content.content.str.extract('([0-9]{4}\s*=\s*100)')
    content['base_year'] = content.base_year.apply(get_base_year)
    content['economic'] = content.content.str.extract('(The Conference Board [A-Z]{1}[a-z]+ Economic Index)')
    content['economic'] = content.economic.str.lower()
    content = content.dropna()
    content.loc[content.economic.str.contains('coincident'), 'economic'] = 'coincident'
    content.loc[content.economic.str.contains('lagging'), 'economic'] = 'lagging'
    content.loc[content.economic.str.contains('leading'), 'economic'] = 'leading'
    content['economic_index'] = content.content.str.extract('([0-9]*[0-9]+[0-9]+.[0-9]{1})')
    content = content.dropna().drop(columns='content').drop_duplicates()
    content['pid'] = pid
    return content

def trans_datetime(x):
    return datetime.strptime(x, '%Y%m')

url = "https://www.conference-board.org/data/bcicountry.cfm"

querystring = {"cid":"1"}

payload = ""
headers = {
    'Host': "www.conference-board.org",
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-User': "?1",
    'Sec-Fetch-Dest': "document",
    'Referer': "https://www.conference-board.org/data/bciarchive.cfm?cid=1",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
    'Cookie': "__utma=220225290.1709580832.1590985503.1590985503.1590985503.1; __utmc=220225290; __utmz=220225290.1590985503.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.2.1709580832.1590985503; _mkto_trk=id:225-WBZ-025&token:_mch-conference-board.org-1590985503172-85844; CFID=Zms0gj7vaxh7azbmtslyjrq5fol3o85r9eq8nsdl3w6qaa84cy-162955667; CFTOKEN=Zms0gj7vaxh7azbmtslyjrq5fol3o85r9eq8nsdl3w6qaa84cy-4ffaeb43e9ce81-5F55FEA5-098E-7B21-714F2487211CBDF2; feathr_session_id=5edb875b42400060327008c3; _gid=GA1.2.1488988923.1591445341; SHB=1",
    'cache-control': "no-cache",
    'Postman-Token': "9dc51ba1-32bd-4432-9fba-e2fd7b90aa42"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

index_latest = get_index_latest(response, "")
index_latest['datetime'] = index_latest.year_month.apply(trans_datetime)
index_latest['economic_index'] = index_latest.economic_index.astype(float)
index_latest['base_year'] = index_latest.base_year.astype(int)
index_latest['datetime'] = index_latest.datetime.astype(str)
index_latest = index_latest[['base_year', 'datetime', 'economic', 'economic_index', 'pid', 'year_month']]
index_latest.to_csv('economic_index_adjusted.csv', mode='a', index=False, header=False)
