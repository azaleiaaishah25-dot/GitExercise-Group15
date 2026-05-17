import pygame
from data.maps import * 
from data.buildings import building_data
from data.dialogues import dialogue_data, item_dialogue_data
from data.quests import quest_descriptions, clue_descriptions


#Master switch 
pygame.init() 

#1. Setup & Variables
tile_size = 60
WIDTH, HEIGHT = 1200, 800 #Resolution Full HD
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Style Heist - Detective Game")
clock = pygame.time.Clock() #limit the pc fps 
font = pygame.font.SysFont(None, 30)

#Game state
game_state = "menu"
debug_mode = False

#Menu Fonts
title_font = pygame.font.SysFont(None, 90)
menu_font = pygame.font.SysFont(None, 45)
small_font = pygame.font.SysFont(None, 28)

#Menu Buttons
start_button = pygame.Rect(WIDTH // 2 - 150, 350, 300, 60)
credits_button = pygame.Rect(WIDTH // 2 - 150, 430, 300, 60)
quit_button = pygame.Rect(WIDTH // 2 - 150, 510, 300, 60)
back_button = pygame.Rect(WIDTH // 2 - 100, 620, 200, 50)

game_exit_button = pygame.Rect(WIDTH - 130, 20, 100, 45)
resume_button = pygame.Rect(WIDTH // 2 - 150, 330, 300, 60)
main_menu_button = pygame.Rect(WIDTH // 2 - 150, 410, 300, 60)
pause_quit_button = pygame.Rect(WIDTH // 2 - 150, 490, 300, 60)

seen_self_dialogues = set()
dialogue_active = False
current_dialogue = []
dialogue_index = 0
dialogue_text_shown = ""
text_speed = 2
text_counter = 0

collected_clues = []
current_clue = None
show_clue_inventory = False

can_interact = False
current_npc = None

quest_log = {}

#Quest System
active_quests = []
completed_quests = []
current_quest = None

quest_popup_text = ""
quest_popup_timer = 0
QUEST_POPUP_DURATION = 150

current_era = "Museum"
game_map = museum_map #Starting at the Museum

#Fog of war 
visited_map = [[False for _ in range(len(museum_map[0]))] for _ in range(len(museum_map))]


#3. Player Variables
player_size = tile_size
player_size = 60
player_x = 1500
player_y = 1600
speed = 10 #pixels per movement per frame


#4. Images
duck_img = pygame.image.load("Images/duck_with_knife.jpg").convert_alpha()
duck_img = pygame.transform.scale(duck_img, (player_size, player_size))

tree_img = pygame.image.load("Images/pixel_tree.jpg").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size))

#5. Functions (Logic)

def check_collision(x, y, current_map):
    player_rect = pygame.Rect(x, y, player_size, player_size)

    # Only check nearby tiles around the player instead of scanning the whole map.
    left_tile = max(0, player_rect.left // tile_size)
    right_tile = min(len(current_map[0]) - 1, player_rect.right // tile_size)
    top_tile = max(0, player_rect.top // tile_size)
    bottom_tile = min(len(current_map) - 1, player_rect.bottom // tile_size)

    for row in range(top_tile, bottom_tile + 1):
        for col in range(left_tile, right_tile + 1):
            tile = current_map[row][col]

            if tile in ["1", "3", "5"]:
                wall_rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)

                if player_rect.colliderect(wall_rect):
                    return True

    return False

def transition_to(new_map_array, new_era_name, spawn_tile_x, spawn_tile_y):
    global game_map, current_era, player_x, player_y, visited_map
    
    
    game_map = new_map_array
    current_era = new_era_name
    
    player_x = spawn_tile_x * tile_size
    player_y = spawn_tile_y * tile_size
    
    visited_map = [[False for _ in range(len(game_map[0]))] for _ in range(len(game_map))]
    
    pygame.time.delay(80)

#This area is the main menu Part
def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):
        color = (180, 140, 70)
    else:
        color = (120, 90, 50)

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3)

    text_surface = menu_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_main_menu():
    screen.fill((15, 10, 20))

    title_text = title_font.render("STYLE HEIST", True, (255, 220, 120))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 180))
    screen.blit(title_text, title_rect)

    subtitle_text = small_font.render("A Detective Time-Travel Fashion Mystery", True, (220, 220, 220))
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 245))
    screen.blit(subtitle_text, subtitle_rect)

    draw_button(start_button, "Start Game")
    draw_button(credits_button, "Credits")
    draw_button(quit_button, "Quit")

    footer_text = small_font.render(
        "UI Design Placeholder - Balqish can redesign this screen",
        True,
        (160, 160, 160)
    )
    footer_rect = footer_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(footer_text, footer_rect)


def draw_credits_screen():
    screen.fill((10, 15, 25))

    title_text = title_font.render("CREDITS", True, (255, 220, 120))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 140))
    screen.blit(title_text, title_rect)

    credit_lines = [
        "Style Heist - Group 15",
        "Sample Line",
        "Programming / Game Systems: Alvin",
        "UI Design Contributor: Balqish",
        "Dialogue / Story Contributor: Azaleia",
        "",
        "Built using Python and Pygame"
    ]

    y = 230
    for line in credit_lines:
        text_surface = menu_font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        screen.blit(text_surface, text_rect)
        y += 45

    draw_button(back_button, "Back")

