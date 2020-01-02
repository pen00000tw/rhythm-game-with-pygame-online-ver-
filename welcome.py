# welcome.py
from tkinter import *
import login
from PIL import Image,ImageTk
import os
class WelcomeWindow:
    #create a constructor
    def __init__(self):
        # create a tkinter window
        self.win = Tk()

        #reset the window and background color
        self.canvas = Canvas(self.win,
                             width=1280, height=720,
                             bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        #show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width/2-1280/2)
        y = int(height/2-720/2)
        str1 = "1280x720+"+ str(x) + "+" + str(y)
        self.win.geometry(str1)

        #disable resize of the window
        self.win.resizable(width=False, height=False)

        #change the title of the window
        self.win.title("哎呀快要滑倒啦")

    def add_frame(self):
        #create a inner frame
        self.frame = Frame(self.win, height=844, width=1500)
        self.frame.place(x=-30, y=-30)

        x, y = 70, 20

        # place the photo in the frame
        # you can find the images from flaticon.com site
        tmp = Image.open(os.getcwd() + '/images/main.jpg')
        self.img = ImageTk.PhotoImage(tmp)
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x-45, y=y+0)

        self.button = Button(self.frame, text="  開始  ",
                             font=('微軟正黑體', 20),
                             bg='pink', fg='white',
                             command=self.login)
        self.button.place(x=615, y=640)
        self.win.mainloop()

    #open a new window on button press
    def login(self):
        # destroy current window
        self.win.destroy()

        #open the new window
        log = login.LoginWindow()
        log.add_frame()
    

if __name__ == "__main__":
    x = WelcomeWindow()
    x.add_frame()
