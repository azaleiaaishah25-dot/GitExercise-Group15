import pygame
import random
import time
import sys
import os

def run_minigame (screen,clock):
    #screen setup
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption ("1990s  Archive Puzzle")
    
    #colours

    WHITE = (245, 245, 245)
    BLACK = (20, 20, 20)
    DARK = (14, 14, 24)
    PANEL = (30, 30, 42)
    GOLD = (255, 220, 120)
    RED = (220, 70, 70)
    GREEN = (80, 220, 130)
    GRAY = (170, 170, 170)

    #fonts
    font_tittle = pygame.font.SysFont("Arial", 46, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 32, bold=True)
    font_text = pygame.font.SysFont("Courier", 24)
    font_small = pygame.font.Sysfont("Courier", 20)

    #puzzles
    Grid_size = 3
    Image_size = 540
    font_tittle

    offset_x =width // 2 - image_size //2
    offset_y = 160 

    total_time = 120

    solved = [
        1,2,3,
        4,5,6,
        7,8,0
    ]

    board = solved.copy()
    moves = 0

#image
    image_paths = [
    "game_images/pearl_necklace.jpg"
]
    
image = None 
    
for path in image_paths:
        if os.path.exists(path):
            image = pygame.image.load(path).convert()
            break

if image is None:
        image = pygame.Surface((Image_size, Image_size))
        image.fill(WHITE)

        missing_text = font_subtitle.render("Pearl Necklace", True, BLACK)
        missing_rect = missing_text.get_rect(center=(Image_size // 2, Image_size // 2))
        image.blit(missing_text, missing_rect)

image = pygame.transform.scale(image, (Image_size, Image_size))