def draw_pause_menu():
    screen.fill((12, 12, 18))

    title_text = title_font.render("PAUSED", True, (220, 220, 220))
    title_rect = title_text.get_rect(center = (WIDTH // 2, 180))
    screen.blit(title_text, title_rect)

    subtitle_text = small_font.render("Take a break, detective.", True, (220, 220, 220))
    subtitle_rect = subtitle_text.get_rect(center = (WIDTH // 2, 245))
    screen.blit(subtitle_text, subtitle_rect)

    draw_button(resume_button, "Resume")
    draw_button(main_menu_button, "Main Menu")
    draw_button(pause_quit_button, "Quit Game")

def add_quest(quest_id):
    if quest_id and quest_id not in active_quests and quest_id not in completed_quests:
        active_quests.append(quest_id)

def complete_quest(quest_id):
    global quest_popup_text, quest_popup_timer

    if quest_id in active_quests:
        active_quests.remove(quest_id)

    if quest_id not in completed_quests:
        completed_quests.append(quest_id)

    quest_name = quest_descriptions.get(quest_id, quest_id)
    quest_popup_text = "QUEST COMPLETE: " + quest_name
    quest_popup_timer = QUEST_POPUP_DURATION

def draw_wrapped_text(surface, text, font, color, x, y, max_width, line_spacing=5):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    for line in lines:
        rendered_line = font.render(line.strip(), True, color)
        surface.blit(rendered_line, (x, y))
        y += font.get_height() + line_spacing

    return y

def draw_quest_navigation():
    # Do not show quest box if no active quest
    if len(active_quests) == 0:
        return

    quest_box = pygame.Rect(20, 90, 320, 190)

    pygame.draw.rect(screen, (20, 20, 20), quest_box)
    pygame.draw.rect(screen, (255, 255, 255), quest_box, 2)

    title = font.render("CURRENT QUEST", True, (255, 255, 0))
    screen.blit(title, (quest_box.x + 15, quest_box.y + 15))

    y = quest_box.y + 55
    max_text_width = quest_box.width - 30

    for quest_id in active_quests[:3]:
        quest_text = quest_descriptions.get(quest_id, quest_id)
        y = draw_wrapped_text(
            screen,
            "- " + quest_text,
            font,
            (255, 255, 255),
            quest_box.x + 15,
            y,
            max_text_width
        )
        y += 8

def draw_quest_complete_popup():
    global quest_popup_timer

    if quest_popup_timer <= 0:
        return

    alpha = int(255 * (quest_popup_timer / QUEST_POPUP_DURATION))

    popup_surface = pygame.Surface((500, 70), pygame.SRCALPHA)
    pygame.draw.rect(popup_surface, (20, 20, 20, alpha), (0, 0, 500, 70))
    pygame.draw.rect(popup_surface, (255, 220, 120, alpha), (0, 0, 500, 70), 3)

    text_surface = font.render(quest_popup_text, True, (255, 255, 255))
    text_surface.set_alpha(alpha)

    text_rect = text_surface.get_rect(center=(250, 35))
    popup_surface.blit(text_surface, text_rect)

    screen.blit(popup_surface, (WIDTH // 2 - 250, 90))

    quest_popup_timer -= 1

def add_clue(clue_id):
    if clue_id and clue_id not in collected_clues:
        collected_clues.append(clue_id)

def draw_clue_inventory():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((10, 10, 15))
    screen.blit(overlay, (0, 0))

    title = title_font.render("CLUE INVENTORY", True, (255, 220, 120))
    title_rect = title.get_rect(center = (WIDTH // 2, 130))
    screen.blit(title, title_rect)

    instruction = small_font.render("Press I to close", True, (220, 220, 220))
    instruction_rect = instruction.get_rect(center = (WIDTH // 2, 130))
    screen.blit(instruction, instruction_rect)

    if len(collected_clues) == 0:
        empty_text = menu_font.render("No clues collected yet.", True, (255, 255, 255))
        empty_rect = empty_text.get_rect(center=(WIDTH // 2, 260))
        screen.blit(empty_text, empty_rect)
        return

    clue_box = pygame.Rect(170, 180, 860, 500)
    pygame.draw.rect(screen, (25, 25, 30), clue_box)
    pygame.draw.rect(screen, (255, 255, 255), clue_box, 3)

    y = clue_box.y + 30

    for clue_id in collected_clues:
        clue_text = clue_descriptions.get(clue_id, clue_id)

        y = draw_wrapped_text(
            screen,
            "- " + clue_text,
            font,
            (255, 255, 255),
            clue_box.x + 30,
            y,
            clue_box.width - 60
        )

        y += 20

def draw_debug_info():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_world_x = mouse_x + camera_x
    mouse_world_y = mouse_y + camera_y

    mouse_col = mouse_world_x // tile_size
    mouse_row = mouse_world_y // tile_size

    player_col = player_x // tile_size
    player_row = player_y // tile_size

    player_center_col = (player_x + player_size // 2) // tile_size
    player_center_row = (player_y + player_size // 2) // tile_size

    current_tile = "Out of Map"
    if 0 <= player_center_row < len(game_map) and 0 <= player_center_col < len(game_map[0]):
        current_tile = game_map[player_center_row][player_center_col]
    
    debug_lines = [
        "DEBUG MODE: ON",
        f"Current Era: {current_era}",
        f"Player Tile: ({player_col}, {player_row})",
        f"Player Center Tile: ({player_center_col}, {player_center_row})",
        f"Current Tile: {current_tile}",
        f"Mouse Tile: ({mouse_col}, {mouse_row})",
        f"Can Interact: {can_interact}",
        f"Current NPC: {current_npc}",
        f"FPS: {int(clock.get_fps())}"
    ]

    debug_box = pygame.Rect(20, 300, 420, 260)
    pygame.draw.rect(screen, (0, 0, 0), debug_box)
    pygame.draw.rect(screen, (255, 255, 0), debug_box, 2)

    y = debug_box.y + 15

    for line in debug_lines:
        text_surface = small_font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (debug_box.x + 15, y))
        y += 25


#6. Main Game Loop
running = True
while running:
    clock.tick(60) # fps

    # A. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Menu Part
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if game_state == "menu":
                    if start_button.collidepoint(event.pos):
                        game_state = "playing"

                    elif credits_button.collidepoint(event.pos):
                        game_state = "credits"

                    elif quit_button.collidepoint(event.pos):
                        running = False

                elif game_state == "credits":
                    if back_button.collidepoint(event.pos):
                        game_state = "menu"

                elif game_state == "playing":
                    if game_exit_button.collidepoint(event.pos):
                        running = False
                
                elif game_state == "pause":
                    if resume_button.collidepoint(event.pos):
                        game_state = "playing"
                    
                    elif main_menu_button.collidepoint(event.pos):
                        game_state = "menu"

                    elif pause_quit_button.collidepoint(event.pos):
                        running = False

        if game_state == "playing":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    show_clue_inventory = not show_clue_inventory

                elif event.key == pygame.K_e:
                    if not dialogue_active and not show_clue_inventory and can_interact:
                        if current_npc in dialogue_data:
                            npc_data = dialogue_data[current_npc]

                            current_dialogue = npc_data["dialogue"]
                            current_quest = npc_data.get("quest")
                            current_clue = npc_data.get("clue")

                            dialogue_active = True
                            dialogue_index = 0
                            dialogue_text_shown = ""
                            text_counter = 0

                elif event.key == pygame.K_F3:
                    debug_mode = not debug_mode

                elif event.key == pygame.K_ESCAPE:
                    game_state = "pause"

                elif event.key == pygame.K_SPACE:
                    if dialogue_active and dialogue_index < len(current_dialogue):
                        current_line = current_dialogue[dialogue_index]

                        if isinstance(current_line, dict):
                            full_text = current_line["text"]
                        else:
                            full_text = current_line

                        if dialogue_text_shown != full_text:
                            dialogue_text_shown = full_text
                        else:
                            dialogue_index += 1
                            text_counter = 0
                            dialogue_text_shown = ""

                            if dialogue_index >= len(current_dialogue):
                                dialogue_active = False

                                if current_quest:
                                    quest_log[current_quest] = "started"
                                    add_quest(current_quest)
                                    current_quest = None

                                if current_clue:
                                    add_clue(current_clue)
                                    current_clue = None


    #Menu Part
    if game_state == "menu":
        draw_main_menu()
        pygame.display.update()
        continue
    elif game_state == "credits":
        draw_credits_screen()
        pygame.display.update()
        continue
    elif game_state == "pause":
        draw_pause_menu()
        pygame.display.update()
        continue


    # B. Movement Logic
    new_x = player_x
    new_y = player_y

    if not dialogue_active and not show_clue_inventory:
        hotkeys = pygame.key.get_pressed()

        if hotkeys[pygame.K_w]:
            new_y -= speed
        if hotkeys[pygame.K_s]:
            new_y += speed
        if hotkeys[pygame.K_a]:
            new_x -= speed
        if hotkeys[pygame.K_d]:
            new_x += speed

    # Move X
    if not check_collision(new_x, player_y, game_map):
        player_x = new_x

    # Move Y
    if not check_collision(player_x, new_y, game_map):
        player_y = new_y

    # Camera
    camera_x = player_x - (WIDTH // 2)
    camera_y = player_y - (HEIGHT // 2)

    map_pixel_width = len(game_map[0]) * tile_size
    map_pixel_height = len(game_map) * tile_size

    camera_x = max(0, min(camera_x, map_pixel_width - WIDTH))
    camera_y = max(0, min(camera_y, map_pixel_height - HEIGHT))

    player_col = player_x // tile_size
    player_row = player_y // tile_size

    # NPC detection
    can_interact = False
    current_npc = None

    for npc_row in range(player_row - 1, player_row + 2):
        for npc_col in range(player_col - 1, player_col + 2):
            if 0 <= npc_row < len(game_map) and 0 <= npc_col < len(game_map[0]):
                if game_map[npc_row][npc_col] == "5":
                    can_interact = True
                    current_npc = (current_era, npc_col, npc_row)

    # Fog of war
    reveal_radius = 3
    for fog_row in range(player_row - reveal_radius, player_row + reveal_radius + 1):
        for fog_col in range(player_col - reveal_radius, player_col + reveal_radius + 1):
            if 0 <= fog_row < len(game_map) and 0 <= fog_col < len(game_map[0]):
                visited_map[fog_row][fog_col] = True

    # C. Teleportation Logic & Door Logic
    player_center_x = player_x + player_size // 2
    player_center_y = player_y + player_size // 2

    tile_col = player_center_x // tile_size
    tile_row = player_center_y // tile_size

    if 0 <= tile_row < len(game_map) and 0 <= tile_col < len(game_map[0]):
        current_tile = game_map[tile_row][tile_col]

        if current_tile == "4":
            if current_era == "Museum":
                transition_to(era_1920s_map, "1920s", 14, 12)
            elif current_era == "1920s":
                transition_to(era_1950s_map, "1950s", 14, 12)
            elif current_era == "1950s":
                transition_to(era_1960s_map, "1960s", 14, 13)
            elif current_era == "1960s":
                transition_to(era_1980s_map, "1980s", 14, 7)
            elif current_era == "1980s":
                transition_to(era_1990s_map, "1990s", 14, 13)
            else:
                transition_to(museum_map, "Museum", 30, 15)

        elif current_tile == "2":
            key = (current_era, tile_col, tile_row)

            if key in building_data:
                building = building_data[key]

                transition_to(
                    building["target_map"],
                    building["name"],
                    building["spawn"][0],
                    building["spawn"][1]
                )

    # Typewriter effect
    if dialogue_active:
        if dialogue_index < len(current_dialogue):
            current_line = current_dialogue[dialogue_index]

            if isinstance(current_line, dict):
                full_text = current_line["text"]
            else:
                full_text = current_line

            if text_counter < len(full_text):
                text_counter += text_speed
                dialogue_text_shown = full_text[:text_counter]

    # D. Drawing
    screen.fill((10, 20, 20))

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            world_x = col_index * tile_size
            world_y = row_index * tile_size

            screen_x = world_x - camera_x
            screen_y = world_y - camera_y

            if -tile_size < screen_x < WIDTH and -tile_size < screen_y < HEIGHT:
                if tile == "1":
                    pygame.draw.rect(screen, (90, 90, 90), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "2":
                    pygame.draw.rect(screen, (101, 67, 33), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "3":
                    screen.blit(tree_img, (screen_x, screen_y))
                elif tile == "4":
                    pygame.draw.rect(screen, (200, 150, 50), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "5":
                    pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "6":
                    pygame.draw.rect(screen, (255, 20, 147), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "9":
                    pygame.draw.rect(screen, (101, 67, 33), (screen_x, screen_y, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, (200, 200, 200), (screen_x, screen_y, tile_size, tile_size))

                # Grid lines
                pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, tile_size, tile_size), 1)

    # Draw Player
    screen.blit(duck_img, (player_x - camera_x, player_y - camera_y))

    # Mini-map
    mini_tile = 5
    map_width = len(game_map[0]) * mini_tile
    start_x = WIDTH - map_width - 20
    start_y = 20

    pygame.draw.rect(screen, (30, 30, 30), (start_x - 2, start_y - 2, map_width + 4, len(game_map) * mini_tile + 4))

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if visited_map[row_index][col_index]:
                mini_x = start_x + (col_index * mini_tile)
                mini_y = start_y + (row_index * mini_tile)

                if tile == "1":
                    pygame.draw.rect(screen, (150, 150, 150), (mini_x, mini_y, mini_tile, mini_tile))
                elif tile == "4":
                    pygame.draw.rect(screen, (200, 150, 50), (mini_x, mini_y, mini_tile, mini_tile))
                else:
                    pygame.draw.rect(screen, (70, 70, 70), (mini_x, mini_y, mini_tile, mini_tile))

    player_mini_x = start_x + (player_x // tile_size) * mini_tile
    player_mini_y = start_y + (player_y // tile_size) * mini_tile
    pygame.draw.circle(screen, (0, 255, 0), (player_mini_x + mini_tile // 2, player_mini_y + mini_tile // 2), 3)

    era_label = font.render(f"TIMELINE: {current_era}", True, (255, 255, 0))
    screen.blit(era_label, (20, 20))

    draw_quest_navigation()

    fps_label = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_label, (20, 50))

    if can_interact and not dialogue_active:
        hint = font.render("Press E", True, (255, 255, 255))
        screen.blit(hint, (player_x - camera_x, player_y - camera_y - 30))

    if dialogue_active:
        box_height = 150
        box_rect = pygame.Rect(50, HEIGHT - box_height - 30, WIDTH - 100, box_height)

        pygame.draw.rect(screen, (0, 0, 0), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)

        if dialogue_index < len(current_dialogue):
            current_line = current_dialogue[dialogue_index]

            if isinstance(current_line, dict):
                speaker = current_line.get("speaker", "")
            else:
                speaker = ""

            speaker_text = font.render(speaker, True, (255, 255, 0))
            rendered_text = font.render(dialogue_text_shown, True, (255, 255, 255))

            screen.blit(speaker_text, (box_rect.x + 20, box_rect.y + 20))
            screen.blit(rendered_text, (box_rect.x + 20, box_rect.y + 55))

        hint = font.render("SPACE to continue", True, (200, 200, 200))
        screen.blit(hint, (box_rect.x + 20, box_rect.y + 105))
    
    if debug_mode:
        draw_debug_info()

    if show_clue_inventory:
        draw_clue_inventory()
        
    pygame.display.update()

pygame.quit()
#4/19/2026 and Earlier dates
#Summary on what I have done in my part for the games:
#Refactored the Architecture, Resolution Upgrade
#Mega Map Installation, Museum and 1920s Jazz Age, Scrolling Camera, Camera Clamping
#Teleportation System, Fog of War Mini-Map, Scene Transitions