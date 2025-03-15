import pygame
from pygame.locals import *
import sys

pygame.init()
frame_size_x = 900
frame_size_y = 500

FPS = 60
velocity = 5
ship_width = 55
ship_height = 40
max_num_of_bullet = 5
bullet_velocity = 7

window_screen = pygame.display.set_mode((frame_size_x,frame_size_y))

pygame.display.set_caption("Space Shooter")

white = (255, 255, 255)  # RGB Code for White
black = (0, 0, 0)  # RGB Code for Black
green = (110, 194, 54)  # RGB Code for Green Bullet
blue = (23, 54, 235)  # RGB Code for Blue Bullet

border = pygame.Rect((frame_size_x // 2) - 5, 0, 10, frame_size_y)

background = pygame.transform.scale(pygame.image.load('gallery/sprites/background.png'),(frame_size_x, frame_size_y)).convert()
space_shooter_logo = pygame.image.load('gallery/sprites/space_shooter.png').convert_alpha()

space_shooter_logo = pygame.transform.scale(space_shooter_logo,(300,150))

green_ship_img = pygame.transform.rotate(pygame.image.load('gallery/sprites/shipGreen.png'), 270)
blue_ship_img = pygame.transform.rotate(pygame.image.load('gallery/sprites/shipBlue.png'), 90)
green_ship = pygame.transform.scale(green_ship_img, (ship_width, ship_height)).convert_alpha()
blue_ship = pygame.transform.scale(blue_ship_img, (ship_width, ship_height)).convert_alpha()

bullet_fire_sound = pygame.mixer.Sound('gallery/audio/sfx_fire.ogg')

def handle_bullets(green_bullets, blue_bullets, green, blue):
    for bullet in green_bullets:
        bullet.x += bullet_velocity
        if blue.colliderect(bullet):
            green_bullets.remove(bullet)
        elif bullet.x > frame_size_x:
            green_bullets.remove(bullet)
    for bullet in blue_bullets:
        bullet.x -= bullet_velocity
        if green.colliderect(bullet):
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)

def green_movement_handler(keys_pressed, green):
    if keys_pressed[pygame.K_w] and green.y - velocity > 0:  #UP
        green.y -= velocity
    if keys_pressed[pygame.K_a] and green.x - velocity > -5:  #LEFT
        green.x -= velocity
    if keys_pressed[pygame.K_s] and green.y - velocity + green.height < frame_size_y - 5:  #DOWN
        green.y += velocity   
    if keys_pressed[pygame.K_d] and green.x - velocity + green.width < border.x - 5:  #RIGHT
        green.x += velocity

def draw_window(green_rect, blue_rect, green_bullets, blue_bullets):
    window_screen.blit(background, (0, 0)) #blit the background
    pygame.draw.rect(window_screen, black, border)
    window_screen.blit(green_ship, (green_rect.x, green_rect.y))
    window_screen.blit(blue_ship, (blue_rect.x, blue_rect.y))
    for bullet in green_bullets:
        pygame.draw.rect(window_screen, green, bullet)  #green bullets
    for bullet in blue_bullets:
        pygame.draw.rect(window_screen, blue, bullet)  #blue bullets
    pygame.display.update()  #Update Screen

def main():
    clock = pygame.time.Clock()
    green_rect = pygame.Rect(100, 100, ship_width, ship_height)
    blue_rect = pygame.Rect(700, 300, ship_width, ship_height)
    green_bullets = []
    blue_bullets = []
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets)< max_num_of_bullet:
                    bullet = pygame.Rect(green_rect.x + green_rect.width, green_rect.y + green_rect.height // 2, 10, 5)
                    green_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_RCTRL and len(blue_bullets)<max_num_of_bullet:
                    bullet = pygame.Rect(blue_rect.x, blue_rect.y + blue_rect.height // 2,  10, 5)
                    blue_bullets.append(bullet)
                    bullet_fire_sound.play()

        print(green_bullets, blue_bullets)
        keys_pressed = pygame.key.get_pressed()
        print(keys_pressed[pygame.K_LEFT], keys_pressed[pygame.K_RIGHT])
        green_movement_handler(keys_pressed, green_rect)
        handle_bullets(green_bullets, blue_bullets, green_rect, blue_rect)
        draw_window(green_rect, blue_rect, green_bullets, blue_bullets)
#------------------------ add code above ------------------------

def welcome_screen():
    while True:
        window_screen.blit(background, (0, 0))
        window_screen.blit(space_shooter_logo, (frame_size_x//3, 40))
        welcome_font = pygame.font.SysFont("impact", 24)
        welcome_text = welcome_font.render("Press Any Key To Begin...", 1, white)
        window_screen.blit(welcome_text, (frame_size_x // 2 - welcome_text.get_width() //2, frame_size_y // 2 - welcome_text.get_height() // 2))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print("Start the game")
                main()
        pygame.display.update()

welcome_screen()