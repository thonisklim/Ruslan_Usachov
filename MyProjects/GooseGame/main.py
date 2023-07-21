import pygame
import os
import random as r

pygame.init()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Oswald', 30)
bg = pygame.transform.scale(pygame.image.load("img/background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 5

PLAYER_IMAGES = os.listdir("img/Goose")
ENEMY_COLOR = (255, 0, 0)
BONUS_COLOR = (0, 255, 0)
FONT_COLOR = (0, 0, 0)
FPS = pygame.time.Clock()

game_display = pygame.display.set_mode((WIDTH, HEIGHT))

img_index = 0
player = pygame.image.load("img/player.png").convert_alpha()
player_rect = player.get_rect()
player_rect.move_ip((WIDTH / 10, HEIGHT / 2))
g_speed = 5
v_speed = 5
score = 0
high_score = 0

enemies = []
bonuses = []


def create_enemy():
    enemy_size = (40, 20)
    enemy = pygame.transform.scale(pygame.image.load("img/enemy.png"), enemy_size)
    enemy_rect = pygame.Rect(WIDTH, r.randint(50, HEIGHT - 50), *enemy_size)
    enemy_move = [r.randint(-15, -3), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (60, 80)
    bonus = pygame.transform.scale(pygame.image.load("img/bonus.png"), bonus_size)
    bonus_rect = pygame.Rect(r.randint(100, WIDTH - 100), -100, *bonus_size)
    bonus_move = [0, 2]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1400)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2400)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 180)
playing = True
while playing:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join("img/Goose/", PLAYER_IMAGES[img_index])).convert_alpha()
            img_index += 1
            if img_index == len(PLAYER_IMAGES):
                img_index = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and player_rect.right < WIDTH:
        player_rect.move_ip(g_speed, 0)
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.move_ip(-g_speed, 0)
    if keys[pygame.K_s] and player_rect.bottom < HEIGHT:
        player_rect.move_ip(0, v_speed)
    if keys[pygame.K_w] and player_rect.top > 0:
        player_rect.move_ip(0, -v_speed)

    bg_X1 -= bg_move
    bg_X2 -= bg_move
    if bg_X1 <= -bg.get_width():
        bg_X1 = bg.get_width()
    elif bg_X2 <= -bg.get_width():
        bg_X2 = bg.get_width()
    game_display.blit(bg, (bg_X1, 0))
    game_display.blit(bg, (bg_X2, 0))


    # if player_rect.bottom > HEIGHT or player_rect.top < 0:
    #     player_speed = [player_speed[0], player_speed[1] * (-1)]
    # elif player_rect.right > WIDTH or player_rect.left < 0:
    #     player_speed = [player_speed[0] * (-1), player_speed[1]]
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        game_display.blit(enemy[0], enemy[1])
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
        if player_rect.colliderect(enemy[1]):
            if score > high_score:
                high_score = score
            playing = False
            print(high_score)

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        game_display.blit(bonus[0], bonus[1])
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
    game_display.blit(player, player_rect)
    game_display.blit(FONT.render(f"{score}", True, FONT_COLOR), (WIDTH - 100, 10))
    pygame.display.flip()
