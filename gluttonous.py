# -*- coding: utf-8 -*-

import cocos
import pygame
import os
import define
from arena import Arena
from gameover import Gameover
import button
import pygame_menu
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gluttonous Python')

# 加载背景图片
background_image = pygame.image.load("background_image.png")
background_image = pygame.transform.scale(background_image, (800,600))

game_paused = False
menu_state = "main"
#定义字体
font = pygame.font.SysFont("SimHei",40)
TEXT_COLOR = (255,255,255)
surface = pygame.display.set_mode((800, 600))
my_theme = pygame_menu.themes.Theme(
    background_color=(0, 0, 0, 0),  # 设置背景颜色
    title_background_color=(0, 0, 0,0),  # 设置标题背景颜色
    title_font_size=50,
    widget_font=font,  # 设置字体
    widget_font_size=30,
    widget_font_color=(255, 255, 255),
    widget_background_color=(0, 0, 0, 180),  # 半透明黑底框
)


class HelloWorld(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.arena = Arena()
        self.add(self.arena)
        self.score = cocos.text.Label('30',
                                      font_name='Times New Roman',
                                      font_size=24,
                                      color=define.GOLD)
        self.score.position = 20, 440
        self.add(self.score, 99999)

        self.gameover = Gameover()
        self.add(self.gameover, 100000)

        self.music()  # 在初始化时调用音乐

    def update_score(self):
        self.score.element.text = str(self.arena.snake.score)

    def end_game(self):
        self.gameover.visible = True
        self.gameover.score.element.text = str(self.arena.snake.score)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena()
            self.add(self.arena)
            self.update_score()

    def music(self):
        pygame.mixer.init()  # 初始化 Pygame 音频系统
        pygame.mixer.music.load(os.path.join( 'music.mp3'))
        pygame.mixer.music.play(-1)

    def set_volume(value):
        pygame.mixer.music.set_volume(value / 100)  # pygame 的音量值范围是 0.0 到 1.0

# 设置菜单功能
def start_the_game():
    print("游戏开始！")
    pygame.quit()  # 退出主菜单窗口
    cocos.director.director.init(caption="Gluttonous Python")
    cocos.director.director.run(cocos.scene.Scene(HelloWorld()))

def set_volume(value):
    pygame.mixer.music.set_volume(value / 100)  # pygame 的音量值范围是 0.0 到 1.0
# 创建“设置”菜单
settings_menu = pygame_menu.Menu('setting', 800, 600, theme=my_theme)
settings_menu.add.range_slider('音乐音量', default=50, range_values=(0, 100), increment=10, onchange=set_volume)
settings_menu.add.button('返回主菜单', pygame_menu.events.BACK)

# 创建菜单
main_menu = pygame_menu.Menu('', 800, 600,
                        theme=my_theme)

# 添加按钮（调用开始游戏函数）
main_menu.add.button('开始游戏', start_the_game)
main_menu.add.button('  设置  ', settings_menu)  # 这里设置按钮打开设置菜单
main_menu.add.button('  退出  ', pygame_menu.events.EXIT)

# 游戏主循环
running = True
while running:
    # 处理事件
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    surface.blit(background_image, (0, 0))
    # 显示菜单
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(surface)

    # 更新屏幕
    pygame.display.flip()


# 退出 pygame
pygame.quit()






