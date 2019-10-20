import pygame.font


class Scoreboard():
    """显示得分的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备包含初始得分图像和最高得分的图像
        self.prep_score()
        self.prep_high_score()

    def prep_high_score(self):
        """将最高得分转换为渲染的图像, 并设置位置"""
        # 圆整high_score, 并添加千位分隔符
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        # 获取high_score的image
        self.high_score_image = pygame.font.SysFont(None, 48).render(high_score_str, True, self.text_color,
                                                                     self.ai_settings.bg_color)
        # 设置high_score的显示位置
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        """将得分转换为一幅渲染的图,并设置它的显示位置"""
        # score_str = str(self.stats.score)

        # 将分数圆整到10的倍数
        rounded_score = round(self.stats.score, -1)
        # 字符串格式设置指令
        score_str = "{:,}".format(rounded_score)

        self.score_image = pygame.font.SysFont(None, 48).render(score_str, True, self.text_color,
                                                                self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        # 显示当前得分
        self.screen.blit(self.score_image, self.score_rect)
        # 显示最高得分
        self.screen.blit(self.high_score_image, self.high_score_rect)
