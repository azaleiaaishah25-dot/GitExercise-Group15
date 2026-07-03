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
                
    screen.fill(18,18,20)

    card = pygame.Rect(WIDTH // 2 - 360, HEIGHT // 2 - 260, 720, 520)
    pygame.draw.rect(screen, (35, 35, 50), card)
    pygame.draw.rect(screen, GOLD, card, 4)

    title = title_font.render("1980s Memory Flash", True, GOLD)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, card.y + 70)))

    instructions = [
        "The 1980s timeline is flashing out of control.",
        "Watch the color pattern carefully.",
        "Repeat the same pattern by clicking the buttons.",
        "Complete 3 rounds before 3 minutes ends.",
        "One wrong click fails the calibration."
    ]

    y = card.y + 150
    for line in instructions:
        text = small_font.render(line, True, WHITE)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, y)))
        y += 45

        start = small_font.render("Press SPACE to start | ESC to cancel", True, (200, 200, 200))
        screen.blit(start, start.get_rect(center=(WIDTH // 2, card.bottom - 45)))

        pygame.display.update()

        return True

    def draw_buttons(highlight=None):
        screen.fill(BLACK)

        title = medium_font.render("1980s MEMORY FLASH", True, GOLD)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        total_left = max(0, int(TOTAL_TIME - (time.time() - start_time)))
        minutes = total_left // 60
        seconds = total_left % 60

        timer_text = small_font.render(f"Time: {minutes}:{seconds:02d}", True, WHITE)
        round_text = small_font.render(f"Round: {round_number}/{ROUNDS_TO_WIN}", True, WHITE)

        screen.blit(timer_text, (30, 30))
        screen.blit(round_text, (30, 65))

        for i, btn in enumerate(buttons):
            color = colors[i]

            if highlight == i:
                color = WHITE

            pygame.draw.rect(screen, color, btn)
            pygame.draw.rect(screen, WHITE, btn, 4)

            label = small_font.render(color_names[i], True, BLACK)
            screen.blit(label, label.get_rect(center=btn.center))

        if message:
            msg = small_font.render(message, True, GOLD)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT - 80)))

        pygame.display.update()

    def flash_sequence():
        for color_index in sequence:
            draw_buttons(color_index)
            pygame.time.delay(FLASH_TIME)
            draw_buttons()
            pygame.time.delay(PAUSE_TIME)

    def show_result(text, color):
        end_time = time.time() + 1.5

        while time.time() < end_time:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            draw_buttons()

            box = pygame.Rect(WIDTH // 2 - 320, HEIGHT // 2 - 90, 640, 180)
            pygame.draw.rect(screen, DARK, box)
            pygame.draw.rect(screen, color, box, 4)

            result_text = medium_font.render(text, True, color)
            screen.blit(result_text, result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            pygame.display.update()

    # Start with instruction card
    if not show_instructions_card():
        return False

    running = True

    while running:
        clock.tick(60)

        # Total 3-minute timer
        if time.time() - start_time >= TOTAL_TIME:
            show_result("Time's up! Failed!", RED)
            return False

        if round_number > ROUNDS_TO_WIN:
            show_result("Calibration Complete!", GREEN)
            return True

        # Add new color to sequence
        sequence.append(random.randint(0, 3))
        player_input = []

        message = "Watch the pattern..."
        draw_buttons()
        pygame.time.delay(700)

        flash_sequence()

        message = "Your turn! Repeat the pattern."
        draw_buttons()

        # Player repeats sequence
        while len(player_input) < len(sequence):
            clock.tick(60)

            if time.time() - start_time >= TOTAL_TIME:
                show_result("Time's up! Failed!", RED)
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    for i, btn in enumerate(buttons):
                        if btn.collidepoint(mouse_x, mouse_y):
                            player_input.append(i)

                            draw_buttons(i)
                            pygame.time.delay(200)
                            draw_buttons()

                            correct_index = len(player_input) - 1

                            if player_input[correct_index] != sequence[correct_index]:
                                show_result("Wrong pattern! Failed!", RED)
                                return False

            draw_buttons()

        # Round complete
        message = f"Round {round_number} complete!"
        draw_buttons()
        pygame.time.delay(900)

        round_number += 1

    return False