import sys

from time import sleep

import pygame

from bullet import Bullet

from alien import Alien


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果没有达到子弹数量限制就创建一颗子弹,并将其加入到编组bullets中"""
    # 创建新子弹, 并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
    for event in pygame.event.get():
        """响应按键和鼠标事件"""
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
    """在玩家点击 Play 按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏统计信息
        stats.reset_stats()

        sb.prep_score()

        stats.game_active = True

        # 重置游戏速度设置
        ai_settings.initialize_dynamic_settings()

        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人, 并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 隐藏光标
        pygame.mouse.set_visible(False)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像,并切换到新屏幕"""
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船
    ship.blitme()

    # 绘制外星人群
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态, 就绘制 Play 按钮
    # if not 如果非 (和 stats.game_active 的值 相反, stats.game_active为false, 则 not stats.game_active 为 True,
    # 则执行冒号后面的代码)
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置,并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    # 检查是否有子弹击中了敌人
    # 如果是这样, 就删除相应的子弹和外星人, 并计算得分
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹击中了敌人
    # 如果是这样, 就删除相应的子弹和外星人, 返回一个字典, 子弹为键, 外星人列表为值
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # 如果 collisions非空, 更新得分
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            # 准备最新分数的image
            sb.prep_score()
        # 如果 collisions非空, 检查最高分
        check_high_score(stats, sb)

    # 如果外星人都被消灭了, 删除现有的子弹,并创建一个新的外星人群,并提高游戏速度
    if len(aliens) == 0:
        # 删除现有的子弹
        bullets.empty()
        # 提高速度设置
        ai_settings.increase_speed()
        # 新建一群外星人
        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """检查是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        # 更新最高分的image
        sb.prep_high_score()


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ship_height)
    number_cows = int(available_space_y / (2 * alien_height))
    return number_cows


def create_alien(ai_settings, screen, aliens, alien_number, cow_number):
    """创建一个外星人并将其放在当前行和编组aliens里"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * cow_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人,并计算一行可以容纳多少外星人,可以容纳多少行
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_cows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人
    for cow_number in range(number_cows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, cow_number)


def check_fleet_edges(ai_settings, aliens):
    """如果有外星人到达边缘是采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移, 并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将ship_left 减 1
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人,并将飞船放到屏幕底部
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘, 并更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)

    aliens.update()

    # 检查外星人和飞船是否发生了碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("ship hit!!!")
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # 检查是否有外星人到达了屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
