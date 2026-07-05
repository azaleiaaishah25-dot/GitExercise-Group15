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
    
    # =========================
    # SPLIT IMAGE INTO TILES
    # =========================
    tiles = []

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_rect = pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            tile = image.subsurface(tile_rect).copy()
            tiles.append(tile)

    # =========================
    # HELPER FUNCTIONS
    # =========================
    def draw_center_text(text, font, color, y):
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(WIDTH // 2, y))
        screen.blit(rendered, rect)

    def draw_wrapped_text(text, font, color, x, y, max_width, line_gap=8):
        words = text.split(" ")
        line = ""

        for word in words:
            test_line = line + word + " "

            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                rendered = font.render(line.strip(), True, color)
                screen.blit(rendered, (x, y))
                y += font.get_height() + line_gap
                line = word + " "

        if line:
            rendered = font.render(line.strip(), True, color)
            screen.blit(rendered, (x, y))
            y += font.get_height() + line_gap

        return y

    def draw_panel(rect):
        pygame.draw.rect(screen, PANEL, rect)
        pygame.draw.rect(screen, GOLD, rect, 3)

    # =========================
    # START SCREEN
    # =========================
    def start_screen():
        while True:
            clock.tick(60)
            screen.fill(DARK)

            draw_center_text("1990s ARCHIVE PUZZLE", font_title, GOLD, 100)

            panel_rect = pygame.Rect(WIDTH // 2 - 430, 170, 860, 440)
            draw_panel(panel_rect)

            y = panel_rect.y + 35

            y = draw_wrapped_text(
                "The archive image has been corrupted. Reconstruct the image to recover the final stolen artifact from the 1990s timeline.",
                font_text,
                WHITE,
                panel_rect.x + 40,
                y,
                panel_rect.width - 80
            )
            y += 25

            instructions = [
                "• Click a tile next to the empty space to move it.",
                "• Arrange the picture back into the correct order.",
                "• Press P to preview the original image.",
                "• Press ESC to quit the puzzle.",
                "• Complete it before the timer runs out."
            ]

            for line in instructions:
                rendered = font_text.render(line, True, WHITE)
                screen.blit(rendered, (panel_rect.x + 40, y))
                y += 42

            draw_center_text("Press SPACE to Start", font_subtitle, GOLD, 690)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True

                    if event.key == pygame.K_ESCAPE:
                        return False

    # =========================
    # COUNTDOWN
    # =========================
    def countdown_screen():
            for count in ["3", "2", "1", "GO!"]:
                start_tick = pygame.time.get_ticks()

            while pygame.time.get_ticks() - start_tick < 700:
                clock.tick(60)
                screen.fill(DARK)

                draw_center_text(count, font_title, GOLD, HEIGHT // 2)

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    # =========================
    # SHUFFLE BOARD
    # =========================
       def shuffle_board():
        nonlocal board

        while True:
            board = solved.copy()

            for _ in range(150):
                empty_index = board.index(0)

                empty_row = empty_index // GRID_SIZE
                empty_col = empty_index % GRID_SIZE

                possible_moves = []

                directions = [
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1)
                ]

                for row_change, col_change in directions:
                    new_row = empty_row + row_change
                    new_col = empty_col + col_change

                    if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                        possible_moves.append(new_row * GRID_SIZE + new_col)

                swap_index = random.choice(possible_moves)

                board[empty_index], board[swap_index] = board[swap_index], board[empty_index]