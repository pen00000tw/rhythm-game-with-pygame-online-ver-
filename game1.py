#程式名稱：哎呀快要滑倒啦

#################################################################################
###                                                                           ###
###                              ### 函示庫引入區 ###                          ###
#################################################################################
import pygame,random,threading
import os,time
import csv
import mutagen.mp3
import db.db
from network import Network
#################################################################################
###                                                                           ###
###                              ### 初始區 ###                                ###
#################################################################################
def initgame():
    pygame.mixer.init(44100,-16,2,1024)    #(頻率,位元,通道數,緩衝)
    pygame.init()
    pygame.display.set_caption("哎呀快要滑倒啦")
#################################################################################
###                                                                           ###
###                              ### 全域變數區 ###                            ###
#################################################################################
def pygamedef(inputsong):
    global songselect,win,clock,song_base_path
    songselect = inputsong
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    song_base_path = os.getcwd() + '/song/' + songselect + '/'

WIN_WIDTH, WIN_HEIGHT = 1280, 720    #螢幕大小
FRAME_PER_SECONDS = 144               #最大幀數(通常不準的啦)
img_base_path = os.getcwd() + '/images/'
sound_base_path = os.getcwd() + '/sounds/'
font_base_path = os.getcwd() + '/fonts/'
run = True #遊戲開始
screen1,screen2,screen3,switch = True,False,False,True #畫面切換
left,right=True,False
x,y = 500,600  #角色初始生成座標
charactermul = 750 #(幀數乘上像素)
objmul = 480 #(幀數乘上像素)
objnum = 500
now = 0.0
counter = 0
score = 0
combo = 0
copyarr = []
clickanimation = False
touchflag = False
arr = []
fall = []  
dirPath = os.getcwd() + '/song'
songlist = [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))] #歌曲列表
songindex = 0
input1 = ''
state = ''
anothercombo = ''
anotherscore = ''
#################################################################################
###                                                                           ###
###                              ### 圖片區 ###                                ###
#################################################################################
def picturedef():
    global click,obj1,obj2,obj3,catchleft,catchright,bg,bg1,bg2,start,end,rankingpanel,rank,retry,img_base_path,song_base_path,selectright
    #動畫區
    click = []  #按鍵動畫
    obj1 = []   #下墜物件1
    obj2 = []   #下墜物件2
    obj3 = []   #下墜物件3
    for i in range(30):
        click.append(pygame.image.load(img_base_path + 'taiko-hit300k-' + str(i) + '.png'))
        obj1.append(pygame.transform.scale(pygame.image.load(img_base_path + 'hit100-' + str(i) +'.png'),(400,400)).convert_alpha())
        obj2.append(pygame.transform.scale(pygame.image.load(img_base_path + 'hit50-' + str(i) +'.png'),(400,400)).convert_alpha())
        obj3.append(pygame.transform.scale(click[i],(400,400)).convert_alpha())

    #角色
    catchleft = pygame.transform.scale(pygame.image.load(img_base_path + 'catchleft.png'),(193,208)).convert_alpha()
    catchright = pygame.transform.scale(pygame.image.load(img_base_path + 'catchright.png'),(193,208)).convert_alpha()

    #背景
    bg = pygame.transform.scale(pygame.image.load(img_base_path + 'menu-background.jpg'),(WIN_WIDTH,WIN_HEIGHT)).convert_alpha()
    bg1 = pygame.transform.scale(pygame.image.load(song_base_path + 'bg1.jpg'),(WIN_WIDTH,WIN_HEIGHT)).convert_alpha()
    bg2 = pygame.transform.scale(pygame.image.load(img_base_path + 'bg2.jpg'),(WIN_WIDTH,WIN_HEIGHT)).convert_alpha()

    #screen1的圖
    start = pygame.image.load(img_base_path + 'start.png').convert_alpha()
    end = pygame.transform.scale(pygame.image.load(img_base_path + 'end.png'),(104,65)).convert_alpha()
    selectright = pygame.image.load(img_base_path + 'selectright.png').convert_alpha()
    #screen3的圖
    rankingpanel = pygame.image.load(img_base_path + 'ranking-panel old.png').convert_alpha()
    rank = pygame.transform.scale(pygame.image.load(img_base_path + 'ranking-XH.png'),(185,222)).convert_alpha()
    retry = pygame.image.load(img_base_path + 'pause-retry.png').convert_alpha()

