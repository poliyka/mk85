import csv
import proxiespool.proxypool as p01
import proxiespool.proxypool01 as p02
import proxiespool.proxypool02 as p03
import threading
import pandas as pd
from queue import Queue


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

# with open(r'mk85_Program\src\db', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(proxies)

# from os.path import dirname, join
# current_dir = dirname(__file__)
# file_path = join(current_dir, "./001.csv")

# poxy = []
# with open(file_path,'r', newline='') as f:
#     reader = csv.reader(f)
#     for i in reader:
#         poxy.append(i)

# for pox in poxy:
#     print(pox)
# Python\mk85_Program\src\db\proxy_List.csv
# with open('Python/mk85_Program/src/db/proxy_List.csv','r') as df1:
#     print(df1)