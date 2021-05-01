#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import math
import random
import sys

import pygame

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)

font = pygame.font.SysFont(None, 20)
font_s = pygame.font.SysFont(None, 40)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space invaders")
backround = pygame.image.load("BACKROUND2.gif")
backround_menu = pygame.image.load("BACKROUND2.gif")
backround_settings = pygame.image.load("BACKROUND2.gif")
backround_skins = pygame.image.load("BACKROUND2.gif")

icon = pygame.image.load("LOGO.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("PLAYER1.png")
playerX = 370
playerY = 500
playerX_change = 0
player_speed = 0.4

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load("ENEMY1.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.22)
    enemyY_change.append(40)

# bullet ready is bullet is invisible
# bullet fire is bullet is visible
bulletImg = pygame.image.load("BULLET1.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_State = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 70)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def player(x, y):
    win.blit(playerImg, (x, y))


def enemy(x, y, i):
    win.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_State
    bullet_State = "fire"
    win.blit(bulletImg, (x + 16, y + 10))


def isCollition(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


click = False


def main_menu():
    global click
    while True:

        screen.fill((0, 0, 0))
        draw_text('MAIN MENU', font, (255, 255, 255), screen, 320, 20)
        win.blit(backround_menu, (0, 0))
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(0, 100, 800, 50)  # x, y, longueur, largeur
        button_2 = pygame.Rect(0, 200, 800, 50)
        button_3 = pygame.Rect(0, 300, 800, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                skins()
        pygame.draw.rect(screen, (255, 255, 255), button_1)  # RGB
        pygame.draw.rect(screen, (255, 255, 255), button_2)
        pygame.draw.rect(screen, (255, 255, 255), button_3)
        draw_text('Play', font, (0, 0, 0), screen, 383, 110)
        draw_text('Settings', font, (0, 0, 0), screen, 352, 210)
        draw_text('Skins', font, (0, 0, 0), screen, 374, 310)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():
    global bullet_State
    global playerX
    global playerY
    global bulletY
    global playerX_change
    global bulletX
    global player_speed
    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            run = True
            while run:

                win.fill((10, 11, 10))
                win.blit(backround, (0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            playerX_change = player_speed * -1
                        if event.key == pygame.K_RIGHT:
                            playerX_change = player_speed
                        if event.key == pygame.K_SPACE:
                            if bullet_State == "ready":
                                bulletX = playerX
                                fire_bullet(bulletX, bulletY)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            playerX_change = 0

                playerX += playerX_change

                if playerX <= 0:
                    playerX = 0
                elif playerX >= 736:
                    playerX = 736

                for i in range(num_enemies):
                    global score_value
                    if enemyY[i] > 440:
                        for j in range(num_enemies):
                            enemyY[j] = 2000
                        game_over_text()
                        break
                    enemyX[i] += enemyX_change[i]
                    if enemyX[i] <= 0:
                        enemyX_change[i] = 0.22
                        enemyY[i] += enemyY_change[i]
                    elif enemyX[i] >= 736:
                        enemyX_change[i] = -0.22
                        enemyY[i] += enemyY_change[i]

                    collision = isCollition(enemyX[i], enemyY[i], bulletX, bulletY)
                    if collision:
                        bulletY = 480
                        bullet_State = "ready"
                        score_value += 1
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)

                    enemy(enemyX[i], enemyY[i], i)

                if bulletY <= 0:
                    bulletY = 480
                    bullet_State = "ready"

                if bullet_State == "fire":
                    fire_bullet(bulletX, bulletY)
                    bulletY -= bulletY_change

                player(playerX, playerY)
                show_score(textX, textY)
                pygame.display.update()

        pygame.display.update()
        mainClock.tick(60)


def skins():
    running = True
    while running:
        screen.fill((0, 0, 0))
        win.blit(backround_skins, (0, 0))

        draw_text('SKINS', font, (255, 255, 255), screen, 360, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def four():
    global num_enemies
    num_enemies = 4


def five():
    global num_enemies
    num_enemies = 5


def six():
    global num_enemies
    num_enemies = 6


def seven():
    global num_enemies
    num_enemies = 7


def eight():
    global num_enemies
    num_enemies = 8


def speed1():
    global player_speed
    player_speed = 0.2


def speed2():
    global player_speed
    player_speed = 0.4


def speed3():
    global player_speed
    player_speed = 0.6


def bullet_slow():
    global bulletY_change
    bulletY_change = 0.5


def bullet_normal():
    global bulletY_change
    bulletY_change = 0.8


def bullet_fast():
    global bulletY_change
    bulletY_change = 2


def bullet_sup_fast():
    global bulletY_change
    bulletY_change = 6.5


def options():
    running = True
    global click
    while running:
        screen.fill((0, 0, 0))
        win.blit(backround_settings, (0, 0))

        nx, ny = pygame.mouse.get_pos()

        button_4 = pygame.Rect(30, 120, 80, 50)  # x, y, longueur, largeur
        button_5 = pygame.Rect(130, 120, 80, 50)
        button_6 = pygame.Rect(230, 120, 80, 50)
        button_7 = pygame.Rect(330, 120, 80, 50)
        button_8 = pygame.Rect(430, 120, 80, 50)
        button_speed1 = pygame.Rect(30, 250, 150, 50)
        button_speed2 = pygame.Rect(200, 250, 150, 50)
        button_speed3 = pygame.Rect(370, 250, 150, 50)
        button_slow = pygame.Rect(30, 380, 100, 50)
        button_normal = pygame.Rect(150, 380, 100, 50)
        button_fast = pygame.Rect(270, 380, 100, 50)
        button_sup_fast = pygame.Rect(390, 380, 100, 50)
        if button_4.collidepoint((nx, ny)):
            if click:
                four()
        if button_5.collidepoint((nx, ny)):
            if click:
                five()
        if button_6.collidepoint((nx, ny)):
            if click:
                six()
        if button_7.collidepoint((nx, ny)):
            if click:
                seven()
        if button_8.collidepoint((nx, ny)):
            if click:
                eight()
        if button_speed1.collidepoint((nx, ny)):
            if click:
                speed1()
        if button_speed2.collidepoint((nx, ny)):
            if click:
                speed2()
        if button_speed3.collidepoint((nx, ny)):
            if click:
                speed3()
        if button_slow.collidepoint((nx, ny)):
            if click:
                bullet_slow()
        if button_normal.collidepoint((nx, ny)):
            if click:
                bullet_normal()
        if button_fast.collidepoint((nx, ny)):
            if click:
                bullet_fast()
        if button_sup_fast.collidepoint((nx, ny)):
            if click:
                bullet_sup_fast()
        pygame.draw.rect(screen, (255, 255, 255), button_4)  # RGB
        pygame.draw.rect(screen, (255, 255, 255), button_5)
        pygame.draw.rect(screen, (255, 255, 255), button_6)
        pygame.draw.rect(screen, (255, 255, 255), button_7)
        pygame.draw.rect(screen, (255, 255, 255), button_8)
        pygame.draw.rect(screen, (255, 255, 255), button_speed1)
        pygame.draw.rect(screen, (255, 255, 255), button_speed2)
        pygame.draw.rect(screen, (255, 255, 255), button_speed3)
        pygame.draw.rect(screen, (255, 255, 255), button_slow)
        pygame.draw.rect(screen, (255, 255, 255), button_normal)
        pygame.draw.rect(screen, (255, 255, 255), button_fast)
        pygame.draw.rect(screen, (255, 255, 255), button_sup_fast)

        draw_text('4', font, (0, 0, 0), screen, 60, 130)
        draw_text('5', font, (0, 0, 0), screen, 160, 130)
        draw_text('6', font, (0, 0, 0), screen, 260, 130)
        draw_text('7', font, (0, 0, 0), screen, 360, 130)
        draw_text('8', font, (0, 0, 0), screen, 460, 130)
        draw_text('Slow', font, (0, 0, 0), screen, 60, 260)
        draw_text('Medium', font, (0, 0, 0), screen, 210, 260)
        draw_text('Fast', font, (0, 0, 0), screen, 410, 260)
        draw_text('Slow', font, (0, 0, 0), screen, 60, 330)
        draw_text('Medium', font, (0, 0, 0), screen, 210, 330)
        draw_text('Fast', font, (0, 0, 0), screen, 410, 330)
        draw_text('Sup.Fast', font, (0, 0, 0), screen, 460, 370)

        draw_text('Enemy Quantity :', font_s, (255, 255, 255), screen, 30, 80)
        draw_text('Player Speed :', font_s, (255, 255, 255), screen, 30, 210)
        draw_text('SETTINGS', font, (255, 255, 255), screen, 330, 20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)


main_menu()
