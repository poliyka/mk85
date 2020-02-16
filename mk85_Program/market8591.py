import numpy as np
import time
import threading
import webbrowser
import pagespidy
import getproxy
import changeproxy
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from queue import Queue
from setting import CURRENT_DIR
from os.path import join


# //MARK: GUI surface
class App_start:
    def __init__(self):
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
        self.button()
        self.bind()
        self.entrySearchGame()
        self.optionMenu(self.games, self.servers, self.items)
        self.listbox()
        self.log_place()
        self.entrySearchItem()
        # self.progressBar()
        self.object_pack()

    # //MARK: Label_GUI
    def titleLabel(self):
        self.leb01 = tk.Label(f5_lb01,
                              text='待交易項目',
                              font=('標楷體', 12),
                              width=15,
                              height=2,
                              bg='Pink'
                              )

        self.leb02 = tk.Label(f6_lb02,
                              text='已完成交易項目',
                              font=('標楷體', 12),
                              width=15,
                              height=2,
                              bg='Plum'
                              )

    def background_label(self):
        global img_icon
        self.background_label01 = tk.Label(f1_search, image=img_icon)
        self.background_label01.place(x=0, y=0, relwidth=1, relheight=1)

    # //MARK: optionMenu_GUI

    def optionMenu(self, games, server, item):
        self.varGames = StringVar()
        self.varServers = StringVar()
        self.varItems = StringVar()
        # 創建optionMenu 控制元件
        # 此處初始下拉選單套入擷取資料中的伺服器名稱
        # tk.OptionMenu 有另一種樣式
        # ttk.OptionMenu(介面,存取之變量,初始文字,選單中的值1,選單中的值2,...,command = 呼叫函式)
        # ttk.OptionMenu(介面,存取之變量,初始文字,*list,...,command = 呼叫函式)
        self.omGames = ttk.OptionMenu(f1_search,
                                      self.varGames,
                                      '請選擇遊戲',
                                      *games,
                                      direction='below',
                                      command=self.saveGame_Option
                                      )

        self.omServers = ttk.OptionMenu(f1_search,
                                        self.varServers,
                                        '請選擇伺服器',
                                        *server,
                                        direction='below',
                                        command=self.saveServer_Option
                                        )

        self.omItems = ttk.OptionMenu(f1_search,
                                      self.varItems,
                                      '請選擇物品',
                                      *item, direction='below',
                                      command=self.saveItem_Option
                                      )

    # 儲存選取變量
    def saveGame_Option(self, option):
        gameOption = self.varGames.get()
        self.btn_hide()

        t = threading.Thread(target=self.getOtherList, args=(gameOption,))
        t.start()
        # 取得代號
        self.gameNum = self.games[findIn2DTo1D(self.games, gameOption)][0]

    def saveServer_Option(self, option):
        serverOption = self.varServers.get()
        # 取得代號
        self.serverNum = self.servers[findIn2DTo1D(
            self.servers, serverOption)][0]

    def saveItem_Option(self, option):
        itemOption = self.varItems.get()
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
        self.btn_show()

    # //MARK: Entry_GUI
    def entrySearchGame(self):
        self.etyGame = ttk.Entry(f1_search, font=('標楷體', 12), width=15)
        self.etyGame.bind('<Return>',self.etyGameKey)

    def entrySearchItem(self):
        self.etyItem = ttk.Entry(f1_search, font=('標楷體', 12), width=15)
        self.etyItem.bind('<Return>',self.etyItemKey)

    # //MARK: Entry_method
    def etyGameKey(self,event):
        if self.etyGame.get() != '':
            self.btn_hide()
            t = threading.Thread(target=self.setmenu)
            t.start()

        else:
            log('請輸入要查詢的遊戲...')
    
    def etyItemKey(self,event):
        if self.varGames.get() != '請選擇遊戲':
            if self.etyItem.get() != '':
                self.btn_hide()
                t = threading.Thread(target=self.btn_set_lisbox)
                t.start()
            else:
                mb1 = mb.askokcancel('Warning', '沒有輸入收尋條件將會爬取大量數據確定繼續?')
                if mb1 == True:
                    self.btn_hide()
                    t = threading.Thread(target=self.btn_set_lisbox)
                    t.start()
                else:
                    log('搜尋中斷...')
        else:
            self.btn_show()
            log('請選擇遊戲在送出')

    # //MARK: Listbox_GUI
    def listbox(self):
        self.varList = tk.StringVar()
        self.varList.set([])
        self.lb = tk.Listbox(f2_list,
                             listvariable=self.varList,
                             font=('標楷體', 12),
                             bg='sky blue',
                             width=50,
                             height=25,
                             highlightcolor="MidnightBlue",
                             selectbackground="pink",
                             selectforeground="MidnightBlue",
                             borderwidth=2,
                             activestyle='none',
                             justify='right'
                             )

        self.varList1 = tk.StringVar()
        self.varList1.set([])
        self.lb1 = tk.Listbox(f2_list,
                              listvariable=self.varList1,
                              font=('標楷體', 12),
                              bg='sky blue',
                              width=50,
                              height=25,
                              highlightcolor="MidnightBlue",
                              selectbackground="pink",
                              selectforeground="MidnightBlue",
                              borderwidth=2,
                              activestyle='none',
                              justify='right'
                              )

        self.lb.bind('<Double-Button-1>', self.clickLink)
        self.lb1.bind('<Double-Button-1>', self.clickLink1)

    def log_place(self):
        global var_Log
        global list_log
        var_Log = tk.StringVar()
        var_Log.set([])

        list_log = tk.Listbox(f3_log,
                              listvariable=var_Log,
                              font=('標楷體', 12),
                              width=102,
                              height=4,
                              bg='DarkSlateBlue',
                              fg='pink',
                              highlightcolor="pink",
                              selectbackground="MidnightBlue",
                              borderwidth=2,
                              activestyle='none'
                              )

        # 有scrollbar版本(待研究)
        # self.scrollbar = Scrollbar(f3_log)
        # self.scrollbar.pack(side='right', fill='y')
        # list_log = tk.Listbox(f3_log, listvariable=var_Log, font=(
        #     '標楷體', 12), width=102, height=3, bg='DarkSlateBlue', highlightcolor="pink", selectbackground="MidnightBlue", borderwidth=2, activestyle='none', yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=list_log.yview)

    # //MARK: popupWindow_GUI
    def clickLink(self, event):
        popup = tk.Toplevel(win)
        popup.title('(待交易)詳細資訊')
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
        popup = tk.Toplevel(win)
        popup.title('(已完成)詳細資訊')
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

    # //MARK: Button_GUI
    def button(self):
        global img_icon_ana
        global img_icon_prx
        self.btnSearch = ttk.Button(f1_search,
                                    text='Search',
                                    width=10,
                                    cursor='hand2',
                                    command=self.btn_search_click
                                    )

        self.btnSend = ttk.Button(f1_search,
                                  text='send',
                                  width=10,
                                  cursor='hand2',
                                  command=self.btn_send_click
                                  )

        self.btnProxy = ttk.Button(f4_proxies,
                                   image=img_icon_prx,
                                   width=3,
                                   cursor='hand2',
                                   command=self.btn_GetProxy
                                   )

        self.btnUp = ttk.Button(f7_up,
                                text='↑',
                                width=3,
                                cursor='hand2',
                                state='disabled',
                                command=self.btn_sort_up
                                )

        self.btnDown = ttk.Button(f8_down,
                                  text='↓',
                                  width=3,
                                  cursor='hand2',
                                  state='disabled',
                                  command=self.btn_sort_down
                                  )

        self.btnAna = ttk.Button(f9_analytics,
                                 image=img_icon_ana,
                                 width=3,
                                 cursor='hand2',
                                 state='disabled',
                                 command=self.btn_analytics
                                 )

    # //MARK: bind
    def bind(self):
        self.btnUp.bind("<Enter>", self.bind_up_Enter)
        self.btnUp.bind("<Leave>", self.bind_up_Leave)
        self.btnDown.bind("<Enter>", self.bind_down_Enter)
        self.btnDown.bind("<Leave>", self.bind_down_Leave)
        self.btnProxy.bind("<Enter>", self.bind_proxy_Enter)
        self.btnProxy.bind("<Leave>", self.bind_proxy_Leave)
        self.btnAna.bind("<Enter>", self.bind_ana_Enter)
        self.btnAna.bind("<Leave>", self.bind_ana_Leave)

    def bind_up_Enter(self, bind):
        self.bn_up = tk.Label(canvas,
                              text='價格↑',
                              font=('標楷體', 14),
                              width=8,
                              height=1,
                              bg='Pink',
                              fg='MidnightBlue'
                              )
        self.bn_up.place(x=900, y=350)

    def bind_down_Enter(self, bind):
        self.bn_down = tk.Label(canvas,
                                text='價格↓',
                                font=('標楷體', 14),
                                width=8, height=1,
                                bg='Pink',
                                fg='MidnightBlue')
        self.bn_down.place(x=900, y=420)

    def bind_ana_Enter(self, bind):
        self.btnAna = tk.Label(canvas,
                               text='分析價格',
                               font=('標楷體', 14),
                               width=8,
                               height=1,
                               bg='Pink',
                               fg='MidnightBlue'
                               )
        self.btnAna.place(x=900, y=450)

    def bind_proxy_Enter(self, bind):
        self.btnProxy = tk.Label(canvas,
                                 text='取得代理',
                                 font=('標楷體', 14),
                                 width=8,
                                 height=1,
                                 bg='Pink',
                                 fg='MidnightBlue'
                                 )
        self.btnProxy.place(x=900, y=500)

    def bind_up_Leave(self, bind):
        self.bn_up.place_forget()

    def bind_down_Leave(self, bind):
        self.bn_down.place_forget()

    def bind_ana_Leave(self, bind):
        self.btnAna.place_forget()

    def bind_proxy_Leave(self, bind):
        self.btnProxy.place_forget()

    # button active/disabled
    def btn_show(self):
        self.btnSearch.config(state='active', text='Search')
        self.omGames.config(state='active')
        self.btnSend.config(state='active')

    def btn_hide(self):
        self.btnSearch.config(state='disabled', text='Searching...')
        self.omGames.config(state='disabled')
        self.btnSend.config(state='disabled')

    # //MARK: btn_method

    def btn_search_click(self):
        if self.etyGame.get() != '':
            self.btn_hide()
            t = threading.Thread(target=self.setmenu)
            t.start()

        else:
            log('請輸入要查詢的遊戲...')
    
    def setmenu(self):
        data = pagespidy.getGameList(self.etyGame.get())
        if data == 'disconnent':
            log('請檢查是否被鎖IP')
        else:
            if data != 'error':
                try:
                    self.games = [i for i in data]
                    self.omGames.set_menu(
                        self.games[0][1], *(i[1] for i in self.games))
                    log('搜尋完成')
                except:
                    log('沒有搜尋到相關遊戲')
            else:
                log('無法取得網頁資料')

        self.btn_show()

    def btn_send_click(self):
        if self.varGames.get() != '請選擇遊戲':
            if self.etyItem.get() != '':
                self.btn_hide()
                t = threading.Thread(target=self.btn_set_lisbox)
                t.start()
            else:
                mb1 = mb.askokcancel('Warning', '沒有輸入收尋條件將會爬取大量數據確定繼續?')
                if mb1 == True:
                    self.btn_hide()
                    t = threading.Thread(target=self.btn_set_lisbox)
                    t.start()
                else:
                    log('搜尋中斷...')
        else:
            self.btn_show()
            log('請選擇遊戲在送出')

    def btn_set_lisbox(self):
        self.itemLists, self.itemLists_Deals = pagespidy.getPageIndex(
            self.gameNum, self.serverNum, self.itemNum, self.etyItem.get())

        if (self.itemLists != [] and self.itemLists_Deals != []):
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
            self.btn_show()
            self.btnAna.config(state='active')
            self.btnUp.config(state='active')
        else:
            log('沒有人在買賣喔')
            self.btn_show()
            self.btnAna.config(state='active')
            self.btnUp.config(state='active')

    def btn_sort_up(self):
        a = []
        b = []
        self.itemLists = sorted(
            self.itemLists, key=lambda s: int(s[2][:-1].replace(',', '')), reverse=True)
        for itemList in self.itemLists:
            a += [itemList[0][:20] + '\t\t' + itemList[2]]
        self.varList.set(a)

        self.itemLists_Deals = sorted(
            self.itemLists_Deals, key=lambda s: int(s[2][:-1].replace(',', '')), reverse=True)

        for itemLists_Deal in self.itemLists_Deals:
            b += [itemLists_Deal[0][:20] + '\t\t' + itemLists_Deal[2]]
        self.varList1.set(b)
        self.btnUp.config(state='disable')
        self.btnDown.config(state='active')

    def btn_sort_down(self):
        a = []
        b = []
        self.itemLists = sorted(
            self.itemLists, key=lambda s: int(s[2][:-1].replace(',', '')))
        for itemList in self.itemLists:
            a += [itemList[0][:20] + '\t\t' + itemList[2]]
        self.varList.set(a)

        self.itemLists_Deals = sorted(
            self.itemLists_Deals, key=lambda s: int(s[2][:-1].replace(',', '')))

        for itemLists_Deal in self.itemLists_Deals:
            b += [itemLists_Deal[0][:20] + '\t\t' + itemLists_Deal[2]]
        self.varList1.set(b)
        self.btnDown.config(state='disable')
        self.btnUp.config(state='active')

    # //MARK: analytics popup
    def btn_analytics(self):
        pass
    
    # //MARK: GetProxy popup
    def btn_GetProxy(self):
        t = threading.Thread(target=changeproxy.App(win))
        t.start()
        time.sleep(0.5)
        changeproxy.set_host_entry(pagespidy.get_host_ip())

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
        self.btnUp.place(x=0, y=0)
        self.btnDown.place(x=0, y=0)
        self.btnAna.place(x=0, y=0)
        list_log.pack()


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


