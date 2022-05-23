import pygame

class Settings():
    # Клас для зберігання усіх налаштувань гри

    def __init__(self):
        # Ініціалізація налаштувань гри
        # Параметри екрану

        self.screen_width = 640
        self.screen_height = 480
        self.background_image = pygame.image.load('Python\Alien_Invasion\img\Sky_stars.bmp')
        self.ship_limit = 3

        # Параметри пулі
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 6

        # Параметри прибульців
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 0.4
        self.alien_speed_factor = 0.3
        # fleet_direction = 1 вправо, -1 вліво
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)