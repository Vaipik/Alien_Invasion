import sys
from types import TracebackType
from xmlrpc.client import Boolean
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # Реагує на натискання клавіш
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()        

def check_keyup_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Реагує на відпускання клавіш
     
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Запуск гри
    if not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        pygame.mouse.set_visible(False)

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)    

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Обробляє натискання клавіш та миші
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
                
def get_number_aliens_x(ai_settings, alien_width):
    # Вираховує кількість прибульців в рядку
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    # Вираховує кількість рядків
    avaliable_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return int(number_rows / 2)

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Створює прибульця та розміщує його в рядку
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # Створення флоту прибульців
    # Створення прибульця та вираховування кількості в одному ряду
    # Інтервал між прибульця становить одного прибульця

    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Створення першого ряду
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    # Досягнення межі края екрану
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    # Знижує флот та змінює його напрямок
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Обробляє зіткнення 
    if stats.ships_left > 0:
        # Зменшення кількості життів
        stats.ships_left -= 1
        sb.prep_ships()
        # Очищення списків
        aliens.empty()
        bullets.empty()
        # Створення нового флоту
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Пауза
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # Перевіряє чи досяг флот краю екрана і після оновлює позиції
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Перевірка колізії прибулець-корабель
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    #
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Перевірка влучання у прибульця
    # При влучані видаляє прибульця і пулю
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        sb.prep_ships()
        create_fleet(ai_settings, screen, ship, aliens)
        
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Оновлює зображення на екрані та відображає новий екран
    screen.blit(ai_settings.background_image, (0, 0))
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    # Відображення останнього екрана
    pygame.display.flip()