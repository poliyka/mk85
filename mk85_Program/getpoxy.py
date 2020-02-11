import csv
import proxiespool.proxypool as p01
import proxiespool.proxypool01 as p02
import proxiespool.proxypool02 as p03
import threading
import pandas as pd
from setting import CURRENT_DIR
from queue import Queue
from os.path import join

file_path = join(CURRENT_DIR, "./src/db/proxy_List.csv")


def get_proxy():
    threads = []
    # threads.append(threading.Thread(target=p01.getproxy))
    # threads.append(threading.Thread(target=p02.getproxy))
    threads.append(threading.Thread(target=p03.getproxy))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    proxies = []
    # proxies += p01.get_q()
    # proxies += p02.get_q()
    proxies += p03.get_q()

    print("finally:",len(proxies))

    with open(r'mk85_Program\src\db', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(proxies)

