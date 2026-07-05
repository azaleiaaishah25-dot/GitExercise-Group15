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
                if board != solved:
                    break

    # =========================
    # DRAW BOARD
    # =========================
    def draw_board(remaining_time, preview_active):
        screen.fill(WHITE)

        draw_center_text("1990s ARCHIVE RECONSTRUCTION", font_title, BLACK, 45)
        draw_center_text("Restore the archive image before time runs out.", font_text, BLACK, 90)

        timer_text = font_text.render(f"Time Left: {remaining_time}s", True, BLACK)
        screen.blit(timer_text, (30, 25))

        moves_text = font_text.render(f"Moves: {moves}", True, BLACK)
        screen.blit(moves_text, (30, 60))

        help_text = font_small.render("P = Preview | ESC = Exit", True, BLACK)
        screen.blit(help_text, (WIDTH - help_text.get_width() - 30, 35))

        for index, tile_num in enumerate(board):
            row = index // GRID_SIZE
            col = index % GRID_SIZE

            x = OFFSET_X + col * TILE_SIZE
            y = OFFSET_Y + row * TILE_SIZE

            tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            if tile_num == 0:
                pygame.draw.rect(screen, BLACK, tile_rect)
            else:
                screen.blit(tiles[tile_num - 1], (x, y))
                pygame.draw.rect(screen, BLACK, tile_rect, 2)

        if preview_active:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(235)
            overlay.fill(DARK)
            screen.blit(overlay, (0, 0))

            draw_center_text("IMAGE PREVIEW", font_title, GOLD, 75)

            screen.blit(image, (OFFSET_X, OFFSET_Y))
            pygame.draw.rect(
                screen,
                GOLD,
                pygame.Rect(OFFSET_X, OFFSET_Y, IMAGE_SIZE, IMAGE_SIZE),
                4
            )

            draw_center_text("Release P to continue the puzzle", font_text, WHITE, 735)

    # =========================
    # CHECK SOLVED
    # =========================
    def is_solved():
        return board == solved

    # =========================
    # GET CLICKED TILE
    # =========================
    def get_tile_index(mouse_pos):
        mouse_x, mouse_y = mouse_pos

        col = (mouse_x - OFFSET_X) // TILE_SIZE
        row = (mouse_y - OFFSET_Y) // TILE_SIZE

        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row * GRID_SIZE + col

        return None

    # =========================
    # MOVE TILE
    # =========================
    def move_tile(index):
        nonlocal moves

        empty_index = board.index(0)

        tile_row, tile_col = divmod(index, GRID_SIZE)
        empty_row, empty_col = divmod(empty_index, GRID_SIZE)

        distance = abs(tile_row - empty_row) + abs(tile_col - empty_col)

        if distance == 1:
            board[index], board[empty_index] = board[empty_index], board[index]
            moves += 1
     # =========================
    # END SCREEN
    # =========================
    def end_screen(title_text, subtitle_text, title_color, show_final_image):
        start_tick = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_tick < 3500:
            clock.tick(60)
            screen.fill(DARK)

            draw_center_text(title_text, font_title, title_color, 85)

            if show_final_image:
                screen.blit(image, (OFFSET_X, OFFSET_Y))
                pygame.draw.rect(
                    screen,
                    GOLD,
                    pygame.Rect(OFFSET_X, OFFSET_Y, IMAGE_SIZE, IMAGE_SIZE),
                    4
                )
            else:
                panel_rect = pygame.Rect(WIDTH // 2 - 350, 250, 700, 180)
                draw_panel(panel_rect)
                draw_center_text(subtitle_text, font_text, WHITE, HEIGHT // 2)

            if show_final_image:
                draw_center_text(subtitle_text, font_text, WHITE, 735)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
     # =========================
    # START MINIGAME
    # =========================
    if not start_screen():
        return False

    countdown_screen()

    shuffle_board()
    start_time = time.time()

    # =========================
    # MAIN LOOP
    # =========================
    while True:
        clock.tick(60)

        elapsed_time = time.time() - start_time
        remaining_time = max(0, TOTAL_TIME - int(elapsed_time))

        keys = pygame.key.get_pressed()
        preview_active = keys[pygame.K_p]

        draw_board(remaining_time, preview_active)
        pygame.display.flip()

        # =========================
        # TIME OUT
        # =========================
        if remaining_time <= 0:
            end_screen(
                "ARCHIVE CORRUPTED",
                "The archive clue was lost. Try again.",
                RED,
                False
            )
        return False

        # =========================
        # WIN
        # =========================
        if is_solved():
            end_screen(
                "ARCHIVE RESTORED",
                "Clue Discovered: Pearl Necklace",
                GREEN,
                True
            )

            return True

        # =========================
        # EVENTS
        # =========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_screen(
                        "PUZZLE EXITED",
                        "You left the archive puzzle.",
                        RED,
                     False
                    )

                    return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not preview_active:
                    clicked_index = get_tile_index(event.pos)

                    if clicked_index is not None:
                         move_tile(clicked_index)


# =========================
# TEST MODE ONLY
# =========================
if __name__ == "__main__":
    pygame.init()

    WIDTH, HEIGHT = 1200, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("1990s Archive Puzzle")

    clock = pygame.time.Clock()

    result = run_minigame(screen, clock)

    print(result)

    pygame.quit()   
