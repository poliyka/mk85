# 8591市場爬蟲程式 v1.8

>待完成

- [ ] 交易圖形化分析(日期/價格)
- [ ] 新增複製貼上功能(pyperclip.copy , paste)
- [ ] chromeDriver 更換代理功能
- [ ] 代理失效刪除功能
- [ ] 點擊項目新增基本資料
- [ ] (研究)左側標籤
- [ ] (研究)同步更新

* * *
>已完成

--ver1.8 (2020/02/13)

- [X] 修復關閉程序但背景程序未關閉問題
- [X] 修正代碼排版增加可視度
- [ ] 代理按鈕實做(進度20%)

--ver1.7 (2020/02/12)

- [X] 修正操作流程上的BUG
- [X] 修正連線失效後處裡
- [X] 正排序/反排序按鈕
- [X] 建立exe執行檔

--ver1.6 (2020/02/11)

- [X] 進行Github 版本控制上傳
- [X] 頁面排版優化
- [X] 新增取得代理按鈕
- [X] 新增Button圖案

--ver1.5 (2020/02/10)

- [X] 改進VScode無法使用相對路徑問題解決辦法
- [X] 解決ChromeDriver重複開啟效能低下問題
- [x] 修正log問題，鍵入方式模組化
- [X] 解決chrome開啟後的Exception

--ver1.0 (2020/02/09)

- [x] 建立GUI介面，使用模組化方式
- [x] 建立可以搜尋所有遊戲的模組
- [x] 分類待交易、已完成交易列表
- [X] 右側LOG模組
- [X] 雙擊項目連接網頁
- [X] 背景圖片放置

* * *

# 使用說明

注意事項 :

1. 取得代理在使用本程式(目前代理按鈕未寫請打開 [__getpoxy.py__](getpoxy.py) 取得)
2. 確定代理文本內不為空白(src/db/[__proxy_List.csv__](src/db))
3. __main__ 程式為 [__market8591.py__](market8591.py)
4. 建議使用03號代理其餘兩個代理並非TW代理可能導致連接失敗
5. 使用Chrome瀏覽器並更新至版本 80.0.3987.87 (正式版本) (64 位元)
6. 沒有安裝相關套件? 沒問題! 我放了一個 market8591.exe 直接運行就可以拉
7. 我的 [Github](https://github.com/poliyka/mk85.git)

使用方式 :

>確定Chrome版本>打開Chrome>設定>關於Chrome>讓他更新至最新版
>鍵入遊戲名稱
<!-- ![image](src/image/bg.jpg) -->
>選擇遊戲>伺服器>雜項>鍵入物品>送出
>更改排序
>雙擊項目可連結至網頁

* * *
未完成:

>目標分析

* * *

# 學習筆記

>pyinstaller

    在cmd環境下cd到檔案目錄
    1.pyinstaller -F -w  --hidden-import pagespidy .\market8591.py
        -F 打包成一個exe文件
        –icon=圖標路徑
        -w 使用視窗，無控制台
        -c 使用控制台，無視窗
        -D 創建一個目錄，包含exe以及其他一些依賴性文件
        --hidden-import module

    2.修改market8591.spec內文 手動import資源
([手動import資源參考](https://codingdailyblog.wordpress.com/2018/03/24/python-pyinstaller%E6%89%93%E5%8C%85exe%E4%B8%80%E4%BD%B5%E5%8C%85%E5%90%AB%E7%85%A7%E7%89%87%E6%AA%94%E6%8A%80%E5%B7%A7/))

    3.再次輸入 pyinstaller -F -w market8591.spec
