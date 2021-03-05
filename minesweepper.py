# coding=utf-8

import tkinter as tk
import random
import getpass
#===========| Global Var |===========#
usr = getpass.getuser()
zone_row = 3
zone_col = 3
num = zone_row*zone_col
cur = list(range(num))
bomb = [4]
bomb_num = len(bomb)
flaged = []
global mines
global minezone
finish = 0
zone_created = 0
lose = 0
win = 0
level = "easy"
#====================================#
fg_sel = {
"X" : 'Black',
"0" : 'Gainsboro',
"1" : 'Blue',
"2" : 'LimeGreen',
"3" : 'Red',
"4" : "FireBrick",
"5" : 'Orange',
"6" : 'Tomato',
"7" : 'SaddleBrown',
"8" : 'Indigo'
}
comment = {
    'easter_start': ["恭喜你触发小彩蛋","你怎么知道这个的？","呀，被你猜到了"],
    'easter_win'  : ["彩蛋就别玩了吧","绿色的彩蛋"],
    'easter_lose' : ["看图说话","红色的彩蛋"],
    'zero_start'  : ["你认真的？0个？","无痛游戏","你不会是来画画的吧？","轻松游戏？"],
    'zero_win'    : ["你开心就好","人嘛，最重要的就是要开心","瞎子都能赢"],
    'zero_lose'   : [],
    'full_start'  : ["我不知道你在玩啥","你难道只是想看爆炸？","你仿佛是在逗我"],
    'full_win'    : [],
    'full_lose'   : ["你就没想过赢是吧？","你说你点开来干啥？"],
    'lucky_start' : ["一步定胜负","One shot one kill","获胜机率%s%%","Lucky Shot"],
    'lucky_win'   : ["你可以去买彩票了","你开挂了吧？","我怀疑你在作弊","你就是天选之人？","%s%%概率的幸运一击"],
    'lucky_lose'  : ["赢了就可以去买彩票了","你只有%s%%的概率能赢","%s%%的概率，太难了"],
    'entry_start' : ["%.2f%%的地雷，入门级别的难度","乱点都能赢","这有些过于简单了","没劲，增加点难度呗","三岁小孩都能赢"],
    'entry_win'   : ["恭喜你成功入门扫雷","还挺简单的吧","快开始下一把"],
    'entry_lose'  : ["这你都能输？！","猴子都比你玩得好","另一种意义上的好运","你运气也忒差了","教学关你就挂了"],
    'easy_start'  : ["%.2f%%的地雷，简单难度","快开始吧，赶紧的","别磨蹭了，快开始"],
    'easy_win'    : ["真简单","基础中的基础","提高一点难度怎么样？"],
    'easy_lose'   : ["你太菜了","再多练几年吧","我还怀疑你这里是空的(指脑袋)","你会不会玩啊？","一点技巧都没有","新手关你都过不了？"],
    'normal_start': ["%.2f%%的地雷，普通难度","热身的程度","蛮简单的，快点","普通难度"],
    'normal_win'  : ["中级水平","还行，不错","掌握了一点技巧吧算是"],
    'normal_lose' : ["来嘛来嘛，再来一局","哎，还是得多练","这才普通难度啊","你运气是真的差"],
    'hard_start'  : ["%.2f%%的地雷，困难难度","开始有点难度了","加油，我看好你哦","困难级别"],
    'hard_win'    : ["属于高手级别了","不错不错，值得鼓励","可以可以"],
    'hard_lose'   : ["你离大师还差得远呢！","再来一把呗","多试试，没准就赢了"],
    'master_start': ["%.2f%%的地雷，大师难度","困难的挑战","富有挑战性的任务","打赢你就是扫雷大师了"],
    'master_win'  : ["不容易啊","运气与技术的胜利","哎哟不错哦"],
    'master_lose' : ["再接再厉","实属有些困难","运气不好","赢了我请你吃鸡"],
    'hell_start'  : ["%.2f%%的地雷，地狱难度","开启突然死亡模式","通常情况下，一发入魂","俄罗斯轮盘赌","点到一个就算赢"],
    'hell_win'    : ["运气太好了","没想到你真能赢","厉害厉害，佩服佩服","感觉运气被透支"],
    'hell_lose'   : ["能赢才怪事","输了不丢人","就没想过你能赢","没几个人能玩通这种难度"]
}
chatlist = {
    'info' : ["你知道吗，这个程序有相当部分容量是我的废话","扫雷最早可以追溯到Jerimac Ratliff于1973年推出的名为“Cube”的游戏",
               "九十年代初，Curt Johnson制作了最初的扫雷，发布于IBM旗下的OS/2系统上","加拿大的微软员工Robert Donner将本作移植到了Windows操作系统上",
               "1992年4月6日，Windows3.1x正式更新，《扫雷》代替《黑白棋》加入操作系统","扫雷最初被加入到Windows里是为了训练用户的鼠标左右键操作能力",
               "从Windows8起，扫雷并不再随附于系统，而是需要用户自行下载","由于国际反地雷组织的抗议，Windows2000意大利版在安装时，用一个名叫《花田》的游戏替换《扫雷》",
               "扫雷玩法简单但同时考验了玩家的逻辑与运气，火爆全世界"],
    'tips'  : ["扫雷的规则很简单，翻开所有安全区你就赢啦","左键翻开区块，右键标定或取消旗子",
               "区块上的数字代表以其为中心的九宫格内存在地雷的数量","点到地雷你就炸啦",
               "如果你给我磕三个响头的话，我可以给你标个地雷(指向左键)","向我鞠三个躬我就告诉你一个安全点(指向右键)",
               "区块附近标全地雷后，双击区块可以快速翻开周边，不过如果你标错地雷的话..."],
    'easter': ["“5...2...0”，这段代码啥意思啊？删了删了",'“"5"是"我"，"4"为"是"，我是.....谁？”，这句代码谁写的啊？'],
    'finish': ["别瞎点了，快重新开始吧","你就算点穿屏幕都不会有其它的东西的","咱们重开一局好不好"]
}
class AnnoyBot:
    def __init__(self,dialog):
        self.dialog = dialog
        self.say("你好 %s，\n我叫Annoy，是作者派来吐槽你的"%usr)
        self.chatcd = 0
        self.hintcd = 0
    def say(self,string):
        self.dialog['text'] = string
    def cmt(self,_type):
        chance = "%.2f"%(100*(num-bomb_num)/num)
        minerate = 100.0*bomb_num/num
        sentence = random.choice(comment.get(level+"_"+_type,[""]))
        if "%s%%" in sentence:
            sentence = sentence%chance
        elif "%.2f" in sentence:
            sentence = sentence%minerate
        self.say(sentence)
    def chat(self,_type=""):
        if finish:
            _type = 'finish'
        if self.chatcd:
            self.chatcd -= 1
            return
        if _type == "": _type = random.choice(['info','tips','easter'])
        sentence =random.choice(chatlist.get(_type,[""]))
        self.say(sentence)
        self.chatcd = 2
    def hint(self,event):
        _type = str(event)
        if zone_created and not finish:
            if not self.hintcd: # run out of hints
                self.say("没有提示啦")
            else:
                if ("ButtonPress" in _type) and (event.num == 1): # left # request bomb hints
                    hint_bomb = [] # find a unflagged bomb with the least nearby_bombs
                    for index in bomb: # find all unflagged bombs and record its nearby_bombs
                        if index not in flaged:
                            hint_bomb.append([mines[index].nearby_bombs,index])
                    if not len(hint_bomb): # there's no bomb that is not flagged
                        if len(flaged) == bomb_num: # only bomb is flagged
                            self.say(random.choice(["别逗，你都标完所有雷了","就这些雷啊，没别的了"]))
                        else: # find one mistaken flag and unflag it
                            misflag = []
                            for index in flaged:
                                if index not in bomb:
                                    misflag.append(index)
                            index = random.choice(misflag)
                            mines[index].setflag()
                            mines[index].cover['text'] = "X"
                            mines[index].cover['bg'] = "yellow"
                            self.say("你这颗雷标错了")
                    else:
                        hint_bomb = sorted(hint_bomb)
                        index = hint_bomb[0][1]
                        mines[index].setflag()
                        mines[index].cover['bg'] = "DodgerBlue"
                        self.say(random.choice(["这颗雷附近的雷比较少","帮你标了一颗雷"]))
                elif ("ButtonPress" in _type) and (event.num == 3): # right # request safe zone
                    hint_zone = [] # find a safe zone with the least nearby_bombs
                    for index in cur: # find all coverd-unflagged zone and record its nearby_bombs
                        if (index not in bomb) and (index not in flaged):
                            hint_zone.append([mines[index].nearby_bombs,index])
                    if not len(hint_zone): # there's no zone left uncoverd or unflagged
                        misflag = []
                        for index in flaged:
                            if index not in bomb:
                                misflag.append(index)
                        index = random.choice(misflag)
                        mines[index].setflag()
                        mines[index].cover['text'] = "X"
                        mines[index].cover['bg'] = "yellow"
                        self.say("全都插上旗子了我怎么给你指点？大发慈悲的告诉你这个标错了")
                    else:
                        hint_zone = sorted(hint_zone)
                        index = hint_zone[0][1]
                        mines[index].detect()
                        mines[index].bg['bg'] = "SkyBlue"
                        mines[index].scaner['bg'] = "SkyBlue"
                        self.say(random.choice(["帮你翻开一个安全区咯","神之一指"]))
                self.hintcd -= 1

