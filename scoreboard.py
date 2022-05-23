import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoredboard():
    # Клас для виводу ігрової інформації
    def __init__(self, ai_settings, screen, stats):
        #
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Налаштування шрифту для виводу рахунку
        self.text_color = (150, 150, 150)
        self.font = pygame.font.SysFont(None, 24)
        # Підготовка вихідного зображення
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        # Вивід кількості житів
        self.prep_ships()

    def prep_level(self):
        #
        self.level_image = self.font.render(f"Level {self.stats.level}", True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.top
        # self.level_rect.left = 50

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            if ship_number == 0:
                self.level_rect.left = ship.rect.width + 10
            else:    
                self.level_rect.left = (ship_number + 1.5) * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        # Перетворення поточного рахунку в графічне зображення
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        # Вивід рахунку в правому верхньому куті
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_high_score(self):
        #
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        # Вивід рахунку по центру зверху
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        # Вивід на екран
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
