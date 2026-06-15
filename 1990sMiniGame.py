import pygame
import sys
import random
import time

pygame.init()

#Screen size

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1990s Archive Puzzle")

clock = pygame.time.Clock()

# colours

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)

#fonts 
font_title = pygame.font.SysFont("Arial", 40, bold=True)
font_text = pygame.font.SysFont("Courier", 24)