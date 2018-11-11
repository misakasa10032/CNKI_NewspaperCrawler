# -*- coding: utf-8 -*-

#################################################
#            Crawler applied in CNKI            #
#                   Part    II                  #
#                Capture  Article               #
#                    Oct 2018                   #  
#            Cheng Xie Fudan University         #
#################################################

import requests
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

#   Designate the proxy. ATTENTION: The format is USER:PASSWORD@IP:PROT
proxies = {
    "http": "http://tc2002429:18je58r4@123.206.71.186:16818/",
}

pattern = re.compile('[\*\\\/:\?"<>\|\r\n]')
cookie_url = 'http://kreader.cnki.net/Kreader/ViewPage.aspx?dbCode=CCND&filename=CZJB20181010A020&tablename=CCNDPREP&uid='
login_url = 'http://login.cnki.net/login/?platform=kns&ForceReLogin=1&ReturnURL=http://www.cnki.net/'
driver = webdriver.Chrome()

#   ADJUSTMENT NEEDED!!!
file_path = 'D:/SHZQB.csv'

df = pd.DataFrame.from_csv(file_path)

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
    t = time.time()
    return cookies, t

ta = time.time()
start_num = 1
end_num = len(df) + 1
for k in range(start_num, end_num):
    t_gap = time.time() - ta
    if (k == start_num or t_gap >= 1200):
        cookies = proc()[0]
        ta = proc()[1]
    page = 1
    n = 1
    stop_flag = 0
    doc = df.loc[k]['doc']
    table_name = df.loc[k]['table_name']
    name = re.sub(pattern, '', str(df.loc[k]['title']))
    referer = referer_part1 + doc + referer_part2 + table_name + referer_part3
    headers['Referer'] = referer
    while stop_flag == 0:
        url = url_part1 + doc + url_part2 + table_name + url_part3 + str(page) + url_part4
        page += 1
        r = requests.post(url = url, headers = headers, cookies = cookies, proxies = proxies)
        if len(r.content) == 17590:
            stop_flag = 1
            continue
        if r.status_code == 200:
            with open('E:/' + name + '_p' + str(n) + '.jpg', 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            n += 1
    print(str(k) + ' is OK')
