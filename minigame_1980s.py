import pygame
import random
import time

 def run_minigame(screen, clock):
    WIDTH, HEIGHT = screen.get_size()

    # Colors
    RED = (200, 50, 50)
    GREEN = (50, 200, 50)
    BLUE = (50, 50, 200)
    YELLOW = (220, 220, 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK = (15, 15, 25)
    GOLD = (255, 220, 120)

    colors = [RED, GREEN, BLUE, YELLOW]
    color_names = ["RED", "GREEN", "BLUE", "YELLOW"]

    # Fonts
    title_font = pygame.font.SysFont(None, 70)
    medium_font = pygame.font.SysFont(None, 42)
    small_font = pygame.font.SysFont(None, 30)