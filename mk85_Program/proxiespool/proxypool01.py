from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import csv
import threading
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
    url = 'http://www.gatherproxy.com/'

    options = webdriver.ChromeOptions()

    options.add_argument('--incognito')
    options.add_argument('--headless')
    
    options.add_argument("user-agent={}".format(USER_AGENT))

    chrome = webdriver.Chrome(chromedriver_path, options=options)
    chrome.implicitly_wait(20)
    chrome.get(url)

    soup = BeautifulSoup(chrome.page_source, 'lxml')
    chrome.quit()

    trs = soup.find(id='tblproxy').find_all('tr')
    proxies = []
    for tr in trs[2:]:
        try:
            proxies.append('http://' + tr['prx'])
        except:
            pass

    thread = []
    for proxy in proxies:
        thread.append(threading.Thread(
            target=get_proxy_pool, args=(proxy, q)))

    for t in thread:
        t.start()
    for t in thread:
        t.join()

    proxies = []
    for i in range(q.qsize()):
        proxies.append([q.get()])

    print('done', len(proxies))
    q1.put(proxies)


def get_q():
    return q1.get()
