from operator import index

import pygame as pg
import sys
import time
import random



pg.init()

# Screen
WIDTH, HEIGHT = 600, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe - Speed Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Images
x_img = pg.image.load("game_images/X.png")
o_img = pg.image.load("game_images/0.png")

x_img = pg.transform.scale(x_img, (120, 120))
o_img = pg.transform.scale(o_img, (120, 120))

# Board
board = [""] * 9
current_player = "X"

# Timer
TURN_TIME = 3
start_time = time.time()

font = pg.font.SysFont(None, 80)
small_font = pg.font.SysFont(None, 40)


def draw_board():
    screen.fill(WHITE)

    # grid lines
    pg.draw.line(screen, BLACK, (200, 0), (200, 600), 5)
    pg.draw.line(screen, BLACK, (400, 0), (400, 600), 5)
    pg.draw.line(screen, BLACK, (0, 200), (600, 200), 5)
    pg.draw.line(screen, BLACK, (0, 400), (600, 400), 5)

    # X/O
    for i in range(9):
        if board[i] != "":
            x = (i % 3) * 200 + 40
            y = (i // 3) * 200 + 40

        if board[i] == "X":
            screen.blit(x_img, (x, y))

        elif board[i] == "O":
            screen.blit(o_img, (x, y))


def check_winner():
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in wins:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None


def reset_game():
    global board, current_player, start_time
    board = [""] * 9
    current_player = "X"
    start_time = time.time()


running = True
winner = None

while running:
    draw_board()

    winner = check_winner()

    # Timer display
    elapsed = time.time() - start_time
    time_left = max(0, int(TURN_TIME - elapsed))
    timer_text = small_font.render(f"Time: {time_left}", True, BLACK)
    screen.blit(timer_text, (10, 10))

    # Auto switch turn if time runs out
    if time_left <= 0 and winner is None:
        current_player = "O" if current_player == "X" else "X"
        start_time = time.time()

    if current_player == "O" and winner is None:
        empty_spots = [i for i, spot in enumerate(board) if spot == ""]

        if empty_spots:
            bot_choice = random.choice(empty_spots)
            board[bot_choice] = "O"

            current_player = "X"
            start_time = time.time()

    winner = check_winner()
    if winner:
        win_text = small_font.render(f"{winner} wins! Press R", True, BLACK)
        screen.blit(win_text, (150, 270))

    elif "" not in board:
        draw_text = small_font.render("Draw! Press R", True, BLACK)
        screen.blit(draw_text, (170, 270))

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                reset_game()
        if event.type == pg.MOUSEBUTTONDOWN and winner is None and current_player == "X":
            x, y = pg.mouse.get_pos()
            row = y // 200
            col = x // 200
            index = row * 3 + col
            
            if board[index] == "":
                board[index] = "X"
                current_player = "O"
                start_time = time.time()
                
pg.quit()