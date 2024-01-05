import re
import os
import json
import copy
from tkinter import *
import tkinter as tk
import pygame
import tkinter.messagebox
import random
import math
import time


##############################   用户账户管理功能   ###############################
#################################################################################

class user_init:
    def __init__(self):
        global player1, player2, temppoints
        self.play1 = user_login('用户1 请登录')
        self.play1.framLogin()
        mainloop()
        id1 = self.play1.processor.id
        type1 = self.play1.processor.type
        record1 = self.play1.processor.record
        # type1, id1, record1 = self.player1.processor.aa
        self.play2 = user_login('用户2 请登录')
        self.play2.framLogin()
        mainloop()
        id2 = self.play2.processor.id
        type2 = self.play2.processor.type
        record2 = self.play2.processor.record
        self.player1 = self.get_player(type1, id1, record1, PieceColor.BLACK)
        self.player2 = self.get_player(type2, id2, record2, PieceColor.WHITE)
        player1 = self.player1
        player2 = self.player2
        temppoints = [self.play1.processor.temppoint, self.play2.processor.temppoint]
        game = front()
        game.framinit()

    def get_player(self,type, id, record, color):   #生成相应的Player对象
        if type == 'user':
            return UserPlayer(type, id, record, color)
        elif type == 'ai1':
            return AI1Player(type, id, record, color)
        elif type == 'ai2':
            return AI2Player(type, id, record, color)
        elif type == 'ai3':
            return AI3Player(type, id, record, color)
        else:
            raise tkinter.messagebox.showinfo('提示', '未登录，请退出！')


class user_login:
    def __init__(self, player):
        self.player = player

    def registing():
        temp = True
        global u_entry, s_entry
        with open("sql.txt", "r") as f:
            data = f.readlines()
            for i in range(0, len(data), 4):
                data[i] = data[i].strip("\n")
                if str(data[i]) == u_entry.get():
                    tkinter.messagebox.showinfo('提示', '该用户名已被注册')
                    temp = False
                    break
        if temp:
            with open("sql.txt", "a") as f:
                f.write(f'\r{u_entry.get()}')
                f.write(f'\r{s_entry.get()}')
                f.write("\r0")
                f.write("\r0")
            ree.destroy()

    def resgister():
        global w4, u_entry, s_entry, ree
        ree = Tk()
        ree.title("注册页面")
        ree.geometry("600x400")
        ree.resizable(False,False)
        w4 = Canvas(ree, width=600, height=400, background='tan')
        title = tk.Label(w4, text="注册", bg='tan', font="仿宋 20 bold")
        title.place(x=280, y=50, )
        user = tk.Label(w4, text="用户名", bg='tan', font="仿宋 20 bold", width=8)
        user.place(x=100, y=130)
        u_entry = tk.Entry(w4, width=15, bg="white", font="仿宋 20 bold")
        u_entry.place(x=230, y=130)
        slab = tk.Label(w4, text="密码", bg='tan', font="仿宋 20 bold", width=8)
        slab.place(x=85, y=200)
        s_entry = tk.Entry(w4, width=15, bg="white", font="仿宋 20 bold", show="*")
        s_entry.place(x=230, y=200)
        agree_btn = tk.Button(w4, text="确认", command=user_login.registing, font="仿宋 20 bold", bg="green", width=8)
        agree_btn.place(x=250, y=280)
        w4.pack()

    def framLogin(self):
        global user_entry, ss_entry, game1
        game1 = Tk()
        game1.title("棋类对战平台")
        game1.iconphoto(True, tk.PhotoImage(file='image.png'))
        game1.geometry("600x400")
        game1.resizable(False,False)
        w3 = Canvas(game1, width=600, height=400, background='tan')
        w3.pack()
        title_lab = tk.Label(w3, text=self.player, bg='tan', font="仿宋 20 bold")
        title_lab.place(x=250, y=50, )
        title_lab = tk.Label(w3, text="(目前AI仅支持五子棋)", bg='tan', font="仿宋 15 bold")
        title_lab.place(x=230, y=80, )
        userlab = tk.Label(w3, text="用户名", bg='tan', font="仿宋 20 bold", width=8)
        userlab.place(x=100, y=130)
        user_entry = tk.Entry(w3, width=15, bg="white", font="仿宋 20 bold")
        user_entry.place(x=230, y=130)
        sslab = tk.Label(w3, text="登录密码", bg='tan', font="仿宋 20 bold", width=8)
        sslab.place(x=85, y=200)
        ss_entry = tk.Entry(w3, width=15, bg="white", font="仿宋 20 bold", show="*")
        ss_entry.place(x=230, y=200)
        self.processor = user_judge()
        login_btn = tk.Button(w3, text="登录", command=self.processor.judge, font="仿宋 20 bold", bg="green", width=8)
        regist_btn = tk.Button(w3, text="注册", command=user_login.resgister, font="仿宋 20 bold", bg="green", width=8)
        vistor_btn = tk.Button(w3, text="游客", command=self.processor.vistor_login, font="仿宋 20 bold", bg="gray", width=8)
        ai1_btn = tk.Button(w3, text="AI-1", command=self.processor.ai1_login, font="仿宋 20 bold", bg="yellow", width=4)
        ai2_btn = tk.Button(w3, text="AI-2", command=self.processor.ai2_login, font="仿宋 20 bold", bg="yellow", width=4)
        ai3_btn = tk.Button(w3, text="AI-3", command=self.processor.ai3_login, font="仿宋 20 bold", bg="yellow", width=4)
        login_btn.place(x=150, y=265)
        regist_btn.place(x=350, y=265)
        vistor_btn.place(x=150, y=340)
        ai1_btn.place(x=350, y=340)
        ai2_btn.place(x=430, y=340)
        ai3_btn.place(x=510, y=340)

class user_judge:
    def __init__(self):
        self.id = None
        self.type = None
        self.record = (None, None)
        self.temppoint = None

    def judge(self):
        global ss_entry, game1
        self.user_entry = user_entry
        temp = False
        with open("sql.txt", "r") as f:
            data = f.readlines()
            for i in range(0, len(data), 4):
                data[i] = data[i].strip("\n")
                data[i+1] = data[i+1].strip("\n")
                if str(data[i]) == self.user_entry.get() and str(data[i + 1]) == ss_entry.get():
                    self.user_goal = self.user_entry.get()
                    temp = True
                    break
        if temp:
            id = f'{self.user_entry.get()}'
            self.id = id
            self.type = 'user'
            self.locating()
            self.record = self.calculate()
            game1.destroy()
        else:
            tkinter.messagebox.showinfo('提示', '密码或用户名不正确')

    def locating(self):
        with open("sql.txt", "r") as f:
            data = f.readlines()
            for i in range(0,len(data),4):
                if str(data[i].strip("\n")) == self.id:
                    self.temppoint = i
                    break
    
    def calculate(self):
        with open("sql.txt", "r") as f:
            data1 = f.readlines()
            f.close()
            for i in range(len(data1)):
                data1[i] = data1[i].strip("\n")
        return (int(data1[self.temppoint+2])+int(data1[self.temppoint+3])), int(data1[self.temppoint+2])


    def SqlReScore(temppoint_i,sig):
        pointS = 0
        with open("sql.txt", "r") as f:
            data = f.readlines()

        with open("sql.txt", "w") as f:
            if sig == 'w':
                for i in data:
                    if pointS-2 == temppoint_i:
                        f.write(f'{int(i)+1}\r')
                    else:
                        f.write(f'{i}')
                    pointS+=1
            elif sig == 'l':
                for i in data:
                    if pointS-3 == temppoint_i:
                        if i == data[-1]:
                            f.write(f'{int(i)+1}')
                        else:
                            f.write(f'{int(i)+1}\r')
                    else:
                        f.write(f'{i}')
                    pointS += 1
        f.close()

    def SqlRecalculate(temppoint_i):
        if temppoint_i != None:
            with open("sql.txt", "r") as f:
                data1 = f.readlines()
                f.close()
                for i in range(len(data1)):
                    data1[i] = data1[i].strip("\n")
            return (int(data1[temppoint_i+2])+int(data1[temppoint_i+3])), int(data1[temppoint_i+2])
        else:
            return None, None

    def vistor_login(self):
        self.id = 'Vistor'
        self.type = 'user'
        game1.destroy()

    def ai1_login(self):
        self.id = 'AI-1'
        self.type = 'ai1'
        self.locating()
        self.record = self.calculate()
        game1.destroy()

    def ai2_login(self):
        self.id = 'AI-2'
        self.type = 'ai2'
        self.locating()
        self.record = self.calculate()
        game1.destroy()

    def ai3_login(self):
        self.id = 'AI-3'
        self.type = 'ai3'
        self.locating()
        self.record = self.calculate()
        game1.destroy()

##############################   前端   ###############################
######################################################################

cell_size = 40 # 格子大小
button_wide = 50  #按钮间隔

class front(Tk):
    def __init__(self):
        self.button_width = 10  # 按钮宽
        self.button_height = 1  # 按钮高

    def framinit(self):
        game = Tk()
        game.title("棋类对战平台")
        game.geometry("600x450")
        im = tk.PhotoImage(file='image.png')
        PhotoLabel=tk.Label(game, image=im)
        PhotoLabel.pack()

        def board_size():
            global b_size
            b_size = int(sizes.get())
            if b_size in range(8,20):
                label.config(text=f'{b_size} * {b_size}')
                return b_size
            else:
                tkinter.messagebox.showinfo('提示', '设置棋盘大小不在正确范围，为您取12 * 12')
                b_size = 8
                label.config(text=f'{b_size}*{b_size}')
                return b_size

        tk.Label(game, text="请设置棋盘大小（整数8至19）", font=('楷体', 15)).pack()
        sizes = Entry(game, width=10,font=('楷体',20))
        sizes.pack()
        label=tk.Label(game, text="点击确认 棋盘大小", font=('楷体', 15))
        label.pack(pady=20)
        tk.Button(game, text="确认", width=self.button_width, height=self.button_height, command=board_size, font=('楷体', 15)).pack()
        w2gobang = tk.Button(game, text="五子棋", width=self.button_width, height=self.button_height, command=frontBuilder.run_gobang, font=('楷体', 15))
        w2go = tk.Button(game, text="围棋", width=self.button_width, height=self.button_height, command=frontBuilder.run_go, font=('楷体', 15))
        w2Re = tk.Button(game, text="黑白棋", width=self.button_width, height=self.button_height, command=frontBuilder.run_re, font=('楷体', 15))
        w2q = tk.Button(game, text="退出", width=self.button_width, height=self.button_height, command=quit, font=('楷体', 15))
        w2gobang.pack()
        w2go.pack()
        w2Re.pack()
        w2q.pack()
        w2q.place(x=245, y=410)
        game.mainloop()
        return b_size
    