#################################################################################
###                                                                           ###
###                              ### 音檔區 ###                                ###
#################################################################################
def musicdef():
    global menuhit,menutouch,objhit,sound_base_path
    menuhit = pygame.mixer.Sound(sound_base_path + 'menuhit.wav')  #滑鼠點擊音效
    menutouch = pygame.mixer.Sound(sound_base_path + 'menutouch.wav') #滑鼠觸碰音效
    objhit = pygame.mixer.Sound(sound_base_path + 'normal-hitwhistle.wav') #打擊音效
    objhit.set_volume(0.7)
#################################################################################
###                                                                           ###
###                              ### 文字區 ###                                ###
#################################################################################
def fontdef(songselect):
    global font,font1,chinese,chinese3,intro1,intro2,intro3,intro4,songname,font_base_path,songname1
    #字型大小設定
    font = pygame.font.Font(font_base_path + "1900805.ttf",72)
    font1 = pygame.font.Font(font_base_path + "1900805.ttf",24)
    chinese = pygame.font.Font(font_base_path + "KTEGAKI.ttf",24)
    chinese3 = pygame.font.Font(font_base_path + "KTEGAKI.ttf",96)

    #生成文字圖片
    intro1 = chinese.render('Game introduce:' +'',True,(0,0,0))
    intro2 = chinese.render('以左右移動人物',True,(0,0,0))
    intro3 = chinese.render('接住落下的方塊',True,(0,0,0))
    intro4 = chinese.render('享受愉快的節奏!',True,(0,0,0))
    #歌曲名稱
    songname = chinese.render(songselect,True,(225,225,225))
    songname1 = chinese.render('Song Select: ' + songselect,True,(0,0,0))
#################################################################################
###                                                                           ###
###                              ### 精靈類別區 ###                            ###
#################################################################################
#人物物件
class Mysprite(pygame.sprite.Sprite):
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
    def load(self,filename):
        self.image = filename
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,left,right,speed):
        if left:
            if self.rect.centerx > 100:
                self.rect.centerx -= speed
        if right:
            if self.rect.centerx < 1200:
                self.rect.centerx += speed
#碰撞物
class obj(pygame.sprite.Sprite):
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.count = 0
        self.burst = False
        self.select = 1
    def load(self,filename):
        if filename == 1:
            self.image = obj1[0]
            self.select = 1
        elif filename == 2:
            self.image = obj2[0]
            self.select = 2
        elif filename == 3:
            self.image = obj3[0]
            self.select = 3
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(500,700)
        self.rect.centery = -20
        self.mask = pygame.mask.from_surface(self.image)
    def update(self,objspeed):
        global combo
        if self.burst == False and self.rect.centery < 800:
            self.rect.centery += objspeed
        elif self.burst == True and self.count < 29:
            if self.count == 0:
                objhit.play()
                combo += 1
            self.count+=1
            if self.select == 1:
                self.image = obj1[self.count]
            elif self.select == 2:
                self.image = obj2[self.count]
            elif self.select == 3:
                self.image = obj3[self.count]
        elif self.rect.centery >= 800:
            combo = 0
            group1.remove(self)
        else:
            group1.remove(self)
                
#精靈初始化
def spriteinit():
    global character,group,group1,win
    character = Mysprite(win)
    group = pygame.sprite.Group()  #人物群組
    group1 = pygame.sprite.Group()  #掉落物群組
#生成掉落物
def falldef():
    global objnum,fall,win
    for i in range(objnum):
        fall.append(obj(win))
        fall[i].load((i % 3) + 1)
#人物load
def characterload():
    global character,group,catchright
    character.load(catchright)
    group.add(character)

