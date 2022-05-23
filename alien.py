import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # Клас, що представляє одного прибульця

    def __init__(self, ai_settings, screen):
        # Ініціалізує прибульця та задає його початкове положення
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Завантаження зображення прибульця
        self.image = pygame.image.load('Python\Alien_Invasion\img\Alien_ship.bmp')
        self.rect = self.image.get_rect()

        # Кожен новий прибулець в лівому верхньому куті екрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Збереження поточної позиції прибульця
        self.x = float(self.rect.x)
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        # Виводить прибульця в поточному положені
        self.screen.blit(self.image, self.rect)