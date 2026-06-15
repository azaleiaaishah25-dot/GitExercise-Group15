import pygame
import sys
import random
import time
pygame.init()

#Screen size
WIDTH, HEIGHT = 1200, 800
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

image = pygame.image.load("game_images/pearl_necklace.jpg").convert()
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
 #board setup

solved = [1, 2, 3,
          4, 5, 6,
          7, 8, 0]

board = solved.copy()

# shuffle shuffle the pieces
def shuffle_board():

    global board

    board = solved.copy()

    for _ in range(100):

        empty = board.index(0)

        row = empty // GRID_SIZE
        col = empty % GRID_SIZE

        possible = []

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:

                possible.append(
                    nr * GRID_SIZE + nc
                )

        swap = random.choice(possible)

        board[empty], board[swap] = (
            board[swap],
            board[empty]
        )
    # DRAW PUZZLE
# =========================
def draw_board():

    screen.fill(WHITE)

    title = font_title.render(
        "1990s ARCHIVE RECONSTRUCTION",
        True,
        BLACK
    )

    instructions = font_text.render(
        "Restore the archive image before time runs out.",
        True,
        BLACK
    )

    screen.blit(title, (140, 20))
    screen.blit(instructions, (180, 70))

    for i, tile_num in enumerate(board):

        row = i // GRID_SIZE
        col = i % GRID_SIZE

        x = OFFSET_X + col * TILE_SIZE
        y = OFFSET_Y + row * TILE_SIZE

        rect = pygame.Rect(
            x,
            y,
            TILE_SIZE,
            TILE_SIZE
        )

        if tile_num == 0:

            pygame.draw.rect(
                screen,
                BLACK,
                rect
            )

        else:

            screen.blit(
                tiles[tile_num - 1],
                (x, y)
            )

            pygame.draw.rect(
                screen,
                BLACK,
                rect,
                2
            )

#checking if win

def is_solved():
    return board == solved

# =========================
# CLICKED TILE
# =========================
def get_tile_index(pos):

    mx, my = pos

    col = (mx - OFFSET_X) // TILE_SIZE
    row = (my - OFFSET_Y) // TILE_SIZE

    if (
        0 <= row < GRID_SIZE
        and
        0 <= col < GRID_SIZE
    ):
        return row * GRID_SIZE + col

    return None

# Moving the tiles

def move_tile(index):

    empty = board.index(0)

    r1, c1 = divmod(index, GRID_SIZE)
    r2, c2 = divmod(empty, GRID_SIZE)

    if abs(r1 - r2) + abs(c1 - c2) == 1:

        board[index], board[empty] = (
            board[empty],
            board[index]
        )
# MAIN GAME LOOP

def run_puzzle():

    shuffle_board()

    start_time = time.time()

    while True:

        clock.tick(60)

        draw_board()

        elapsed = time.time() - start_time
        remaining = max(0, 180 - int(elapsed))

        timer = font_text.render(
            f"Time Left: {remaining}s",
            True,
            BLACK
        )

        screen.blit(timer, (20, 20))

        pygame.display.flip()

        # -----------------
        # TIME OUT
        # -----------------
        if remaining <= 0:

            screen.fill(WHITE)

            fail = font_title.render(
                "ARCHIVE CORRUPTED",
                True,
                BLACK
            )

            screen.blit(
                fail,
                (
                    WIDTH//2 - fail.get_width()//2,
                    HEIGHT//2
                )
            )

            pygame.display.flip()
            pygame.time.wait(3000)

            return "fail"

        # -----------------
        # WIN
        # -----------------
        if is_solved():

            screen.fill(WHITE)

            screen.blit(
                image,
                (OFFSET_X, OFFSET_Y)
            )

            win = font_title.render(
                "ARCHIVE RESTORED",
                True,
                BLACK
            )

            clue = font_text.render(
                "Clue Discovered: Pearl Necklace",
                True,
                BLACK
            )

            screen.blit(
                win,
                (
                    WIDTH//2 - win.get_width()//2,
                    30
                )
            )

            screen.blit(
                clue,
                (
                    WIDTH//2 - clue.get_width()//2,
                    740
                )
            )

            pygame.display.flip()
            pygame.time.wait(4000)

            return "win"

        # -----------------
        # EVENTS
        # -----------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                index = get_tile_index(
                    event.pos
                )

                if index is not None:

                    move_tile(index)

# =========================
# RUN
# =========================
if __name__ == "__main__":

    result = run_puzzle()

    print(result)

    pygame.quit()