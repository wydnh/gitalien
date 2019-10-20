import pygame

from settings import Settings

from game_stats import GameStats

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from button import Button

from scoreboard import Scoreboard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    # 创建一个外星人编组
    aliens = Group()
    # 创建一个外星人的群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建 Play 按钮
    play_button = Button(ai_settings, screen, 'Play')

    # 创建一个记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb)

        if stats.game_active:
            # 根据移动标志调整飞船的位置
            ship.update()

            # 更新子弹位置,并删除已消失的子弹
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # 更新外星人的位置
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        # 更新屏幕上的图像,并切换到新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
