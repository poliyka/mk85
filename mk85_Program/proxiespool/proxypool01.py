import requests
import csv
import threading
import re
import numpy as np
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from queue import Queue
from setting import USER_AGENT,CURRENT_DIR
from os.path import join

# -----init-----
chromedriver_path = join(CURRENT_DIR, "./src/webdriver/chromedriver.exe")
q = Queue()
q1 = Queue()

def get_proxy_pool(proxy, q):
    url = 'https://www.8591.com.tw/'
    # url = 'https://www.google.com.tw/'
    proxies = {
        proxy.split(':')[0]: proxy
    }

    headers = {
        'User-Agent': USER_AGENT
    }

    try:
        time.sleep(np.random.randint(1, 3))
        resp = requests.get(url, headers=headers,
                            proxies=proxies, timeout=3)

        if resp.status_code == 200:
            print(proxy, resp)
            q.put(proxy)
        else:
            print(proxy, resp)
    except:
        pass


def getproxy():
    url = 'http://spys.one/free-proxy-list/TW/'

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument("user-agent={}".format(USER_AGENT))

    chrome = webdriver.Chrome(chromedriver_path, options=options)
    chrome.implicitly_wait(20)
    chrome.get(url)
    soup = BeautifulSoup(chrome.page_source, 'lxml')
    chrome.quit()
    result = re.compile(
        r'^(\d\d\d|\d\d|\d).(\d\d\d|\d\d|\d).(\d\d\d|\d\d|\d).(\d\d\d|\d\d|\d)')
    trs = soup.find_all('tr', class_='spy1xx')

    proxies = []
    for tr in trs[1:]:
        for p in tr.find_all('td', colspan='1')[1:-7]:
            try:
                a = p.text.split(' ')[0]
            except:
                a = p.text
        for x in result.findall(tr.find('td').text):
            proxies.append(a + '://' + x[0] + '.' + x[1] + '.' + x[2] +
                           '.' + x[3] + ':' + tr.find('td').text.split(':')[2])

    thread = []
    for proxy in proxies:
        thread.append(threading.Thread(
            target=get_proxy_pool, args=(proxy, q)))

    for t in thread:
        t.start()
        time.sleep(np.random.randint(1, 3))
    for t in thread:
        t.join()

    proxies = []
    for i in range(q.qsize()):
        proxies.append([q.get()])

    print('done', len(proxies))
    q1.put(proxies)


def get_q():
    return q1.get()
