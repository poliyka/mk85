import tkinter as tk
from tkinter import StringVar, ttk
import webbrowser
import requests
from bs4 import BeautifulSoup
from setting import USER_AGENT, CURRENT_DIR
from urllib.request import urlretrieve
import os
from PIL import ImageTk, Image
from os.path import join


class App_start:
    def __init__(self, popup, url, datas, img, deal_time=None):
        self.url = url
        self.popup = popup
        self.datas = datas
        self.img = img
        self.deal_time = deal_time

        self.label()
        self.button()
        self.packSpace()

    def label(self):
        self.lab = ttk.Label(self.popup,
                             image=self.img,
                             relief='groove'
                             )

        self.lab_detail = tk.Label(self.popup,
                                   text='賣家留言:\n' +
                                   self.datas[index(self.datas, 0)],
                                   anchor='nw',
                                   height=28,
                                   width=25,
                                   bg='white',
                                   justify='left',
                                   relief='solid',
                                   wraplength=160
                                   )
        self.lab_goodsNum = ttk.Label(self.popup,
                                      text=index(self.datas, 1) +
                                      self.datas[index(self.datas, 1)],
                                      anchor='nw',
                                      justify='left'
                                      )

        if self.deal_time == None:
            self.lab_time = ttk.Label(self.popup,
                                      text=index(self.datas, 2) +
                                      self.datas[index(self.datas, 2)],
                                      anchor='nw',
                                      justify='left'
                                      )
        else:
            self.lab_time = ttk.Label(
                self.popup,
                text='成交時間: ' + self.deal_time[0] + ' ' + self.deal_time[1],
                anchor='nw',
                justify='left'
            )

        self.lab_type = ttk.Label(self.popup,
                                  text=index(self.datas, 3) +
                                  self.datas[index(self.datas, 3)],
                                  anchor='nw',
                                  justify='left'
                                  )

        self.lab_num = ttk.Label(self.popup,
                                 text=index(self.datas, 4) + ' '+
                                 self.datas[index(self.datas, 4)],
                                 anchor='nw',
                                 justify='left'
                                 )

        self.lab_evaluation = ttk.Label(self.popup,
                                        text=index(self.datas, 5) + ' ' +
                                        self.datas[index(self.datas, 5)],
                                        anchor='nw',
                                        justify='left'
                                        )

        self.lab_percent = ttk.Label(self.popup,
                                     text=index(self.datas, 6) + ' ' +
                                     self.datas[index(self.datas, 6)],
                                     anchor='nw',
                                     justify='left'
                                     )

        self.lab_speed = ttk.Label(self.popup,
                                   text=index(self.datas, 7) +
                                   self.datas[index(self.datas, 7)],
                                   anchor='nw',
                                   justify='left'
                                   )

    def button(self):
        self.btn_ok = ttk.Button(
            self.popup, text="打開頁面", command=self.windestroy)
        # self.btn_can = ttk.Button(
        #     self.popup, text="Cancel", command=self.wincancel)

    def packSpace(self):
        self.lab.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
        self.lab_detail.grid(row=0, rowspan=10, column=1,
                             padx=5, pady=5, sticky='nw')
        self.lab_goodsNum.grid(row=1, column=0, padx=5, sticky='nw')
        self.lab_time.grid(row=2, column=0, padx=5, sticky='nw')
        self.lab_type.grid(row=3, column=0, padx=5, sticky='nw')
        self.lab_num.grid(row=4, column=0, padx=5, sticky='nw')
        self.lab_evaluation.grid(row=5, column=0, padx=5, sticky='nw')
        self.lab_percent.grid(row=6, column=0, padx=5, sticky='nw')
        self.lab_speed.grid(row=7, column=0, padx=5, sticky='nw')

        self.btn_ok.grid(row=9, column=0, padx=5)
        # self.btn_can.grid(row = 9, column = 1, padx=5, sticky= 'nw')

    def windestroy(self):
        webbrowser.open(self.url)
        self.popup.destroy()

    # def wincancel():
    #     self.popup.destroy()


def index(dictionary, i):
    index = list(dictionary.keys())[i]
    return index