#################################################################################
###                                                                           ###
###                              ### 渲染區 ###                                ###
#################################################################################
#主渲染函式
def redrawGameWindow():
    global clickanimation,screen1,screen2,switch,now,score,combo,counter,copyarr,songname1,input1,songselect,anothercombo,anotherscore
    fps = font1.render('FPS:' + str(int(clock.get_fps())),True,(0,0,0))
    if screen1:
        #切換畫面
        if switch:
            switch = False
            playmusic('bgm.mp3',False,0.2)
        win.blit(bg, (0, 0))
        win.blit(fps,(1150,0))
        win.blit(intro1,(125,100))
        win.blit(intro2,(125,150))
        win.blit(intro3,(125,200))
        win.blit(intro4,(125,250))
        win.blit(start,(1050,500))
        win.blit(end,(10,585))
        win.blit(songname1,(150,675))
        win.blit(selectright,(960,675))
        #按鍵動畫
        if clickanimation:
            for i in range(30):
                clock.tick(60)
                clickfps = font1.render('FPS:' + str(int(clock.get_fps())),True,(0,0,0))
                win.blit(bg, (0, 0))
                win.blit(clickfps,(1150,0))
                win.blit(intro1,(125,100))
                win.blit(intro2,(125,150))
                win.blit(intro3,(125,200))
                win.blit(intro4,(125,250))
                win.blit(start,(1050,500))
                win.blit(end,(10,585))
                win.blit(songname1,(150,675))
                win.blit(selectright,(960,675))
                win.blit(click[i % 30],(pygame.mouse.get_pos()[0] - 400,pygame.mouse.get_pos()[1] - 400))
                pygame.display.update()
        
    if screen2:
        if switch:
            switch = False
            for i in range(objnum):
                fall[i].__init__(win)
                fall[i].load((i % 3) + 1)
            character.rect.centerx = x #初始人物座標X
            character.rect.centery = y #初始人物座標Y
            counter = 0
            score = 0
            combo = 0
            playmusic('audio.mp3',True,0.5)
            now = time.time() #音樂撥放時開始計時
            copyarr = arr.copy()
            t.running.set()           #另一執行序開始產生物件
        if left:
            character.image = catchleft
        if right:
            character.image = catchright
        speed = charactermul / int(clock.get_fps())  #單位為像素
        objspeed = objmul / int(clock.get_fps())   #單位為像素
        group.update(left,right,speed)
        group1.update(objspeed)
        text = font.render('SCORE:' + str(score),True,(0,0,0))
        text1 = font.render('COMBO:' + str(combo),True,(0,0,0))
        another = font.render('SCORE:' + anotherscore,True,(0,0,0))
        another1 = font.render('COMBO:' + anothercombo,True,(0,0,0))
        win.blit(bg1,(0,0))
        win.blit(text,(25,25)) #繪製分數
        win.blit(text1,(25,100))
        win.blit(another,(800,25))
        win.blit(another1,(800,100))
        win.blit(fps,(1150,0))
        group.draw(win)
        group1.draw(win)
    if screen3:
        if switch:
            switch = False
            playmusic('transfer.mp3',False,0.7)
            data = (input1,score,songselect) #寫入資料庫
            db.db.writerecord(data)
        printscore = chinese3.render(str(score),True,(100,100,100))
        printcombo = chinese3.render(str(combo),True,(100,100,100))
        win.blit(bg2,(0,0))
        win.blit(fps,(1150,0))
        win.blit(rankingpanel,(0,0))
        win.blit(printscore,(75,70))
        win.blit(printcombo,(75,450))
        win.blit(rank,(405,415))
        win.blit(songname,(73,640))
        win.blit(retry,(1150,450))
        if clickanimation:
            for i in range(30):
                clock.tick(60)
                clickfps = font1.render('FPS:' + str(int(clock.get_fps())),True,(0,0,0))
                win.blit(bg2,(0,0))
                win.blit(clickfps,(1150,0))
                win.blit(rankingpanel,(0,0))
                win.blit(printscore,(75,70))
                win.blit(printcombo,(75,450))
                win.blit(rank,(405,415))
                win.blit(songname,(73,640))
                win.blit(retry,(1150,450))
                win.blit(click[i % 30],(pygame.mouse.get_pos()[0] - 400,pygame.mouse.get_pos()[1] - 400))
                pygame.display.update()
    pygame.display.update()
