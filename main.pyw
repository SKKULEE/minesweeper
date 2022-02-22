import pygame as pg
from random import choice
from tkinter import messagebox, Tk
import os
from sys import exit

#파이게임 초기화
pg.init()
#tkinter 설정
Tk().wm_withdraw()



#For Compiling
def resource_path(relative_path):
    try:
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



#기본 변수
board_size = 16
cell_size = 24
partition_size = 2

CAPTION = "minesweeper"
ICON = pg.image.load(resource_path("image/mine.png"))
WIDTH = (cell_size + partition_size) * board_size + partition_size
HEIGHT = WIDTH + 36 #tab_size
FPS = 30
CELL_FONT = pg.font.SysFont("arial", 20, True, False)
SYS_FONT = pg.font.SysFont("arial", 26, True, False)

#창 설정
WINDOW = pg.display
WINDOW.set_caption(CAPTION)
WINDOW.set_icon(ICON)
SCREEN = WINDOW.set_mode((WIDTH, HEIGHT))
pg.time.Clock().tick(FPS)

#기본 색
BLACK   = (  0,   0,   0)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)
MAGENTA = (255,   0, 255)
CYAN    = (  0, 255, 255)
WHITE   = (255, 255, 255)

#확장 색
DARK_GRAY = (127, 127, 127)
LIGHT_GRAY = (195, 195, 195)
LIGHT_BLUE = (127, 127, 255)
LIGHT_GREEN = (124, 218, 124)
BROWN = (155, 103, 60)
VIOLET = (102, 0, 161)
ORANGE = (255, 165, 0)



#전역 변수
max_mine = 40
num_color = [LIGHT_GRAY, LIGHT_BLUE, LIGHT_GREEN, RED, BLUE, BROWN, GREEN, VIOLET, ORANGE]
mine_image = pg.transform.scale(pg.image.load(resource_path("image/mine.png")), [cell_size, cell_size])
flag_image = pg.transform.scale(pg.image.load(resource_path("image/flag.png")), [cell_size, cell_size])
not_mine_image = pg.transform.scale(pg.image.load(resource_path("image/not_mine.png")), [cell_size, cell_size])
tab_size = 36
vic = False
dft = False



#클래스
class board:
    def __init__(self):
        self.content = [[cell(self, i, j) for i in range(board_size)] for j in range(board_size)]
        self.mine_left = max_mine

    def init(self):
        self.random_mine_generate(max_mine)

    def random_mine_generate(self, n):
        mine_layed = 0
        while mine_layed < max_mine:
            picked = choice(choice(self.content))
            if picked.has_mine:
                continue
            if not picked.is_sealed:
                continue
            picked.set_mine()
            mine_layed += 1
        self.cell_content_init()

    def cell_content_init(self):
        for i in range(board_size):
            for j in range(board_size):
                self.content[j][i].content = 0
                for k in range(-1, 2):
                    for m in range(-1, 2):
                        if 0 <= j+k < board_size and 0 <= i+m < board_size and self.content[j+k][i+m].has_mine:
                            self.content[j][i].content += 1

    def render(self):
        txt = SYS_FONT.render("Mine Left: %d" % self.mine_left, True, BLACK)
        SCREEN.blit(txt, [5, 5])
        for i in self.content:
            for j in i:
                j.render()

