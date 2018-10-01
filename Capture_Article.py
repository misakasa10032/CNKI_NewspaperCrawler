# -*- coding: utf-8 -*-

#################################################
#            Crawler applied in CNKI            #
#                    Sep 2018                   #  
#            Cheng Xie Fudan University         #
#################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

username = '94035008115874'
password = '962145'
url_0 = 'http://www.797g.cn/e/member/login/'
driver = webdriver.Chrome()
driver.get(url_0)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(username)
driver.find_element_by_xpath('//*[@id="username"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="maincolumn"]/div[1]/div[2]/table/tbody/tr[5]/td[2]/input').send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/a[6]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="maincolumn"]/div[2]/div[2]/span[2]/a').click()
time.sleep(1)
driver.close()
driver.switch_to.window(driver.window_handles[-1])
driver.find_element_by_xpath('/html/body/center/div/a[1]').click()
driver.switch_to.frame(driver.find_element_by_id('iframeResult'))
driver.find_element_by_xpath('/html/body/div/ul[1]/li[10]/h4/a')
url_1 = 'http://sg.ab22.top:90/kns/brief/result.aspx?dbPrefix=CCND'
driver.get(url_1)
m = driver.find_element_by_id('txt_1_sel')
m.find_element_by_xpath("//option[@value = 'TI']").click()
file_path = 'E:/ZGZQB.csv'
df = pd.DataFrame.from_csv(file_path)
for item in df['title']:
    driver.find_element_by_xpath('//*[@id="txt_1_value1"]').send_keys(item)
    driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_id('iframeResult'))
    driver.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a').click()
    driver.switch_to.window(driver.window_handles[-1])
    close_flag = 0
    while close_flag == 0:
        if driver.title == '载入成功！':
            driver.close()
            close_flag = 1
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath('//*[@id="txt_1_value1"]').clear()