#################################################################################
###                                                                           ###
###                          ### 其他函數 ###                                  ###
#################################################################################

#播放音樂函式(音檔名稱(string),是否為所選歌曲,音量(0~1))
def playmusic(musicname,songbase,volume):
    filename = ''
    if songbase == False:
        filename = sound_base_path + musicname
    else:
        filename = song_base_path + musicname
    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(2000)
    pygame.mixer.quit()
    mp3 = mutagen.mp3.MP3(filename)
    pygame.mixer.init(mp3.info.sample_rate,-16,2,1024)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

#碰撞偵測
def detectCollisions(x1, y1, w1, h1, x2, y2, w2, h2):
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True 
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2): 
        return True 
    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2): 
        return True 
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2): 
        return True 
    else:
        return False
#產生物件
#################################################################################
###                                                                           ###
###                          ### 墜落物生成時間區 ###                          ###
#################################################################################
def general():
    global arr
    with open(song_base_path + 'map.kuanmin', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            arr = row.copy()
    arr[:] = [float(x) for x in arr]
#################################################################################
###                                                                           ###
###                          ### 執行序區 ###                                  ###
#################################################################################
class que(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = threading.Event()
        self.running.clear()
    def run(self):
        global now, counter,screen1,screen2,screen3,switch,t,copyarr
        while True:
            self.running.wait()
            if copyarr ==[] and len(group1) == 0:
                screen1 = False
                screen2 = False
                screen3 = True
                switch = True
                #pygame.mixer.music.fadeout(3000)
                self.running.clear()
            tmp = time.time() - now
            if copyarr != [] and tmp >= copyarr[0]:
                group1.add(fall[counter])
                del copyarr[0]
                counter += 1
class multiplayers(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = threading.Event()
        self.running.clear()
    def run(self):
        global screen2,anotherscore,anothercombo,score,state,screen1,screen2,switch,n,state,combo
        n = Network()
        while True:
            if screen1 == True:
                state = n.send('prepare')
                if state == '0,0':
                    screen2 = True
                    screen1 = False
                    switch = True
            if screen2 == True:
                a = str(score) + ',' + str(combo)
                tmp = n.send(n.send(a)).split(',')
                if len(tmp) > 1:
                    anotherscore = tmp[0]
                    anothercombo = tmp[1]
def startque():
    global t
    t = que()
    t.start()
    t1 = multiplayers()
    t1.start()
#################################################################################
###                                                                           ###
###                          ### 主程式區 ###                                  ###
#################################################################################
def main(inputsong,username):
    #輸入歌曲
    print(inputsong)
    print(username)
    global run,clickanimation,switch,left,right,charactermul,screen1,screen2,screen3,start,end,retry \
    ,score,touchflag,selectright,songindex,songname1,songselect,song_base_path,bg1,songname,input1
    input1 = username
    initgame()
    pygamedef(inputsong)
    picturedef()
    musicdef()
    fontdef(inputsong)
    spriteinit()
    falldef()
    characterload()
    general()
    startque()
    while run:
        clock.tick(FRAME_PER_SECONDS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        mousep = pygame.mouse.get_pressed()
        #開始畫面判斷
        if screen1 == True: 
            if mousep[0] == True:
                menuhit.play()
                clickanimation = True
            else:
                clickanimation = False
            if detectCollisions(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],8,8,10,585,104,65): #結束
                if touchflag == False:
                    touchflag =True
                    menutouch.play()
                end = pygame.transform.scale(pygame.image.load(img_base_path + 'end.png'),(114,75)).convert_alpha()
                if mousep[0] == True:
                    pygame.mixer.music.fadeout(2000)
                    run = False
            elif detectCollisions(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],8,8,960,675,60,30):#換歌
                if touchflag == False:
                    touchflag =True
                    menutouch.play()
                selectright = pygame.transform.scale(pygame.image.load(img_base_path + 'selectright.png'),(70,40)).convert_alpha()
                if mousep[0] == True:
                    songindex+=1
                    if songindex > len(songlist) - 1:
                        songindex = 0
                    songselect = songlist[songindex]
                    songname1 = chinese.render('Song Select: ' + songselect,True,(0,0,0))
                    songname = chinese.render(songselect,True,(225,225,225))
                    song_base_path = os.getcwd() + '/song/' + songselect + '/'
                    bg1 = pygame.transform.scale(pygame.image.load(song_base_path + 'bg1.jpg'),(WIN_WIDTH,WIN_HEIGHT)).convert_alpha()
                    playmusic('audio.mp3',True,0.5)
                    general()
            elif detectCollisions(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],8,8,1050,500,208,134):#開始
                if touchflag == False:
                    touchflag = True
                    menutouch.play()
                start = pygame.transform.scale(pygame.image.load(img_base_path + 'start.png'),(218,144)).convert_alpha()
                if mousep[0] == True:
                    for i in range(30):
                        clickfps = font1.render('FPS:' + str(int(clock.get_fps())),True,(0,0,0))
                        clock.tick(60)
                        win.blit(bg, (0, 0))
                        win.blit(clickfps,(1150,0))
                        win.blit(intro1,(125,100))
                        win.blit(intro2,(125,150))
                        win.blit(intro3,(125,200))
                        win.blit(intro4,(125,250))
                        win.blit(start,(1050,500))
                        win.blit(end,(10,585))
                        win.blit(songname1,(150,675))
                        win.blit(selectright,(960,675))
                        win.blit(click[i % 30],(pygame.mouse.get_pos()[0] - 400,pygame.mouse.get_pos()[1] - 400))
                        pygame.display.update()
                    clickanimation = False
                    screen1 = False
                    screen2 = True
                    screen3 = False
                    switch = True
                    
                    #pygame.mixer.music.fadeout(2000)
                    
            else:
                touchflag = False
                end = pygame.transform.scale(pygame.image.load(img_base_path + 'end.png'),(104,65)).convert_alpha()
                start = pygame.image.load(img_base_path + 'start.png').convert_alpha()
                selectright = pygame.image.load(img_base_path + 'selectright.png').convert_alpha()
        #遊戲中
        elif screen2 == True:
            if keys[pygame.K_LEFT]:
                left = True
                right = False
            elif keys[pygame.K_RIGHT]:
                left = False
                right = True
            else:
                left = False
                right = False
            if keys[pygame.K_LSHIFT]:
                charactermul = 1500
            else:
                charactermul = 750
            tmp = pygame.sprite.spritecollide(character,group1,False,pygame.sprite.collide_mask)
            if tmp:
                for i in tmp:
                    score += 100
                    i.burst = True
        elif screen3 == True:
            if mousep[0] == True:
                clickanimation = True
                menuhit.play()
            else:
                clickanimation = False
            if detectCollisions(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],8,8,1150,450,83,85):
                if touchflag == False:
                    touchflag = True
                    menutouch.play()
                retry = pygame.transform.scale(pygame.image.load(img_base_path + 'pause-retry.png'),(113,97)).convert_alpha()
                if mousep[0] == True:
                    printscore = chinese3.render(str(score),True,(100,100,100))
                    printcombo = chinese3.render(str(combo),True,(100,100,100))
                    for i in range(30):
                        clock.tick(60)
                        clickfps = font1.render('FPS:' + str(int(clock.get_fps())),True,(0,0,0))
                        win.blit(bg2,(0,0))
                        win.blit(clickfps,(1150,0))
                        win.blit(rankingpanel,(0,0))
                        win.blit(printscore,(75,70))
                        win.blit(printcombo,(75,450))
                        win.blit(rank,(405,415))
                        win.blit(songname,(73,640))
                        win.blit(retry,(1150,450))
                        win.blit(click[i % 30],(pygame.mouse.get_pos()[0] - 400,pygame.mouse.get_pos()[1] - 400))
                        pygame.display.update()
                    clickanimation = False
                    screen1 = True
                    screen2 = False
                    screen3 = False
                    switch = True
                    #pygame.mixer.music.fadeout(2000)
            else:
                retry = pygame.image.load(img_base_path + 'pause-retry.png').convert_alpha()
                touchflag = False
        else:
            clickanimation = False
        redrawGameWindow()        
    pygame.quit()
if __name__ == "__main__":
    main('LiSA - unlasting (TV Size)','Kuanmin')