class frontBuilder:
    @staticmethod
    def run_gobang():
        global screen, gametype, b_size
        gametype = 0
        try:
            b_size
        except NameError:
            tkinter.messagebox.showinfo('提示', '未设置棋盘大小，推荐8 * 8')
            b_size = 8

        pygame.init()
        game_gobang = Gobang_interface(b_size)
        screen, buttons = game_gobang.run()
        ButtonFactory(buttons)
        PieceBoard(b_size)
        ButtonActionFactory(screen, game_gobang.playchess)
        pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][0], frontBuilder.get_loc(1, b_size), 18)
        pygame.draw.circle(screen, (41, 36, 33), frontBuilder.get_loc(1, b_size), 18,2)
        pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][1], frontBuilder.get_loc(7, b_size), 18)
        pygame.draw.circle(screen, (41, 36, 33), frontBuilder.get_loc(7, b_size), 18,2)
        myfont = pygame.font.Font("Kaiti.ttf", 20)
        textImage = myfont.render(f'用户名:{player1.id}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(2, b_size-0.5))
        textImage = myfont.render(f'总:{user_judge.SqlRecalculate(temppoints[0])[0]} 胜:{user_judge.SqlRecalculate(temppoints[0])[1]}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(2, b_size))
        textImage = myfont.render(f'用户名:{player2.id}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(8, b_size-0.5))
        textImage = myfont.render(f'总:{user_judge.SqlRecalculate(temppoints[1])[0]} 胜:{user_judge.SqlRecalculate(temppoints[1])[1]}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(8, b_size))
        pygame.display.update()
        game_gobang.ai_init()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 执行关闭程序的操作
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    act_x, act_y = pygame.mouse.get_pos()
                    game_gobang.mouse_clicks(act_x, act_y)
                    pygame.display.update()

     
    @staticmethod
    def run_go():
        global screen, gametype, b_size
        gametype = 1
        try:
            b_size
        except NameError:
            tkinter.messagebox.showinfo('提示', '未设置棋盘大小，推荐8 * 8')
            b_size = 8

        pygame.init()
        game_go = Go_interface(b_size)
        screen, buttons = game_go.run()
        ButtonFactory(buttons)
        PieceBoard(b_size)
        ButtonActionFactory(screen, game_go.playchess)
        pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][0], frontBuilder.get_loc(1, b_size), 18)
        pygame.draw.circle(screen, (41, 36, 33), frontBuilder.get_loc(1, b_size), 18,2)
        pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][1], frontBuilder.get_loc(7, b_size), 18)
        pygame.draw.circle(screen, (41, 36, 33), frontBuilder.get_loc(7, b_size), 18,2)
        myfont = pygame.font.Font("Kaiti.ttf", 20)
        textImage = myfont.render(f'用户名:{player1.id}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(2, b_size-0.5))
        textImage = myfont.render(f'总:{user_judge.SqlRecalculate(temppoints[0])[0]} 胜:{user_judge.SqlRecalculate(temppoints[0])[1]}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(2, b_size))
        textImage = myfont.render(f'用户名:{player2.id}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(8, b_size-0.5))
        textImage = myfont.render(f'总:{user_judge.SqlRecalculate(temppoints[1])[0]} 胜:{user_judge.SqlRecalculate(temppoints[1])[1]}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(8, b_size))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 执行关闭程序的操作
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    act_x, act_y = pygame.mouse.get_pos()
                    game_go.mouse_clicks(act_x, act_y)
                    pygame.display.update()


    @staticmethod
    def run_re():
        global screen, gametype, b_size
        gametype = 2
        try:
            b_size
        except NameError:
            tkinter.messagebox.showinfo('提示', '黑白棋初始大小推荐8 * 8')
            b_size = 8

        pygame.init()
        game_re = Re_interface(b_size)
        screen, buttons = game_re.run()
        ButtonFactory(buttons)
        PieceBoard(b_size)
        ButtonActionFactory(screen, game_re.playchess)
        PieceBoard.re_started()
        frontBuilder.set_piece(screen, b_size // 2 - 1, b_size // 2 - 1)
        frontBuilder.set_piece(screen, b_size // 2, b_size // 2 - 1)
        frontBuilder.set_piece(screen, b_size // 2 - 1, b_size // 2)
        frontBuilder.set_piece(screen, b_size // 2, b_size // 2)
        pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][0], frontBuilder.get_loc(1, b_size+1), 18)
        pygame.draw.circle(screen, (41, 36, 33), frontBuilder.get_loc(1, b_size+1), 18,2)
        pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][1], frontBuilder.get_loc(7, b_size+1), 18)
        pygame.draw.circle(screen, (41, 36, 33), frontBuilder.get_loc(7, b_size+1), 18,2)
        myfont = pygame.font.Font("Kaiti.ttf", 20)
        textImage = myfont.render(f'用户名:{player1.id}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(2, b_size+0.5))
        textImage = myfont.render(f'总:{user_judge.SqlRecalculate(temppoints[0])[0]} 胜:{user_judge.SqlRecalculate(temppoints[0])[1]}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(2, b_size+1))
        textImage = myfont.render(f'用户名:{player2.id}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(8, b_size+0.5))
        textImage = myfont.render(f'总:{user_judge.SqlRecalculate(temppoints[1])[0]} 胜:{user_judge.SqlRecalculate(temppoints[1])[1]}', True, (41, 36, 33))
        screen.blit(textImage, frontBuilder.get_loc(8, b_size+1))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 执行关闭程序的操作
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    act_x, act_y = pygame.mouse.get_pos()
                    game_re.mouse_clicks(act_x, act_y)
                    pygame.display.update()



    @staticmethod
    def Board(screen, size):
        if gametype == 2:
            screen.fill((190, 170, 150), pygame.rect.Rect(0, 0, 20+ (size)*cell_size +20, 20+ (size)*cell_size +20)) 
            screen.fill((163,100,6), pygame.rect.Rect(20, 20, (size)*cell_size, (size)*cell_size))
            frontBuilder.set_board(screen, size)
            for i in range(size):
                for j in range(size):
                    if PieceBoard.fetch_value((i, j)):
                        frontBuilder.set_piece(screen, i, j)
        else:
            screen.fill((190, 170, 150), pygame.rect.Rect(0, 0, 20+ (size-1)*cell_size +20, 20+ (size-1)*cell_size +20)) 
            screen.fill((163,100,6), pygame.rect.Rect(20, 20, (size-1)*cell_size, (size-1)*cell_size))
            frontBuilder.set_board(screen, size)
            for i in range(size):
                for j in range(size):
                    if PieceBoard.fetch_value((i, j)):
                        frontBuilder.set_piece(screen, i, j)
        return screen
    
    @staticmethod
    def set_board(screen, size):
        if gametype == 2:
            for row in range(size):
                for col in range(size):
                    pygame.draw.rect(screen, (0, 0, 0), (col * cell_size + 20, row * cell_size + 20,
                                                        cell_size, cell_size), 1)
        else:
            for row in range(size-1):
                for col in range(size-1):
                    pygame.draw.rect(screen, (0, 0, 0), (col * cell_size + 20, row * cell_size + 20,
                                                        cell_size, cell_size), 1)
    
    @staticmethod
    def set_piece(screen,x,y):#画棋子
        if PieceBoard.in_judge((x,y)):
            if gametype == 2:
                pos = frontBuilder.get_Re_loc(x, y)
            else:
                pos = frontBuilder.get_loc(x, y)
            pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][PieceBoard.pool[x, y] - 1], pos, 18)
            pygame.draw.circle(screen, (41, 36, 33), pos, 18,2)

    @staticmethod
    def get_loc(x,y):   #返回棋子在界面上的实际位置
        map_x = x * cell_size + 20
        map_y = y * cell_size + 20
        return (map_x, map_y)
    
    def get_Re_loc(x, y):
        map_x = x * cell_size + 40
        map_y = y * cell_size + 40
        return (map_x, map_y)


class Gobang_interface:
    def __init__(self, board_size):
        pygame.init()
        self.board_size = board_size  # 棋盘大小
        self.screen_width = 20 + (self.board_size-1) * cell_size + 20 + 200  # 屏幕宽度
        self.screen_height = 20 + (self.board_size-1) * cell_size + 100  # 屏幕高度
        self.button_x = 20 + (self.board_size-1) * cell_size + 20 + 20  # 按钮的横坐标
        self.button_y = 20  # 按钮的纵坐标
        self.obj = [PlayGobang(), PlayGo(), PlayRe()]
        self.playchess = self.obj[0]
        self.player1 = player1
        self.player2 = player2

    def run(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("五子棋")
        clock = pygame.time.Clock()

        while True:
            screen.fill((190, 170, 150)) # 填充背景色为浅棕色
            screen.fill((163,100,6), pygame.rect.Rect(20, 20, (self.board_size-1) * cell_size, (self.board_size-1) * cell_size))  # 填充棋盘色为深棕色

            # 绘制棋盘
            for row in range(self.board_size-1):
                for col in range(self.board_size-1):
                    pygame.draw.rect(screen, (0, 0, 0), (col * cell_size + 20, row * cell_size + 20,
                                                        cell_size, cell_size), 1)

            # 绘制按钮
            buttons = []
            buttons.append(RestartButton(screen, self.button_x, self.button_y, True))
            buttons.append(RetractButton(screen, self.button_x, self.button_y + button_wide * 1, True))
            buttons.append(GiveInButton(screen, self.button_x, self.button_y + button_wide * 2, True))
            buttons.append(SaveButton(screen, self.button_x, self.button_y + button_wide * 3, True))
            buttons.append(CoverButton(screen, self.button_x, self.button_y + button_wide * 4, True))
            for button in buttons:
                button.draw()
            
            pygame.display.flip()
            clock.tick(60)
            return screen, buttons
    
    def mouse_clicks(self, map_x, map_y):   #将鼠标点击位置转化为输入系统的坐标/位置
        act_obj = self.get_act(map_x, map_y)
        playchess = act_obj.react(screen, self.obj[0])
        if playchess:
            self.playchess = playchess

        if self.playchess.status:   # 处理完鼠标点击后创造AI下棋指令
            flag1, flag2 = self.ai_clicks()

    def get_act(self,map_x, map_y):   
        if map_x >= self.button_x:
            return ButtonAct(map_x,map_y)
        else:
            return ChessAct(map_x,map_y)

    # 内部调用函数（创造AI下棋指令）
    def ai_clicks(self):   #AI下棋响应
        self.player1, flag1 = self.ai_play(self.player1)
        self.player2, flag2 = self.ai_play(self.player2) 
        return (flag1, flag2)

    def ai_init(self):   #AI下棋初始化 
        while self.playchess.status == True:
            flag1, flag2 = self.ai_clicks()
            if flag1 and flag2:     #如果是AI-AI对阵，则一直下到结束，否则仅初始化AI棋步
                continue
            break

    def ai_play(self, player):   #AI下棋
        flag = False     #AI是否下棋的判别
        if player.get_status() and player.color == self.playchess.color:
            x,y = player.play()
            self.act_obj = ChessAct(None, None, x, y)
            self.update()
            flag = True
        return (player, flag)
    
    # 根据用户/AI指令更新后端playchess
    def update(self):
        playchess = self.act_obj.react(screen, self.playchess)  # 对实例类进行反应
        if playchess:
            self.playchess = playchess




class Go_interface:
    def __init__(self, board_size):
        pygame.init()
        self.board_size = board_size  # 棋盘大小
        self.screen_width = 20 + (self.board_size-1) * cell_size + 20 + 200  # 屏幕宽度
        self.screen_height = 20 + (self.board_size-1) * cell_size + 100  # 屏幕高度
        self.button_x = 20 + (self.board_size-1) * cell_size + 20 + 20  # 按钮的横坐标
        self.button_y = 20  # 按钮的纵坐标
        self.obj = [PlayGobang(), PlayGo(), PlayRe()]
        self.playchess = self.obj[1]

    def run(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("围棋")
        clock = pygame.time.Clock()

        while True:
            screen.fill((190, 170, 150)) # 填充背景色为灰色
            screen.fill((163,100,6), pygame.rect.Rect(20, 20, (self.board_size-1) * cell_size, (self.board_size-1) * cell_size))  # 填充棋盘色为棕色

            # 绘制棋盘
            for row in range(self.board_size-1):
                for col in range(self.board_size-1):
                    pygame.draw.rect(screen, (0, 0, 0), (col * cell_size + 20, row * cell_size + 20,
                                                        cell_size, cell_size), 1)

            # 绘制按钮
            buttons = []
            buttons.append(RestartButton(screen, self.button_x, self.button_y, True))
            buttons.append(RetractButton(screen, self.button_x, self.button_y + button_wide * 1, True))
            buttons.append(GiveInButton(screen, self.button_x, self.button_y + button_wide * 2, True))
            buttons.append(SaveButton(screen, self.button_x, self.button_y + button_wide * 3, True))
            buttons.append(CoverButton(screen, self.button_x, self.button_y + button_wide * 4, True))
            buttons.append(SkipButton(screen, self.button_x, self.button_y + button_wide * 5, True))
            for button in buttons:
                button.draw()
            
            pygame.display.flip()
            clock.tick(60)
            return screen, buttons

    def mouse_clicks(self, map_x, map_y):   #将鼠标点击位置转化为输入系统的坐标/位置
        act_obj = self.get_act(map_x, map_y)
        playchess = act_obj.react(screen, self.obj[1])
        if playchess:
            self.playchess = playchess

    def get_act(self,map_x, map_y):   
        if map_x >= self.button_x:
            return ButtonAct(map_x,map_y)
        else:
            return ChessAct(map_x,map_y)


class Re_interface:
    def __init__(self, board_size):
        pygame.init()
        self.board_size = board_size  # 棋盘大小
        self.screen_width = 20 + (self.board_size) * cell_size + 20 + 200  # 屏幕宽度
        self.screen_height = 20 + (self.board_size) * cell_size + 100  # 屏幕高度
        self.button_x = 20 + (self.board_size) * cell_size + 20 + 20  # 按钮的横坐标
        self.button_y = 20  # 按钮的纵坐标
        self.obj = [PlayGobang(), PlayGo(), PlayRe()]
        self.playchess = self.obj[2]

    def run(self):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("黑白棋")
        clock = pygame.time.Clock()

        while True:
            screen.fill((190, 170, 150)) # 填充背景色为灰色
            screen.fill((163,100,6), pygame.rect.Rect(20, 20, (self.board_size) * cell_size, (self.board_size) * cell_size))  # 填充棋盘色为棕色

            # 绘制棋盘
            for row in range(self.board_size):
                for col in range(self.board_size):
                    pygame.draw.rect(screen, (0, 0, 0), (col * cell_size + 20, row * cell_size + 20,
                                                        cell_size, cell_size), 1)

            # 绘制按钮
            buttons = []
            buttons.append(RestartButton(screen, self.button_x, self.button_y, True))
            buttons.append(RetractButton(screen, self.button_x, self.button_y + button_wide * 1, True))
            buttons.append(GiveInButton(screen, self.button_x, self.button_y + button_wide * 2, True))
            buttons.append(SaveButton(screen, self.button_x, self.button_y + button_wide * 3, True))
            buttons.append(CoverButton(screen, self.button_x, self.button_y + button_wide * 4, True))
            for button in buttons:
                button.draw()
            
            pygame.display.flip()
            clock.tick(60)
            return screen, buttons

    def mouse_clicks(self, map_x, map_y):   #将鼠标点击位置转化为输入系统的坐标/位置
        act_obj = self.get_act(map_x, map_y)
        playchess = act_obj.react(screen, self.obj[2])
        if playchess:
            self.playchess = playchess

    def get_act(self,map_x, map_y):   
        if map_x >= self.button_x:
            return ButtonAct(map_x,map_y)
        else:
            return ChessAct(map_x,map_y)




#棋子种类枚举类
class ChessType:
    GOBANG = 0   #五子棋索引为0
    GO = 1   #围棋索引为1
    Re = 2


#按钮享元类
class ButtonFactory:
    pool = dict()
    start = dict()
    def __new__(cls, button_list, *args, **kwargs):
        for button in button_list:
            cls.pool[button.text] = button
        cls.start = cls.pool

    @staticmethod
    def get_keys():
        return list(ButtonFactory.pool.keys())

    @staticmethod
    def get_values():
        return list(ButtonFactory.pool.values())

    @staticmethod
    def get_started():
        ButtonFactory.pool = ButtonFactory.start
        if gametype == 1:  #围棋
            ButtonFactory.pool[ButtonFactory.get_keys()[5]].status = True


#定义按钮类
class Button:
    def __init__(self, screen, text, x, y, color:list, status):
        pygame.font.init()
        self.screen = screen
        self.button_color = color
        self.text = text
        self.status = status
        self.width = 160 # 按钮宽度
        self.height = 30 # 按钮高度
        self.text_color = (0, 0, 0)
        self.font = pygame.font.Font("Kaiti.ttf",20)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x,y)
        self.initiate()

    #按钮初始化
    def initiate(self):
        self.img = self.font.render(self.text, True, self.text_color, self.button_color[self.status])
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.rect.center

    #按钮填色
    def draw(self):
        self.screen.fill(self.button_color[self.status],self.rect)
        self.screen.blit(self.img,self.img_rect)

    #外部接口
    def click(self):
        self.mouse_click()
        self.draw()

    #外部接口
    def unclick(self):
        self.mouse_unclick()
        self.draw()

    #按钮点击变色
    def mouse_click(self):
        if self.status:
            self.img = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.status = False   #点击后按钮状态变为关闭
    #按钮点击复原
    def mouse_unclick(self):
        self.img = self.font.render(self.text, True, self.text_color, self.button_color[0])
        self.status = True   #点击后按钮状态变为开启

#重新开始
class RestartButton(Button):
    def __init__(self, screen, x, y, status):
        super().__init__(screen, "重新开始", x, y, [(227, 207, 87), (227, 207, 87)], status)

#悔棋
class RetractButton(Button):
    def __init__(self, screen, x, y, status):
        super().__init__(screen, "悔棋", x, y, [(128, 138, 135), (128, 138, 135)], status)

#认输
class GiveInButton(Button):
    def __init__(self, screen, x, y, status):
        super().__init__(screen, "投降", x, y, [(255, 255, 255), (255, 255, 255)], status)

#保存在指定文件
class SaveButton(Button):
    def __init__(self, screen, x, y, status):
        super().__init__(screen, "保存", x, y, [(37, 70, 232), (37, 70, 232)], status)

#指定文件读取存档覆盖
class CoverButton(Button):
    def __init__(self, screen, x, y, status):
        super().__init__(screen, "回放", x, y, [(37, 70, 232), (37, 70, 232)], status)

#弃子（仅限围棋）
class SkipButton(Button):
    def __init__(self, screen, x, y, status):
        super().__init__(screen, "弃子", x, y, [(128, 138, 135), (128, 138, 135)], status)


# 按钮指令实现类
class AbstractAction:
    def __init__(self, obj, screen, playchess):
        self.obj = obj
        self.screen = screen
        self.playchess = playchess

    # 外部接口
    def react(self):
        if self.obj.status == True:
            self.mouse_react()
            self.back_react()
            self.button_recover()
        return self.playchess

    # 鼠标响应
    def mouse_react(self):
        self.obj.click()
    # 前端响应
    def fore_react(self):
        pass
    # 后端响应
    def back_react(self):
        self.fore_react()
    # 按钮恢复
    def button_recover(self):
        pass

class RestartAction(AbstractAction):
    def fore_react(self):
        print("响应按钮: {0}".format(self.obj.text))
        pygame.quit()
        if gametype == 0:
            frontBuilder.run_gobang()
        elif gametype == 1:
            frontBuilder.run_go()
        elif gametype == 2:
            frontBuilder.run_re()

    def back_react(self):
        self.fore_react()
        PieceBoard(b_size)
        ButtonFactory.get_started()
        if gametype == 0:
            self.buttonAction = ButtonActionFactory(self.screen, PlayGobang())
        elif gametype == 1:
            self.buttonAction = ButtonActionFactory(self.screen, PlayGo())
        elif gametype == 2:
            self.buttonAction = ButtonActionFactory(self.screen, PlayRe())

    def button_recover(self):
        self.obj.unclick()

class RetractAction(AbstractAction):
    def react(self):
        print("响应按钮: {0}".format(self.obj.text))
        self.mouse_react()
        self.back_react()
        self.button_recover()
        return self.playchess

    def back_react(self):
        playchess = self.playchess.retract()
        if playchess != None:
            self.playchess = playchess
            self.fore_react()

    def fore_react(self):
        frontBuilder.Board(screen, PieceBoard.size)

    def button_recover(self):
        ButtonFactory.pool["悔棋"].unclick()

class GiveInAction(AbstractAction):
    def back_react(self):
        playchess = self.playchess.givein()
        if playchess != None:
            self.playchess = playchess

class SaveAction(AbstractAction):
    def react(self):
        print("响应按钮: {0}".format(self.obj.text))
        self.mouse_react()
        self.fore_react()
        self.back_react()
        self.button_recover()
        return self.playchess

    def back_react(self):
        self.state, playchess = self.playchess.memento(self.file_loc, player1.id)  
        if playchess != None:
            self.playchess = playchess

    def fore_react(self):
        if player1.id != 'Vistor' and player1.id != 'AI-1' and player1.id != 'AI-2' and player1.id != 'AI-3' and player1.record != None:    #判断save操作对象id，并判断是否为已登录账号
            id = player1.id
        else:
            raise tkinter.messagebox.showinfo('提示', '用户保存错误')
        #memento界面显示
        self.memo_interface = MementoComposite(id, "save")
        self.file_loc = self.memo_interface.build()

    def button_recover(self):
        self.obj.unclick()
        self.memo_interface.output(self.state, self.file_loc)

class CoverAction(AbstractAction):
    def react(self):
        print("响应按钮: {0}".format(self.obj.text))
        self.mouse_react()
        self.fore_react()
        self.back_react()
        self.button_recover()
        return self.playchess

    def back_react(self):
        self.state, self.history, playchess = self.playchess.cover(self.file_loc)  
        if playchess != None:
            self.playchess = playchess

    def fore_react(self):
        if player1.id != 'Vistor' and player1.id != 'AI-1' and player1.id != 'AI-2' and player1.id != 'AI-3' and player1.record != None:    #判断save操作对象id，并判断是否为已登录账号
            id = player1.id
        else:
            raise tkinter.messagebox.showinfo('提示', '用户无法回放')
        #memento界面显示
        self.memo_interface = MementoComposite(id, "cover")
        self.file_loc = self.memo_interface.build()
        print(self.file_loc)

    def button_recover(self):
        self.obj.unclick()
        self.memo_interface.output(self.state, self.file_loc)
        self.screen = self.memo_interface.cover_interface(self.screen, self.playchess, self.history)

class SkipAction(AbstractAction):
    def react(self):
        print("响应按钮: {0}".format(self.obj.text))
        if self.obj.status == True:
            self.back_react()
        else:
            raise tkinter.messagebox.showinfo('提示', '弃子不合理')
        return self.playchess

    def back_react(self):
        playchess = self.playchess.skip()
        if playchess != None:
            self.playchess = playchess

    def button_recover(self):
        ButtonFactory.pool["弃子"].unclick()


#Button享元类索引列表顺序对应
class ButtonActionFactory:
    pool = dict()
    def __new__(cls, screen, playchess, *args, **kwargs):
        cls.screen = screen
        cls.playchess = playchess

        key = ButtonFactory.get_keys()[0]
        obj = ButtonFactory.pool[key]
        cls.pool[key] = RestartAction(obj, screen, playchess)

        key = ButtonFactory.get_keys()[1]
        obj = ButtonFactory.pool[key]
        cls.pool[key] = RetractAction(obj, screen, playchess)

        key = ButtonFactory.get_keys()[2]
        obj = ButtonFactory.pool[key]
        cls.pool[key] = GiveInAction(obj, screen, playchess)

        key = ButtonFactory.get_keys()[3]
        obj = ButtonFactory.pool[key]
        cls.pool[key] = SaveAction(obj, screen, playchess)

        key = ButtonFactory.get_keys()[4]
        obj = ButtonFactory.pool[key]
        cls.pool[key] = CoverAction(obj, screen, playchess)

        if gametype == 1:
            key = ButtonFactory.get_keys()[5]
            obj = ButtonFactory.pool[key]
            cls.pool[key] = SkipAction(obj, screen, playchess)



#指令策略类
#指令策略类:根据使用者点击位置的不同区分出不同的指令类,并进行操作
class Act:
    def __init__(self, map_x, map_y, x = None, y = None):    #(map_x, map_y)支持输入棋盘坐标，(x,y)支持输入确切坐标
        self.act_type = None
        self.map_x = map_x
        self.map_y = map_y
        if x != None and y != None:
            self.act_loc = (x, y)
        else:
            try:
                self.act_loc = self.get_act_loc()
            except Exception as e:
                print(e)

    def get_act_loc(self):
        pass

    def react(self, screen, playchess):
        pass

    def result(self,playchess):
        # 若终局则输出结果
        if playchess.status == False:
            if playchess.even:
                tkinter.messagebox.showinfo('提示', '游戏结束: 平局！\n请点击‘重新开始’或者退出游戏')
            elif playchess.winner:
                tkinter.messagebox.showinfo('提示', '游戏结束: {0} 胜!\n请点击‘重新开始’或者退出游戏'.format(playchess.winner.text))
            ButtonFactory.pool["重新开始"].unclick()

#下棋指令类
class ChessAct(Act):
    def __init__(self, map_x, map_y, x = None, y = None):
        Act.__init__(self, map_x, map_y, x, y)
        self.act_type = "CHESS"

    def get_act_loc(self):
        if gametype == 2:
            return ((self.map_x - 20) // cell_size , (self.map_y - 20) // cell_size)
        else:
            return (self.map_x // (cell_size // 2) // 2, self.map_y // (cell_size // 2) // 2)
    

    def react(self, screen, playchess):

        try:
            # 若棋局在进行中,则对指令进行回应
            if playchess.status == True:
                # 调用后端处理落子(不必区分棋的种类)
                playchess.play(self.act_loc)
                # 画棋子
                frontBuilder.Board(screen, b_size)

            # 若终局则输出结果
            self.result(playchess)
            return playchess

        except Exception as e:
            print(e)
        return playchess


#按钮指令类
class ButtonAct(Act):
    def __init__(self, map_x, map_y):
        Act.__init__(self, map_x, map_y)
        self.act_type = "BUTTON"

    def get_act_loc(self):
        return self.map_y // button_wide

    def react(self, screen, playchess):

        try:
            key = ButtonFactory.get_keys()[self.act_loc]
            obj = ButtonFactory.pool[key]

            if self.act_loc <= 6:
                playchess = ButtonActionFactory.pool[key].react()

                # 判断，若终局则输出结果
                self.result(playchess)
                return playchess
        except Exception as e:
            print(e)

        return playchess



#棋子颜色枚举类
class PieceColor:
    BLACK = 1   #黑棋颜色索引为1
    WHITE = 2   #白棋颜色索引为2
    EVEN = 3    #平局颜色索引为3

#棋子基类
class Piece:
    def __init__(self, color_index, text):
        self.color = color_index
        self.text = text

#黑棋类
class Black(Piece):
    def __init__(self):
        Piece.__init__(self, PieceColor.BLACK, "BLACK")

#白棋类
class White(Piece):
    def __init__(self):
        Piece.__init__(self, PieceColor.WHITE, "WHITE")

#棋盘类
class PieceBoard:
    size = int
    pool = dict()
    def __new__(cls, size):
        cls.size = size
        for i in range(cls.size):
            for j in range(cls.size):
                cls.pool[(i, j)] = None

    #判断给定坐标是否在边界条件内
    @staticmethod
    def in_judge(pos:tuple):
        if pos[0] >= 0 and pos[1] >= 0 and (pos[0] + 1) <= PieceBoard.size and (pos[1] + 1) <= PieceBoard.size:
            return True
        return False

    # 返回给定坐标处的棋子信息
    @staticmethod
    def fetch_value(pos:tuple):
        if PieceBoard.in_judge(pos):
            return PieceBoard.pool[pos]
        return False

    # 返回给定坐标处的棋子对象
    @staticmethod
    def fetch_obj(pos:tuple):
        objs = [Black(),White()]
        if PieceBoard.fetch_value(pos):
            return objs[PieceBoard.fetch_value(pos) - 1]
        return False

    # 恢复初始化状态
    @staticmethod
    def get_started():
        PieceBoard.pool = dict()
        for i in range(PieceBoard.size):
            for j in range(PieceBoard.size):
                PieceBoard.pool[(i, j)] = None
    
    # 返回棋盘上的空点位集合
    @staticmethod
    def fetch_empty():
        empty_list = []
        for i in range(PieceBoard.size):
            for j in range(PieceBoard.size):
                if PieceBoard.pool[(i, j)] == None:
                    empty_list.append((i,j))
        return empty_list

    @staticmethod
    def re_started():
        PieceBoard.pool[(PieceBoard.size // 2 - 1, PieceBoard.size // 2 - 1)] = PieceColor.WHITE
        PieceBoard.pool[(PieceBoard.size // 2 , PieceBoard.size // 2)] = PieceColor.WHITE
        PieceBoard.pool[(PieceBoard.size // 2, PieceBoard.size // 2 - 1)] = PieceColor.BLACK
        PieceBoard.pool[(PieceBoard.size // 2 - 1, PieceBoard.size // 2)] = PieceColor.BLACK

    @staticmethod
    def at_edge(pos):
        if pos[0] == 0 or pos[0] == PieceBoard.size - 1 or pos[1] == 0 or pos[1] == PieceBoard.size - 1:
            return True
        return False


# 备忘录组件
class MementoComposite:
    def __init__(self, id, status = "save"):
        self.status = status
        self.id = id
        self.account_path = "Gamevideos" 

    def build(self):
        os.makedirs(self.account_path, exist_ok=True)
        self.file_loc = os.path.join(self.account_path, self.id) + '.txt'
        return self.file_loc

    def output(self, state, file_loc):
        if self.status == "save":
            MementoComposite.react_save_memento(state, file_loc)
        elif self.status == "cover":
            MementoComposite.react_cover_memento(state, file_loc)
        else:
            raise tkinter.messagebox.showinfo('提示', '文件错误')

    def cover_interface(self, screen, playchess, history):
        if self.status == "cover":
            coverPiecepool = copy.deepcopy(PieceBoard.pool)
            type_p = ['五子棋', '围棋', '黑白棋'][playchess.type]
            if b_size != playchess.size or gametype != playchess.type:
                tkinter.messagebox.showinfo('提示',f'请退出，设置棋盘大小为{playchess.size}，并选择{type_p}')
            else:
                for i in range(len(history)):
                    time.sleep(0.5)
                    PieceBoard.pool = history[i]
                    self.screen = frontBuilder.Board(screen, PieceBoard.size)
                    pygame.display.update()
            return screen

    # @staticmethod
    # def set_memento():
    #     file_loc = input("输入文件名保存局面至当前路径，或者输入'Y'确认创建Memo.json文件保存: ")
    #     file_loc = MementoComposite.get_file_loc(file_loc)
    #     print("保存局面至 {0}".format(file_loc))
    #     return file_loc

    # @staticmethod
    # def cover_memento():
    #     file_loc = input("输入当前路径文件名覆盖局面，或者输入'Y'确认Memo.json文件覆盖: ")
    #     file_loc = MementoComposite.get_file_loc(file_loc)
    #     print("{0} 覆盖局面".format(file_loc))
    #     return file_loc

    @staticmethod
    def react_save_memento(flag, file_loc):
        if flag:
            tkinter.messagebox.showinfo('提示', f'文件成功保存至{file_loc}')
        else:
            raise tkinter.messagebox.showinfo('提示', '文件保存错误')
        
    def react_cover_memento(flag, file_loc):
        if flag:
            tkinter.messagebox.showinfo('提示', f'文件成功从{file_loc}读取')
        else:
            raise tkinter.messagebox.showinfo('提示', '文件读取错误')
        
    @staticmethod
    def get_file_loc(file_loc):
        if file_loc != "Y":
            return str(file_loc)
        else:
            return "Memo.json"


class PlayChess:
    def __init__(self):
        self.objs = [Black(), White()]
        self.obj = None
        self.color = PieceColor.BLACK  

        self.type = gametype
        self.initiate()

    #按钮指令处理
    def initiate(self):
        self.last_pool = [None, None]  
        self.history = []  #历史记录
        self.retraction = [True, True]  # 仅可以悔棋一次
        self.skip_step = [False, False]  
        self.give_in = [False, False]  # 是否认输
        self.status = True  # 是否进行中
        self.winner = None
        self.even = False

    #下棋操作处理，是外部的函数接口
    def play(self, loc):
        pass

   #交替下棋顺序
    def exchange(self):
        if gametype == 2:
            if self.color == PieceColor.BLACK:
                self.color = PieceColor.WHITE
                pygame.draw.circle(screen, (150,0,0), frontBuilder.get_loc(7, b_size+1), 20, 3)
                pygame.draw.circle(screen, (190, 170, 150), frontBuilder.get_loc(1, b_size+1), 20, 3)
            else:
                self.color = PieceColor.BLACK
                pygame.draw.circle(screen, (150,0,0), frontBuilder.get_loc(1, b_size+1), 20, 3)
                pygame.draw.circle(screen, (190, 170, 150), frontBuilder.get_loc(7, b_size+1), 20, 3)
        else:
            if self.color == PieceColor.BLACK:
                self.color = PieceColor.WHITE
                pygame.draw.circle(screen, (150,0,0), frontBuilder.get_loc(7, b_size), 20, 3)
                pygame.draw.circle(screen, (190, 170, 150), frontBuilder.get_loc(1, b_size), 20, 3)
            else:
                self.color = PieceColor.BLACK
                pygame.draw.circle(screen, (150,0,0), frontBuilder.get_loc(1, b_size), 20, 3)
                pygame.draw.circle(screen, (190, 170, 150), frontBuilder.get_loc(7, b_size), 20, 3)
        print("下一子:{0}".format(["BLACK", "WHITE"][self.color - 1]))

    def save_lastpool(self):
        self.last_pool[1] = self.last_pool[0]
        self.last_pool[0] = dict(PieceBoard.pool)

    def finish(self, finish_flag):
        self.status = False
        if finish_flag == PieceColor.BLACK or finish_flag == PieceColor.WHITE:
            self.winner = self.objs[finish_flag - 1]
            if self.winner == self.objs[0]:
                user_judge.SqlReScore(temppoints[0],'w')
                user_judge.SqlReScore(temppoints[1],'l')
            elif self.winner == self.objs[1]:
                user_judge.SqlReScore(temppoints[1],'w')
                user_judge.SqlReScore(temppoints[0],'l')
        elif finish_flag == PieceColor.EVEN:
            self.even = True

    # 保存棋局记录
    def save_history(self):
        self.history.append(dict(PieceBoard.pool))

    def retract(self):
        self.exchange()
        # 允许悔棋
        if self.retraction[self.color - 1] and self.last_pool[self.color - 1]:
            PieceBoard.pool = self.last_pool[1]
            if PieceBoard.pool == None:
                PieceBoard.get_started()
            self.retraction[self.color - 1] = False
        # 不允许悔棋
        else:
            self.exchange()
            raise tkinter.messagebox.showinfo('提示', '无法悔棋')
        return self

    # 投降
    def givein(self):
        self.exchange()
        self.finish(self.color)
        return self

    # 跳步，仅围棋可以
    def skip(self):
        self.skip_step[self.color - 1] = True
        if self.skip_step != [True, True]:
            self.exchange()
        elif self.type == 1:
            self.finish(GoFinish().do())
        return self

    def memento(self, loc, id1):
        self.origin = Originator(self.history, PieceBoard.size, self.type, self.color, id1)

        caretaker = Caretaker(self.origin.creatMemento())
        state = self.origin.saveMemento(caretaker.memento, loc)
        return state, self

    def cover(self, loc):
        self.origin = Originator(PieceBoard.pool, PieceBoard.size, self.type, self.color)
        if os.path.exists(loc):
            history, size, type, color = self.origin.recoverMemento(loc)
            PieceBoard.size = size
            self.size = size
            self.type = type
            self.color = color
            PieceBoard(PieceBoard.size)
            PieceBoard.pool = history[-1]
            self.initiate()
            return True, history, self
        else:
            raise tkinter.messagebox.showinfo('提示', '文件读取错误！')
        

class PlayGobang(PlayChess):
    def __init__(self):
        PlayChess.__init__(self)

    def play(self, loc):
        self.obj = self.objs[self.color - 1]   #调用棋子类
        place_flag = Place(loc, self.obj).do()   
        # 判断是否落子
        if place_flag:
            # 判断是否结束对局
            finish_flag = GobangFinish(loc, self.obj).do()   #传递棋子类
            if finish_flag:
                self.finish(finish_flag)

            self.save_lastpool()  # 保存落子后的状态
            self.save_history()
            self.exchange()


class PlayGo(PlayChess):
    def __init__(self):
        PlayChess.__init__(self)

    def play(self, loc):
        self.obj = self.objs[self.color - 1]
        place_flag = Place(loc, self.obj).do()
        # 判断是否落子
        if place_flag:
            # 判断是否存在提子
            eaten_flag = GoProcess(loc, self.obj).do()
            # 判断打劫
            self.is_robbery(eaten_flag)
            # 保存落子后的状态
            self.save_lastpool()
            self.save_history()
            self.recover_skip()
            # 交换行棋顺序
            self.exchange()

    #将skip_step恢复为没有跳步
    def recover_skip(self):
        self.skip_step[self.color - 1] = False

    #劫争
    def is_robbery(self, eaten_flag):
        if eaten_flag and self.last_pool[1] == PieceBoard.pool:
            PieceBoard.pool = self.last_pool[0]
            raise tkinter.messagebox.showinfo('提示', '不合理位置')


class PlayRe(PlayChess):
    def __init__(self):
        PlayChess.__init__(self)

    def play(self, loc):
        self.obj = self.objs[self.color - 1]
        place_flag = RePlace(loc, self.obj).do()     #判断是否落子，并处理翻转过程
        if place_flag:
            finish_flag = ReFinish(loc, self.obj).do()     #判断是否终局
            if finish_flag:
                self.finish(finish_flag)
            # 保存落子后的状态
            self.save_lastpool()
            self.save_history()
            # 交换棋权
            self.exchange()

            next_flag = ReProcess(loc, self.objs[self.color - 1]).do()     #判断下一个落子方是否有合法棋步
            if next_flag == False:
                print("No legal position. Forced abstention for {0}".format(["BLACK", "WHITE"][self.color - 1]))
                self.exchange()



##############################   后端   ###############################
######################################################################

#行为管理类
class AbstractManager:
    def __init__(self, loc, obj):
        self.loc = loc
        self.obj = obj

    def do(self):
        return True

class Place(AbstractManager):    #支持落子及落子位置合法性判断
    def do(self):
        if PieceBoard.in_judge(self.loc) and PieceBoard.fetch_value(self.loc) == None:
            PieceBoard.pool[self.loc] = self.obj.color
            print("{0}:{1}".format(self.obj.text, self.loc))
            return True
        else:
            raise tkinter.messagebox.showinfo('提示', '不合理位置')

class GoProcess(AbstractManager):    #支持围棋提子和不合法位置提示
    def do(self):
        self.eaten_list = []
        block = BlockConnection(self.loc, self.obj)

        #提取相连的对方棋子中的死棋
        self.get_opp(block)

        #判断不合法落子
        valid_flag = self.valid(block)

        #判断己方相连棋子是否有死棋（当对方棋子无死棋时）
        self.get_self(block)

        #处理提子操作
        self.eat(self.eaten_list)

        #返回是否提子
        return self.get_result(valid_flag)

    # 对于给定位置，判断连接的棋块是否是活棋
    def alive(self, loc, obj):
        block = BlockConnection(loc, obj)
        return (block.get_range(), block.judge())

    def valid(self,block):
        if self.eaten_list:
            return True
        valid_flag = False
        for i in block.search(self.loc):
            obj = PieceBoard.fetch_obj(i)
            if obj and obj.color != self.obj.color:
                continue
            valid_flag = True
        return valid_flag

    # 判断是否为不合法位置
    def valid_Error(self, flag):
        if flag == False:
            raise tkinter.messagebox.showinfo('提示', '不合理位置')

    #获取对方提子
    def get_opp(self, block):
        for i in block.search(self.loc):
            obj = PieceBoard.fetch_obj(i)
            if obj and obj.color != self.obj.color:
                sub_range, sub_judge = self.alive(i, PieceBoard.fetch_obj(i))
                if sub_judge == False:
                    self.eaten_list.extend(sub_range)

    # 获取己方提子
    def get_self(self, block):
        if block.judge() == False and self.eaten_list == []:
            self.eaten_list.extend(block.get_range())

    # 吃子
    def eat(self, eaten_list):
        for i in eaten_list:
            PieceBoard.pool[i] = None

    def get_result(self,valid_flag):
        # 处理不合法落子
        self.valid_Error(valid_flag)

        # 返回
        if self.eaten_list == []:
            return False
        else:
            print("吃子:{0}".format(self.eaten_list))
            return True

class GoFinish(AbstractManager):    #支持围棋结束
    def __init__(self):
        pass

    def do(self):
        flag_win = GoWin().check()
        if flag_win:
            return flag_win
        return False

class GobangFinish(AbstractManager):    #支持五子棋结束
    def do(self):
        flag_win = GobangWin(self.loc, self.obj).check()
        flag_even = GobangEven(self.loc, self.obj).check()
        if flag_win:
            return flag_win
        elif flag_even:
            return flag_even
        return False



class RePlace(AbstractManager):
    def do(self):
        '''
        if self.place() == True:    #支持落子位置合法性判断
            PieceBoard.pool[self.loc] = self.obj.color
            if self.eat() == True:    #支持黑白棋特有的落子位置合法性判断，并在eat函数中执行翻转操作
                print("{0}:{1}".format(self.obj.text, self.loc))
                return True
            else:
                PieceBoard.pool[self.loc] = None
        raise PlacementError
        '''
        if self.check() == True:
            print("{0}:{1}".format(self.obj.text, self.loc))
            self.eat()
            return True
        else:
            raise tkinter.messagebox.showinfo('提示', '不合理位置')

    def check(self):
        if self.place() == True:  # 支持落子位置合法性判断
            PieceBoard.pool[self.loc] = self.obj.color
            if self.get_eatenlist() == True:  # 支持黑白棋特有的落子位置合法性判断，并在eat函数中执行翻转操作
                return True
            else:
                PieceBoard.pool[self.loc] = None
        return False

    def eat(self):
        #对翻转列表中的棋子进行翻转操作
        for i in self.eaten_list:
            PieceBoard.pool[i] = self.obj.color

    def place(self):
        if PieceBoard.in_judge(self.loc) and PieceBoard.fetch_value(self.loc) == None:
            return True
        else:
            raise tkinter.messagebox.showinfo('提示', '不合理位置')

    def get_eatenlist(self):
        obj = self.exchange(self.obj)    #翻转目标为对方棋子
        linearShape = ShapeIterator()    #创建形状迭代器类
        linearShape.add(Horizontal(self.get_adjacent(self.loc, "plus", None), obj))
        linearShape.add(Horizontal(self.get_adjacent(self.loc, "minus", None), obj))
        linearShape.add(Vertical(self.get_adjacent(self.loc, None, "plus"), obj))
        linearShape.add(Vertical(self.get_adjacent(self.loc, None, "minus"), obj))
        linearShape.add(Leftoblique(self.get_adjacent(self.loc, "minus", "plus"), obj))
        linearShape.add(Leftoblique(self.get_adjacent(self.loc, "plus", "minus"), obj))
        linearShape.add(Rightoblique(self.get_adjacent(self.loc, "plus", "plus"), obj))
        linearShape.add(Rightoblique(self.get_adjacent(self.loc, "minus", "minus"), obj))

        self.eaten_list = []
        for shape in linearShape:
            #求出线性连通区域坐标边界和连通棋子数量
            left, right = shape.get_range()
            num = shape.count()

            #线性连通区域多于1个棋子
            if num > 1:
                # 求出线性连通区域毗邻的两颗棋子的坐标
                left_out = (left[0] + (left[0] - right[0]) / (num - 1), left[1] + (left[1] - right[1]) / (num - 1))
                right_out = (right[0] + (right[0] - left[0]) / (num - 1), right[1] + (right[1] - left[1]) / (num - 1))
                # 判断毗邻棋子是否为异色棋子；若是，则将线性区域中的棋子添加至被翻转列表
                if PieceBoard.fetch_value(left_out) == self.obj.color and PieceBoard.fetch_value(right_out) == self.obj.color:
                    for i in range(num):
                        self.eaten_list.append((left[0] + (right[0] - left[0]) / (num - 1) * i, left[1] + (right[1] - left[1]) / (num - 1) * i))
            #线性连通区域等于1个棋子
            elif num == 1:
                out = (left[0] + (left[0] - self.loc[0]), left[1] + (left[1] - self.loc[1]))
                if PieceBoard.fetch_value(out) == self.obj.color:
                    self.eaten_list.append(left)

        #返回是否存在翻转
        if self.eaten_list:
            return True
        return False

    def get_adjacent(self, loc, act1 = None, act2 = None):     #获取坐标的邻近位置
        adj_loc0 = loc[0]
        adj_loc1 = loc[1]
        if act1 == "plus":
            adj_loc0 += 1
        if act1 == "minus":
            adj_loc0 -= 1
        if act2 == "plus":
            adj_loc1 += 1
        if act2 == "minus":
            adj_loc1 -= 1
        return (adj_loc0, adj_loc1)

    def exchange(self, obj):     #变更棋子对象
        if obj.color == PieceColor.BLACK:
            return White()
        else:
            return Black()


class ReProcess(AbstractManager):
    def do(self):
        # 通过遍历棋盘判断目标方是否有合法位置可下
        flag = False  # 判断变量，初始假设为无合法位置
        for i in range(PieceBoard.size):
            for j in range(PieceBoard.size):
                if PieceBoard.pool[(i, j)] == None:  # 当棋盘上存在空点时
                    if RePlace((i, j), self.obj).check() :  # 判断空点处目标方是否能行棋
                        PieceBoard.pool[(i, j)] = None
                        flag = True
                        break
            else:
                continue
            break
        return flag


class ReFinish(AbstractManager):
    def do(self):
        #通过遍历棋盘判断是否终局
        flag = True     #终局判断变量，初始假设为达成终局
        for i in range(PieceBoard.size):
            for j in range(PieceBoard.size):
                if PieceBoard.pool[(i , j)] == None:     #当棋盘上存在空点时
                    if RePlace((i, j), Black()).check() or RePlace((i, j), White()).check():     #判断空点处双方是否能行棋，若能行棋，则未达成终局
                        PieceBoard.pool[(i, j)] = None
                        flag = False
                        break
            else:
                continue
            break

        #未达成终局情况
        if flag == False:
            return False

        #达成终局情况
        flag = ReOutcome(self.loc, self.obj).check()
        return flag




#全局判断类
class AbstractOverall:
    def __init__(self, loc, obj):
        self.loc = loc
        self.obj = obj

    def check(self):
        pass

# 五子棋胜负局判断类
class GobangWin(AbstractOverall):
    def __init__(self, loc, obj):
        AbstractOverall.__init__(self, loc, obj)

    def check(self):
        check_list = []
        check_list.append(Horizontal(self.loc, self.obj))
        check_list.append(Vertical(self.loc, self.obj))
        check_list.append(Leftoblique(self.loc, self.obj))
        check_list.append(Rightoblique(self.loc, self.obj))
        for i in range(4):
            check_list[i].get_range()
            if check_list[i].count() >= 5:
                return self.obj.color
        return False

# 五子棋平局判断类
class GobangEven(AbstractOverall):
    def __init__(self, loc, obj):
        AbstractOverall.__init__(self, loc, obj)

    def check(self):
        for i in range(PieceBoard.size):
            for j in range(PieceBoard.size):
                if PieceBoard.pool[(i , j)] == None:
                    return False
        return PieceColor.EVEN

# 围棋胜负局判断类
class GoWin(AbstractOverall):
    def __init__(self):
        pass

    # 暂不支持围棋结果判断
    def check(self):
        pass


class ReOutcome(AbstractOverall):
    def __init__(self, loc, obj):
        AbstractOverall.__init__(self, loc, obj)

    def check(self):
        black_num = 0
        white_num = 0
        #求出棋盘上黑白棋子的数量
        for i in range(PieceBoard.size):
            for j in range(PieceBoard.size):
                if PieceBoard.pool[(i , j)] == PieceColor.BLACK:
                    black_num += 1
                elif PieceBoard.pool[(i , j)] == PieceColor.WHITE:
                    white_num += 1
        #根据黑白棋数量判定结局
        if black_num > white_num:
            return PieceColor.BLACK
        elif black_num < white_num:
            return PieceColor.WHITE
        else:
            return PieceColor.EVEN



class AbstractLocal:
    def __init__(self, loc, obj):
        self.loc = loc
        self.obj = obj

    def get_range(self):
        pass

# 线性连接判断类
class LinearConnection(AbstractLocal):
    def __init__(self, loc, obj):
        AbstractLocal.__init__(self, loc, obj)

    def get_range(self):
        self.left = self.loc
        self.right = self.loc
        for i in range(1, PieceBoard.size):
            loc_plus = self.loc_plus(i)
            if loc_plus and PieceBoard.fetch_value(loc_plus) == self.obj.color:
                self.right = loc_plus
            else:
                break

        for i in range(1, PieceBoard.size):
            loc_minus = self.loc_minus(i)
            if loc_minus and PieceBoard.fetch_value(loc_minus) == self.obj.color:
                self.left = loc_minus
            else:
                break

        return (self.left, self.right)

    def count(self):
        num = max(abs(self.left[0]-self.right[0]),abs(self.left[1]-self.right[1])) + 1
        return num

    def loc_plus(self, i):
        return None

    def loc_minus(self, i):
        return None

# 水平连接棋型
class Horizontal(LinearConnection):
    def loc_plus(self, i):
        return (self.loc[0] + i, self.loc[1])
    def loc_minus(self, i):
        return (self.loc[0] - i, self.loc[1])

# 竖直连接棋型
class Vertical(LinearConnection):
    def loc_plus(self, i):
        return (self.loc[0], self.loc[1] + i)
    def loc_minus(self, i):
        return (self.loc[0], self.loc[1] - i)

# 左斜连接棋型
class Leftoblique(LinearConnection):
    def loc_plus(self, i):
        return (self.loc[0] + i, self.loc[1] - i)
    def loc_minus(self, i):
        return (self.loc[0] - i, self.loc[1] + i)

# 右斜连接棋型
class Rightoblique(LinearConnection):
    def loc_plus(self, i):
        return (self.loc[0] + i, self.loc[1] + i)
    def loc_minus(self, i):
        return (self.loc[0] - i, self.loc[1] - i)

# 围棋块状连接判断类
class BlockConnection(AbstractLocal):
    def __init__(self, loc, obj):
        AbstractLocal.__init__(self, loc, obj)
        self.list = []

    # 找出与给定位置块状连接的所有点
    def get_range(self):
        self.find_range(self.loc)
        return self.list

    def find_range(self, loc):
        self.list.append(loc)
        for i in self.search(loc):
            if PieceBoard.fetch_value(i) == self.obj.color and (i not in self.list):
                self.find_range(i)

    # 判断与给定位置相连的棋块是否有气
    def judge(self):
        self.list_judge = []
        flag = self.find_judge(self.loc)  
        return flag

    def find_judge(self, loc):
        self.list_judge.append(loc)
        for pos in self.search(loc):
            if PieceBoard.fetch_value(pos) == None:
                return True
            elif PieceBoard.fetch_value(pos) == self.obj.color and (pos not in self.list_judge):
                flag = self.find_judge(pos)
                if flag:
                    return True
        return False

    def search(self, loc):
        search_list = [self.up(loc), self.right(loc), self.down(loc), self.left(loc)]
        return search_list

    def up(self, loc):
        return (loc[0], loc[1] - 1)

    def down(self, loc):
        return (loc[0], loc[1] + 1)

    def left(self, loc):
        return (loc[0] - 1, loc[1])

    def right(self, loc):
        return (loc[0] + 1, loc[1])

#形状迭代器
class ShapeIterator:
    def __init__(self):
        self.checklist = []
        self.num = 0

    def add(self, shape:AbstractLocal):
        if PieceBoard.in_judge(shape.loc) and shape.obj.color == PieceBoard.fetch_value(shape.loc):      #确认棋盘对应位置上的棋子与翻转的目标棋子颜色相同后再将目标形状添加至checklist
            self.checklist.append(shape)

    def __iter__(self):
        return self

    def __next__(self):
        if self.num < len(self.checklist):
            ret = self.checklist[self.num]
            self.num += 1
            return ret
        else:
            raise StopIteration


class Originator:
    def __init__(self, history, size, type, color, id1 = None):
        self.state = dict()
        self.state.update({"Size":size, "Type":type, "Color":color, "id1":id1})
        self.history = history
        # self.state.update(situ)

    def creatMemento(self):
        return Memento(self.state)

    def restoreMemento(self, memento):
        self.state = memento.getState()

    def saveMemento(self, memento, file_loc):
        try:
            self.restoreMemento(memento)
            with open(file_loc, mode='w') as f:
                f.write(json.dumps(self.state))
                for i, situ in enumerate(self.history):
                    situ = json.dumps({str(k): situ[k] for k in situ.keys()})
                    f.write("\n")
                    f.write(json.dumps(situ))
            return True
        except Exception as e:
            return False

    def recoverMemento(self, file_loc):
        try:
            with open(file_loc, mode='r') as f:
                history = []
                lines = f.readlines()
                state = json.loads(lines[0])
                for i in range(1, len(lines)):
                    line = json.loads(lines[i])
                    line = json.loads(line)
                    line = {self._tuple(k): line[k] for k in line.keys()}
                    history.append(line)

            self.state = state
            self.history = history

            return self.history, self.state["Size"], self.state["Type"], self.state["Color"]
        except Exception as e:
            return False

    def _tuple(self, key):
        pat1 = '\d'         # 匹配数字
        pat2 = '\D'         # 匹配非数字
        if re.findall(pat1, key):
            key_split = re.split(pat2, key)
            tuple_list = []
            for split in key_split:
                if split:
                    tuple_list.append(int(split))
            return tuple(tuple_list)
        else:
            return str(key)

class Memento:
    def __init__(self,state):
        self.state = state

    def getState(self):
        return self.state

class Caretaker:
    def __init__(self,memento):
        self.memento = memento

    def saveMemento(self, memento):
        self.memento = memento

    def getMemento(self):
        return self.memento



class SWITCH:
    ON = 1
    OFF = 2

class Player:
    def __init__(self,type,id,record,color):
        self.type = type
        self.id = id
        self.record = record
        self.color = color
        self.switch = None   #标识是否自主下棋
        self.init()

    def init(self):
        pass

    def play(self):
        pass

    def get_status(self):   #返回是否自主下棋的标识
        if self.switch == SWITCH.ON:
            return True
        else:
            return False

    def update_record(self):   #是否支持更新判断
        if self.record:
            return True
        return False

class UserPlayer(Player):
    def init(self):
        self.switch = SWITCH.OFF   #用户类不能自主下棋

#AI角色
class AIPlayer(Player):
    def init(self):
        self.switch = SWITCH.ON   #AI类可以自主下棋


#五子棋一级AI
class AI1Player(AIPlayer):
    def play(self):
        empty_list = PieceBoard.fetch_empty()   #获取棋盘上的空点位
        pos = empty_list[random.randint(0, len(empty_list) - 1)]   #从空点位中随机选取一个点
        return (pos[0], pos[1])

#五子棋二级AI
class AI2Player(AIPlayer):

    # 二级AI基本思路：假设下在棋盘任意空点位，对下完后的棋型进行评分，选出评分最高的点
    # 人工规则：对五子棋的七种基本棋型给出评分，每步下完后给出局部评分
    def play(self):
        self.empty_list = PieceBoard.fetch_empty()  # 获取棋盘上的空点位
        max_value = 0            #评分最高的值
        max_pos = tuple()        #评分最高的位置
        self.score()        #初始化棋型评分

        for pos in self.empty_list:
            value = self.get_value(pos)
            if value > max_value:
                max_value = value
                max_pos = pos

        if max_pos:
            return (max_pos[0], max_pos[1])
        elif self.empty_list:
            return self.empty_list[len(self.empty_list)//2]
        else:
            return None

    # 评分过程
    def get_value(self, pos):
        value = 0
        single_flag = False
        self.oppo_color = self.exchange(self.color)
        # 若己方下在此位置，获得局部棋型评分，视为己方主动赢得的评分
        obj = [Black(), White()][self.color - 1]
        PieceBoard.pool[pos] = obj.color
        linearShape = ShapeIterator()
        linearShape.add(Horizontal(pos,obj))
        linearShape.add(Vertical(pos,obj))
        linearShape.add(Leftoblique(pos,obj))
        linearShape.add(Rightoblique(pos,obj))
        for shape in linearShape:
            left, right = shape.get_range()    #获取每个方向的连接棋子个数
            num = shape.count()
            value += self.get_rules(left, right, num, self.color)
            if num == 1:
                single_flag = True
        if single_flag:
            value += self.get_single(pos, self.color)
            #print("single {0}:{1}".format(pos, self.get_single(pos, self.color)))
        PieceBoard.pool[pos] = None

        # 若己方未下，而下一步对方下在此位置，获得对方的局部评分，视为己方阻击对方赢得的评分
        obj = [Black(), White()][self.oppo_color - 1]
        PieceBoard.pool[pos] = obj.color
        linearShape = ShapeIterator()
        linearShape.add(Horizontal(pos, obj))
        linearShape.add(Vertical(pos, obj))
        linearShape.add(Leftoblique(pos, obj))
        linearShape.add(Rightoblique(pos, obj))
        for shape in linearShape:
            left, right = shape.get_range()  # 获取每个方向的连接棋子个数
            num = shape.count()
            value += self.get_rules(left, right, num, self.oppo_color)
            if num == 1:
                single_flag = True
        if single_flag:
            value += self.get_single(pos, self.oppo_color)
        PieceBoard.pool[pos] = None

        return value

    # n>=2时的评分规则
    def get_rules(self, left, right, num, color):
        oppo_color = self.exchange(color)         # 初始化获取对方棋色
        # 局部连五子棋型
        if num >= 5:
            return self.FIVE                     #连五子 00000

        # 局部连四子棋型
        if num == 4:
            left_out, right_out = self.get_out(left, right)
            free_list = self.check_out(left_out, right_out, oppo_color)
            if len(free_list) == 2:
                return self.FOUR_LIVE        #活四 0000
            elif len(free_list) == 1:
                return self.FOUR_SLEEP       #眠四 0000x
            else:
                return 0                     #连四子两边都被堵死，无效棋型

        # 局部连三子棋型
        if num == 3:
            left_out, right_out = self.get_out(left, right)
            free_list = self.check_out(left_out, right_out, oppo_color)
            #print("free_list", free_list)
            if len(free_list) == 2:
                # 有4种情况
                left_out2, right_out2 = self.get_out(left_out, right_out)
                free_list2_self = self.check_out(left_out2, right_out2, color)
                if len(free_list2_self) == 0:
                    #print("两个眠四", color)
                    return self.FOUR_SLEEP * 2  # 两个眠四 0*000*0
                elif len(free_list2_self) == 1:
                    #print("眠四", color)
                    return self.FOUR_SLEEP       #眠四 0*000
                else:
                    free_list2 = self.check_out(left_out2, right_out2, oppo_color)
                    if len(free_list2) == 0:
                        #print("眠三", color)
                        return self.THREE_SLEEP     #眠三 x*000*x
                    #print("活三", color)
                    return self.THREE_LIVE      #活三 000

            elif len(free_list) == 1:
                #print("眠三", color)
                return self.THREE_SLEEP       #眠三 000x
            else:
                return 0                     #连三子两边都被堵死，无效棋型

        # 局部连二子棋型
        if num == 2:
            left_out, right_out = self.get_out(left, right)
            free_list = self.check_out(left_out, right_out, oppo_color)
            if len(free_list) == 2:
                # 有10种情况
                left_out2, right_out2 = self.get_out(left_out, right_out)
                ocu_list2_self = self.check_in(left_out2, right_out2, color)
                ocu_list2 = self.check_in(left_out2, right_out2, oppo_color)
                left_out3, right_out3 = self.get_out(left_out2, right_out2)
                ocu_list3_self = self.check_in(left_out3, right_out3, color)
                ocu_list3 = self.check_in(left_out3, right_out3, oppo_color)
                if ocu_list2_self:
                    if len(ocu_list2_self) == 2 and len(ocu_list3_self) == 2:
                        return self.FOUR_SLEEP * 2   # 两个眠四 00*00*00
                    elif len(ocu_list2_self) == 2 and len(ocu_list3_self) == 1:
                        return self.FOUR_SLEEP + self.THREE_LIVE   # 眠四+活三 0*00*00
                    elif len(ocu_list2_self) == 2 and len(ocu_list3) == 2:
                        return self.THREE_SLEEP * 2   # 两个眠三 x0*00*0x
                    elif len(ocu_list2_self) == 2 and len(ocu_list3) == 1:
                        return self.THREE_SLEEP + self.THREE_LIVE   # 眠三+活三 x0*00*0
                    elif len(ocu_list2_self) == 2:
                        return self.THREE_LIVE * 2    # 两个活三 0*00*0
                    else:
                        if ocu_list3_self and self.aja(ocu_list2_self,ocu_list3_self):
                            return self.FOUR_SLEEP    # 眠四 00*00
                        elif ocu_list3 and self.aja(ocu_list2_self,ocu_list3):
                            return self.THREE_SLEEP    # 眠三 x0*00
                        else:
                            return self.THREE_LIVE    # 活三 0*00
                else:
                    if ocu_list3_self:
                        return self.THREE_SLEEP   # 眠三 00**0
                    return self.TWO_LIVE          # 活二

            elif len(free_list) == 1:
                # 有2种情况
                if self.check_in(left, free_list[0], color) and self.check_in(right, free_list[0], color):
                    return self.THREE_SLEEP   # 眠三 x00*0
                return self.TWO_SLEEP         # 眠二 x00
            else:
                return 0                    # 连二子两边都被堵死，无效棋型
        return 0


    # n=1时的评分规则（仅考虑冲四和活三棋型的计分）
    def get_single(self, pos, color):
        checklist = self.get_checklist(pos)
        value = 0
        for loc in checklist:
            add_value = 0
            for i in range(3):
                out = (loc[0] + (loc[0] - pos[0]) * (i + 1), loc[1] + (loc[1] - pos[1]) * (i + 1))
                if PieceBoard.fetch_value(out) == color:
                    if i == 1:
                        add_value = self.THREE_LIVE   #活三 00x0
                    elif i == 2:
                        add_value = self.FOUR_SLEEP  # 眠四 000x0
                else:
                    break
            value += add_value
        return value

    # 分值
    def score(self):
        self.FIVE = 50000
        self.FOUR_LIVE = 15000
        self.FOUR_SLEEP = 8000
        self.THREE_LIVE = 4500
        self.THREE_SLEEP = 3500
        self.TWO_LIVE = 100
        self.TWO_SLEEP = 50

    # 获取连通区域的外边界
    def get_out(self, left, right):
        num = max(abs(left[0] - right[0]), abs(left[1] - right[1])) + 1
        left_out = (left[0] + (left[0] - right[0]) / (num - 1), left[1] + (left[1] - right[1]) / (num - 1))
        right_out = (right[0] + (right[0] - left[0]) / (num - 1), right[1] + (right[1] - left[1]) / (num - 1))
        return (left_out, right_out)

    # 查询边界是否被堵（传递的color为对方棋色）,返回未被堵的边界
    def check_out(self, left_out, right_out, color):
        free_list = []
        if PieceBoard.in_judge(left_out) and PieceBoard.fetch_value(left_out) != color:
            free_list.append(left_out)
        if PieceBoard.in_judge(right_out) and PieceBoard.fetch_value(right_out) != color:
            free_list.append(right_out)
        return free_list

    # 查询是否是指定颜色，返回是指定颜色的集合
    def check_in(self, left_out, right_out, color):
        ocu_list = []
        if PieceBoard.in_judge(left_out) and PieceBoard.fetch_value(left_out) == color:
            ocu_list.append(left_out)
        if PieceBoard.in_judge(right_out) and PieceBoard.fetch_value(right_out) == color:
            ocu_list.append(right_out)
        return ocu_list

    # 获取对方棋色
    def exchange(self, color):
        if color == PieceColor.BLACK:
            return PieceColor.WHITE
        else:
            return PieceColor.BLACK

    # 判断两个目标序列是否相邻
    def aja(self, list1, list2):
        for loc1 in list1:
            for loc2 in list2:
                if max(abs(loc1[0] - loc2[0]), abs(loc1[1] - loc2[1])) == 1:
                    return True
        return False

    # 目标坐标周围一圈坐标
    def get_checklist(self, pos):
        list = [(pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]), (pos[0]-1, pos[1]+1), (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]), (pos[0]+1, pos[1]+1)]
        check_list = []
        for loc in list:
            if PieceBoard.in_judge(loc) and PieceBoard.fetch_value(loc) == None:
                check_list.append(loc)
        return check_list

class AI3Player(AIPlayer):
    def play(self):
        self.empty_list = PieceBoard.fetch_empty()  # 获取棋盘上的空点位
        area = PieceBoard.size * PieceBoard.size
        if len(self.empty_list) == area:
            return(self.empty_list[len(self.empty_list)//2])

        root = Node(None, None, -1)

        value_dict = self.get_value(PieceBoard.pool)  # 初始估值
        pos_list0 = []  # 有初始估值的位置
        prob_list0 = []  # 初始估值
        sum = 0
        for value in value_dict.values():
            sum += value

        # 为根节点建立子节点
        #print(value_dict)
        for key in value_dict.keys():
            if value_dict[key] != 0:
                pos_list0.append(key)
                prob_list0.append(value_dict[key] / sum)
                root.set_son(Node(key, root, root.layer + 1))

        #创建蒙特卡洛模拟，根据棋局不同阶段传递不同参数
        if area - len(self.empty_list) > 7:
            self.monte_carlo(10000, 5, root, pos_list0, prob_list0)
        else:
            self.monte_carlo(5000, 10, root, pos_list0, prob_list0)

        # 已得到蒙特卡洛树，采用max min方法得到置信度值最大的坐标，考虑2层
        C = math.sqrt(2)
        uct0_list = []
        for son0 in root.son:
            uct1_list = []
            for son1 in son0.son:
                uct2_list = []
                for son2 in son1.son:
                    if son2.total:
                        son2.uct = son2.win + C * math.sqrt(math.log(son1.total) / son2.total)
                        uct2_list.append(son2.uct)
                if uct2_list:
                    son1.uct = max(uct2_list)
                if son1.uct == 0:
                    if son1.total:
                        son1.uct = son1.win + C * math.sqrt(math.log(son0.total) / son1.total)
                uct1_list.append(son1.uct)

            if uct1_list:
                son0.uct = min(uct1_list)
            if son0.uct == 0:
                if son0.total:
                    son0.uct = son0.win + C * math.sqrt(math.log(root.total) / son0.total)
            uct0_list.append(son0.uct)

        if uct0_list:
            root.uct = max(uct0_list)

        # 获取目标坐标
        for son in root.son:
            if son.uct == root.uct:
                return son.pos

    def monte_carlo(self, n, dep, root, pos_list0, prob_list0):
        # 控制模拟次数
        for i in range(n):
            father = root
            pos_list = pos_list0
            prob_list = prob_list0
            self.pool = dict(PieceBoard.pool)

            # 循环下棋过程
            color = self.color
            obj = [Black(), White()][color - 1]
            k = 0
            while k < dep:  # 控制树的纵深
                item = self.random_pick(pos_list, prob_list)
                # item = pos_list[random.randint(0, len(pos_list) - 1)]
                father.set_son(Node(item, father, father.layer + 1))
                father = self.get_son(father, item)
                # print("father:", father)
                PieceBoard.pool[item] = color
                # 达到终局条件，反向传播，并跳出循环
                if GobangWin(item, obj).check():
                    while True:
                        father.add_total()
                        if color == self.color:
                            father.add_win()
                        if father.layer == -1:
                            break
                        father = father.father
                        # print("finish")
                    break
                # 未达到终局条件，继续循环
                else:
                    value_dict = self.get_value(PieceBoard.pool)  # 初始估值
                    pos_list = []  # 有初始估值的位置
                    prob_list = []  # 初始估值
                    sum = 0
                    for value in value_dict.values():
                        sum += value

                    # 为父节点建立子节点
                    for key in value_dict.keys():
                        if value_dict[key] != 0:
                            pos_list.append(key)
                            prob_list.append(value_dict[key] / sum)

                color = self.exchange(color)
                obj = [Black(), White()][color - 1]
                k += 1

            PieceBoard.pool = self.pool

    def get_value(self,pool):
        value = dict()
        for pos in pool.keys():
            value[pos] = 0
            if pool[pos] == None:
                aja1 = self.get_aja(pos,1)

                for x in aja1:
                    if PieceBoard.in_judge(x) and pool[x] != None:
                        value[pos] += 1
                        if PieceBoard.at_edge(x):
                            value[pos] -= 0.5

        return value

    def get_aja(self, pos, i):
        return [(pos[0]-i, pos[1]-i), (pos[0]-i, pos[1]), (pos[0]-i, pos[1]+i), (pos[0], pos[1]-i), (pos[0], pos[1]+i), (pos[0]+i, pos[1]-i), (pos[0]+i, pos[1]), (pos[0]+i, pos[1]+i)]

    # 按一定概率分布从列表中选取一个元素
    def random_pick(self, list, prob):
        x = random.uniform(0, 1)
        cumulative_prob = 0.0
        item = list[0]
        for item, item_prob in zip(list, prob):
            cumulative_prob += item_prob
            if x < cumulative_prob:
                break
        return item

    def get_son(self, father, pos):
        for son in father.son:
            if son.pos == pos:
                return son

    # 棋色易色
    def exchange(self, color):
        if color == PieceColor.BLACK:
            return PieceColor.WHITE
        else:
            return PieceColor.BLACK


class Node:
    def __init__(self, pos, father, layer):
        self.pos = pos
        self.father = father
        self.layer = layer
        self.value = None  # 估值函数

        self.son = []

        self.uct = 0  #置信度
        self.win = 0  #胜的次数
        self.total = 0  #总的次数

    def set_layer(self,layer):
        self.layer = layer

    def set_son(self, obj):
        for son in self.son:
            if son.pos == obj.pos:
                return
        self.son.append(obj)

    def add_win(self):
        self.win += 1

    def add_total(self):
        self.total += 1




######### 代码运行示例 ########

a = user_init()