class mine:
    def __init__(self,zone,index):
        self.row = index // zone_col
        self.col = index % zone_col
        self.index = index
        u_row = [] if self.row == 0          else [self.row-1]
        d_row = [] if self.row == zone_row-1 else [self.row+1]
        nearby_row = sorted([self.row] + u_row + d_row)
        l_col = [] if self.col == 0          else [self.col-1]
        r_col = [] if self.col == zone_col-1 else [self.col+1]
        nearby_col = sorted([self.col] + l_col + r_col)
        self.nearby = []
        for _row in nearby_row:
            for _col in nearby_col:
                self.nearby.append(_row*zone_col+_col)
        self.nearby.remove(self.index)
        self.nearby_bombs = 0
        for near in self.nearby:
            if near in bomb:
                self.nearby_bombs += 1
        self.minescan = "X" if self.index in bomb else (self.nearby_bombs if self.nearby_bombs else "")
        self.bg = tk.Frame(zone,width=31,height=30,bd=1,relief="sunken",bg=("Red" if self.index in bomb else "Gainsboro"))
        self.scaner = tk.Label(zone,text=self.minescan,font=('microsoft yahei',12,'bold'),
                               fg=fg_sel.get(str(self.minescan),"Gainsboro"),bg=("Red" if self.index in bomb else "Gainsboro"))
        self.cover = tk.Button(zone, width=3, height=1, bd=2)
        self.bg.bind("<Double-Button-1>",self.click)
        self.scaner.bind("<Double-Button-1>",self.click)
        self.cover.bind("<ButtonRelease-1>",self.click)
        self.cover.bind("<ButtonRelease-3>",self.click)
        self.bg.grid(column=self.col,row=self.row)
        self.scaner.grid(column=self.col,row=self.row)
        self.cover.grid(column=self.col,row=self.row)
        self.uncover = False
        self.flag = False
    def click(self,event):
        Annoy.chat()
        _type = str(event)
        if "ButtonRelease" in _type: # mouse release
            if event.num == 1: # left
                self.detect()
            if event.num == 3: # right
                self.setflag()
        if "ButtonPress" in _type and (event.num == 1): # left
            nearby_flag = len(set(self.nearby).intersection(set(flaged)))
            if nearby_flag == self.minescan: # uncover nearby mines if nearby flags == nearby bombs
                for near in self.nearby:
                    if not mines[near].uncover:
                        mines[near].detect()
    def detect(self):
        global cur
        global finish
        global lose
        global win
        if finish or self.flag: return
        # print(self.index)
        self.cover.destroy()
        self.uncover = True
        cur.remove(self.index)
        if (self.nearby_bombs == 0) and (self.index not in bomb): # iteratively uncover nearby mines if nearby bomb is 0
            for near in self.nearby:
                if not mines[near].uncover:
                    mines[near].detect()
        if lose or win: return
        if self.index in bomb: # trigger bomb -> lose and finish
            lose = 1
            for index in bomb: # uncover all other bombs
                if not mines[index].uncover:
                    mines[index].detect()
            for index in flaged: # hightlight all mistaken flags
                if index not in bomb:
                    mines[index].cover['text'] = "X"
                    mines[index].cover['bg'] = "yellow"
            finish = 1
            print("You Lose")
            Annoy.cmt("lose")
            remain['fg'] = "red"
            remain['text'] = "你输了"
        elif len(cur) == bomb_num: # find all bombs -> win and finish
            win = 1
            for index in bomb: # set flag to bombs that are not flagged
                if not mines[index].flag:
                    mines[index].setflag()
            finish = 1
            print("You Win")
            Annoy.cmt("win")
            remain['fg'] = "green"
            remain['text'] = "你赢了"
    def setflag(self):
        global remain
        if finish: return
        if not self.flag: # set flag
            self.cover["text"] = "P"
            self.cover["bg"] = "limegreen"
            self.cover["disabledforeground"] = "orangered"
            self.cover["state"] = "disabled"
            flaged.append(self.index)
            self.flag = True
        else: # unset flag
            self.cover["text"] = ""
            self.cover["bg"] = "SystemButtonFace"
            self.cover["state"] = "normal"
            flaged.remove(self.index)
            self.flag = False
        remain['text'] = "剩余：%s"%(bomb_num-len(flaged))

