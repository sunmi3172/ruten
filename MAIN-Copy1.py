#!/usr/bin/env python
# coding: utf-8

# In[6]:


from selenium import webdriver
import bs4 as bs

import sys
import time
import os
import csv
import re
import pandas as pd


# In[12]:


chrome_path = "./chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
driver = webdriver.Chrome(chrome_path)
driver.get("https://www.ruten.com.tw/")

list_ = ["iphone充電線"]
result = [[] for _ in range(30)]
num_page = 2
num_product = 10

###  define 研究的產品 (罐頭)

for name_reach in list_ :
    ### 搜尋名稱
    driver.find_element_by_xpath("//input[@id='keyword']").send_keys(name_reach)
    ### 搜尋
    driver.find_element_by_xpath("//input[@class='rt-header-search-submit']").click()
    
    ### 切換顯示方式
    driver.find_element_by_xpath("//a[contains(@class,'list')]").click()
    
    for next_page in range(num_page):
        print(f"Now on page {next_page}")
        time.sleep(3)
        soup = bs.BeautifulSoup(driver.find_element_by_xpath("//*").get_attribute("outerHTML"), 'html.parser')
        #商品ID 80個
        ID=[]
        for a in soup.find_all('dl','col3f'):
            ID.append(a.get('_id'))
        #廣告/優先
        AD = list(map(lambda x: x.text,soup.find_all('span', class_='ads_tag')))[:num_product]
        #紅黃框
        RY=[]
        for a in soup.find_all('dl','col3f'):
            RY.append(a.get('class'))
        #追蹤人數
        Trace = list(map(lambda x: x.text,soup.find_all(title=re.compile('追蹤清單'))))[:num_product]
        
        result[20].extend(ID)
        result[21].extend(AD)
        result[22].extend(RY)
        result[23].extend(Trace)
        
        for product in range(1, num_product + 1):
            print(f"Now on page {product}")
            ### click each product
            time.sleep(3)
            driver.find_element_by_xpath(
                "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/dl[1]/dd[1]/dl[{}]/dd[1]/div[1]/a[1]/img[1]".format(product)).click()
            
            time.sleep(3)
            ### switch to current page 
            hand = driver.window_handles

            driver.switch_to_window(hand[1])
            
            #page = driver.current_url
            #page = Page(driver.current_url)
            soup = bs.BeautifulSoup(driver.find_element_by_xpath("//*").get_attribute("outerHTML"), 'html.parser')
            ######################################
            #產品名
            result[0].append(soup.find('span', class_='vmiddle').text)
            #圖片數
            imag = soup.find('ul', class_='item-gallery-thumbnail-list js-img-list')
            result[1].append(len (imag))
            #商品編號
            result[2].append(soup.find('span', class_='content').text)
            #直購價
            result[3].append(soup.find('strong', class_ = "rt-text-xx-large").text)
            #庫存
            result[4].append(soup.find('strong', class_="rt-text-isolated").text)
            #已賣數量 
            sell_num = soup.find('strong', class_='rt-text-x-large number')
            if sell_num != None:
                result[5].append(sell_num.text)
            else:
                result[5].append('0')
            #賣家!!
            se = soup.find('div', class_='seller-disc')
            seller_ID =  [s for s in se.stripped_strings][0]
            result[6].append(seller_ID)
            #評價!!
            reputation =  [s for s in se.stripped_strings][1]
            result[7].append(reputation)
            #問與答
            q = soup.find_all('span', class_ ='rt-text-parentesis count')
            QA = [qa for qa in q][0]
            result[8].append(QA.text)
            #購買人次
            buyer_num = [qa for qa in q][1]
            result[9].append(buyer_num.text)
     ###### #payment
            result[10].append(list(map(lambda x: x.text, soup.find_all('span', class_='vmiddle'))))
            #status
            result[11].append(soup.find('li', class_='status').text)
            #location
            result[12].append(soup.find('li', class_='location').text)
            #upload_time
            result[13].append(soup.find('li', class_='upload-time').text)
            #買家限制
            limitation = soup.find('li', class_="limitation")
            if limitation != None:
                result[14].append(limitation.find('span').text)
            else:
                result[14].append("0")
            #result[11].append(limitbuy(soup))
            #result[11].append((soup.find('li', class_="limitation")).text if limit != None else 'NA')
            #result[11].append(remain.text if remain != None else 'NA')
            #start_price
            result[15].append(soup.find('li', class_="initiation").find('span').text)
            #end
            result[16].append(soup.find('li', class_="putforward").text)
     ###### #delivery
            tmp = []
            for ele in map(lambda x: x.text.split('\n'), soup.find_all('ul', class_='detail-list')):
                tmp += ele
            result[17].append(list(filter(lambda x: len(x) > 0, map(lambda x: x.lstrip().rstrip(), tmp))))
            #all_sell_num
            result[18].append(soup.find('p', class_="seller-disc seller-disc-divider").find('strong').text)
            #update_time
            update_time = soup.find('span', class_="date")
            if update_time != None:
                result[19].append(update_time.text)
            else:
                result[19].append("0")
          

            ######################################
            driver.close()

            driver.switch_to_window(hand[0])

        
        driver.find_element_by_xpath("//div[contains(@class,'block_C')]//li[14]//a[1]").click()


# In[9]:


result[0]


# In[13]:


month = 1
day = 18
path = "\mydata"
item = ['name','image_num','productID','price','inventory','sell_num','seller_ID','reputation','QA', 'buyer_num','payment','status','location','upload-time','buylimit','start_price','end','delivery','all_sell_num','update-time', 'a', 'b', 'c', 'd']

if os.path.isdir(path):
    os.makedirs(path)
with open(f'{month}_{day}_ruten.csv','w', newline='',encoding='utf-8') as csv_file:
    writer=csv.writer(csv_file)
    #變數名稱
    writer.writerow(item)
    #資料
    for i in range(len(result[0])):
        writer.writerow([result[j][i] for j in range(len(item))])


# In[4]:


print(result[10])
len(result)


# In[ ]:




