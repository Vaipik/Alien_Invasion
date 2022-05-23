from turtle import Screen, screensize
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # Створює об'єкт пулі в поточній позиції корабля
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Створення пулі в позиції 0, 0 та визначення правильної позиції
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Позиця пулі у плавающій точці
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # Переміщення пулі вверх по екрану
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        # Вивід пулі на екран
        pygame.draw.rect(self.screen, self.color, self.rect)