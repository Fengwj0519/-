import re
import json
import copy
from tkinter import *
import tkinter as tk
import pygame
import tkinter.messagebox


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
        game.geometry("600x400")
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
                tkinter.messagebox.showinfo('提示', '设置棋盘大小不在正确范围，为您取15 * 15')
                b_size = 15
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
        w2q = tk.Button(game, text="退出", width=self.button_width, height=self.button_height, command=quit, font=('楷体', 15))
        w2gobang.pack()
        w2go.pack()
        w2q.pack()
        game.mainloop()
        return b_size
    
class frontBuilder:
    @staticmethod
    def run_gobang():
        global screen, gametype
        gametype = 0
        pygame.init()
        game_gobang = Gobang_interface(b_size)
        screen, buttons = game_gobang.run()
        ButtonFactory(buttons)
        PieceBoard(b_size)
        ButtonActionFactory(screen, game_gobang.playchess)

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
        global screen, gametype
        gametype = 1
        pygame.init()
        game_go = Go_interface(b_size)
        screen, buttons = game_go.run()
        ButtonFactory(buttons)
        PieceBoard(b_size)
        ButtonActionFactory(screen, game_go.playchess)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 执行关闭程序的操作
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    act_x, act_y = pygame.mouse.get_pos()
                    game_go.mouse_clicks(act_x, act_y)
                    pygame.display.update()

    @staticmethod
    def Board(screen, size):
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
        for row in range(size-1):
            for col in range(size-1):
                pygame.draw.rect(screen, (0, 0, 0), (col * cell_size + 20, row * cell_size + 20,
                                                    cell_size, cell_size), 1)
    
    @staticmethod
    def set_piece(screen,x,y):#画棋子
        if PieceBoard.in_judge((x,y)):
            pos = frontBuilder.get_loc(x, y)
            pygame.draw.circle(screen, [(41, 36, 33),(255, 245, 238)][PieceBoard.pool[x, y] - 1], pos, 18)
            pygame.draw.circle(screen, (41, 36, 33), pos, 18,2)

    @staticmethod
    def get_loc(x,y):   #返回棋子在界面上的实际位置
        map_x = x * cell_size + 20
        map_y = y * cell_size + 20
        return (map_x, map_y)


class Gobang_interface:
    def __init__(self, board_size):
        pygame.init()
        self.board_size = board_size  # 棋盘大小
        self.screen_width = 20 + (self.board_size-1) * cell_size + 20 + 200  # 屏幕宽度
        self.screen_height = 20 + (self.board_size-1) * cell_size + 20  # 屏幕高度
        self.button_x = 20 + (self.board_size-1) * cell_size + 20 + 20  # 按钮的横坐标
        self.button_y = 20  # 按钮的纵坐标
        self.obj = [PlayGobang(), PlayGo()]
        self.playchess = self.obj[0]

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

    def get_act(self,map_x, map_y):   
        if map_x >= self.button_x:
            return ButtonAct(map_x,map_y)
        else:
            return ChessAct(map_x,map_y)


class Go_interface:
    def __init__(self, board_size):
        pygame.init()
        self.board_size = board_size  # 棋盘大小
        self.screen_width = 20 + (self.board_size-1) * cell_size + 20 + 200  # 屏幕宽度
        self.screen_height = 20 + (self.board_size-1) * cell_size + 20  # 屏幕高度
        self.button_x = 20 + (self.board_size-1) * cell_size + 20 + 20  # 按钮的横坐标
        self.button_y = 20  # 按钮的纵坐标
        self.obj = [PlayGobang(), PlayGo()]
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

#棋子种类枚举类
class ChessType:
    GOBANG = 0   #五子棋索引为0
    GO = 1   #围棋索引为1


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
        super().__init__(screen, "覆盖", x, y, [(37, 70, 232), (37, 70, 232)], status)

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

    def back_react(self):
        self.fore_react()
        PieceBoard(b_size)
        ButtonFactory.get_started()
        if gametype == 0:
            self.buttonAction = ButtonActionFactory(self.screen, PlayGobang())
        elif gametype == 1:
            self.buttonAction = ButtonActionFactory(self.screen, PlayGo())

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
        self.state, playchess = self.playchess.memento(self.file_loc)  
        if playchess != None:
            self.playchess = playchess

    def fore_react(self):
        #memento界面显示
        self.memo_interface = MementoComponent("save")
        self.file_loc = self.memo_interface.build()

    def button_recover(self):
        self.obj.unclick()
        self.memo_interface.output(self.state)

class CoverAction(AbstractAction):
    def react(self):
        print("响应按钮: {0}".format(self.obj.text))
        self.mouse_react()
        self.fore_react()
        self.back_react()
        self.button_recover()
        return self.playchess

    def back_react(self):
        self.state, playchess = self.playchess.cover(self.file_loc)  
        if playchess != None:
            self.playchess = playchess

    def fore_react(self):
        #memento界面显示
        self.memo_interface = MementoComponent("cover")
        self.file_loc = self.memo_interface.build()

    def button_recover(self):
        self.obj.unclick()
        self.memo_interface.output(self.state)
        self.screen = self.memo_interface.cover_interface(self.screen, self.playchess)

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
class Act:
    def __init__(self, map_x, map_y):
        self.act_type = None
        self.map_x = map_x
        self.map_y = map_y
        self.act_loc = self.get_act_loc()

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
    def __init__(self, map_x, map_y):
        Act.__init__(self, map_x, map_y)
        self.act_type = "CHESS"

    def get_act_loc(self):
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