def SetWindow():
    '''Set window to the center of screen'''
    top.update_idletasks()
    top_w = top.winfo_width()
    top_h = top.winfo_height()
    screen_w = top.winfo_screenwidth()
    screen_h = top.winfo_screenheight()
    x = (screen_w - top_w)//2
    y = (screen_h - top_h)//2
    top.geometry("+%s+%s"%(x,y))
    top.deiconify()
    chatbox['wraplength'] = 200 + top_w - 226

def CreateZone():
    global mines
    global minezone
    global zone_created
    minezone = tk.Frame(bd=5,relief="ridge")
    mines = [mine(minezone,i) for i in range(num)]
    minezone.pack(expand="yes",padx=8,pady=8,side="left",anchor='center')
    zone_created = 1

def GetConfig():
    global num
    global cur
    global bomb
    global bomb_num
    global flaged
    global level
    global zone_row
    global zone_col
    zone_row = int(cfg_row.get('0.0','end'))
    zone_col = int(cfg_col.get('0.0','end'))
    bomb_num = int(cfg_bomb.get('0.0','end'))
    easter_egg = 0
    if zone_row == 5 and zone_col == 2 and bomb_num == 0: # Easter Egg: Love
        easter_egg = 1
        zone_row = 7
        zone_col = 7
        num = zone_row*zone_col
        bomb = [   9 ,   11,
                15,16,17,18,19,
                22,23,24,25,26,
                   30,31,32,
                      38]
        bomb_num = len(bomb)
    elif zone_row == 5 and zone_col == 4 and bomb_num == 3: # Easter Egg: Who am I
        easter_egg = 1
        zone_row = 14
        zone_col = 7
        num = zone_row*zone_col
        bomb = [         3 ,
                   8 ,9 ,10,11,12,
                      16,   18,
                21,22,23,24,25,26,27,

                   36,37,38,39,40,
                   43,         47,
                   50,51,52,53,54,
                   57,         61,
                   64,65,66,67,68,
                         73,
                   78,79,80,81,82,
                         87,
                         94]
        bomb_num = len(bomb)
    else:
        num = zone_row*zone_col
        bomb = sorted(random.sample(range(num),bomb_num))
    cur = list(range(num))
    flaged = []
    remain["fg"] = "blue"
    remain["text"] = "剩余：%s"%bomb_num
    print("Bomb is %s"%bomb)
    if (0<num<=400) and (0<zone_row<=20) and (0<zone_col<=30) and (0<=bomb_num<=num):
        Annoy.hintcd = 0
        if easter_egg:
            level = "easter"
        elif bomb_num == 0:
            level = "zero"
        elif bomb_num == num:
            level = "full"
        elif bomb_num == num - 1:
            level = "lucky"
        elif bomb_num < num*0.05:
            level = "entry"
        elif num*0.05 <= bomb_num < num*0.1:
            level = "easy"
            Annoy.hintcd = 1
        elif num*0.1 <= bomb_num < num*0.2:
            level = "normal"
            Annoy.hintcd = 2
        elif num*0.2 <= bomb_num < num*0.3:
            level = "hard"
            Annoy.hintcd = 4
        elif num*0.3 <= bomb_num < num*0.4:
            level = "master"
            Annoy.hintcd = 6
        else:
            level = "hell"
            Annoy.hintcd = 8
        return 1
    else:
        if num>400:
            Annoy.say("太多了我处理得很慢，别超过400个")
        elif zone_row>20:
            Annoy.say("太宽了我怕你屏幕塞不下，别超过20行")
        elif zone_col>30:
            Annoy.say("太宽了我怕你屏幕塞不下，别超过30列")
        return 0

