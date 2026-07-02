import pygame as pg
import time
import random
from pathlib import Path


def run_minigame(screen, clock):
    WIDTH, HEIGHT = screen.get_size()

    # Board position
    BOARD_SIZE = 600
    CELL_SIZE = 200
    board_x = WIDTH // 2 - BOARD_SIZE // 2
    board_y = HEIGHT // 2 - BOARD_SIZE // 2

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (200, 40, 40)
    GREEN = (40, 160, 60)

    # Settings
    TURN_TIME = 3
    BOT_DELAY = 0.5
    TOTAL_TIME = 180
    ROUNDS_TO_WIN = 3

    font = pg.font.SysFont(None, 80)
    small_font = pg.font.SysFont(None, 40)
    tiny_font = pg.font.SysFont(None, 28)

    # Load images
    base_path = Path(__file__).resolve().parent
    image_path = base_path / "game_images"

    x_img = pg.image.load(image_path / "X.png").convert_alpha()
    o_img = pg.image.load(image_path / "0.png").convert_alpha()

    x_img = pg.transform.scale(x_img, (120, 120))
    o_img = pg.transform.scale(o_img, (120, 120))

    # Game variables
    board = [""] * 9
    current_player = "X"

    turn_start_time = time.time()
    total_start_time = time.time()

    bot_waiting = False
    bot_start_time = 0

    player_wins = 0
    waiting_next_round = False
    next_round_time = 0

    message = ""
    game_over = False
    mission_success = False

    def show_instruction_card():
        waiting = True

        while waiting:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False
                    elif event.key == pg.K_ESCAPE:
                        return False

            screen.fill((20, 20, 30))

            card = pg.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 230, 600, 460)
            pg.draw.rect(screen, (35, 35, 50), card)
            pg.draw.rect(screen, (255, 220, 120), card, 4)

            title = small_font.render("1950s Timeline Calibration", True, (255, 220, 120))
            screen.blit(title, title.get_rect(center=(WIDTH // 2, card.y + 55)))

            instructions = [
                "Win 3 Tic Tac Toe rounds.",
                "You only have 3 minutes.",
                "You are X. The robot is O.",
                "The robot only moves after you click.",
                "Move within 3 seconds each turn."
            ]

            y = card.y + 130
            for line in instructions:
                text = tiny_font.render(line, True, WHITE)
                screen.blit(text, text.get_rect(center=(WIDTH // 2, y)))
                y += 45

            start = tiny_font.render("Press SPACE to start | ESC to cancel", True, (200, 200, 200))
            screen.blit(start, start.get_rect(center=(WIDTH // 2, card.bottom - 50)))

            pg.display.update()

        return True

    def draw_board():
        screen.fill(WHITE)

        # Grid lines
        pg.draw.line(screen, BLACK, (board_x + 200, board_y), (board_x + 200, board_y + 600), 5)
        pg.draw.line(screen, BLACK, (board_x + 400, board_y), (board_x + 400, board_y + 600), 5)
        pg.draw.line(screen, BLACK, (board_x, board_y + 200), (board_x + 600, board_y + 200), 5)
        pg.draw.line(screen, BLACK, (board_x, board_y + 400), (board_x + 600, board_y + 400), 5)

        # X/O
        for i in range(9):
            if board[i] != "":
                x = board_x + (i % 3) * CELL_SIZE + 40
                y = board_y + (i // 3) * CELL_SIZE + 40

                if board[i] == "X":
                    screen.blit(x_img, (x, y))
                elif board[i] == "O":
                    screen.blit(o_img, (x, y))

    def check_winner():
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in wins:
            if board[a] == board[b] == board[c] != "":
                return board[a]

        return None

    def reset_round():
        nonlocal board, current_player, turn_start_time
        nonlocal bot_waiting, bot_start_time

        board = [""] * 9
        current_player = "X"
        turn_start_time = time.time()

        bot_waiting = False
        bot_start_time = 0

    def bot_move():
        empty_spots = [i for i, spot in enumerate(board) if spot == ""]

        if empty_spots:
            bot_choice = random.choice(empty_spots)
            board[bot_choice] = "O"

    def finish_round(result):
        nonlocal player_wins, waiting_next_round, next_round_time
        nonlocal message, game_over, mission_success

        if result == "X":
            player_wins += 1
            message = f"Round won! {player_wins}/{ROUNDS_TO_WIN}"

        elif result == "O":
            message = "Robot won this round!"

        elif result == "TIMEOUT":
            message = "Too slow! Round failed!"

        else:
            message = "Draw round!"

        if player_wins >= ROUNDS_TO_WIN:
            game_over = True
            mission_success = True
            message = "Mission Complete! You won 3 rounds!"
        else:
            waiting_next_round = True
            next_round_time = time.time() + 1.2

    def draw_status():
        total_elapsed = time.time() - total_start_time
        total_left = max(0, int(TOTAL_TIME - total_elapsed))

        minutes = total_left // 60
        seconds = total_left % 60

        total_text = tiny_font.render(f"Total Time: {minutes}:{seconds:02d}", True, BLACK)
        screen.blit(total_text, (30, 30))

        wins_text = tiny_font.render(f"Wins: {player_wins}/{ROUNDS_TO_WIN}", True, BLACK)
        screen.blit(wins_text, (30, 60))

        if not game_over and not waiting_next_round:
            if current_player == "X" and not bot_waiting:
                elapsed = time.time() - turn_start_time
                turn_left = max(0, int(TURN_TIME - elapsed))

                turn_text = tiny_font.render(f"Your Turn: {turn_left}", True, BLACK)
                screen.blit(turn_text, (30, 90))

            elif current_player == "O" and bot_waiting:
                bot_text = tiny_font.render("Robot thinking...", True, BLACK)
                screen.blit(bot_text, (30, 90))

    def draw_center_message(text, color):
        box = pg.Rect(WIDTH // 2 - 270, HEIGHT // 2 - 60, 540, 120)
        pg.draw.rect(screen, WHITE, box)
        pg.draw.rect(screen, BLACK, box, 4)

        msg = tiny_font.render(text, True, color)
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    # Instruction card
    if not show_instruction_card():
        return False

    running = True

    while running:
        clock.tick(60)

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False

            if event.type == pg.MOUSEBUTTONDOWN:
                if not game_over and not waiting_next_round:
                    if current_player == "X" and not bot_waiting:
                        mouse_x, mouse_y = pg.mouse.get_pos()

                        if board_x <= mouse_x <= board_x + BOARD_SIZE and board_y <= mouse_y <= board_y + BOARD_SIZE:
                            row = (mouse_y - board_y) // CELL_SIZE
                            col = (mouse_x - board_x) // CELL_SIZE
                            index = row * 3 + col

                            if 0 <= index < 9 and board[index] == "":
                                board[index] = "X"

                                winner = check_winner()

                                if winner:
                                    finish_round(winner)

                                elif "" not in board:
                                    finish_round("DRAW")

                                else:
                                    current_player = "O"
                                    bot_waiting = True
                                    bot_start_time = time.time()

        # Total 3-minute timer
        total_elapsed = time.time() - total_start_time

        if total_elapsed >= TOTAL_TIME and not game_over:
            game_over = True
            mission_success = False
            message = "Time's up! Mission failed!"

        # Next round after short delay
        if waiting_next_round and time.time() >= next_round_time:
            waiting_next_round = False
            reset_round()

        # Player turn timer
        if not game_over and not waiting_next_round:
            if current_player == "X" and not bot_waiting:
                elapsed = time.time() - turn_start_time

                if elapsed >= TURN_TIME:
                    finish_round("TIMEOUT")

        # Bot only moves after player clicks
        if not game_over and not waiting_next_round:
            if current_player == "O" and bot_waiting:
                if time.time() - bot_start_time >= BOT_DELAY:
                    bot_move()

                    winner = check_winner()

                    if winner:
                        bot_waiting = False
                        finish_round(winner)

                    elif "" not in board:
                        bot_waiting = False
                        finish_round("DRAW")

                    else:
                        current_player = "X"
                        bot_waiting = False
                        turn_start_time = time.time()

        # Draw
        draw_board()
        draw_status()

        if waiting_next_round:
            draw_center_message(message, BLACK)

        if game_over:
            if mission_success:
                draw_center_message(message, GREEN)
            else:
                draw_center_message(message, RED)

            pg.display.update()
            pg.time.delay(1500)
            return mission_success

        pg.display.update()

    return False