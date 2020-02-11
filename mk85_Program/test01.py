# from tkinter import *
# import tkinter.simpledialog as sp
# import webbrowser
# data = [
#     ['Python', 'https://www.google.com.tw/'],
#     ['tkinter', 'https://tw.news.yahoo.com/'],
#     ['Widget', 'https://www.google.com/search?q=%E7%BF%BB%E8%AD%AF&oq=%E7%BF%BB%E8%AD%AF&aqs=chrome..69i57j69i59j0l3j69i60j69i61l2.2252j0j4&sourceid=chrome&ie=UTF-8']
# ]
# win = Tk()
# lb = Listbox(win, selectmode="EXTENDED")
# for item in data:
#     lb.insert(END, item[0])

# def popupmsg(event):
#     popup = Tk()
#     url = data[lb.curselection()[0]][1]
#     def windesokay():
#         webbrowser.open(url)
#         popup.destroy()
#     def windescancel():
#         popup.destroy()

#     lab = Label(popup, text='你將前往下列網址\n' + url)
#     lab.pack()
#     btn = Button(popup,text="Okay",command = windesokay)
#     btn.pack()
#     btn = Button(popup,text="Cancel",command = windescancel)
#     btn.pack()
#     popup.mainloop()


# lb.bind('<Double-Button-1>', popupmsg)

# lb.pack()
# win.mainloop()