# //MARK: src_image
def src_image():
    img_bg_path = join(CURRENT_DIR, './src/image/bg.png')
    img_bg01_path = join(CURRENT_DIR, './src/image/bg01.png')
    img_icon_path = join(CURRENT_DIR, './src/image/icon.jpg')
    img_icon_ana_path = join(CURRENT_DIR, './src/image/icon_ana.png')
    img_icon_prx_path = join(CURRENT_DIR, './src/image/icon_prx.png')

    src_image = {}
    src_image['img_bg'] = ImageTk.PhotoImage(Image.open(img_bg_path))
    src_image['img_bg01'] = ImageTk.PhotoImage(Image.open(img_bg01_path))
    src_image['img_icon'] = ImageTk.PhotoImage(Image.open(img_icon_path))
    src_image['img_icon_ana'] = ImageTk.PhotoImage(
        Image.open(img_icon_ana_path))
    src_image['img_icon_prx'] = ImageTk.PhotoImage(
        Image.open(img_icon_prx_path))
    return src_image

# Exit


def closeWindow():
    pagespidy.close_chrome()
    win.destroy()


# //MARK: __Main__
if __name__ == '__main__':

    # //MARK: init
    var_Log = ''
    list_log = ''
    chrome = ''
    log_index = []

    # ------serface-------
    win = tk.Tk()
    win.geometry('1240x600')
    win.title('RO仙境傳說8591市場快速查詢程式-v1.9')
    # win.configure(bg='LightPink')

    # ----圖片變數要在win之後否則error
    img_bg = src_image()['img_bg']
    img_bg01 = src_image()['img_bg01']
    img_icon = src_image()['img_icon']
    img_icon_ana = src_image()['img_icon_ana']
    img_icon_prx = src_image()['img_icon_prx']

    # 中容器
    canvas = tk.Canvas(win, width=1240, height=865,
                       highlightthickness=0, borderwidth=0)
    canvas.create_image(600, 400, image=img_bg01)
    canvas.pack()

    f1_search = tk.Frame(win)
    f2_list = tk.Frame(win)
    f3_log = tk.Frame(win)
    f4_proxies = tk.Frame(win)
    f5_lb01 = tk.Frame(win)
    f6_lb02 = tk.Frame(win)
    f7_up = tk.Frame(win)
    f8_down = tk.Frame(win)
    f9_analytics = tk.Frame(win)

    canvas.create_window(650, 580, width=1300, height=50, window=f1_search)
    canvas.create_window(445, 270, width=817, height=433, window=f2_list)
    canvas.create_window(445, 522, width=817, height=64, window=f3_log)
    canvas.create_window(880, 500, width=35, height=35, window=f4_proxies)
    canvas.create_window(250, 27, width=125, height=38, window=f5_lb01)
    canvas.create_window(650, 27, width=125, height=38, window=f6_lb02)
    canvas.create_window(880, 385, width=31, height=25, window=f7_up)
    canvas.create_window(880, 420, width=31, height=25, window=f8_down)
    canvas.create_window(880, 468, width=35, height=35, window=f9_analytics)

    App_start()
    # ---------give------------
    pagespidy.set_var_Log(var_Log, list_log)
    getproxy.set_var_Log(var_Log, list_log)

    # --------Background-------
    # t = threading.Thread(target=pagespidy.init_get_cookie)
    # t.start()

    # --------TkinterEnd-------
    win.protocol('WM_DELETE_WINDOW', closeWindow)
    win.mainloop()
