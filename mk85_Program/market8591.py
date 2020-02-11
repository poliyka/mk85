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
from setting import CURRENT_DIR
from os.path import join

#//MARK: init
img_bg_path = join(CURRENT_DIR, './src/image/bg01.jpg')
img_icon_path = join(CURRENT_DIR, './src/image/icon.jpg')
log_index = []

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

#//MARK: GUI surface
class App:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
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
        self.entrySerchGame()
        self.botton_Serch()
        self.optinMenu(self.games, self.servers, self.items)
        self.listbox()
        self.log_place()
        self.entrySerchItem()
        self.botton_send()
        # self.progressBar()
        self.object_pack()

    # //MARK: Label_GUI
    def titleLabel(self):
        self.leb01 = tk.Label(f2, text='待交易項目', font=(
            '標楷體', 12), width=15, height=2, bg='Pink')
        self.leb02 = tk.Label(f2, text='已完成交易項目', font=(
            '標楷體', 12), width=15, height=2, bg='Plum')
        self.scro = ttk.Scrollbar(f2)

    def background_label(self):
        global img_bg
        self.background_label01 = tk.Label(f1, image=img_bg)
        self.background_label01.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label02 = tk.Label(f2, image=img_bg)
        self.background_label02.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label03 = tk.Label(f3, image=img_bg)
        self.background_label03.place(x=0, y=0, relwidth=1, relheight=1)

    # //MARK: optinMenu_GUI
    def optinMenu(self, games, server, item):
        self.var01 = StringVar()
        self.var02 = StringVar()
        self.var03 = StringVar()
#       創建optionMenu 控制元件
#       此處初始下拉選單套入擷取資料中的伺服器名稱
#       tk.OptionMenu 有另一種樣式
#       ttk.OptionMenu(介面,存取之變量,初始文字,選單中的值1,選單中的值2,...,command = 呼叫函式)
#       ttk.OptionMenu(介面,存取之變量,初始文字,*list,...,command = 呼叫函式)
        self.omGames = ttk.OptionMenu(
            f1, self.var01, '請選擇遊戲', *games, direction='below', command=self.saveGame_Option)

        self.omServers = ttk.OptionMenu(
            f1, self.var02, '請選擇伺服器', *server, direction='below', command=self.saveServer_Option)

        self.omItems = ttk.OptionMenu(
            f1, self.var03, '請選擇物品', *item, direction='below', command=self.saveItem_Option)

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
    def entrySerchGame(self):
        self.etyGame = ttk.Entry(f1, font=('標楷體', 12), width=15)

    def entrySerchItem(self):
        self.etyitem = ttk.Entry(f1, font=('標楷體', 12), width=15)

    #//MARK: Listbox_GUI
    def listbox(self):
        self.varList = tk.StringVar()
        self.varList.set([])
        self.lb = tk.Listbox(f2, listvariable=self.varList, font=(
            '標楷體', 12), bg='sky blue', width=50, height=25, highlightcolor="MidnightBlue", selectbackground="pink", selectforeground="MidnightBlue", borderwidth=2, activestyle='none')

        self.varList1 = tk.StringVar()
        self.varList1.set([])
        self.lb1 = tk.Listbox(f2, listvariable=self.varList1, font=(
            '標楷體', 12), selectmode='SINGLE', bg='sky blue', width=50, height=25, highlightcolor="MidnightBlue", selectbackground="pink", selectforeground="MidnightBlue", borderwidth=2, activestyle='none')
        self.lb.bind('<Double-Button-1>', self.clickLink)
        self.lb1.bind('<Double-Button-1>', self.clickLink1)

    def log_place(self):
        global var_Log
        global list_log
        var_Log = tk.StringVar()
        var_Log.set([])

        self.scrollbar = Scrollbar(f3)
        self.scrollbar.pack(side='right', fill='y')

        list_log = tk.Listbox(f3, listvariable=var_Log, font=(
            '標楷體', 12), width=50, height=30, highlightcolor="pink", selectbackground="MidnightBlue", borderwidth=2, activestyle='none', yscrollcommand=self.scrollbar.set)

        self.scrollbar.config(command=list_log.yview)

    # //MARK: poupwindow_GUI
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

    #//MARK: Botton_GUI
    def botton_Serch(self):
        self.btnSearch = ttk.Button(
            f1, text='Serch', width=10, command=self.btn_search_click)

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

        self.btnSearch.config(state='active', text='Serch')
        self.omGames.config(state='active')
        self.btnSend.config(state='active')

    def btn_search_click(self):
        self.btnSearch.config(state='disabled', text='Serching...')
        self.omGames.config(state='disabled')
        self.btnSend.config(state='disabled')
        t = threading.Thread(target=self.setmenu)
        t.start()

    def botton_send(self):
        self.btnSend = ttk.Button(
            f1, text='send', width=10, command=self.btnSendClick)

    def btn_set_lisbox(self):
        self.itemLists, self.itemLists_Deals = pagespidy.getPageIndex(
            self.gameNum, self.serverNum, self.itemNum, self.etyitem.get())

        a, b = [], []
        # 重新排列價格 低->高
        self.itemLists = sorted(
            self.itemLists, key=lambda s: int(s[2][:-1].replace(',', '')))
        for itemList in self.itemLists:
            a += [itemList[0][:20] + '\t\t' + itemList[2]]

        self.varList.set(a)
        # 未使用MultThread所以不需要排列
        for itemLists_Deal in self.itemLists_Deals:
            b += [itemLists_Deal[0][:20] + '\t\t' + itemLists_Deal[2]]
        self.varList1.set(b)
        del a
        del b

        self.btnSearch.config(state='active')
        self.omGames.config(state='active')
        self.btnSend.config(state='active')

    def btnSendClick(self):
        self.btnSearch.config(state='disabled')
        self.omGames.config(state='disabled')
        self.btnSend.config(state='disabled')
        t = threading.Thread(target=self.btn_set_lisbox)
        t.start()

    def progressBar(self):
        self.progressbar = ttk.Progressbar(
            f1, orient="horizontal", length=300, mode="determinate")
    
    # //MARK: object_pack
    def object_pack(self):
        # Frame1
        self.etyGame.grid(row=0, column=0, padx=10, pady=5)
        self.btnSearch.grid(row=0, column=1, padx=10, pady=5)
        self.omGames.grid(row=0, column=2, padx=10, pady=5)
        self.omServers.grid(row=0, column=3, padx=10, pady=5)
        self.omItems.grid(row=0, column=4, padx=10, pady=5)
        self.etyitem.grid(row=0, column=5, padx=10, pady=5)
        self.btnSend.grid(row=0, column=6, padx=10, pady=5)
        # self.progressbar.grid(row=1, column=0, columnspan= 6, padx=10, pady=5)
        # Frame2
        self.leb01.grid(row=0, column=0, padx=5, pady=5)
        self.leb02.grid(row=0, column=1, padx=5, pady=5)
        self.lb.grid(row=1, column=0, padx=2, pady=5)
        self.lb1.grid(row=1, column=1, padx=2, pady=5)
        list_log.pack()


