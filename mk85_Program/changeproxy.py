import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox as mb
import numpy as np
import time
from PIL import ImageTk, Image
import threading
from queue import Queue
import getproxy
from setting import CURRENT_DIR
from os.path import join


class App_start:
    def __init__(self):

        self.label()
        self.radio_button()
        self.entry()
        self.bind_entry()
        self.button()
        self.object_pack()
        
    # //MARK: Label
    def label(self):
        title_text = '''選擇遊戲時使用的是本地的IP(localhost)\n收尋物品項目時使用的是代理IP\n請使用下列功能更換代理IP\n確保IP不被官方阻擋
        '''
        self.label_title = tk.Label(f1_label,
                                    width=60,
                                    height=5,
                                    text=title_text,
                                    font=('標楷體', 12),
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

        self.label_op01 = tk.Label(f2_option,
                                    width=11,
                                    height=1,
                                    text='本地IP更換:',
                                    font=('標楷體', 12),
                                    fg='MidnightBlue',
                                    anchor='nw',
                                    justify='left'
                                    )
        
        self.label_op02 = tk.Label(f2_option,
                                    width=60,
                                    height=1,
                                    text='本地網路是否使用代理(將影響搜尋遊戲基本資訊的效率)',
                                    font=('標楷體', 12),
                                    fg='MidnightBlue',
                                    anchor='nw',
                                    justify='left'
                                    )
        
        self.label_op03 = tk.Label(f2_option,
                                    width=11,
                                    height=1,
                                    text='請輸入代理:',
                                    font=('標楷體', 12),
                                    fg='MidnightBlue',
                                    anchor='nw',
                                    justify='left'
                                    )
        
        self.label_op04 = tk.Label(f2_option,
                                    width=19,
                                    height=1,
                                    text='更換搜尋物品代理IP:',
                                    font=('標楷體', 12),
                                    fg='MidnightBlue',
                                    anchor='nw',
                                    justify='left'
                                    )
    # //MARK: Radiobutton        
    def radio_button(self):
        self.var_yn = tk.IntVar()
        self.var_po = tk.IntVar()
        self.rd_y = ttk.Radiobutton(f2_option,
                                    variable=self.var_yn,
                                    text='Y',
                                    value=1,
                                    
                                    command=self.rd_yn_selection
                                    )
        
        self.rd_n = ttk.Radiobutton(f2_option,
                                    variable=self.var_yn,
                                    text='N',
                                    value=0,
                                    command=self.rd_yn_selection
                                    )
        
        self.rd_po01 = ttk.Radiobutton(f2_option,
                                    variable=self.var_po,
                                    text='代理池1 (推薦TW)',
                                    value=1,
                                    command=self.rd_po_selection
                                    )
        
        self.rd_po02 = ttk.Radiobutton(f2_option,
                                    variable=self.var_po,
                                    text='代理池2',
                                    value=2,
                                    command=self.rd_po_selection
                                    )
        
        self.rd_po03 = ttk.Radiobutton(f2_option,
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
        if self.var_yn.get() == 0:
            self.entry_op01.config(state='disable')
            self.btn_host_ip_change.config(state='disabled')
    
    def rd_po_selection(self):
        pass
    
    # //MARK: Entry
    def entry(self):
        self.var_en01 = tk.StringVar()
        self.entry_op01 = tk.Entry(f2_option,
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
    
    def bind_en_Enter(self,bind):
        self.bn_en01 = tk.Label(f2_option,
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
        
    def bind_en_Leave(self,bind):
        self.bn_en01.place_forget()
    
    #//MARK: button    
    def button(self):
        self.btn_host_ip_change = ttk.Button(f2_option,
                                             text='更換代理',
                                             width=10, cursor='hand2',
                                             state='disable',
                                             command=self.btn_host_ip_change_click
                                             )
        
        self.btn_proxies_ip_change = ttk.Button(f2_option,
                                             text='取得代理池',
                                             width=10, cursor='hand2',
                                             command=self.btn_proxies_ip_change_click
                                             )
    
    #button click method
    def btn_host_ip_change_click(self):
        pass
    
    def btn_proxies_ip_change_click(self):
        pass
    
    #//MARK: object_pack
    def object_pack(self):
        self.label_title.place(x=0, y=0)
        self.label_op01.place(x=0,y=0)
        self.label_op02.place(x=0,y=25)
        self.rd_y.place(x=410,y=25)
        self.rd_n.place(x=445,y=25)
        self.label_op03.place(x=0,y=50)
        self.entry_op01.place(x=100,y=53)
        self.btn_host_ip_change.place(x=380,y=50)
        self.label_op04.place(x=0,y=100)
        self.rd_po01.place(x=15,y=130)
        self.rd_po02.place(x=15,y=160)
        self.rd_po03.place(x=15,y=190)
        self.btn_proxies_ip_change.place(x=15,y=220)


# //MARK: GUI_surface
win = tk.Tk()
win.geometry('500x700')
win.title('更變代理')

canvas = tk.Canvas(win, width=500, height=700,
                   highlightthickness=0, borderwidth=0,bg='black')
# canvas.create_image(600, 400, image=img_bg01)
canvas.pack()

f1_label = tk.Frame(win)
f2_option = tk.Frame(win,bg='PowderBlue')
f3_log = tk.Frame(win,bg='PowderBlue')

canvas.create_window(250, 50, width=480, height=80, window=f1_label)
canvas.create_window(250, 225, width=480, height=250, window=f2_option)
canvas.create_window(250, 520, width=480, height=320, window=f3_log)


App_start()

win.mainloop()
