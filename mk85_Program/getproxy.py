import csv
import proxiespool.proxypool as p01
import proxiespool.proxypool01 as p02
import proxiespool.proxypool02 as p03
import threading
from setting import CURRENT_DIR
from queue import Queue
from os.path import join

#----inti----- 
proxy_list_path = join(CURRENT_DIR, "./src/db/proxy_List.csv")
var_Log = ''
list_Log = ''
log_index = []
# -------取得log---------
def set_var_Log(var_Log1,list_Log1):
    global var_Log
    global list_Log
    var_Log = var_Log1
    list_Log = list_Log1
    
def get_log_index():
    return log_index

def set_log_index(log_index1):
    log_index = log_index1
    
# -------使用log---------
def log(text):
    global log_index
    log_index.append(text)
    var_Log.set(log_index)
    list_Log.selection_clear(0,"end")
    list_Log.selection_set("end")
    # 以下兩個方法都是focus最後一行
    list_Log.see("end")
    # list_Log.yview_moveto(1)

# //MARK:取得代理01
def get_proxy01():
    threads = []
    threads.append(threading.Thread(target=p01.getproxy))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    proxies = []
    proxies += p01.get_q()
    log("Finish:取得("+str(len(proxies))+")個代理")

    with open(proxy_list_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(proxies)

# //MARK:取得代理02
def get_proxy02():
    threads = []
    threads.append(threading.Thread(target=p02.getproxy))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    proxies = []
    proxies += p02.get_q()
    log("Finish:取得("+str(len(proxies))+")個代理")

    with open(proxy_list_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(proxies)

# //MARK:取得代理03
def get_proxy03():
    threads = []
    threads.append(threading.Thread(target=p03.getproxy))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    proxies = []
    proxies += p03.get_q()
    # log("Finish:取得("+str(len(proxies))+")個代理")

    with open(proxy_list_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(proxies)