class cell:
    def __init__(self, master_board, x, y):
        self.has_mine = False
        self.is_sealed = True
        self.is_flaged = False
        self.boss = master_board
        self.x = x
        self.y = y
        self.content = None

    def set_mine(self):
        self.has_mine = True

    def open(self):
        if self.is_sealed == False or self.is_flaged:
            return
        self.is_sealed = False
        if self.has_mine:
            defeat()
        elif self.content == None:
            self.boss.init()
            if self.content == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= self.y+i < board_size and 0<= self.x+j < board_size:
                            self.boss.content[self.y+i][self.x+j].open()
        elif self.content == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= self.x+j < board_size and 0 <= self.y+i < board_size:
                        self.boss.content[self.y+i][self.x+j].open()

    def set_flag(self):
        self.is_flaged = True
        self.boss.mine_left -= 1

    def deflag(self):
        self.is_flaged = False
        self.boss.mine_left += 1

    def render(self):
        xp = partition_size + (cell_size + partition_size) * self.x
        yp = partition_size + (cell_size + partition_size) * self.y + tab_size
        xl = yl = cell_size

        if not self.is_sealed:
            if not self.has_mine:
                pg.draw.rect(SCREEN, WHITE, [xp, yp, xl, yl])
                if self.content != None and self.content != 0:
                    txt = CELL_FONT.render(str(self.content), True, num_color[self.content])
                    rect = txt.get_rect()
                    rect.center = (xp + xl/2, yp + yl/2)
                    SCREEN.blit(txt, rect)
            else:
                pg.draw.rect(SCREEN, LIGHT_GRAY, [xp, yp, xl, yl])
                SCREEN.blit(mine_image, [xp, yp])
        else:
            pg.draw.rect(SCREEN, LIGHT_GRAY, [xp, yp, xl, yl])
            if self.is_flaged:
                if not self.has_mine and dft != False:
                    SCREEN.blit(not_mine_image, [xp, yp])
                else:
                    SCREEN.blit(flag_image, [xp, yp])




#함수
def fill_background():
    SCREEN.fill(DARK_GRAY)

def mouse_position():
    return pg.mouse.get_pos()

def is_LMBdown_event(e):
    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
        return True
    return False

def is_LMB_able(b):
     if b != None and b.is_sealed and not b.is_flaged:
         return True
     return False

def is_RMBdown_event(e):
    if e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
        return True
    return False

def is_RMB_able(b):
     if b != None and b.is_sealed:
         return True
     return False

def button_with_cursor():
    mp = list(mouse_position())
    mp[0], mp[1] = mp[1] - 36, mp[0] #tab_size subtraction
    if partition_size <= mp[0] % (cell_size + partition_size) and partition_size <= mp[1] % (cell_size + partition_size):
        if (cell_size + partition_size) * board_size <= mp[0] or (cell_size + partition_size) * board_size <= mp[0] <= mp[1]:
            return None
        return game_board.content[mp[0] // (cell_size + partition_size)][mp[1] // (cell_size + partition_size)]
    else:
        return None

def defeat():
    global game_board, dft
    for i in game_board.content:
        for j in i:
            if j.has_mine:
                j.is_sealed = False
    dft = True

def all_found():
    num = 0
    for i in game_board.content:
        for j in i:
            if not j.is_sealed or j.has_mine:
                num += 1
    if num == board_size ** 2:
        return True
    return False

def victory():
    global vic
    vic = True



#게임 초기화
game_board = board()



#실행부
RUNNING = True
while RUNNING:
    fill_background()
    game_board.render()

    if vic == True:
        if messagebox.askretrycancel("Game Over!", "Victory! ^.^\nRetry?"):
            game_board = board()
            vic = False
        else:
            exit(0)

    elif dft == True: #왜 이렇게 되지?
        dft = 2

    elif dft == 2:
        if messagebox.askretrycancel("Game Over!", "You Step On A Mine... T.T\nRetry?"):
            game_board = board()
            dft = False
        else:
            exit(0)

    if all_found():
        victory()

    WINDOW.update()

    for event in pg.event.get():
        if is_LMBdown_event(event):
            current_button = button_with_cursor()
            if is_LMB_able(current_button):
               current_button.open()
        elif is_RMBdown_event(event):
            current_button = button_with_cursor()
            if is_RMB_able(current_button):
               if current_button.is_flaged:
                   current_button.deflag()
               else:
                   current_button.set_flag()
        elif event.type == pg.QUIT:
            if messagebox.askyesno("Exit?", "You Really Want To Quit?"):
                pg.display.quit()
                RUNNING = False