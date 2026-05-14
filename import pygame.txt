import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (200, 200, 200)

# Game settings
FPS         = 60
PADDLE_W    = 12
PADDLE_H    = 90
BALL_SIZE    = 14
PADDLE_SPEED = 6
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

clock = pygame.time.Clock()
font_big   = pygame.font.SysFont("monospace", 72, bold=True)
font_small = pygame.font.SysFont("monospace", 28)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_W, PADDLE_H)

    def move(self, up_key, down_key, keys):
        if keys[up_key]   and self.rect.top    > 0:
            self.rect.y -= PADDLE_SPEED
        if keys[down_key] and self.rect.bottom < HEIGHT:
            self.rect.y += PADDLE_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=4)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect