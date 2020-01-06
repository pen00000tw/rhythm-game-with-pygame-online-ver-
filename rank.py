# login.py
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import db.db
#import dashboard
import register
import selectsong
from PIL import Image, ImageTk
import os
class rankWindow:
    def __init__(self,songname):
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win,
                             width=800, height=600,
                             bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.songname = songname
        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 800 / 2)
        str1 = "800x600+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("排行榜")

    def add_frame(self):
        self.frame = Frame(self.win, height=600, width=800)
        self.frame.place(x=0, y=0)

        treeview = ttk.Treeview(self.frame,height=23,columns=['1','2','3','4','5'],show='headings')
        vbar = ttk.Scrollbar(self.frame,orient=VERTICAL,command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)
        treeview.column('1',width=60,anchor='center')
        treeview.column('2',width=100,anchor='center')
        treeview.column('3',width=120,anchor='center')
        treeview.column('4',width=300,anchor='center')
        treeview.column('5',width=200,anchor='center')
        treeview.heading('1',text='名次')
        treeview.heading('2',text='ID')
        treeview.heading('3',text='分數')
        treeview.heading('4',text='歌名')
        treeview.heading('5',text='遊玩時間')
        treeview.grid()
        treeview.place(x=10,y=10)
        res=db.db.rank(self.songname)
        if res:
            index = 0
            for i in res:
                index+=1
                tmp = list(i)
                tmp.insert(0,index)
                treeview.insert('','end',values=tmp)
        else:
            messagebox.showinfo('錯誤!','查詢失敗或是無紀錄!')
        self.button = Button(self.frame,text="關閉",font='微軟正黑體 15 bold',command=self.win.destroy)
        self.button.place(x=370,y=500)
        self.win.mainloop()