def StartGame():
    global finish
    global lose
    global win
    if zone_created: minezone.pack_forget()
    finish = 0
    lose = 0
    win = 0
    valid_num = 0
    try:
        valid_num = GetConfig()
    except:
        Annoy.say("你的输入有问题啊")
    if valid_num:
        CreateZone()
        SetWindow()
        Annoy.cmt("start")

top = tk.Tk()
top.title("叨叨扫雷")
top.resizable(False,False)
chatbox = tk.Label(top,width=20,height=3,bg='white',wraplength=200,justify='center',font=('microsoft yahei',12,'bold'))
chatbox.pack(side="top",anchor='n',padx=10,pady=10,fill='x',expand='yes')
Annoy = AnnoyBot(chatbox)
chatbox.bind("<Triple-Button-1>",Annoy.hint)
chatbox.bind("<Triple-Button-3>",Annoy.hint)
config = tk.LabelFrame(top,relief="sunken",bd=3)
config.pack(side="left",expand="no",fill=tk.NONE,padx=10,anchor='w')
cfg_info_row  = tk.Label(config,text="行",font=('microsoft yahei',12))
cfg_info_col  = tk.Label(config,text="列",font=('microsoft yahei',12))
cfg_info_bomb = tk.Label(config,text="炸弹",font=('microsoft yahei',12))
cfg_row  = tk.Text(config,width=5,height=1,font=('microsoft yahei',12))
cfg_col  = tk.Text(config,width=5,height=1,font=('microsoft yahei',12))
cfg_bomb = tk.Text(config,width=5,height=1,font=('microsoft yahei',12))
cfg_info_col .grid(column=0,row=1,padx=2,pady=2)
cfg_info_row .grid(column=0,row=0,padx=2,pady=2)
cfg_info_bomb.grid(column=0,row=2,padx=2,pady=2)
cfg_row .grid(column=1,row=0,padx=2,pady=2)
cfg_col .grid(column=1,row=1,padx=2,pady=2)
cfg_bomb.grid(column=1,row=2,padx=2,pady=2)
cfg_row.insert(0.0,5)
cfg_col.insert(0.0,5)
cfg_bomb.insert(0.0,5)
start = tk.Button(config,text="开始",command=StartGame).grid(column=0,row=4,padx=2,pady=2)
end = tk.Button(config,text="结束",command=top.destroy).grid(column=1,row=4,padx=2,pady=2,sticky="e")
remain = tk.Label(config,width=10,height=1,font=('microsoft yahei',12),fg='blue')
remain.grid(column=0,columnspan=2,row=5,padx=2,pady=2)
SetWindow()
top.mainloop()
