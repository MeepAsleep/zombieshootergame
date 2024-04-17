import pygame
import random
import math
from pygame import mixer

game_state = 1

# Intialize PyGame
pygame.init()

# Create Screen
screen: None = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('top-view.png')

# Background Music
mixer.music.load('Funny Zombie Invasion Theme Song.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Zombie Attack')
icon = pygame.image.load('hunter.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('gangster.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
num_of_enemies = 3

for i in range(100):
    enemyImg.append(pygame.image.load('zombie.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(-40)
    enemyY_change.append(0.1)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 5
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (0, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    restart_text = over_font.render("RESTART", True, (255, 255, 255))
    screen.blit(restart_text, (250, 400))
    screen.blit(over_text, (200, 250))
    game_state = 0



def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Backgroung Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke L or R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_DOWN:
                playerY_change = 1
            if event.key == pygame.K_UP:
                playerY_change = -1
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if game_state == 0 and event.key == pygame.K_SPACE:
                game_state = 1
                num_of_enemies = 3
                score_value = 0
                continue


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerX_change = 0
                playerY_change = 0
    # Boundary Check
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY <= 350:
        playerY = 350
    elif playerY >= 536:
        playerY = 536

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = -40
            if score_value%10 == 0:
                num_of_enemies+=1

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