# 备忘录组件
class MementoComponent():
    def __init__(self, status = "save"):
        self.status = status

    def build(self):
        if self.status == "save":
            self.file_loc = MementoComponent.set_memento()
        elif self.status == "cover":
            self.file_loc = MementoComponent.cover_memento()
        else:
            raise tkinter.messagebox.showinfo('提示', '文件错误')
        return self.file_loc

    def output(self, state):
        if self.status == "save":
            MementoComponent.react_save_memento(state)
        elif self.status == "cover":
            MementoComponent.react_cover_memento(state)
        else:
            raise tkinter.messagebox.showinfo('提示', '文件错误')

    def cover_interface(self, screen, playchess):
        if self.status == "cover":
            coverPiecepool = copy.deepcopy(PieceBoard.pool)
            type_p = ['五子棋', '围棋'][playchess.type]
            if b_size != playchess.size or gametype != playchess.type:
                tkinter.messagebox.showinfo('提示',f'请退出，设置棋盘大小为{playchess.size}，并选择{type_p}')
            else:
                PieceBoard.pool = coverPiecepool
                self.screen = frontBuilder.Board(screen, PieceBoard.size)
            return screen

    @staticmethod
    def set_memento():
        file_loc = input("输入文件名保存局面至当前路径，或者输入'Y'确认创建Memo.json文件保存: ")
        file_loc = MementoComponent.get_file_loc(file_loc)
        print("保存局面至 {0}".format(file_loc))
        return file_loc

    @staticmethod
    def cover_memento():
        file_loc = input("输入当前路径文件名覆盖局面，或者输入'Y'确认Memo.json文件覆盖: ")
        file_loc = MementoComponent.get_file_loc(file_loc)
        print("{0} 覆盖局面".format(file_loc))
        return file_loc

    @staticmethod
    def react_save_memento(flag):
        if flag:
            tkinter.messagebox.showinfo('提示', '文件保存成功')
        else:
            raise tkinter.messagebox.showinfo('提示', '文件保存错误')
        
    def react_cover_memento(flag):
        if flag:
            tkinter.messagebox.showinfo('提示', '文件读取成功')
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
        if self.color == PieceColor.BLACK:
            self.color = PieceColor.WHITE
        else:
            self.color = PieceColor.BLACK
        print("下一子:{0}".format(["BLACK", "WHITE"][self.color - 1]))

    def save_lastpool(self):
        self.last_pool[1] = self.last_pool[0]
        self.last_pool[0] = dict(PieceBoard.pool)

    def finish(self, finish_flag):
        self.status = False
        if finish_flag == PieceColor.BLACK or finish_flag == PieceColor.WHITE:
            self.winner = self.objs[finish_flag - 1]
        elif finish_flag == PieceColor.EVEN:
            self.even = True

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

    def memento(self, loc):
        self.origin = Originator(PieceBoard.pool, PieceBoard.size, self.type, self.color)

        caretaker = Caretaker(self.origin.creatMemento())
        state = self.origin.saveMemento(caretaker.memento, loc)
        return state, self

    def cover(self, loc):
        self.origin = Originator(PieceBoard.pool, PieceBoard.size, self.type, self.color)
        size, type, color, situ = self.origin.recoverMemento(loc)
        if size and color and situ:
            PieceBoard.size = size
            self.size = size
            self.type = type
            self.color = color
            PieceBoard(PieceBoard.size)
            PieceBoard.pool = situ
            self.initiate()
            return True, self
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


class Originator:
    def __init__(self, situ, size, type, color):
        self.state = dict()
        self.state.update({"Size":size, "Type":type, "Color":color})
        self.state.update(situ)

    def creatMemento(self):
        return Memento(self.state)

    def restoreMemento(self, memento):
        self.state = memento.getState()

    def saveMemento(self, memento, file_loc):
        try:
            self.restoreMemento(memento)
            with open(file_loc, mode='w') as f:
                state = json.dumps({str(k): self.state[k] for k in self.state})
                f.write(json.dumps(state))
            return True
        except Exception as e:
            return False

    def recoverMemento(self, file_loc):
        try:
            with open(file_loc, mode='r') as f:
                state = json.load(f)
                state = json.loads(state)
                state = {self._tuple(k): state[k] for k in state}

            self.state = state
            situ = {}
            for i, key in enumerate(list(self.state.keys())):
                if i >= 3:
                    situ.update({key:list(self.state.values())[i]})

            return self.state["Size"],self.state["Type"],self.state["Color"],situ
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





######### 代码运行示例 ########

game = front()
game.framinit()
