# login.py
from tkinter import *
from tkinter import messagebox
import db.db
#import dashboard
import login
from PIL import Image, ImageTk
import os
class RegisterWindow:
    def __init__(self):
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win,
                             width=600, height=500,
                             bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)

        # disable resize of the window
        self.win.resizable(width=False, height=False)

        # change the title of the window
        self.win.title("註冊")

    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)

        x, y = 70, 20
        image = Image.open(os.getcwd() + '/images/login.png')
        image = image.resize((150,150), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+80, y=y+0)

        # now create a login form
        self.label = Label(self.frame, text="使用者註冊")
        self.label.config(font=("微軟正黑體", 20, 'bold'))
        self.label.place(x=150, y=y+150)

        self.uidlabel = Label(self.frame, text="帳號:")
        self.uidlabel.config(font=("微軟正黑體", 12, 'bold'))
        self.uidlabel.place(x=75, y=y+205)

        self.userid = Entry(self.frame, font='Courier 12')
        self.userid.place(x=125, y=y+205)

        self.pwdlabel = Label(self.frame, text="密碼:")
        self.pwdlabel.config(font=("微軟正黑體", 12, 'bold'))
        self.pwdlabel.place(x=75, y=y+235)

        self.password = Entry(self.frame, show='*',
                              font='Courier 12')
        self.password.place(x=125, y=y+235)

        self.namelabel = Label(self.frame, text="暱稱:")
        self.namelabel.config(font=("微軟正黑體", 12, 'bold'))
        self.namelabel.place(x=75, y=y+265)

        self.name = Entry(self.frame, font='Courier 12')
        self.name.place(x=125, y=y+265)

        self.button = Button(self.frame, text="註冊",
                             font='微軟正黑體 15 bold',
                             command=self.register)
        self.button.place(x=225, y=y+290)
        self.button1 = Button(self.frame, text="返回",
                             font='微軟正黑體 15 bold',
                             command=self.login)
        self.button1.place(x=155,y=y+290)
        self.win.mainloop()

    def register(self):
        # get the data and store it into tuple (data)
        data = (
            self.userid.get(),
            self.name.get(),
            self.password.get()
        )
        # validations
        if self.userid.get() == "":
            messagebox.showinfo("警告!","帳號未填")
        elif self.password.get() == "":
            messagebox.showinfo("警告!", "密碼未填")
        elif self.name.get() == "":
            messagebox.showinfo("警告!", "暱稱未填")
        else:
            res = db.db.user_check(self.userid.get())
            if res:
                messagebox.showinfo("警告！", "帳號已被使用!")
            else:
                db.db.user_register(data)
                messagebox.showinfo("系統", "註冊成功")
    def login(self):
        self.win.destroy()
        log = login.LoginWindow()
        log.add_frame()

