import tkinter as tk
from tkinter import StringVar, ttk
from tkinter.ttk import *
import numpy as np
from PIL import ImageTk, Image
import threading
from queue import Queue
import os
import webbrowser
import pagespidy
import getproxy
from setting import CURRENT_DIR
from os.path import join

# //MARK: GUI surface


class App:
    def __init__(self, f1_search, f2_list, f3_log, f4_proxies, f5_lb01, f6_lb02):
        self.f1_search = f1_search
        self.f2_list = f2_list
        self.f3_log = f3_log
        self.f4_proxies = f4_proxies
        self.f5_lb01 = f5_lb01
        self.f6_lb02 = f6_lb02
        self.games = []
        self.servers = []
        self.items = []
        self.gameNum = ''
        self.serverNum = ''
        self.itemNum = ''
        self.itemLists = []
        self.itemLists_Deals = []
        self.log_text = []

        self.background_label()
        self.titleLabel()
        self.entrySearchGame()
        self.botton_Search()
        self.botton_getproxy()
        self.optinMenu(self.games, self.servers, self.items)
        self.botton_send()
        self.listbox()
        self.log_place()
        self.entrySearchItem()
        # self.progressBar()
        self.object_pack()

    # //MARK: Label_GUI
    def titleLabel(self):
        self.leb01 = tk.Label(f5_lb01, text='待交易項目', font=(
            '標楷體', 12), width=15, height=2, bg='Pink')
        self.leb02 = tk.Label(f6_lb02, text='已完成交易項目', font=(
            '標楷體', 12), width=15, height=2, bg='Plum')

    def background_label(self):
        global img_icon
        self.background_label01 = tk.Label(f1_search, image=img_icon)
        self.background_label01.place(x=0, y=0, relwidth=1, relheight=1)

    # //MARK: optinMenu_GUI

    def optinMenu(self, games, server, item):
        self.var01 = StringVar()
        self.var02 = StringVar()
        self.var03 = StringVar()
        # 創建optionMenu 控制元件
        # 此處初始下拉選單套入擷取資料中的伺服器名稱
        # tk.OptionMenu 有另一種樣式
        # ttk.OptionMenu(介面,存取之變量,初始文字,選單中的值1,選單中的值2,...,command = 呼叫函式)
        # ttk.OptionMenu(介面,存取之變量,初始文字,*list,...,command = 呼叫函式)
        self.omGames = ttk.OptionMenu(
            f1_search, self.var01, '請選擇遊戲', *games, direction='below', command=self.saveGame_Option)

        self.omServers = ttk.OptionMenu(
            f1_search, self.var02, '請選擇伺服器', *server, direction='below', command=self.saveServer_Option)

        self.omItems = ttk.OptionMenu(
            f1_search, self.var03, '請選擇物品', *item, direction='below', command=self.saveItem_Option)

    # 儲存選取變量
    def saveGame_Option(self, option):
        gameOption = self.var01.get()
        self.omGames.config(state='disabled')
        self.btnSearch.config(state='disabled')
        self.btnSend.config(state='disabled')
        t = threading.Thread(target=self.getOtherList, args=(gameOption,))
        t.start()
        # 取得代號
        self.gameNum = self.games[findIn2DTo1D(self.games, gameOption)][0]

    def saveServer_Option(self, option):
        serverOption = self.var02.get()
        # 取得代號
        self.serverNum = self.servers[findIn2DTo1D(
            self.servers, serverOption)][0]

    def saveItem_Option(self, option):
        itemOption = self.var03.get()
        # 取得代號
        self.itemNum = self.items[findIn2DTo1D(self.items, itemOption)][0]

    # //MARK: 取得其他列表
    def getOtherList(self, gameName):
        otherList = pagespidy.getOtherList(gameName)
        self.servers = otherList['serverList']
        self.items = otherList['itemList']
        self.omServers.set_menu(
            self.servers[0][1], *(i[1] for i in self.servers))
        self.omItems.set_menu(self.items[0][1], *(i[1] for i in self.items))
        self.omGames.config(state='active')
        self.btnSearch.config(state='active')
        self.btnSend.config(state='active')

    # //MARK: Entry_GUI
    def entrySearchGame(self):
        self.etyGame = ttk.Entry(f1_search, font=('標楷體', 12), width=15)

    def entrySearchItem(self):
        self.etyItem = ttk.Entry(f1_search, font=('標楷體', 12), width=15)

    # //MARK: Listbox_GUI
    def listbox(self):
        self.varList = tk.StringVar()
        self.varList.set([])
        self.lb = tk.Listbox(f2_list, listvariable=self.varList, font=(
            '標楷體', 12), bg='sky blue', width=50, height=25, highlightcolor="MidnightBlue", selectbackground="pink", selectforeground="MidnightBlue", borderwidth=2, activestyle='none')

        self.varList1 = tk.StringVar()
        self.varList1.set([])
        self.lb1 = tk.Listbox(f2_list, listvariable=self.varList1, font=(
            '標楷體', 12), selectmode='SINGLE', bg='sky blue', width=50, height=25, highlightcolor="MidnightBlue", selectbackground="pink", selectforeground="MidnightBlue", borderwidth=2, activestyle='none')
        self.lb.bind('<Double-Button-1>', self.clickLink)
        self.lb1.bind('<Double-Button-1>', self.clickLink1)

    def log_place(self):
        global var_Log
        global list_log
        var_Log = tk.StringVar()
        var_Log.set([])

        list_log = tk.Listbox(f3_log, listvariable=var_Log, font=(
            '標楷體', 12), width=102, height=4, bg='DarkSlateBlue', fg='pink', highlightcolor="pink",
                               selectbackground="MidnightBlue", borderwidth=2, activestyle='none')

        # 有scrollbar版本
        # self.scrollbar = Scrollbar(f3_log)
        # self.scrollbar.pack(side='right', fill='y')
        # list_log = tk.Listbox(f3_log, listvariable=var_Log, font=(
        #     '標楷體', 12), width=102, height=3, bg='DarkSlateBlue', highlightcolor="pink", selectbackground="MidnightBlue", borderwidth=2, activestyle='none', yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=list_log.yview)

    # //MARK: popupWindow_GUI
    def clickLink(self, event):
        popup = tk.Tk()
        url = self.itemLists[self.lb.curselection()[0]][1]

        def windestroy():
            webbrowser.open(url)
            popup.destroy()

        def wincancel():
            popup.destroy()

        lab = ttk.Label(popup, text='你將前往下列網址\n' + url)
        lab.pack()
        btn = ttk.Button(popup, text="Okay", command=windestroy)
        btn.pack()
        btn = ttk.Button(popup, text="Cancel", command=wincancel)
        btn.pack()
        popup.mainloop()

    def clickLink1(self, event):
        popup = tk.Tk()
        url = self.itemLists_Deals[self.lb1.curselection()[0]][1]

        def windestroy():
            webbrowser.open(url)
            popup.destroy()

        def wincancel():
            popup.destroy()

        lab = ttk.Label(popup, text='你將前往下列網址\n' + url)
        lab.pack()
        btn = ttk.Button(popup, text="Okay", command=windestroy)
        btn.pack()
        btn = ttk.Button(popup, text="Cancel", command=wincancel)
        btn.pack()
        popup.mainloop()

    # //MARK: Botton_GUI
    def botton_Search(self):
        self.btnSearch = ttk.Button(
            f1_search, text='Search', width=10, command=self.btn_search_click)

    def btn_search_click(self):
        self.btnSearch.config(state='disabled', text='Searching...')
        self.omGames.config(state='disabled')
        self.btnSend.config(state='disabled')
        t = threading.Thread(target=self.setmenu)
        t.start()

    def setmenu(self):
        if self.etyGame.get() != '':
            data = pagespidy.getGameList(self.etyGame.get())
            if data != 'error':
                try:
                    self.games = [i for i in data]
                    self.omGames.set_menu(
                        self.games[0][1], *(i[1] for i in self.games))
                    log('收尋完成')
                except:
                    log('沒有收尋到相關遊戲')

        self.btnSearch.config(state='active', text='Search')
        self.omGames.config(state='active')
        self.btnSend.config(state='active')

    def botton_getproxy(self):
        self.btnProxy = ttk.Button(
            f4_proxies, text='Get Proxies', width=10, command=self.btn_GetProxy)

    def btn_GetProxy(self):
        pass

    def botton_send(self):
        self.btnSend = ttk.Button(
            f1_search, text='send', width=10, command=self.btnSendClick)

    def btnSendClick(self):
        self.btnSearch.config(state='disabled')
        self.omGames.config(state='disabled')
        self.btnSend.config(state='disabled')
        t = threading.Thread(target=self.btn_set_lisbox)
        t.start()

    def btn_set_lisbox(self):
        self.itemLists, self.itemLists_Deals = pagespidy.getPageIndex(
            self.gameNum, self.serverNum, self.itemNum, self.etyItem.get())

        a, b = [], []
        # 重新排列價格 低->高
        self.itemLists = sorted(
            self.itemLists, key=lambda s: int(s[2][:-1].replace(',', '')))
        for itemList in self.itemLists:
            a += [itemList[0][:20] + '\t\t' + itemList[2]]

        self.varList.set(a)
        # 未使用Mult-Thread所以不需要排列
        for itemLists_Deal in self.itemLists_Deals:
            b += [itemLists_Deal[0][:20] + '\t\t' + itemLists_Deal[2]]
        self.varList1.set(b)
        del a
        del b

        self.btnSearch.config(state='active')
        self.omGames.config(state='active')
        self.btnSend.config(state='active')

    # ---進度條---
    # def progressBar(self):
    #     self.progressbar = ttk.Progressbar(
    #         f1_search, orient="horizontal", length=300, mode="determinate")

    # //MARK: object_pack

    def object_pack(self):
        # Frame1
        self.etyGame.grid(row=0, column=0, padx=37, pady=11)
        self.btnSearch.grid(row=0, column=1, padx=1, pady=11)
        self.omGames.grid(row=0, column=2, padx=20, pady=11)
        self.omServers.grid(row=0, column=3, padx=20, pady=11)
        self.omItems.grid(row=0, column=4, padx=20, pady=11)
        self.etyItem.grid(row=0, column=5, padx=10, pady=11)
        self.btnSend.grid(row=0, column=6, padx=1, pady=11)
        # self.progressbar.grid(row=1, column=0, columnspan= 6, padx=10, pady=5)
        # Frame2
        self.leb01.grid(row=0, column=0)
        self.leb02.grid(row=0, column=1)
        self.lb.grid(row=1, column=0, padx=1, pady=1)
        self.lb1.grid(row=1, column=1, padx=1, pady=1)
        self.btnProxy.place(x=0, y=0)
        list_log.pack()


