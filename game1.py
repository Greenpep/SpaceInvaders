import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
big_background = pygame.image.load("background.png")
background = pygame.transform.scale(big_background, (800, 600))

# Background sound
mixer.music.load("background_sound.mp3")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
big_enemyIMG = pygame.image.load("enemy.png")
'''
enemyIMG = pygame.transform.scale(big_enemyIMG, (64, 64))
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemyX_change = 0.3
enemyY_change = 40
'''

enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 9

for i in range(num_of_enemies):
    enemyIMG.append(pygame.transform.scale(big_enemyIMG, (64, 64)))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

text_x = 10
text_y = 10

# Game Over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(((enemy_x - bullet_x) ** 2) + ((enemy_y - bullet_y) ** 2))
    if distance < 30:
        return True
    else:
        return False


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


# Game Loop
running = True
while running:

    # RBG
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.5
            if event.key == pygame.K_d:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound("bullet_sound.mp3")
                bullet_sound.play()
                # get the current x coordinate of the spaceship and save it as bulletX
                bulletX = playerX
                fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and playerX_change > 0:
                playerX_change = 0.5
            elif event.key == pygame.K_d and playerX_change < 0:
                playerX_change = -0.5
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # Player boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_sound = mixer.Sound("explosion_sound.mp3")
            explosion_sound.play()
            # bullet
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            # enemy
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(text_x, text_y)
    pygame.display.update()