# //MARK: src_image
def src_image():
    src_image = {}
    src_image['img_bg'] = ImageTk.PhotoImage(Image.open(img_bg_path))
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


# -------Main--------
if __name__ == '__main__':

    # -------init--------
    var_Log = ''
    list_log = ''
# ------serface-------
    win = tk.Tk()
    win.geometry('1240x600')
    win.title('RO仙境傳說8591市場快速查詢程式')
    img_bg = src_image()['img_bg']
    win.configure(bg='LightPink')

    canvas = tk.Canvas(win, width=1024, height=865,
                       highlightthickness=0, borderwidth=0, bg='LightPink')
    # canvas.create_image(400, 400, image=img_bg)
    canvas.pack()

    f1 = tk.Frame(win, width=390, height=300, borderwidth=5)
    f1.pack(side='bottom', padx=3, pady=3)
    f2 = tk.Frame(win, width=390, height=600, borderwidth=5)
    f2.pack(side='top', padx=3, pady=3)
    f3 = tk.Frame(win, width=390, height=600, borderwidth=5)
    f3.pack(side='right', padx=3, pady=3)

    canvas.create_window(517, 570, width=1165, height=50, window=f1)
    canvas.create_window(350, 290, width=830, height=500, window=f2)
    canvas.create_window(950, 290, width=300, height=500, window=f3)

    App(f1, f2)
    pagespidy.set_var_Log(var_Log, list_log)
    # --------Background-------
    # t = threading.Thread(target=pagespidy.init_get_cookie)
    # t.start()

    # --------TkinterEnd-------
    win.mainloop()
