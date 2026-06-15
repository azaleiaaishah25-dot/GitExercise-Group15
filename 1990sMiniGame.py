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

# the puzzle grid and settings

GRID_SIZE = 3
IMAGE_SIZE = 600
TILE_SIZE = IMAGE_SIZE // GRID_SIZE

OFFSET_X = 200
OFFSET_Y = 120

# image loader

image = pygame.image.load("downloads/pearl_necklace.jpg").convert()
image = pygame.transform.scale(image, (IMAGE_SIZE, IMAGE_SIZE))

# Split image into pieces
tiles = []

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        tile = image.subsurface(
            pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
        ).copy()

        tiles.append(tile)

