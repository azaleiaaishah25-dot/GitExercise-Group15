import pygame
import random
import time

pygame.init()

# Screen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon Says - 1980s Security Panel")

# Colors
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (200, 200, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [RED, GREEN, BLUE, YELLOW]

# Button positions
buttons = [
    pygame.Rect(100, 100, 180, 180),  # red
    pygame.Rect(320, 100, 180, 180),  # green
    pygame.Rect(100, 320, 180, 180),  # blue
    pygame.Rect(320, 320, 180, 180),  # yellow
]