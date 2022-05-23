import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        # Ініціалізація корабля та його початкове положення
        super().__init__()
        
        self.screen = screen
        self.ai_settings = ai_settings

        # Завантаження зображення корабля та отримання прямокутника
        self.image = pygame.image.load('Python\Alien_Invasion\img\Ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Кожен новий корабель з'являється з краю екрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        # Оновлює позицію корабля з урахування флагу
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
    
    def blitme(self):
        # Малює корабель в поточній позиції
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx