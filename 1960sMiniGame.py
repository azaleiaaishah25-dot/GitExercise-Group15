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