import pygame
import sys
import random

# Initializing Setup
pygame.init()
clock = pygame.time.Clock()

# Setting Game Window
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colours
background_colour = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Setting Player and Opponent
player_width = int(screen_width * 0.01)
player_height = int(screen_height * 0.125)
player_x_pos = int(screen_width * 0.05)
opponent_x_pos = int(screen_width * 0.95)
both_y_pos = int(screen_height-player_height)/2

# Game Variables
velocity = 7
player_speed = 0
opponent_speed = velocity
ball_radius = player_height * 0.2
ball_x_pos = (screen_width-ball_radius)/2
ball_y_pos = (screen_height-ball_radius)/2
ball_x_speed = velocity * random.choice((1, -1))
ball_y_speed = velocity * random.choice((1, -1))

# Defining Game Objects
player = pygame.Rect(player_x_pos, both_y_pos, player_width, player_height)
opponent = pygame.Rect(opponent_x_pos, both_y_pos, player_width, player_height)
ball = pygame.Rect(ball_x_pos, ball_y_pos, ball_radius, ball_radius)


def ball_animation():
    global ball_x_speed, ball_y_speed

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_y_speed *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_start()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_x_speed *= -1


def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_start():
    global ball_x_speed, ball_y_speed

    ball.center = (ball_x_pos, ball_y_pos)
    ball_x_speed *= random.choice((1, -1))
    ball_y_speed *= random.choice((1, -1))


while True:
    # Handling Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += velocity
            if event.key == pygame.K_UP:
                player_speed -= velocity
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += velocity
            if event.key == pygame.K_DOWN:
                player_speed -= velocity

    # Game Logic
    ball_animation()
    player_animation()
    opponent_animation()

    # Drawing Game Objects
    screen.fill(background_colour)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    # Updating Screen
    pygame.display.flip()
    clock.tick(60)