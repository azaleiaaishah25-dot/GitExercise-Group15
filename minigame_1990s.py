import pygame
import random
import time
import sys
import os


def run_minigame(screen, clock):
    # =========================
    # SCREEN SETUP
    # =========================
    WIDTH, HEIGHT = screen.get_size()

    pygame.display.set_caption("1990s Archive Puzzle")

    # =========================
    # COLOURS
    # =========================
    WHITE = (245, 245, 245)
    BLACK = (20, 20, 20)
    DARK = (14, 14, 24)
    PANEL = (30, 30, 42)
    GOLD = (255, 220, 120)
    RED = (220, 70, 70)
    GREEN = (80, 220, 130)
    GRAY = (170, 170, 170)

    # =========================
    # FONTS
    # =========================
    font_title = pygame.font.SysFont("Arial", 46, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 32, bold=True)
    font_text = pygame.font.SysFont("Courier", 24)
    font_small = pygame.font.SysFont("Courier", 20)

    # =========================
    # PUZZLE SETTINGS
    # =========================
    GRID_SIZE = 3
    IMAGE_SIZE = 540
    TILE_SIZE = IMAGE_SIZE // GRID_SIZE

    OFFSET_X = WIDTH // 2 - IMAGE_SIZE // 2
    OFFSET_Y = 160

    TOTAL_TIME = 180

    solved = [
        1, 2, 3,
        4, 5, 6,
        7, 8, 0
    ]

    board = solved.copy()
    moves = 0

    # =========================
    # IMAGE LOADING
    # =========================
    image_paths = [
        "game_images/pearl_necklace.jpg",
        "Images/1990necklace1.jpeg",
        "Images/1990necklace1.jpg",
        "Images/pearl_necklace.jpg"
    ]

    image = None

    for path in image_paths:
        if os.path.exists(path):
            image = pygame.image.load(path).convert()
            break

    if image is None:
        image = pygame.Surface((IMAGE_SIZE, IMAGE_SIZE))
        image.fill(WHITE)

        missing_text = font_subtitle.render("Pearl Necklace", True, BLACK)
        missing_rect = missing_text.get_rect(center=(IMAGE_SIZE // 2, IMAGE_SIZE // 2))
        image.blit(missing_text, missing_rect)

    image = pygame.transform.scale(image, (IMAGE_SIZE, IMAGE_SIZE))
    