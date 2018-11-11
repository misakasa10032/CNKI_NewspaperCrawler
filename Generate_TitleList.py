# -*- coding: utf-8 -*-

#################################################
#            Crawler applied in CNKI            #
#                   Part    I                   #
#               Generate Title List             #
#                    Oct 2018                   #  
#            Cheng Xie Fudan University         #
#################################################

import requests
from bs4 import BeautifulSoup
import pandas as pd

#   The parameters for obtaining the articles
url_a = 'http://navi.cnki.net/knavi/NPaperDetail/GetArticleDataXsltByDate'
headers_a0 = {'Host': 'navi.cnki.net',
'Connection': 'keep-alive',
'Content-Length': '58',
'Accept': '*/*',
'Origin': 'http://navi.cnki.net',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://navi.cnki.net/KNavi/NPaperDetail?pcode=CCND&bzpym='}

#   The parameters for obtaining the dates
url_b = 'http://navi.cnki.net/knavi/NPaperDetail/GetDateGroupList'
headers_b0 = {'Host': 'navi.cnki.net',
'Connection': 'keep-alive',
'Content-Length': '28',
'Accept': '*/*',
'Origin': 'http://navi.cnki.net',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Referer': 'http://navi.cnki.net/KNavi/NPaperDetail?pcode=CCND&bzpym='}

'''   Designate the start time and the end time. ATTENTION: The start time and end time must be business day.
ADJUSTMENT NEEDED!!!'''
start_time = '2018-09-01'
end_time = '2018-10-10'

#   Designate the proxy. ATTENTION: The format is USER:PASSWORD@IP:PROT
proxies = {
    "http": "http://tc2002429:18je58r4@123.206.71.186:16818/",
}

#   Designate the map from name to code
n2c_dict = {'中国证券报': 'CZJB', '光明日报': 'GMRB', '经济日报': 'JJRB', '科技日报': 'KJRB', '经济参考报': 'JJCK', '华夏时报': 'HXSB', '证券日报': 'CJRB', '证券时报': 'ZJSB', '上海证券报': 'SHZJ', '中国能源报': 'SHCA', '中国自然资源报': 'GTZY', '中国冶金报': 'CYJB', '中国电力报': 'CDLB', '中国煤炭报': 'CMTB', '中国石油报': 'SHYO', '中国贸易报': 'CMYB', '中国有色金属报': 'YSJS', '中国建材报': 'CJCB', '中国石化报': 'CSHB', '中国黄金报': 'ZGHJ', '中国矿业报': 'CKYB', '中煤地质报': 'ZMDZ', '中国工业报': 'CGYB', '华北电力报': 'HBDL', '地质勘查导报': 'DZKC', '石油管道报': 'SYGD', '铜陵有色报': 'TLYS', '期货日报': 'QHBR'}

def replace_slash(char):
    if '/' in char:
        char = char.replace('/', '-')
    else:
        pass
    return char

def add_zero(m):
    if m < 10:
        m = '0' + str(m)
    else:
        m = str(m)
    return m

'''   The name of the file must be in English
ADJUSTMENT NEEDED!!!'''
out_path = 'E:/outcome.csv'

#   Obtain titles, authors, sources
df = pd.DataFrame(columns = ['date', 'title', 'author', 'source', 'doc', 'table_name'], index = ['date'])
k = 1

'''   Designate the name of the newspaper
ADJUSTMENT NEEDED!!!'''
news = '中国证券报'

#   Request for obtaining the source code underlying the dates
dict_ym = {}
#   ADJUSTMENT MIGHT BE NEEDED!!!
for year in range(2000, 2019):
    body_b = 'py=' + n2c_dict[news] + '&pcode=CCND&year=' + str(year)
    headers_b = headers_b0
    headers_b['Referer'] = headers_b['Referer'] + n2c_dict[news]
    r_b = requests.post(url = url_b, data = body_b, headers = headers_b, proxies = proxies)
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
if start_time[0:4] != end_time[0:4]:
    for m_0 in range(int(start_time[5:7]), 13):
        if m_0 == int(start_time[5:7]):
            critical_index = dict_ym[start_time[0:7]].index(start_time)
            date_list.extend(dict_ym[start_time[0:7]][0:critical_index + 1])
        else:
            if start_time[0:4] + '-' + add_zero(m_0) in dict_ym.keys():
                date_list.extend(dict_ym[start_time[0:4] + '-' + add_zero(m_0)][0: ])
    for y_0 in range(int(start_time[0:4]) + 1, int(end_time[0:4])):
        for m_0 in range(1,13):
            if str(y_0) + '-' + add_zero(m_0) in dict_ym.keys():
                date_list.extend(dict_ym[str(y_0) + '-' + add_zero(m_0)][0: ])
    for m_0 in range(1, int(end_time[5:7]) + 1):
        if m_0 == int(end_time[5:7]):
            critical_index = dict_ym[end_time[0:7]].index(end_time)
            date_list.extend(dict_ym[end_time[0:7]][critical_index: ])
        else:
            if end_time[0:4] + '-' + add_zero(m_0) in dict_ym.keys():
                date_list.extend(dict_ym[end_time[0:4] + '-' + add_zero(m_0)][0: ])
elif start_time[0:7] != end_time[0:7]:
    critical_index = dict_ym[start_time[0:7]].index(start_time)
    date_list.extend(dict_ym[start_time[0:7]][0:critical_index + 1])
    for m_0 in range(int(start_time[5:7]) + 1, int(end_time[5:7])):
        date_list.extend(dict_ym[start_time[0:4] + '-' + add_zero(m_0)][0: ])
    critical_index = dict_ym[end_time[0:7]].index(end_time)
    date_list.extend(dict_ym[end_time[0:7]][critical_index: ])
else:
    critical_index0 = dict_ym[start_time[0:7]].index(start_time)
    critical_index1 = dict_ym[end_time[0:7]].index(end_time)
    date_list.extend(dict_ym[start_time[0:7]][critical_index1: critical_index0 + 1])

#   Capture the titles
for date in date_list:
    body_a = 'py=' + n2c_dict[news] + '&pcode=CCND&pageIndex=1&pageSize=500&date=' + str(date)
    headers_a = headers_a0
    headers_a['Referer'] = headers_a0['Referer'] + n2c_dict[news]
    r_a = requests.post(url = url_a, data = body_a, headers = headers_a, proxies = proxies)
    r = r_a.content.decode()
    soup = BeautifulSoup(r, 'lxml')
    for j in soup.find_all(name = 'tr')[1: ]:
        title = j.find(name = 'a', attrs = {'target': '_blank'}).string
        author = j.find_all(name = 'td')[3].string
        source = news
        href = j.find(name = 'a', attrs = {'target': '_blank'})['href'].strip()
        doc = href[51:67]
        table_name = href[78: ]
        df = df.append({'date': pd.to_datetime(date), 'title': title, 'author': author, 'source': source, 'doc': doc, 'table_name': table_name}, ignore_index = True)
    #   Exhibit the proceeding
    print(k/len(date_list))
    k += 1

#   The output
df.sort_index()
df = df.drop([0])
df.to_csv(out_path)
