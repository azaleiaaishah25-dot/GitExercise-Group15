import pygame
import random 
import sys
 
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colours for the game

BLACK          = (10, 10, 12)
WHITE          = (255, 255, 255)
MOD_ORANGE     = (242, 100, 25)
MUSTARD_YELLOW = (246, 190, 0)
CHERRY_RED     = (213, 0, 50)
CULTURE_BLACK  = (20, 20, 20)

#fonts
font_tittle =pygame.font.SysFont('Arial', 60)
font_bold = pygame.font.SysFont("courier", 22, bold=True)
font_text = pygame.font.SysFont("courier", 18)

# The game variables
score = 0
grid_timer = 0
color_flip_rate = 90