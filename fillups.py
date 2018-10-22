# -*- coding: utf-8 -*-

#################################################
#            Crawler applied in CNKI            #
#                   Part    III                 #
#                   FILLUP                      #
#                    Oct 2018                   #  
#            Cheng Xie Fudan University         #
#################################################

import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

n2c_dict = {'中国证券报': 'CZJB', '光明日报': 'GMRB', '经济日报': 'JJRB', '科技日报': 'KJRB', '经济参考报': 'JJCK', '华夏时报': 'HXSB', '证券日报': 'CJRB', '证券时报': 'ZJSB', '上海证券报': 'SHZJ', '中国能源报': 'SHCA', '中国自然资源报': 'GTZY', '中国冶金报': 'CYJB', '中国电力报': 'CDLB', '中国煤炭报': 'CMTB', '中国石油报': 'SHYO', '中国贸易报': 'CMYB', '中国有色金属报': 'YSJS', '中国建材报': 'CJCB', '中国石化报': 'CSHB', '中国黄金报': 'ZGHJ', '中国矿业报': 'CKYB', '中煤地质报': 'ZMDZ', '中国工业报': 'CGYB', '华北电力报': 'HBDL', '地质勘查导报': 'DZKC', '石油管道报': 'SYGD', '铜陵有色报': 'TLYS', '期货日报': 'QHBR'}
path_table = 'E:/outcome1.csv'
df = pd.DataFrame.from_csv(path_table)
title_series = df['title']
url_par1 = 'http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CCND'
url_par2 = '&filename='
url_par3 = '&dbname='
url_part1 = 'http://kreader.cnki.net/Kreader/OpenFile.ashx?dbCode=CCND&doc='
url_part2 = '&tabelName='
url_part3 = '&format=png&uid=WEEvREcwSlJHSldRa1FhdkJkVWEyZnB6MDVwNnNGNGg2aG5YczlNb204dz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&page='
url_part4 = '&mpc=%202'
referer_part1 = 'http://kreader.cnki.net/Kreader/ReadPage.aspx?FileName='
referer_part2 = '&TableName='
referer_part3 = '&uid=WEEvREcwSlJHSldRa1FhdkJkVWEyZnB6MDVwNnNGNGg2aG5YczlNb204dz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&dbCode=CCND&cpn=1'
headers = {'Host': 'kreader.cnki.net',
'Proxy-Connection': 'keep-alive',
'Proxy-Authorization': 'Basic MTgyMTA2OTAxMDU6MTAyMDE3',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'}
pattern = re.compile('[\*\\\/:\?"<>\|]')
cookie_url = 'http://kreader.cnki.net/Kreader/ViewPage.aspx?dbCode=CCND&filename=CZJB20181010A020&tablename=CCNDPREP&uid='
login_url = 'http://login.cnki.net/login/?platform=kns&ForceReLogin=1&ReturnURL=http://www.cnki.net/'
driver = webdriver.Chrome()
k = 1
out_path = 'E:/out.csv'
def proc():
    driver.get(login_url)
    driver.find_element_by_xpath('//*[@id="TextBoxUserName"]').send_keys('18362928852')
    driver.find_element_by_xpath('//*[@id="TextBoxPwd"]').send_keys('K5462789m')
    driver.find_element_by_xpath('//*[@id="Button1"]').send_keys(Keys.ENTER)
    driver.get(cookie_url)
    driver.switch_to.window(driver.window_handles[-1])
    cookie = driver.get_cookies()
    cookies = {}
    cookies['Ecp_notFirstLogin'] = cookie[1]['value']
    cookies['Ecp_ClientId'] = cookie[6]['value']
    cookies['cnkiUserKey'] = cookie[5]['value']
    cookies['UM_distinctid'] = '1662a66fd9253-094fb4e3d288cf-36664c08-100200-1662a66fd944db'
    cookies['ASP.NET_SessionId'] = cookie[2]['value']
    cookies['SID'] = cookie[0]['value']
    cookies['Ecp_session'] = '1'
    cookies['LID'] = cookie[3]['value']
    cookies['c_m_LinID'] = cookie[7]['value']
    cookies['c_m_expire'] = cookie[8]['value']
    cookies['Ecp_LoginStuts'] = cookie[-1]['value']
    return cookies   

for item in title_series:
    if type(item) == float:
        doc = df.loc[k]['doc']
        table_name = df.loc[k]['table_name']
        url = url_par1 + url_par2 + doc + url_par3 + table_name
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        title_string = soup.find(name = 'h2').get_text()
        df.loc[k]['title'] = title_string
        cookies = proc()
        page = 1
        n = 1
        stop_flag = 0
        name = re.sub(pattern, '', title_string)
        referer = referer_part1 + doc + referer_part2 + table_name + referer_part3
        headers['Referer'] = referer
        while stop_flag == 0:
            url = url_part1 + doc + url_part2 + table_name + url_part3 + str(page) + url_part4
            page += 1
            r = requests.post(url = url, headers = headers, cookies = cookies)
            if len(r.content) == 17590:
                stop_flag = 1
                continue
            if r.status_code == 200:
                with open('E:/' + name + '_p' + str(n) + '.jpg', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
                n += 1
    k += 1
df.sort_index()
df.to_csv(out_path)