from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import db.db
import login
import game
from PIL import Image, ImageTk
import os

class SelectWindow:
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
        self.win.title("歌曲選擇")
    def add_frame(self,username):
        self.frame = Frame(self.win, height = 400, width=450)
        self.frame.place(x=80, y=50)
        self.username = username
        x, y = 70, 20
        image = Image.open(os.getcwd() + '/images/login.png')
        image = image.resize((150,150), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+80, y=y+0)
        
        
        self.label = Label(self.frame, text="歌曲選擇")
        self.label.config(font=("微軟正黑體", 20, 'bold'))
        self.label.place(x=170, y=y+150)
        dirPath = os.getcwd() + '/song'
        result = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]
        self.com = ttk.Combobox(self.frame, values=result,state = "readonly",width = 30)
        self.com.place(x=115,y=y+200)
        self.com.current(0)

        self.button = Button(self.frame, text = "單人遊戲",font='微軟正黑體 15 bold',command=self.single)
        self.button.place(x = 125,y=y+255)
        self.button1 = Button(self.frame, text = "多人遊戲",font="微軟正黑體 15 bold")
        self.button1.place(x = 225, y=y+255)
        self.win.mainloop()
    def single(self):
        self.songname = self.com.get()
        self.win.destroy()
        game.main(self.songname,self.username)



