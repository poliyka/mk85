import tkinter as tk
import getproxy
import csv
import pyperclip
import threading
from tkinter import StringVar, ttk
from setting import CURRENT_DIR
from os.path import join
from tkinter import messagebox as mb


# //MARK: init
proxy_path = join(CURRENT_DIR, "./src/db/proxy_List.csv")
proxy_List = []
log_index = []
varList_log = ''
lb_log = ''
num = 1

with open(proxy_path, 'r', newline='') as f:
    reader = csv.reader(f)
    for i in reader:
        proxy_List += i

def set_log_index(log_index1):
    global log_index
    log_index = log_index1

def log(text):
    global log_index
    log_index.append(text)
    varList_log.set(log_index)
    lb_log.selection_clear(0, "end")
    lb_log.selection_set("end")
    # 以下兩個方法都是focus最後一行
    lb_log.see("end")
    # list_log.yview_moveto(1)


class App_start:
    def __init__(self, f1_label, f2_option, f3_log):
        self.f1_label = f1_label
        self.f2_option = f2_option
        self.f3_log = f3_log

        self.label()
        self.radio_button()
        self.entry()
        self.bind_entry()
        self.button()
        self.listbox()
        self.object_pack()

    # //MARK: Label
    def label(self):
        # title_text = '''選擇遊戲時使用的是本地的IP(localhost)\n收尋物品項目時使用的是代理IP\n請使用下列功能更換代理IP\n確保IP不被官方阻擋
        # '''
        title_text = '開發中暫無功能'
        self.label_title = tk.Label(self.f1_label,
                                    width=60,
                                    height=5,
                                    text=title_text,
                                    font=('標楷體', 36),
                                    bg='PowderBlue',
                                    fg='MidnightBlue',
                                    anchor='nw',
                                    justify='left',
                                    wraplength=450
                                    )
        # anchor (分布位置參數)
        # nw        n        ne
        # w      center    e
        # sw        s        se

        self.label_op01 = tk.Label(self.f2_option,
                                   width=11,
                                   height=1,
                                   text='本地IP更換:',
                                   font=('標楷體', 12),
                                   fg='MidnightBlue',
                                   anchor='nw',
                                   justify='left'
                                   )

        self.label_op02 = tk.Label(self.f2_option,
                                   width=60,
                                   height=1,
                                   text='本地網路是否使用代理(將影響搜尋遊戲基本資訊的效率)',
                                   font=('標楷體', 12),
                                   fg='MidnightBlue',
                                   anchor='nw',
                                   justify='left'
                                   )

        self.label_op03 = tk.Label(self.f2_option,
                                   width=11,
                                   height=1,
                                   text='請輸入代理:',
                                   font=('標楷體', 12),
                                   fg='MidnightBlue',
                                   anchor='nw',
                                   justify='left'
                                   )

        self.label_op04 = tk.Label(self.f2_option,
                                   width=19,
                                   height=1,
                                   text='更換搜尋物品代理IP:',
                                   font=('標楷體', 12),
                                   fg='MidnightBlue',
                                   anchor='nw',
                                   justify='left'
                                   )

        self.var_op05 = tk.StringVar()
        self.var_op05.set('目前代理個數(' + str(len(proxy_List)) + ')')
        self.label_op05 = tk.Label(self.f2_option,
                                   width=16,
                                   height=1,
                                   textvariable=self.var_op05,
                                   font=('標楷體', 12),
                                   fg='MidnightBlue',
                                   bg='pink',
                                   anchor='nw',
                                   justify='left'
                                   )
        
    
    # //MARK: Radiobutton
    def radio_button(self):
        self.var_yn = tk.IntVar()
        self.var_po = tk.IntVar()
        self.rd_y = tk.Radiobutton(self.f2_option,
                                   text='Y',
                                   font=('標楷體', 10),
                                   variable=self.var_yn,
                                   value=1,
                                   command=self.rd_yn_selection
                                   )

        self.rd_n = tk.Radiobutton(self.f2_option,
                                   text='N',
                                   font=('標楷體', 10),
                                   variable=self.var_yn,
                                   value=0,
                                   command=self.rd_yn_selection
                                   )
        self.rd_n.select()

        self.rd_po01 = tk.Radiobutton(self.f2_option,
                                      variable=self.var_po,
                                      text='代理池1 (推薦TW)',
                                      value=1,
                                      command=self.rd_po_selection
                                      )
        self.rd_po01.select()

        self.rd_po02 = tk.Radiobutton(self.f2_option,
                                      variable=self.var_po,
                                      text='代理池2',
                                      value=2,
                                      command=self.rd_po_selection
                                      )

        self.rd_po03 = tk.Radiobutton(self.f2_option,
                                      variable=self.var_po,
                                      text='代理池3',
                                      value=3,
                                      command=self.rd_po_selection
                                      )

    # radioButton method
    def rd_yn_selection(self):
        if self.var_yn.get() == 1:
            self.entry_op01.config(state='normal')
            self.btn_host_ip_change.config(state='active')
            log('本地網路代理開啟'
                )
        if self.var_yn.get() == 0:
            self.entry_op01.config(state='disable')
            self.btn_host_ip_change.config(state='disabled')
            log('本地網路代理關閉')
        
    def rd_po_selection(self):
        global num
        if self.var_po.get() ==1:
            num = 1
        if self.var_po.get() ==2:
            num = 2
        if self.var_po.get() ==3:
            num = 3
            

    # //MARK: Entry
    def entry(self):
        self.var_en01 = tk.StringVar()
        self.entry_op01 = tk.Entry(self.f2_option,
                                   width=32,
                                   textvariable=self.var_en01,
                                   font=('標楷體', 12),
                                   fg='blue',
                                   state='disable',
                                   justify='left'
                                   )

    # bind_entry event
    def bind_entry(self):
        self.entry_op01.bind("<Enter>", self.bind_en_Enter)
        self.entry_op01.bind("<Leave>", self.bind_en_Leave)

    def bind_en_Enter(self, bind):
        self.bn_en01 = tk.Label(self.f2_option,
                                text='http:\\\\xxx.xxx.xxx.xxx:xxxx\n協定:\\\\IP:port',
                                font=('標楷體', 12),
                                width=30,
                                height=2,
                                bg='Pink',
                                fg='MidnightBlue',
                                anchor='nw',
                                justify='left'
                                )
        self.bn_en01.place(x=100, y=75)

    def bind_en_Leave(self, bind):
        self.bn_en01.place_forget()

    # //MARK: button

    def button(self):
        self.btn_host_ip_change = ttk.Button(self.f2_option,
                                             text='更換代理',
                                             width=10, cursor='hand2',
                                             state='disable',
                                             command=self.btn_host_ip_change_click
                                             )

        self.btn_proxies_ip_change = ttk.Button(self.f2_option,
                                                text='取得代理池',
                                                width=10, cursor='hand2',
                                                command=self.btn_proxies_ip_change_click
                                                )

        self.btn_copy = ttk.Button(self.f2_option,
                                   text='複製',
                                   width=10, cursor='hand2',
                                   command=self.btn_copy_click
                                   )

    # button click method
    def btn_host_ip_change_click(self):
        pass
    
    def thread_log(self):
        global proxy_path
        global num
        global log_index
        log('正在取得代理池....')
        t = threading.Thread(target=getproxy.get_proxies, args=(num,log_index))
        t.start()
        t.join()
        
        proxy_List = []
        with open(proxy_path, 'r', newline='') as f:
            reader = csv.reader(f)
            for i in reader:
                proxy_List += i
                
            self.var_op05.set('目前代理個數(' + str(len(proxy_List)) + ')')
            self.varList_proxies.set(proxy_List)
        
    
    def btn_proxies_ip_change_click(self):
        t = threading.Thread(target=self.thread_log)
        t.start()

    def btn_copy_click(self):
        pyperclip.copy(self.lb_proxies.get(self.lb_proxies.curselection()[0]))
        log('已複製第('+str(self.lb_proxies.curselection()[0]+1)+')項代理')

    # //MARK: Listbox

    def listbox(self):
        global varList_log
        global lb_log

        varList_log = tk.StringVar()
        varList_log.set([])
        lb_log = tk.Listbox(self.f3_log,
                            listvariable=varList_log,
                            font=('標楷體', 12),
                            width=29,
                            height=20,
                            bg='DarkSlateBlue',
                            fg='pink',
                            highlightcolor="pink",
                            selectbackground="MidnightBlue",
                            borderwidth=2,
                            activestyle='none'
                            )

        self.varList_proxies = tk.StringVar()
        self.varList_proxies.set(proxy_List)
        self.lb_proxies = tk.Listbox(self.f3_log,
                                     listvariable=self.varList_proxies,
                                     font=('標楷體', 12),
                                     width=29,
                                     height=20,
                                     bg='DarkSlateBlue',
                                     fg='pink',
                                     highlightcolor="pink",
                                     selectbackground="MidnightBlue",
                                     borderwidth=2,
                                     activestyle='none'
                                     )
        
    # //MARK: object_pack

    def object_pack(self):
        self.label_title.place(x=0, y=0)
        self.label_op01.place(x=0, y=0)
        self.label_op02.place(x=0, y=25)
        self.rd_y.place(x=410, y=25)
        self.rd_n.place(x=445, y=25)
        self.label_op03.place(x=0, y=50)
        self.entry_op01.place(x=100, y=53)
        self.btn_host_ip_change.place(x=380, y=50)
        self.label_op04.place(x=0, y=100)
        self.rd_po01.place(x=15, y=130)
        self.rd_po02.place(x=15, y=160)
        self.rd_po03.place(x=15, y=190)
        self.btn_proxies_ip_change.place(x=15, y=220)
        self.label_op05.place(x=245, y=230)
        self.btn_copy.place(x=400, y=225)
        lb_log.pack(side='left')
        self.lb_proxies.pack(side='right')


# //MARK: GUI_surface

def App(win):
    newwin = tk.Toplevel(win)
    newwin.geometry('500x700')
    newwin.title('更變代理')

    canvas = tk.Canvas(newwin, width=500, height=700,
                       highlightthickness=0, borderwidth=0, bg='PowderBlue')
    # canvas.create_image(600, 400, image=img_bg01)
    canvas.pack()

    f1_label = tk.Frame(newwin)
    f2_option = tk.Frame(newwin, bg='PowderBlue')
    f3_log = tk.Frame(newwin, bg='PowderBlue')

    canvas.create_window(250, 50, width=480, height=80, window=f1_label)
    canvas.create_window(250, 225, width=480, height=250, window=f2_option)
    canvas.create_window(250, 520, width=480, height=320, window=f3_log)

    App_start(f1_label, f2_option, f3_log)
    getproxy.set_var_Log(varList_log,lb_log)
