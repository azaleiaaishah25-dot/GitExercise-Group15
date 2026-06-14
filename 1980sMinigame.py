import pygame
import random
import time

pygame.init()

# Screen
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon Says - 1980s Security Panel")

# Colors
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 200)
YELLOW = (200, 200, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

colors = [RED, GREEN, BLUE, YELLOW]

# Button positions
buttons = [
    pygame.Rect(100, 100, 180, 180),  # red
    pygame.Rect(320, 100, 180, 180),  # green
    pygame.Rect(100, 320, 180, 180),  # blue
    pygame.Rect(320, 320, 180, 180),  # yellow
]

font = pygame.font.SysFont(None, 40)

def draw_buttons(highlight=None):
    screen.fill(BLACK)
    for i, btn in enumerate(buttons):
        color = colors[i]
        if highlight == i:
            color = WHITE  # flash effect
        pygame.draw.rect(screen, color, btn)
    pygame.display.update()

def flash_sequence(sequence):
    for i in sequence:
        draw_buttons(i)
        pygame.time.delay(500)
        draw_buttons()
        pygame.time.delay(200)

def run_simon_says():
    sequence = []
    player_input = []
    level = 1

    running = True

    while running:
        # add new step
        sequence.append(random.randint(0, 3))
        player_input = []

        flash_sequence(sequence)

        while len(player_input) < len(sequence):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    for i, btn in enumerate(buttons):
                        if btn.collidepoint(x, y):
                            player_input.append(i)
                            draw_buttons(i)
                            pygame.time.delay(200)
                            draw_buttons()

                            # check wrong input
                            if player_input[-1] != sequence[len(player_input) - 1]:
                                screen.fill(BLACK)
                                msg = font.render("FAILED - RESETTING", True, WHITE)
                                screen.blit(msg, (150, 280))
                                pygame.display.update()
                                pygame.time.delay(1500)
                                return  # exit game

        # level complete
        level += 1

        if level > 5:
            screen.fill(BLACK)
            msg = font.render("UNLOCKED CLUE!", True, WHITE)
            screen.blit(msg, (200, 280))
            pygame.display.update()
            pygame.time.delay(2000)
            return


# Run directly for testing
if __name__ == "__main__":
    run_simon_says()
    pygame.quit()