def App(win, url, title, deal_time=None):
    headers = {
        'User-Agent': USER_AGENT
    }

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    datas = {}

    # 詳細說明
    if deal_time == None:
        de = soup.find('div', class_='editor-detail')
        detail = de.text.strip()
        datas['內文'] = detail

    # 商品資訊、刊登時間

        info = soup.find('div', class_='Wgoods_info')
        infos = info.find_all('span')
        info = []
        for i, ifo in enumerate(infos):
            if i == 0:
                info.append(ifo.text.strip()[:-5].replace(' ', ''))
            else:
                info.append((ifo.text.strip()))

        datas[info[0].split('：')[0] + '：'] = info[0].split('：')[1]
        datas[info[1].split('：')[0] + '：'] = info[1].split('：')[1]
        datas[info[2].split('：')[0] + '：'] = info[2].split('：')[1]

        # 賣家資料
        seller = soup.find('div', class_='line')
        tds = seller.find_all('td')
        num = []
        for td in tds[:2]:
            num.append(td.text.strip())
        datas[num[0]] = num[1]

        # 賣家評價
        ul = seller.find('ul', class_='tableBottom')
        lis = ul.find_all('li')
        evaluation = lis[0].text.strip().split('\n')
        datas[evaluation[0]] = evaluation[1]

        # 正評率
        percent = lis[1].text.strip().split('\n')
        datas[percent[0]] = percent[1]

        # 交易速度
        speed = []
        font = lis[2].find('font', class_='tdbLeft')
        speed.append(font.text.strip())
        point = lis[2].find(id='font-color')
        speed.append(point.text.strip()+'/5')
        datas[speed[0]] = speed[1]

    else:
        # 詳細說明
        detail = soup.find('div', class_='user-content')
        detail = detail.text.strip()
        datas['內文'] = detail

        # 商品資訊、刊登時間
        info = soup.find('div', class_='Wgoods_info')
        infos = info.find_all('span')
        info = []
        for i, ifo in enumerate(infos):
            if i == 2:
                continue
            else:
                info.append((ifo.text.strip()))

        datas[info[0].split('：')[0] + '：'] = info[0].split('：')[1]
        datas[info[1].split('：')[0] + '：'] = info[1].split('：')[1]
        datas[info[2].split('：')[0] + '：'] = info[2].split('：')[1]

        # 賣家資料
        seller = soup.find('div', class_='seller')
        td = seller.find('li')
        num = [td.find('span', class_='seller-item').text.strip(),
               td.find('div', class_='sellerInfo').text.strip()]
        datas[num[0]] = num[1]

        # 賣家評價
        ul = seller.find('ul', class_='seller-list seller-eval clearfix')
        lis = ul.find('li')
        spans = lis.find_all('span')
        evaluation = []
        for span in spans:
            evaluation.append(span.text.strip())
        datas[evaluation[0]] = evaluation[1]

        # 正評率
        lis = ul.find_all('li')
        percent0 = lis[1].find('span', class_='seller-item')
        percent0 = percent0.text.strip().replace('\xa0', '')
        percent1 = lis[1].find('span', class_='seller-info')
        percent1 = percent1.text.strip()
        datas[percent0] = percent1

        # 交易速度
        speed = []
        font = lis[2].find(id='dealspeed-title').find('span')
        speed.append(font.text.strip())
        point = lis[2].find_all('span')[2]
        speed.append(point.text.strip().split('/')[0].replace('(', '') + '/5')
        datas[speed[0]] = speed[1]

    # 圖片下載
    try:
        # 抓圖
        pic = soup.find('img', class_='ware-pic')
        img = 'https:' + pic['src']
        urlretrieve(img, 'mk85_Program\src\image\image.png')
        img_path = join(CURRENT_DIR, './src/image/image.png')
        src_image = {'img': ImageTk.PhotoImage(
            Image.open(img_path))}
    except:
        noimg_path = join(CURRENT_DIR, './src/image/noimage.png')
        src_image = {'img': ImageTk.PhotoImage(
            Image.open(noimg_path).resize((250, 250)))}

    popup = tk.Toplevel(win)
    if deal_time == None:
        popup.title('(待交易)'+title)
    else:
        popup.title('(已交易)'+title)

    App_start(popup, url, datas, src_image['img'], deal_time)
    popup.mainloop()


if __name__ == '__main__':
    win = tk.Tk()
    url = 'https://www.8591.com.tw/mallList-wareDetail.html?id=2357213469'
    title = '123'
    App(win, url, title)
