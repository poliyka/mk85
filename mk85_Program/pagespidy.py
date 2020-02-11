import requests
import time
import threading
import re
import random
import csv
import numpy as np
import os
from queue import Queue
from bs4 import BeautifulSoup
from selenium import webdriver
from setting import USER_AGENT,CURRENT_DIR
from os.path import join

#//MARK: init_path
chromedriver_path = join(CURRENT_DIR, "./src/webdriver/chromedriver.exe")
proxy_path = join(CURRENT_DIR, "./src/db/proxy_List.csv")
# ---------init-----------
q = Queue()
q1 = Queue()
COOKIES = []
PROXY = ''
var_Log = ''
list_log = ''
log_index = []
chrome = ''
count = 0
check_int = 1 
# -------取得代理--------
proxy_List = []
with open(proxy_path, 'r', newline='') as f:
    reader = csv.reader(f)
    for i in reader:
        proxy_List += i

# -------取得log---------
def set_var_Log(var_Log1,list_log1):
    global var_Log
    global list_log
    var_Log = var_Log1
    list_log = list_log1
    
def get_log_index():
    return log_index

    
# -------使用log---------
def log(text):
    global log_index
    log_index.append(text)
    var_Log.set(log_index)
    list_log.selection_clear(0,"end")
    list_log.selection_set("end")
    # 以下兩個方法都是focus最後一行
    list_log.see("end")
    # list_log.yview_moveto(1)

# -------mothod----------

# -----取得cookies(沒有功能紀錄用)-------
# COOKIES = chrome.get_cookies()
# # 唯一判斷selenium有沒有正常開啟的判斷式 
# while COOKIES == []:
#     init_get_cookie()
#     chrome.quit()
# chrome.quit()    

# //MARK: 取得遊戲目錄
def getGameList(key):
    global COOKIES
    global chrome
    global log_index
    global count
    global check_int
    # 判斷是否初次開啟
    if count == 0:
        log('正在嘗試連線...')
        url = 'https://www.8591.com.tw/'
        prefs = {"profile.managed_default_content_settings.images": 2}
        
        # 網頁selenium,Option
        options = webdriver.ChromeOptions()
        # 關閉顯示視窗
        options.add_argument('--headless')
        # 無痕模式開啟
        # options.add_argument('--incognito')
        # 固定視窗大小
        options.add_argument('–window-size=1024,1024')
        # 植入代理
        # options.add_argument('--proxy-server={}'.format(PROXY))
        # 植入USER_AGENT
        options.add_argument("user-agent={}".format(USER_AGENT))
        # 取消加載圖片提高效率
        options.add_experimental_option("prefs", prefs)

        chrome = webdriver.Chrome(chromedriver_path, options=options)
        chrome.implicitly_wait(20)
        chrome.delete_all_cookies()
        chrome.get(url)
        COOKIES = chrome.get_cookies()
        # -----判斷連線是否成功
        while COOKIES == []:
            log('連線失敗...嘗試重新連線(' + str(check_int) + ')')
            chrome.quit()
            check_int += 1
            
            if check_int == 4:
                log('無法連線網頁...請確定網路(非代理)')
                check_int = 1
                return 'error'
            getGameList(key)
    if check_int != 4:        
        count += 1

        # 使用者輸入關鍵字取得遊戲列表
        gameSerchXpath = '/html/body/div[2]/div[3]/form/div/div[1]/input[2]'
        gameInput = chrome.find_element_by_xpath(gameSerchXpath)
        gameInput.clear()
        gameInput.send_keys(key)
        time.sleep(1)

        soup = BeautifulSoup(chrome.page_source, 'lxml')
        if soup != None:
            lis = soup.find(id='TS_gameList').find_all('li')
            gameList = []
            for i, li in enumerate(lis):
                if i != 0:
                    gameList.append([li['val'].strip('_'), li.text.strip()])

            return gameList
        else:
            log('無法取得網頁資料')
            chrome.quit()
            return 'error'
    else:
        return 'error'
    
