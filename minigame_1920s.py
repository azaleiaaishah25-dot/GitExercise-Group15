import random
from pathlib import Path

import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MARGIN = 20


class Card:
    def __init__(self, symbol, position, size, image):
        self.symbol = symbol
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], size, size)
        self.revealed = False
        self.matched = False
        self.image = image

    def draw(self, screen):
        color = WHITE if self.revealed or self.matched else GREEN
        pygame.draw.rect(screen, color, self.rect)

        if self.revealed or self.matched:
            screen.blit(self.image, (self.position[0] + 10, self.position[1] + 10))


def _show_result(screen, clock, text, color, duration=2000):
    width, height = screen.get_size()
    font = pygame.font.Font(None, 74)
    end_time = pygame.time.get_ticks() + duration

    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return False

        message = font.render(text, True, color)
        screen.blit(message, message.get_rect(center=(width // 2, height // 2)))
        pygame.display.flip()
        clock.tick(60)

    return True

def show_instructions_page(screen,clock,title,instructions):
    WIDTH,HEIGHT =screen.get_size()

    title_font = pygame.font.Font(None, 74)
    instruction_font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    waiting = True
    while waiting:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            elif event.type == pygame.K_ESCAPE:
                return False
        screen.fill((15, 15, 25))

        card_rect = pygame.Rect(160, 120, WIDTH - 320, HEIGHT - 240)
        pygame.draw.rect(screen, (30, 30, 45), card_rect)
        pygame.draw.rect(screen, (255, 220, 120), card_rect, 4)

        title_surface = title_font.render(title, True, (255, 220, 120))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 180))
        screen.blit(title_surface, title_rect)

        y = 260
        for line in instructions:
            text_surface = instruction_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
            screen.blit(text_surface, text_rect)
            y += 45

        start_text = small_font.render("Press SPACE to start | Press ESC to cancel", True, (200, 200, 200))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT - 170))
        screen.blit(start_text, start_rect)

        pygame.display.update()

    return True
        

def run_minigame(screen, clock):
    instruction_ok = show_instructions_page(
        screen,
        clock,
        "1920s Timeline Calibration",
        [
            "The timeline is unstable.",
            "Complete the challenge to unlock the next era.",
            "Use the controls shown in the mini-game.",
            "Win the mini-game to continue your investigation."
        ]
    )

    if not instruction_ok:
        return False

    """Run the 1920s memory game and return True only when the player wins."""
    width, height = screen.get_size()
    big_font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    # Keep the 4x4 grid inside the main game's existing window.
    card_size = min(
        140,
        (width - (3 * MARGIN) - 40) // 4,
        (height - (3 * MARGIN) - 160) // 4,
    )
    grid_width = (4 * card_size) + (3 * MARGIN)
    grid_height = (4 * card_size) + (3 * MARGIN)
    start_x = (width - grid_width) // 2
    start_y = 80 + ((height - 160 - grid_height) // 2)

    positions = [
        (start_x + col * (card_size + MARGIN), start_y + row * (card_size + MARGIN))
        for row in range(4)
        for col in range(4)
    ]

    image_folder = Path(__file__).resolve().parent / "game_images"
    image_size = card_size - 20
    images = [
        pygame.transform.smoothscale(
            pygame.image.load(str(image_folder / f"{number}.png")),
            (image_size, image_size),
        )
        for number in range(1, 9)
    ]

    pairs = list(range(8)) * 2
    random.shuffle(pairs)
    cards = [
        Card(pairs[index], positions[index], card_size, images[pairs[index]])
        for index in range(16)
    ]

    # Show every card for five seconds before starting the timer.
    memorize_end = pygame.time.get_ticks() + 5000
    while pygame.time.get_ticks() < memorize_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return False

        screen.fill(BLACK)
        for card in cards:
            card.revealed = True
            card.draw(screen)

        text = big_font.render("Memorize!", True, WHITE)
        screen.blit(text, text.get_rect(center=(width // 2, 45)))
        pygame.display.flip()
        clock.tick(60)

    for card in cards:
        card.revealed = False

    first_card = None
    second_card = None
    reveal_time = None
    matches = 0
    attempts = 0
    time_limit = 120
    start_time = pygame.time.get_ticks()

    while True:
        current_ticks = pygame.time.get_ticks()

        if reveal_time is not None and current_ticks - reveal_time >= 1000:
            first_card.revealed = False
            second_card.revealed = False
            first_card = None
            second_card = None
            reveal_time = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if second_card is not None:
                    first_card.revealed = False
                    second_card.revealed = False
                    first_card = None
                    second_card = None
                    reveal_time = None

                for card in cards:
                    if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                        card.revealed = True

                        if first_card is None:
                            first_card = card
                        else:
                            second_card = card
                            attempts += 1

                            if first_card.symbol == second_card.symbol:
                                first_card.matched = True
                                second_card.matched = True
                                matches += 1
                                first_card = None
                                second_card = None
                            else:
                                reveal_time = current_ticks
                        break

        elapsed_time = (current_ticks - start_time) // 1000
        time_left = max(0, time_limit - elapsed_time)

        screen.fill(BLACK)
        for card in cards:
            card.draw(screen)

        timer = small_font.render(f"Time: {time_left}", True, WHITE)
        screen.blit(timer, timer.get_rect(center=(width // 2, height - 75)))

        score = small_font.render(
            f"Matches: {matches}  Attempts: {attempts}", True, WHITE
        )
        screen.blit(score, score.get_rect(center=(width // 2, height - 35)))

        pygame.display.flip()

        if matches == 8:
            _show_result(screen, clock, "You Win!", GREEN)
            return True

        if time_left == 0:
            _show_result(screen, clock, "Time's Up!", RED)
            return False

        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    test_screen = pygame.display.set_mode((1200, 800))
    test_clock = pygame.time.Clock()
    run_minigame(test_screen, test_clock)
    pygame.quit()
