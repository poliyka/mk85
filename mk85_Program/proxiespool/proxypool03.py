import requests
import random
from queue import Queue
from bs4 import BeautifulSoup
import threading
import csv
from setting import USER_AGENT

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

    url = 'https://www.us-proxy.org/'
    headers = {
        'User-Agent': USER_AGENT
    }
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'lxml')
        trs = soup.find('tbody').find_all('tr')
        datas = []
        for tr in trs:
            tds = tr.find_all('td')
            data = []
            for td in tds[:2]:
                data.append(td.text)
            datas.append(data)

        proxy = []
        for data in datas:
            proxy.append('https://' + data[0] + ':' + data[1])

        thread = []
        for i in range(len(proxy)):
            thread.append(threading.Thread(
                target=get_proxy_pool, args=(proxy[i], q)))

        for t in thread:
            t.start()
        for t in thread:
            t.join()

        proxies = []
        for i in range(q.qsize()):
            proxies.append([q.get()])

        print('done', len(proxies))

        q1.put(proxies)
    else:
        print('proxy網站無法連結')


def get_q():
    return q1.get()
