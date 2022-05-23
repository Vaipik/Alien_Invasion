import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoredboard

def run_game():
    # Ініціалізація гри та створення об'єкту екрана
    pygame.init()
    ai_settings = Settings()
    screen  = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) 
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    ship = Ship(ai_settings, screen)
    stats = GameStats(ai_settings)
    sb = Scoredboard(ai_settings, screen, stats)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen,ship, aliens)

    # Запуск основного циклу гри
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:    
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()