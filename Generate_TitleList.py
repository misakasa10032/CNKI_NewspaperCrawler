# -*- coding: utf-8 -*-

#################################################
#            Crawler applied in CNKI            #
#                    Sep 2018                   #  
#            Cheng Xie Fudan University         #
#################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd

#   The parameters for obtaining the articles
url_a = 'http://navi.cnki.net/knavi/NPaperDetail/GetArticleDataXsltByDate'
headers_a = {'Host': 'navi.cnki.net',
'Connection': 'keep-alive',
'Content-Length': '59',
'Accept': '*/*',
'Origin': 'http://navi.cnki.net',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://navi.cnki.net/KNavi/NPaperDetail?pcode=CCND&bzpym=CZJB'}
body_a0 = 'py=CZJB&pcode=CCND&pageIndex=1&pageSize=500&date='

#   The parameters for obtaining the dates
url_b = 'http://navi.cnki.net/knavi/NPaperDetail/GetDateGroupList'
headers_b = {'Host': 'navi.cnki.net',
'Connection': 'keep-alive',
'Content-Length': '28',
'Accept': '*/*',
'Origin': 'http://navi.cnki.net',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://navi.cnki.net/KNavi/NPaperDetail?pcode=CCND&bzpym=CZJB'}
body_b0 = 'py=CZJB&pcode=CCND&year='

#   Designate the start time and the end time. ATTENTION: The start time and end time must be business day.
start_time = '2013-01-04'
end_time = '2018-09-29'

#   Request for obtaining the source code underlying the dates
dict_ym = {}
def replace_slash(char):
    if '/' in char:
        char = char.replace('/', '-')
    else:
        pass
    return char
for year in range(2000, 2019):
    body_b = body_b0 + str(year)
    r_b = requests.post(url = url_b, data = body_b, headers = headers_b)
    String_b = BeautifulSoup(r_b.content.decode(), 'lxml')
    date_list = String_b.find_all(name = 'a', attrs = {'href': 'javascript:void(0);'})
    flag_0 = 0
    y_m = '1900-01'
    for date_a in date_list:
        date = replace_slash(date_a.string)
        y_m = replace_slash(y_m)
        if y_m != date[0:7]:
            y_m = date[0:7]
            dict_ym[y_m] = []
            dict_ym[y_m].append(date)
        else:
            dict_ym[y_m].append(date)

#   Ascertain the dates involved.
date_list = []
def add_zero(m):
    if m < 10:
        m = '0' + str(m)
    else:
        m = str(m)
    return m
for m_0 in range(int(start_time[5:7]), 13):
    if m_0 == int(start_time[5:7]):
        critical_index = dict_ym[start_time[0:7]].index(start_time)
        date_list.extend(dict_ym[start_time[0:7]][0:critical_index + 1])
    else:
        date_list.extend(dict_ym[start_time[0:4] + '-' + add_zero(m_0)][0: ])
for y_0 in range(int(start_time[0:4]) + 1, int(end_time[0:4])):
    for m_0 in range(1,13):
        date_list.extend(dict_ym[str(y_0) + '-' + add_zero(m_0)][0: ])
for m_0 in range(1, int(end_time[5:7]) + 1):
    if m_0 == int(end_time[5:7]):
        critical_index = dict_ym[end_time[0:7]].index(end_time)
        date_list.extend(dict_ym[end_time[0:7]][critical_index: ])
    else:
        date_list.extend(dict_ym[end_time[0:4] + '-' + add_zero(m_0)][0: ])

#   The name of the file must be in English
out_path = 'E:/outcome.csv'

#   Obtain titles, authors, sources
df = pd.DataFrame(columns = ['date', 'title', 'author', 'source'], index = ['date'])
k = 1
for date in date_list:
    body_a = body_a0 + str(date)
    r_a = requests.post(url = url_a, data = body_a, headers = headers_a)
    r = r_a.content.decode()
    soup = BeautifulSoup(r, 'lxml')
    for j in soup.find_all(name = 'tr')[1: ]:
        title = j.find(name = 'a', attrs = {'target': '_blank'}).string
        author = j.find_all(name = 'td')[3].string
        source = '中国证券报'
        df = df.append({'date': pd.to_datetime(date), 'title': title, 'author': author, 'source': source}, ignore_index = True)
    #   Exhibit the proceeding
    print(k/len(date_list))
    k += 1

#   The output
df.sort_index()
df = df.drop([0])
out_path = 'E:/ZGZQ_part2.csv'
df.to_csv(out_path)
            