# //MARK: src_image
def src_image():
    src_image = {}
    src_image['img_bg'] = ImageTk.PhotoImage(Image.open(img_bg_path))
    src_image['img_bg01'] = ImageTk.PhotoImage(Image.open(img_bg01_path))
    src_image['img_icon'] = ImageTk.PhotoImage(Image.open(img_icon_path))
    return src_image

# -------Math--------


def findIn2DTo1D(list2D, find):
    a = np.array(list2D)
    mask = a == find
    count = 0
    for i in mask:
        for j in i:
            if j == True:
                return count
        count += 1
    return None

# \\MARK: give and get
# -------取得log---------


def get_log_index():
    return log_index
# -------使用log---------


def log(text):
    global log_index
    log_index = pagespidy.get_log_index()
    log_index.append(text)
    var_Log.set(log_index)
    list_log.selection_clear(0, "end")
    list_log.selection_set("end")
    # 以下兩個方法都是focus最後一行
    list_log.see("end")
    # list_log.yview_moveto(1)


# //MARK: __Main__
if __name__ == '__main__':

    # //MARK: init
    var_Log = ''
    list_log = ''
    log_index = []

    img_bg_path = join(CURRENT_DIR, './src/image/bg.png')
    img_bg01_path = join(CURRENT_DIR, './src/image/bg01.png')
    img_icon_path = join(CURRENT_DIR, './src/image/icon.jpg')

    # ------serface-------
    win = tk.Tk()
    win.geometry('1240x600')
    win.title('RO仙境傳說8591市場快速查詢程式')
    # win.configure(bg='LightPink')

    # ----圖片變數要在win之後否則error
    img_bg = src_image()['img_bg']
    img_bg01 = src_image()['img_bg01']
    img_icon = src_image()['img_icon']

    # 中容器
    canvas = tk.Canvas(win, width=1240, height=865,
                       highlightthickness=0, borderwidth=0)
    canvas.create_image(600, 400, image=img_bg01)
    canvas.pack()

    f1_search = tk.Frame(win)
    f2_list = tk.Frame(win)
    f3_log = tk.Frame(win)
    f4_proxies = tk.Frame(win, width=80, height=25)
    f5_lb01 = tk.Frame(win, width=80, height=40)
    f6_lb02 = tk.Frame(win, width=80, height=40)

    canvas.create_window(650, 580, width=1300, height=50, window=f1_search)
    canvas.create_window(445, 270, width=817, height=433, window=f2_list)
    canvas.create_window(445, 522, width=817, height=64, window=f3_log)
    canvas.create_window(55, 25, width=80, height=25, window=f4_proxies)
    canvas.create_window(250, 27, width=125, height=38, window=f5_lb01)
    canvas.create_window(650, 27, width=125, height=38, window=f6_lb02)
    # f4_proxies.place(x=5, y=5)
    # f5_lb01.place(x=170, y=11)
    # f6_lb02.place(x=590, y=11)

    App(f1_search, f2_list, f3_log, f4_proxies, f5_lb01, f6_lb02)
    pagespidy.set_var_Log(var_Log, list_log)
    getproxy.set_var_Log(var_Log, list_log)
    # --------Background-------
    # t = threading.Thread(target=pagespidy.init_get_cookie)
    # t.start()

    # --------TkinterEnd-------
    win.mainloop()
