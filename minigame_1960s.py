import pygame as pg
import random
import time


def run_minigame(screen, clock):
    WIDTH, HEIGHT = screen.get_size()

    # COLORS
    BLACK = (10, 10, 20)
    WHITE = (255, 255, 255)
    YELLOW = (255, 220, 120)
    PINK = (255, 80, 180)
    PURPLE = (120, 80, 200)
    GREEN = (60, 220, 120)
    RED = (220, 60, 60)
    BLUE = (80, 160, 255)

    # FONTS
    title_font = pg.font.SysFont(None, 70)
    big_font = pg.font.SysFont(None, 120)
    medium_font = pg.font.SysFont(None, 42)
    small_font = pg.font.SysFont(None, 30)

    # GAME SETTINGS
    GOAL_SCORE = 15
    MAX_MISSES = 5
    TOTAL_TIME = 45

    NOTE_SPEED = 7
    HIT_LINE_Y = HEIGHT - 180
    HIT_WINDOW = 60

    notes = [
    {"label": "A", "key": pg.K_a, "name": "LEFT"},
    {"label": "S", "key": pg.K_s, "name": "DOWN"},
    {"label": "W", "key": pg.K_w, "name": "UP"},
    {"label": "D", "key": pg.K_d, "name": "RIGHT"},
    ]

    lane_count = 4
    lane_width = 140
    total_lane_width = lane_width * lane_count
    start_x = WIDTH // 2 - total_lane_width // 2

    lanes = []
    for i in range(lane_count):
        lane_x = start_x + i * lane_width + lane_width // 2
        lanes.append(lane_x)

    score = 0
    misses = 0
    current_note = None
    start_time = time.time()
    last_spawn_time = 0
    spawn_delay = 0.7

    feedback_text = ""
    feedback_timer = 0

    # =========================
    # INSTRUCTION CARD
    # =========================
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

            screen.fill((18, 12, 30))

            card = pg.Rect(WIDTH // 2 - 360, HEIGHT // 2 - 260, 720, 520)
            pg.draw.rect(screen, (35, 25, 55), card)
            pg.draw.rect(screen, YELLOW, card, 4)

            title = title_font.render("1960s Go-Go Rhythm", True, YELLOW)
            screen.blit(title, title.get_rect(center=(WIDTH // 2, card.y + 70)))

            instructions = [
                "The Youthquake timeline is unstable.",
                "Press the W A S D keys when the note reaches the hit line.",
                "Correct timing gives you points.",
                "Get 15 correct hits before time runs out.",
                "5 misses will fail the calibration."
            ]

            y = card.y + 150
            for line in instructions:
                text = small_font.render(line, True, WHITE)
                screen.blit(text, text.get_rect(center=(WIDTH // 2, y)))
                y += 45

            controls = medium_font.render("Use W A S D", True, PINK)
            screen.blit(controls, controls.get_rect(center=(WIDTH // 2, card.y + 390)))

            start = small_font.render("Press SPACE to start | ESC to cancel", True, (200, 200, 200))
            screen.blit(start, start.get_rect(center=(WIDTH // 2, card.bottom - 45)))

            pg.display.update()

        return True

    # =========================
    # NOTE SYSTEM
    # =========================
    def spawn_note():
        note_index = random.randint(0, len(notes) - 1)
        note_data = notes[note_index]

        return {
            "label": note_data["label"],
            "key": note_data["key"],
            "name": note_data["name"],
            "lane": note_index,
            "x": lanes[note_index],
            "y": 80
        }

    def draw_background():
        screen.fill(BLACK)

        # 1960s dance floor vibe
        for i in range(0, WIDTH, 80):
            color = PURPLE if i % 160 == 0 else BLUE
            pg.draw.circle(screen, color, (i, 80), 18)

        title = medium_font.render("1960s GO-GO RHYTHM CHALLENGE", True, YELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        # Lanes
        for i, lane_x in enumerate(lanes):
            lane_rect = pg.Rect(lane_x - 55, 90, 110, HEIGHT - 230)
            pg.draw.rect(screen, (25, 25, 45), lane_rect)
            pg.draw.rect(screen, (70, 70, 100), lane_rect, 2)

            lane_label = medium_font.render(notes[i]["label"], True, WHITE)
            screen.blit(lane_label, lane_label.get_rect(center=(lane_x, HEIGHT - 90)))

        # Hit line
        pg.draw.line(screen, PINK, (start_x - 40, HIT_LINE_Y), (start_x + total_lane_width + 40, HIT_LINE_Y), 6)

        hit_text = small_font.render("HIT LINE", True, PINK)
        screen.blit(hit_text, hit_text.get_rect(center=(WIDTH // 2, HIT_LINE_Y + 30)))

    def draw_status():
        time_left = max(0, int(TOTAL_TIME - (time.time() - start_time)))

        score_text = small_font.render(f"Score: {score}/{GOAL_SCORE}", True, WHITE)
        miss_text = small_font.render(f"Misses: {misses}/{MAX_MISSES}", True, WHITE)
        time_text = small_font.render(f"Time: {time_left}", True, WHITE)

        screen.blit(score_text, (30, 90))
        screen.blit(miss_text, (30, 120))
        screen.blit(time_text, (30, 150))

    def draw_note(note):
        note_circle = pg.Rect(0, 0, 90, 90)
        note_circle.center = (note["x"], note["y"])

        pg.draw.ellipse(screen, YELLOW, note_circle)
        pg.draw.ellipse(screen, WHITE, note_circle, 4)

        symbol = big_font.render(note["label"], True, BLACK)
        screen.blit(symbol, symbol.get_rect(center=note_circle.center))

    def draw_feedback():
        if feedback_timer > 0:
            color = GREEN if feedback_text == "PERFECT!" else RED
            text = medium_font.render(feedback_text, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT - 40)))

    def show_result(message, color):
        end_time = time.time() + 1.5

        while time.time() < end_time:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            draw_background()
            draw_status()

            box = pg.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 90, 600, 180)
            pg.draw.rect(screen, (20, 20, 30), box)
            pg.draw.rect(screen, color, box, 4)

            text = medium_font.render(message, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

            pg.display.update()

    # =========================
    # START GAME
    # =========================
    if not show_instruction_card():
        return False

    current_note = spawn_note()
    last_spawn_time = time.time()

    running = True

    while running:
        clock.tick(60)

        # Timer
        time_left = TOTAL_TIME - (time.time() - start_time)

        if time_left <= 0:
            show_result("Time's up! Calibration failed!", RED)
            return False

        if score >= GOAL_SCORE:
            show_result("Calibration Complete!", GREEN)
            return True

        if misses >= MAX_MISSES:
            show_result("Too many misses! Failed!", RED)
            return False

        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False

                if current_note:
                    if event.key == current_note["key"]:
                        distance = abs(current_note["y"] - HIT_LINE_Y)

                        if distance <= HIT_WINDOW:
                            score += 1
                            feedback_text = "PERFECT!"
                            feedback_timer = 30
                            current_note = spawn_note()
                            last_spawn_time = time.time()
                        else:
                            misses += 1
                            feedback_text = "TOO EARLY!"
                            feedback_timer = 30
                            current_note = spawn_note()
                            last_spawn_time = time.time()

                    elif event.key in [pg.K_a, pg.K_s, pg.K_w, pg.K_d]:
                        misses += 1
                        feedback_text = "WRONG KEY!"
                        feedback_timer = 30
                        current_note = spawn_note()
                        last_spawn_time = time.time()

        # Move note
        if current_note:
            current_note["y"] += NOTE_SPEED

            if current_note["y"] > HIT_LINE_Y + HIT_WINDOW:
                misses += 1
                feedback_text = "MISSED!"
                feedback_timer = 30
                current_note = spawn_note()
                last_spawn_time = time.time()

        # Feedback timer
        if feedback_timer > 0:
            feedback_timer -= 1

        # Draw
        draw_background()
        draw_status()

        if current_note:
            draw_note(current_note)

        draw_feedback()

        pg.display.update()

    return False