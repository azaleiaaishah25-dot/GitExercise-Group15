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

    # Settings
    TOTAL_TIME = 180      # 3 minutes
    ROUNDS_TO_WIN = 3     # complete 3 rounds
    FLASH_TIME = 500
    PAUSE_TIME = 250

    # Button positions - centered nicely for 1200x800
    button_size = 180
    gap = 40
    start_x = WIDTH // 2 - button_size - gap // 2
    start_y = HEIGHT // 2 - button_size - gap // 2

    buttons = [
        pygame.Rect(start_x, start_y, button_size, button_size),                            # red
        pygame.Rect(start_x + button_size + gap, start_y, button_size, button_size),        # green
        pygame.Rect(start_x, start_y + button_size + gap, button_size, button_size),        # blue
        pygame.Rect(start_x + button_size + gap, start_y + button_size + gap, button_size, button_size),  # yellow
    ]

    sequence = []
    player_input = []
    round_number = 1
    start_time = time.time()

    message = ""
def show_instructions_card():
    waiting = True

    while waiting:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    return False
