# -*- coding: utf-8 -*-

#################################################
#            Crawler applied in CNKI            #
#                   Part    II                  #
#                Capture  Article               #
#                    Sep 2018                   #  
#            Cheng Xie Fudan University         #
#################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

#   Before running the program, you have to check the access to CNKI
url_0 = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CCND'
driver = webdriver.Chrome()
driver.get(url_0)
m = driver.find_element_by_id('txt_1_sel')
m.find_element_by_xpath("//option[@value = 'TI']").click()
file_path = 'E:/ZGZQB.csv'
df = pd.DataFrame.from_csv(file_path)
for item in df['title']:
    driver.find_element_by_xpath('//*[@id="txt_1_value1"]').send_keys(item)
    driver.find_element_by_xpath('//*[@id="btnSearch"]').send_keys(Keys.ENTER)
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_id('iframeResult'))
    driver.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/a').click()
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element_by_xpath('//*[@id="pdfDown"]').send_keys(Keys.ENTER)
    close_flag = 0
    while close_flag == 0:
        if len(driver.window_handles) > 2:
            time.sleep(1)
            driver.close()
            close_flag = 1
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath('//*[@id="txt_1_value1"]').clear()
