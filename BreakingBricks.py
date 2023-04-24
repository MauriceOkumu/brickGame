import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Breaking bricks')

clock = pygame.time.Clock()
bat = pygame.image.load('./images/paddle.png')
bat = bat.convert_alpha()
bat_rect = bat.get_rect()
bat_rect[1] = screen.get_height() - 100

ball = pygame.image.load('./images/football.png')
ball = ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start = (200, 200)
ball_speed = (3.0, 3.0)

ball_rect.topleft = ball_start

brick = pygame.image.load('./images/brick.png')
brick = brick.convert_alpha()
brick_rect = brick.get_rect()


def break_bricks():
    sx, sy = ball_speed
    pos_x = 0
    ball_served = False
    bricks = []
    brick_rows = 5
    gap = 10
    brick_cols = screen.get_width() // (brick_rect[2] + gap)
    side_gap = (screen.get_width() - (brick_rect[2] + gap) * brick_cols + gap) // 2
    for y in range(brick_rows):
        brickY = y * (brick_rect[3] + gap)
        for x in range(brick_cols):
            brickX = x * (brick_rect[2] + gap) + side_gap
            bricks.append((brickX, brickY))
    game_over = False

    while not game_over:
        dt = clock.tick(50)
        screen.fill((0, 0, 0))

        for b in bricks:
            screen.blit(brick, b)

        screen.blit(bat, bat_rect)
        screen.blit(ball, ball_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            pos_x -= 0.5 * dt
        if pressed[K_RIGHT]:
            pos_x += 0.5 * dt
        if pressed[K_SPACE]:
            ball_served = True
        bat_rect[0] = pos_x

        # Ball hitting the bat
        if screen.get_width() >= ball_rect[0] >= bat_rect[0] and \
            ball_rect[1] >= bat_rect[1] - ball_rect.height and \
            sy > 0:
            sy *= -1
            continue
        # Top
        if ball_rect[1] <= 0:
            ball_rect[1] = 0
            sy *= -1
        # Bottom
        if ball_rect[1] >= screen.get_height() - ball_rect.height:
            ball_rect[1] = screen.get_height() - ball_rect.height
            sy *= -1
        # Left
        if ball_rect[0] <= 0:
            ball_rect[0] = 0
            sx *= -1
        # Right
        if ball_rect[0] >= screen.get_width() - ball_rect.width:
            ball_rect[0] = screen.get_width() - ball_rect.width
            sx *= -1
        if ball_served:
            ball_rect[0] += sx
            ball_rect[1] += sy

        pygame.display.update()

    pygame.quit()