# //MARK: 用game收尋結果取得Server資料
def getOtherList(gameName):
    global COOKIES
    global chrome
    log('正在點選遊戲')

    # 尋找遊戲列表
    gameSerchXpath = '/html/body/div[2]/div[3]/form/div/div[1]/input[2]'
    gameInput = chrome.find_element_by_xpath(gameSerchXpath)
    gameInput.clear()
    gameInput.send_keys(gameName)

    # 點選遊戲名稱
    time.sleep(1)
    gameSerchXpath = '/html/body/div[2]/div[3]/form/div/div[1]/div/ul/li[2]'
    gameInput = chrome.find_element_by_xpath(gameSerchXpath).click()

    # 尋找伺服器
    gameSerchXpath = '/html/body/div[2]/div[3]/form/div/div[2]/input[2]'
    gameInput = chrome.find_element_by_xpath(gameSerchXpath)

    OtherList = {}
    soup = BeautifulSoup(chrome.page_source, 'lxml')
    if soup != None:
        lis = soup.find(id='searchServer_ul').find_all('li')
        serverList = []
        for li in lis:
            serverList.append([li['val'].strip('_'), li.text.strip()])
        OtherList['serverList'] = serverList
    else:
        return None

    if soup != None:
        lis = soup.find(id='searchType_ul').find_all('li')
        itemList = []
        for li in lis:
            itemList.append([li['val'].strip('_'), li.text.strip()])
        OtherList['itemList'] = itemList
    else:
        return None

    return OtherList


# //MARK: 取得頁面資料(總頁面)
def getPageIndex(searchGame, searchServer='', searchType='', searchKey=''):
    ts = time.time()
    t = threading.Thread(target=getPageIndex_Deal, args=(
        searchGame, searchServer, searchType, searchKey))
    t.start()

    url = 'https://www.8591.com.tw/mallList-list.html'

    headers = {
        'User-Agent': USER_AGENT
    }

    form_data = {
        'group': '1',
        'searchType': searchType,
        'priceSort': '1',
        'ratios': '0',
        'searchGame': searchGame,
        'searchServer': searchServer,
        'searchKey': searchKey,
    }
    # 更換代理IP
    check = False
    while check == False:
        try:
            poxy_url = random.choice(proxy_List)
            proxies = {
                poxy_url.split(':')[0]: poxy_url
            }
            resp = requests.get(
                url, form_data, headers=headers, proxies=proxies)
            if resp.status_code == 200:
                check = True
        except:
            check = False

    soup = BeautifulSoup(resp.text, 'lxml')
    # 第一頁資料
    log('正在取得資料')
    links = soup.find(id='wc_list').find_all('a', class_='detail_link')

    # 找到總頁數
    try:
        span = soup.find('span', class_='R')
        totalRows = int(span.text)
        firstRow = 0
    except:
        totalRows = 0
        firstRow = 0

    thread = []
    while (totalRows - firstRow) >= 0:
        t = threading.Thread(target=thread_1, args=(
            url, headers, proxy_List, searchGame, searchServer, searchType, searchKey, firstRow, totalRows, q))
        thread.append(t)
        firstRow += 21

    for th in thread:
        th.start()
        time.sleep(np.random.randint(1,3))
    for th in thread:
        th.join()

    itemList = []
    for i in range(q.qsize()):
        itemList += q.get()

    itemList_deal = q1.get()

    log('費時:' + str(round((time.time()-ts), 5)) + '秒')
    return itemList, itemList_deal

