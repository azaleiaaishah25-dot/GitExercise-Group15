# Initialize Pygame
import pygame
import random
import time

pygame.init()

images = [
    pygame.image.load("game_images/1.png"),
    pygame.image.load("game_images/2.png"),
    pygame.image.load("game_images/3.png"),
    pygame.image.load("game_images/4.png"),
    pygame.image.load("game_images/5.png"),
    pygame.image.load("game_images/6.png"),
    pygame.image.load("game_images/7.png"),
    pygame.image.load("game_images/8.png"),
]

symbols = list(range(8)) * 2
images = [pygame.transform.scale(img, (120, 120)) for img in images] 

# Set up display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
big_font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Card settings
CARD_SIZE = 140
MARGIN = 20

def create_card_positions():
    positions = []
    # Calculate total grid sizes
    grid_width = (4 * CARD_SIZE) + (3 * MARGIN)
    grid_height = (4 * CARD_SIZE) + (3 * MARGIN)
    
    # Calculate starting offsets to center the grid
    start_x = (WIDTH - grid_width) // 2
    start_y = (HEIGHT - grid_height) // 2

    for i in range(4): # Rows
        for j in range(4): # Columns
            x = start_x + j * (CARD_SIZE + MARGIN)
            y = start_y + i * (CARD_SIZE + MARGIN)
            positions.append((x, y))
    return positions

positions = create_card_positions()

# Generate pairs
def generate_pairs():
    symbols = list(range(8)) * 2
    random.shuffle(symbols)
    return symbols

pairs = generate_pairs()

# Card class
class Card:
    def __init__(self, symbol, position):
        self.symbol = symbol
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], CARD_SIZE, CARD_SIZE)
        self.revealed = False
        self.matched = False
        self.image = images[symbol]


    def draw(self, screen):
        if self.revealed or self.matched:
            pygame.draw.rect(screen, WHITE, self.rect)
            screen.blit(self.image, (self.position[0] + 10, self.position[1] + 10))


        else:
            pygame.draw.rect(screen, GREEN, self.rect)

# Create cards
cards = [Card(pairs[i], positions[i]) for i in range(16)]

# Game variables
first_card = None
second_card = None
reveal_time = None  # <--- ADD THIS LINE
matches = 0
attempts = 0
running = True
clock = pygame.time.Clock()

# TIMER START (ONLY ONCE)
start_time = pygame.time.get_ticks()
time_limit = 120 # 120 seconds to win

# Memorize screen
screen.fill(BLACK)
for card in cards:
    card.revealed = True
    card.draw(screen)

screen.blit(big_font.render("Memorize!", True, WHITE), (150, 500))
pygame.display.flip()

time.sleep(5)

for card in cards:
    card.revealed = False

# MAIN LOOP
while running:
    screen.fill(BLACK)
    current_ticks = pygame.time.get_ticks()

    # --- 1. NON-BLOCKING AUTOMATIC FLIP BACK ---
    # If 1000 milliseconds (1 second) have passed since a mismatch, flip them back
    if reveal_time is not None and (current_ticks - reveal_time >= 1000):
        if first_card and second_card:
            first_card.revealed = False
            second_card.revealed = False
        first_card = None
        second_card = None
        reveal_time = None

    # --- 2. EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If a mismatch is already face up and you click a 3rd card, 
            # instantly flip the old pair down so the player doesn't have to wait!
            if second_card is not None:
                first_card.revealed = False
                second_card.revealed = False
                first_card = None
                second_card = None
                reveal_time = None

            # Process the new card click
            for card in cards:
                if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                    card.revealed = True

                    if first_card is None:
                        first_card = card
                    else:
                        second_card = card
                        attempts += 1
                        
                        # Check immediately if they match
                        if first_card.symbol == second_card.symbol:
                            first_card.matched = True
                            second_card.matched = True
                            matches += 1
                            # Clear variables instantly so they stay face up permanently
                            first_card = None
                            second_card = None
                            reveal_time = None
                        else:
                            # Save the timestamp! The game will keep running, 
                            # and auto-flip these after 1 second unless a 3rd card is clicked.
                            reveal_time = current_ticks

    # --- 3. TIMER CALCULATIONS ---
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, time_limit - int(elapsed_time))

    timer_text = small_font.render(f"Time: {time_left}", True, WHITE)
    timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
    screen.blit(timer_text, timer_rect)

    # GAME OVER BY TIME
    if time_left == 0:
        over_text = big_font.render("Time's Up!", True, RED)
        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    # --- 4. DRAW GRAPHICS & TEXT ---
    for card in cards:
        card.draw(screen)

    score_text = small_font.render(f"Matches: {matches} Attempts: {attempts}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(score_text, score_rect)

    # WIN CHECK
    if matches == 8:
        win_text = big_font.render("You Win!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()