import csv
import proxiespool.proxypool01 as p01
import proxiespool.proxypool02 as p02
import proxiespool.proxypool03 as p03
import threading
import changeproxy
from setting import CURRENT_DIR
from queue import Queue
from os.path import join

#----inti----- 
proxy_list_path = join(CURRENT_DIR, "./src/db/proxy_List.csv")
varList_log = ''
lb_log = ''
log_index = []

# -------取得log---------
def set_var_Log(varList_log1,lb_log1):
    global varList_log
    global lb_log
    varList_log = varList_log1
    lb_log = lb_log1
    
# -------使用log---------
def log(text):
    global log_index
    log_index.append(text)
    varList_log.set(log_index)
    lb_log.selection_clear(0, "end")
    lb_log.selection_set("end")
    # 以下兩個方法都是focus最後一行
    lb_log.see("end")
    # list_log.yview_moveto(1)  


def get_proxies(num,log_index1):
    # //MARK:取得代理01
    global log_index
    log_index = log_index1
    
    if num == 1:
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
        
        changeproxy.set_log_index(log_index)
    
    # //MARK:取得代理02
    elif num == 2:
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
        
        changeproxy.set_log_index(log_index)
    
    # //MARK:取得代理03
    elif num == 3:
        threads = []
        threads.append(threading.Thread(target=p03.getproxy))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        proxies = []
        proxies += p03.get_q()
        log("Finish:取得("+str(len(proxies))+")個代理")

        with open(proxy_list_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(proxies)
        
        changeproxy.set_log_index(log_index)