# //MARK: 取得頁面資料(已交易)
def thread_1(url, headers, proxy_List, searchGame, searchServer, searchType, searchKey, firstRow, totalRows, q):

    form_data = {
        'group': '1',
        'searchType': searchType,
        'priceSort': '1',
        'ratios': '0',
        'searchGame': searchGame,
        'searchServer': searchServer,
        'searchKey': searchKey,
        'firstRow': str(firstRow),
        'totalRows': str(totalRows),
    }

    check = False
    while check == False:
        try:
            poxy_url = random.choice(proxy_List)
            proxies = {
                poxy_url.split(':')[0]: poxy_url
            }
            resp = requests.get(
                url, form_data, headers=headers, proxies=proxies)
            if resp.status_code == 200:
                check = True
        except:
            check = False

    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.find(id='wc_list').find_all('a', class_='detail_link')
    itemList = []

    for link in links:
        itemList.append(
            [link['title'], 'https://www.8591.com.tw/' + link['href']])

    moneys = soup.find(id='wc_list').find_all('b')
    for i, money in enumerate(moneys):
        itemList[i].append(money.text.strip())
    
    if totalRows != 0:
        log('(待交易)第' + str(int(firstRow/21)+1) + '頁/第' + str(int(totalRows/21) if totalRows%21 == 0 
                                                           else (int(totalRows/21)+1)) + '頁')
    else:
        log('(待交易)第' + str(int(firstRow/21)+1) + '頁/第' + str(int(firstRow/21)+1) + '頁')
            
    q.put(itemList)

# //MARK: 取得頁面資料(已交易)
def getPageIndex_Deal(searchGame, searchServer='', searchType='', searchKey=''):
    url = 'https://www.8591.com.tw/mallList-list.html'

    headers = {
        'User-Agent': USER_AGENT}
    # 取得已完成交易資料
    form_data = {
        'searchGame': searchGame,
        'searchServer': searchServer,
        'buyStatus': '1',
        'searchType': searchType,
        'searchKey': searchKey,
        'uid': '',
    }
    # 更換代理IP
    check = False
    while check == False:
        try:
            poxy_url = random.choice(proxy_List)
            proxies = {
                poxy_url.split(':')[0]: poxy_url
            }
            resp = requests.get(
                url, form_data, headers=headers, proxies=proxies)
            if resp.status_code == 200:
                check = True
        except:
            check = False

    soup = BeautifulSoup(resp.text, 'lxml')

    # 第一頁資料
    links = soup.find(id='wc_list').find_all('a', class_='detail_link')
    itemList_deal = []
    count = 0

    try:
        span = soup.find('span', class_='R')
        totalRows = int(span.text)
        firstRow = 0
    except:
        totalRows = 0
        firstRow = 0

    while (totalRows - firstRow) >= 0:

        form_data = {
            'group': '1',
            'buyStatus': '1',
            'searchType': searchType,
            'priceSort': '1',
            'ratios': '0',
            'searchGame': searchGame,
            'searchServer': searchServer,
            'searchKey': searchKey,
            'firstRow': str(firstRow),
            'totalRows': str(totalRows),
        }

        # 更換代理IP
        check = False
        while check == False:
            try:
                poxy_url = random.choice(proxy_List)
                proxies = {
                    poxy_url.split(':')[0]: poxy_url
                }
                resp = requests.get(
                    url, form_data, headers=headers, proxies=proxies)
                if resp.status_code == 200:
                    check = True
            except:
                check = False

        soup = BeautifulSoup(resp.text, 'lxml')
        links = soup.find(id='wc_list').find_all('a', class_='detail_link')

        for link in links:
            itemList_deal.append(
                [link['title'], 'https://www.8591.com.tw/' + link['href']])

        moneys = soup.find(id='wc_list').find_all('b')
        for money in moneys:
            itemList_deal[count].append(money.text.strip())
            count += 1
        firstRow += 21
        if totalRows != 0:
            log('(已交易)第' + str(int(firstRow/21)) + '頁/第' + str(int(totalRows/21) if totalRows%21 == 0 
                                                           else (int(totalRows/21)+ 1)) + '頁')
        else:
            log('(已交易)第' + str(int(firstRow/21)) + '頁/第' + str(int(firstRow/21)) + '頁')
            
    q1.put(itemList_deal)
