import pygame
import json
import os
from data.maps import * 
from data.buildings import building_data
from data.dialogues import dialogue_data, item_dialogue_data, era_dialogues
from data.quests import quest_descriptions, clue_descriptions
from data.music import play_music, stop_music, set_music_volume
from minigame_1920s import run_minigame as run_1920s_minigame
from minigame_1950s import run_minigame as run_1950s_minigame
from minigame_1960s import run_minigame as run_1960s_minigame
from minigame_1980s import run_minigame as run_1980s_minigame

DB_FILE = "players.json"

map_lookup = {
    "Museum": museum_map,
    "1920s": era_1920s_map,
    "1950s": era_1950s_map,
    "1960s": era_1960s_map,
    "1980s": era_1980s_map
    
}

npc_map = {
    ("Museum", 3, 2): "manager",

    ("1920s", 13, 6): "elegant_woman",
    ("1920s", 19, 11): "rich_gentleman",

    ("1950s", 13, 3): "gallery_host",

    ("1960s", 4, 7): "fashion_enthusiast",
    ("1960s", 23, 7): "gallery_staff",

    ("1980s", 13, 13): "fashion_curator",
    ("1980s", 14, 2): "archive_staff",

    ("1990s", 13, 3): "curator_assistant",
    ("1990s", 14, 2): "senior_curator",
    ("1990s", 13, 12): "visitor",
}

def load_database():
    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_database(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_profile_data(profile_name):
    global player_x, player_y, current_era
    global active_quests, completed_quests, current_user, collected_items
    global game_map, visited_map

    db = load_database()
    current_user = profile_name

    if profile_name not in db:
        db[profile_name] = {
            "player_x": 1500,
            "player_y": 1600,
            "current_era": "Museum",
            "active_quests": [],
            "completed_quests": [],
            "collected_items": []
        }
        save_database(db)

    player_x = db[profile_name]["player_x"]
    player_y = db[profile_name]["player_y"]
    current_era = db[profile_name]["current_era"]
    active_quests = db[profile_name]["active_quests"]
    completed_quests = db[profile_name]["completed_quests"]
    collected_items = db[profile_name].get("collected_items", [])

    game_map = map_lookup.get(current_era, museum_map)

    visited_map = [
        [False for _ in range(len(game_map[0]))]
        for _ in range(len(game_map))
    ]

    play_music(current_era)


def save_current_profile():
    if current_user == "":
        return

    db = load_database()

    db[current_user]["player_x"] = player_x
    db[current_user]["player_y"] = player_y
    db[current_user]["current_era"] = current_era
    db[current_user]["active_quests"] = active_quests
    db[current_user]["completed_quests"] = completed_quests
    db[current_user]["collected_items"] = collected_items

    save_database(db)

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
current_user = ""

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

profile_1_btn = pygame.Rect(WIDTH // 2 - 150, 300, 300, 60)
profile_2_btn = pygame.Rect(WIDTH // 2 - 150, 380, 300, 60)
profile_3_btn = pygame.Rect(WIDTH // 2 - 150, 460, 300, 60)

seen_self_dialogues = set()
dialogue_active = False
current_dialogue = []
dialogue_index = 0
dialogue_text_shown = ""
text_speed = 2
text_counter = 0

minigame_after_dialogue = None

minigames = {
    "1920s": run_1920s_minigame,
    "1950s": run_1950s_minigame,
    "1960s": run_1960s_minigame,
    "1980s": run_1980s_minigame,
    
}

required_npcs_by_era = {
    "1920s": ["elegant_woman", "rich_gentleman"],
    "1950s": ["gallery_host"],
    "1960s": ["fashion_enthusiast", "gallery_staff"],
    "1980s": ["fashion_curator", "archive_staff"],
    "1990s": ["curator_assistant", "senior_curator", "visitor"]
}

talked_to_npcs = []
current_dialogue_npc = None
completed_minigames = []


collected_clues = []
current_clue = None
show_clue_inventory = False

collected_items = []
current_item_quest = None

show_item_choice = False
current_item_choice_era = ""
choice_items_rects = []

wrong_choice_text = ""
wrong_choice_timer = 0

current_item_quest = None

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

item_descriptions = {
    "gogo_boots_recovered": "Go-Go Boots - A stolen artifact recovered from the wrong era.",
    "acid_wash_denim_jacket_recovered": "Acid Wash Denim Jacket - A fashion piece hidden in the 1950s.",
    "flannel_shirt_recovered": "Flannel Shirt - A checkered shirt hidden in the 1960s.",
    "bowling_shirt_recovered": "Bowling Shirt - A casual shirt hidden in the 1980s.",
    "pearl_necklace_recovered": "Pearl Necklace - The final accessory recovered from the 1990s."
}

current_era = "Museum"
game_map = museum_map #Starting at the Museum


#Fog of war 
visited_map = [[False for _ in range(len(museum_map[0]))] for _ in range(len(museum_map))]


#3. Player Variables
player_size = 60
speed = 10 #pixels per movement per frame


#4. Images
player_img = pygame.image.load("Images/main_character_120x120.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (120, 120))

tree_img = pygame.image.load("Images/pixel_tree.jpg").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size))

menu_bg_img = pygame.image.load("Images/menu_game.png").convert()
menu_bg_img = pygame.transform.scale(menu_bg_img, (WIDTH, HEIGHT))

credits_bg_img = pygame.image.load("Images/credits.png").convert()
credits_bg_img = pygame.transform.scale(credits_bg_img, (WIDTH, HEIGHT))

era_backgrounds = {}

era_backgrounds["Museum"] = pygame.image.load("Images/museum_map.jpeg").convert()
era_backgrounds["1920s"] = pygame.image.load("Images/eras_1920s_Background.jpeg").convert()
era_backgrounds["1950s"] = pygame.image.load("Images/eras_1950s_Backgrounds.jpeg").convert()
era_backgrounds["1960s"] = pygame.image.load("Images/eras_1960s_Backgrounds.jpeg").convert()
era_backgrounds["1980s"] = pygame.image.load("Images/eras_1980s_Backgrounds.jpeg").convert()

scaled_era_backgrounds = {}
for era_name,bg_img in era_backgrounds.items():
    era_map = map_lookup [era_name]

    map_pixel_width = len(era_map[0]) * tile_size
    scaled_era_backgrounds[era_name] = pygame.transform.scale(bg_img, (map_pixel_width, len(era_map) * tile_size))

def load_npc_image(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (90, 120))

npc_images = {
    "manager": load_npc_image("Images/manager.png"),
    "elegant_woman": load_npc_image("Images/elegant-woman.png"),
    "rich_gentleman": load_npc_image("Images/rich-gentleman.png"),
    "gallery_host": load_npc_image("Images/gallery-host.png"),
    "fashion_enthusiast": load_npc_image("Images/fashion-enthusiast.png"),
    "gallery_staff": load_npc_image("Images/gallery-staff.png"),
    "curator_assistant": load_npc_image("Images/curator-assistant.png"),
    "visitor": load_npc_image("Images/visitor.png"),
    "senior_curator": load_npc_image("Images/senior-curator.png"),
}

ITEM_FOLDER = os.path.join("Images")

def load_item_image(filename, width=65, height=65):
    path = os.path.join(ITEM_FOLDER, filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (width, height))

item_images = {
    "1950_pants_1": load_item_image("1950pants.jpeg"),
    "1950_pants_2": load_item_image("1950pants2.jpeg"),
    "1950_pants_3": load_item_image("1950pants3.jpeg"),
    "1950_pants_4": load_item_image("1950pants4.jpeg"),

    "1960_shirt_1": load_item_image("1960shirt1.jpeg"),
    "1960_shirt_2": load_item_image("1960shirt2.jpeg"),
    "1960_shirt_3": load_item_image("1960shirt3.jpeg"),
    "1960_shirt_4": load_item_image("1960shirt4.jpeg"),

    "1980_shirt_1": load_item_image("1980shirt1.jpeg"),
    "1980_shirt_2": load_item_image("1980shirt2.jpeg"),
    "1980_shirt_3": load_item_image("1980shirt3.jpeg"),
    "1980_shirt_4": load_item_image("1980shirt4.jpeg"),

    "1990_necklace_1": load_item_image("1990necklace1.jpeg"),
    "1990_necklace_2": load_item_image("1990necklace2.jpeg"),
    "1990_necklace_3": load_item_image("1990necklace3.jpeg"),
    "1990_necklace_4": load_item_image("1990necklace4.jpeg"),

    "boots_1": load_item_image("boots1.jpeg"),
    "boots_2": load_item_image("boots2.jpeg"),
    "boots_3": load_item_image("boots3.jpeg"),
    "boots_4": load_item_image("boots4.jpeg"),
}

display_item_groups = {
    "1920s":{
        "box_col": 20,
        "box_row": 3,
        "items": ["boots_1", "boots_2", "boots_3", "boots_4"]
    },

    "1950s": {
        "box_col": 4,
        "box_row": 4,
        "items": ["1950_pants_1", "1950_pants_2", "1950_pants_3", "1950_pants_4"]
    },
    
    "1960s": {
        "box_col": 10,
        "box_row": 4,
        "items": ["1960_shirt_1", "1960_shirt_2", "1960_shirt_3", "1960_shirt_4"]
    },

    "1980s": {
        "box_col": 3,
        "box_row": 9,
        "items": ["1980_shirt_1", "1980_shirt_2", "1980_shirt_3", "1980_shirt_4"]
    },

    "1990s": {
        "box_col": 19,
        "box_row": 3,
        "items": ["1990_necklace_1", "1990_necklace_2", "1990_necklace_3", "1990_necklace_4"]
    },
}


npc_images = {
    "manager": load_npc_image("Images/manager.png"),
    "elegant_woman": load_npc_image("Images/elegant-woman.png"),
    "rich_gentleman": load_npc_image("Images/rich-gentleman.png"),
    "gallery_host": load_npc_image("Images/gallery-host.png"),
    "fashion_enthusiast": load_npc_image("Images/fashion-enthusiast.png"),
    "gallery_staff": load_npc_image("Images/gallery-staff.png"),
    "curator_assistant": load_npc_image("Images/curator-assistant.png"),
    "visitor": load_npc_image("Images/visitor.png"),
    "senior_curator": load_npc_image("Images/senior-curator.png"),
}


ITEM_FOLDER = os.path.join("Images")

def load_item_image(filename, width=65, height=65):
    path = os.path.join(ITEM_FOLDER, filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, (width, height))


item_images = {
    "1950_pants_1": load_item_image("1950pants.jpeg"),
    "1950_pants_2": load_item_image("1950pants2.jpeg"),
    "1950_pants_3": load_item_image("1950pants3.jpeg"),
    "1950_pants_4": load_item_image("1950pants4.jpeg"),

    "1960_shirt_1": load_item_image("1960shirt1.jpeg"),
    "1960_shirt_2": load_item_image("1960shirt2.jpeg"),
    "1960_shirt_3": load_item_image("1960shirt3.jpeg"),
    "1960_shirt_4": load_item_image("1960shirt4.jpeg"),

    "1980_shirt_1": load_item_image("1980shirt1.jpeg"),
    "1980_shirt_2": load_item_image("1980shirt2.jpeg"),
    "1980_shirt_3": load_item_image("1980shirt3.jpeg"),
    "1980_shirt_4": load_item_image("1980shirt4.jpeg"),

    "1990_necklace_1": load_item_image("1990necklace1.jpeg"),
    "1990_necklace_2": load_item_image("1990necklace2.jpeg"),
    "1990_necklace_3": load_item_image("1990necklace3.jpeg"),
    "1990_necklace_4": load_item_image("1990necklace4.jpeg"),

    "boots_1": load_item_image("boots1.jpeg"),
    "boots_2": load_item_image("boots2.jpeg"),
    "boots_3": load_item_image("boots3.jpeg"),
    "boots_4": load_item_image("boots4.jpeg"),
}

display_item_groups = {
    "1920s": {
        "box_col": 20,
        "box_row": 3,
        "items": ["boots_1", "boots_2", "boots_3", "boots_4"],
        "correct_item": "boots_2",
        "dialogue_key": ("1920s", 10, 4),
        "artifact_id": "gogo_boots_recovered"
    },

    "1950s": {
        "box_col": 4,
        "box_row": 4,
        "items": ["1950_pants_1", "1950_pants_2", "1950_pants_3", "1950_pants_4"],
        "correct_item": "1950_pants_4",
        "dialogue_key": ("1950s", 10, 4),
        "artifact_id": "acid_wash_denim_jacket_recovered"
    },

    "1960s": {
        "box_col": 10,
        "box_row": 4,
        "items": ["1960_shirt_1", "1960_shirt_2", "1960_shirt_3", "1960_shirt_4"],
        "correct_item": "1960_shirt_1",
        "dialogue_key": ("1960s", 10, 4),
        "artifact_id": "flannel_shirt_recovered"
    },

    "1980s": {
        "box_col": 3,
        "box_row": 9,
        "items": ["1980_shirt_1", "1980_shirt_2", "1980_shirt_3", "1980_shirt_4"],
        "correct_item": "1980_shirt_1",
        "dialogue_key": ("1980s", 10, 4),
        "artifact_id": "bowling_shirt_recovered"
    },

    "1990s": {
        "box_col": 19,
        "box_row": 3,
        "items": ["1990_necklace_1", "1990_necklace_2", "1990_necklace_3", "1990_necklace_4"],
        "correct_item": "1990_necklace_1",
        "dialogue_key": ("1990s", 10, 4),
        "artifact_id": "pearl_necklace_recovered"
    },
}

map_item_pictures = [
    # 1920s shoes display
    {"era": "1920s", "image": "boots_1", "col": 10, "row": 4, "offset_x": 0, "offset_y": 0},
    {"era": "1920s", "image": "boots_2", "col": 10, "row": 4, "offset_x": 75, "offset_y": 0},
    {"era": "1920s", "image": "boots_3", "col": 10, "row": 4, "offset_x": 0, "offset_y": 75},
    {"era": "1920s", "image": "boots_4", "col": 10, "row": 4, "offset_x": 75, "offset_y": 75},

    # 1950s denim display
    {"era": "1950s", "image": "1950_pants_1", "col": 10, "row": 4, "offset_x": 0, "offset_y": 0},
    {"era": "1950s", "image": "1950_pants_2", "col": 10, "row": 4, "offset_x": 75, "offset_y": 0},
    {"era": "1950s", "image": "1950_pants_3", "col": 10, "row": 4, "offset_x": 0, "offset_y": 75},
    {"era": "1950s", "image": "1950_pants_4", "col": 10, "row": 4, "offset_x": 75, "offset_y": 75},

    # 1960s shirt display
    {"era": "1960s", "image": "1960_shirt_1", "col": 10, "row": 4, "offset_x": 0, "offset_y": 0},
    {"era": "1960s", "image": "1960_shirt_2", "col": 10, "row": 4, "offset_x": 75, "offset_y": 0},
    {"era": "1960s", "image": "1960_shirt_3", "col": 10, "row": 4, "offset_x": 0, "offset_y": 75},
    {"era": "1960s", "image": "1960_shirt_4", "col": 10, "row": 4, "offset_x": 75, "offset_y": 75},

    # 1980s shirt display
    {"era": "1980s", "image": "1980_shirt_1", "col": 10, "row": 4, "offset_x": 0, "offset_y": 0},
    {"era": "1980s", "image": "1980_shirt_2", "col": 10, "row": 4, "offset_x": 75, "offset_y": 0},
    {"era": "1980s", "image": "1980_shirt_3", "col": 10, "row": 4, "offset_x": 0, "offset_y": 75},
    {"era": "1980s", "image": "1980_shirt_4", "col": 10, "row": 4, "offset_x": 75, "offset_y": 75},

    # 1990s necklace display
    {"era": "1990s", "image": "1990_necklace_1", "col": 10, "row": 4, "offset_x": 0, "offset_y": 0},
    {"era": "1990s", "image": "1990_necklace_2", "col": 10, "row": 4, "offset_x": 75, "offset_y": 0},
    {"era": "1990s", "image": "1990_necklace_3", "col": 10, "row": 4, "offset_x": 0, "offset_y": 75},
    {"era": "1990s", "image": "1990_necklace_4", "col": 10, "row": 4, "offset_x": 75, "offset_y": 75},
]

#5. Functions (Logic)

def teleport_is_unlocked(era_name):
    #museum portal must remain available to enter 1920s
    if era_name == "Museum":
        return True
    group = display_item_groups.get(era_name)

    if not group:
        return False
    artifact_collected =group ["artifact_id"] in collected_items
    minigame_completed = era_name in completed_minigames

    return artifact_collected and minigame_completed


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

def start_self_dialogue(era_name):
    global dialogue_active, current_dialogue, dialogue_index
    global dialogue_text_shown, text_counter
    global current_quest, current_clue
    global minigame_after_dialogue


    if era_name in era_dialogues and era_name not in seen_self_dialogues:
        current_dialogue = [
            {"speaker": "PLAYER", "text": line}
            for line in era_dialogues[era_name]
        ]

        dialogue_active = True
        dialogue_index = 0
        dialogue_text_shown = ""
        text_counter = 0
    
        current_quest = None
        current_clue = None

        seen_self_dialogues.add(era_name)


def transition_to(new_map_array, new_era_name, spawn_tile_x, spawn_tile_y):
    global game_map, current_era, player_x, player_y, visited_map
    global dialogue_active, current_dialogue, dialogue_index
    global dialogue_text_shown, text_counter
    global current_quest, current_clue

    game_map = new_map_array
    current_era = new_era_name
    play_music(current_era)

    player_x = spawn_tile_x * tile_size
    player_y = spawn_tile_y * tile_size

    visited_map = [[False for _ in range(len(game_map[0]))] for _ in range(len(game_map))]

    start_self_dialogue(new_era_name)

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
    screen.blit(menu_bg_img, (0, 0))

    draw_button(start_button, "Start Game")
    draw_button(credits_button, "Credits")
    draw_button(quit_button, "Quit")
    
    footer_text = small_font.render(
        "for the fashion and detective enthusiasts. (c) 2024 Style Heist - Group 15",
        True,
        (160, 160, 160)
    )
    footer_rect = footer_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(footer_text, footer_rect)

def draw_profiles_screen():
    screen.blit(credits_bg_img, (0, 0)) 
    
    title_text = title_font.render("SELECT PROFILE", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 180))
    screen.blit(title_text, title_rect)
    
    draw_button(profile_1_btn, "Save Slot 1")
    draw_button(profile_2_btn, "Save Slot 2")
    draw_button(profile_3_btn, "Save Slot 3")
    draw_button(back_button, "Back")


def draw_credits_screen():
    screen.blit(credits_bg_img, (0, 0))

    title_text = title_font.render("CREDITS", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 140))
    screen.blit(title_text, title_rect)

    credit_lines = [
        "Style Heist - Group 15",
        "Sample Line",
        "Programming / Game Systems: Alvin",
        "UI Design Contributor: Azaleia",
        "Dialogue / Story Contributor: Balqish",
        "",
        "Built using Python and Pygame"
    ]

    y = 230
    for line in credit_lines:
        text_surface = menu_font.render(line, True, (0, 0, 0))
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

def add_items(item_id):
    if item_id and item_id not in collected_items:
        collected_items.append(item_id)

def draw_clue_inventory():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((10, 10, 15))
    screen.blit(overlay, (0, 0))

    title = title_font.render("EVIDENCE INVENTORY", True, (255, 220, 120))
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    instruction = small_font.render("Press I to close", True, (220, 220, 220))
    instruction_rect = instruction.get_rect(center=(WIDTH // 2, 140))
    screen.blit(instruction, instruction_rect)

    inventory_box = pygame.Rect(140, 180, 920, 520)
    pygame.draw.rect(screen, (25, 25, 30), inventory_box)
    pygame.draw.rect(screen, (255, 255, 255), inventory_box, 3)

    y = inventory_box.y + 30

    # ==================
    # CLUES SECTION
    # ==================
    clue_title = menu_font.render("CLUES COLLECTED", True, (255, 255, 0))
    screen.blit(clue_title, (inventory_box.x + 30, y))
    y += 55

    if len(collected_clues) == 0:
        empty_text = font.render("No clues collected yet.", True, (200, 200, 200))
        screen.blit(empty_text, (inventory_box.x + 30, y))
        y += 40
    else:
        for clue_id in collected_clues:
            clue_text = clue_descriptions.get(clue_id, clue_id)

            y = draw_wrapped_text(
                screen,
                "- " + clue_text,
                font,
                (255, 255, 255),
                inventory_box.x + 30,
                y,
                inventory_box.width - 60
            )
            y += 10

    y += 30

    # ==================
    # ARTIFACT SECTION
    # ==================
    item_title = menu_font.render("RECOVERED ARTIFACTS", True, (255, 255, 0))
    screen.blit(item_title, (inventory_box.x + 30, y))
    y += 55

    if len(collected_items) == 0:
        empty_text = font.render("No artifacts recovered yet.", True, (200, 200, 200))
        screen.blit(empty_text, (inventory_box.x + 30, y))
    else:
        for item_id in collected_items:
            item_text = item_descriptions.get(item_id, item_id)

            y = draw_wrapped_text(
                screen,
                "- " + item_text,
                font,
                (255, 255, 255),
                inventory_box.x + 30,
                y,
                inventory_box.width - 60
            )
            y += 10

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

def draw_map_item_pictures():
    for item in map_item_pictures:
        if item["era"] == current_era:
            world_x = item["col"] * tile_size + item["offset_x"]
            world_y = item["row"] * tile_size + item["offset_y"]

            screen_x = world_x - camera_x
            screen_y = world_y - camera_y

            item_img = item_images[item["image"]]
            screen.blit(item_img, (screen_x, screen_y))

def draw_display_item_groups():
    if current_era not in display_item_groups:
        return

    group = display_item_groups[current_era]

    box_x = group["box_col"] * tile_size - camera_x
    box_y = group["box_row"] * tile_size - camera_y

    item_size = 55
    gap = 20

    positions = [
        (box_x + 10, box_y + 10),
        (box_x + 10 + item_size + gap, box_y + 10),
        (box_x + 10, box_y + 10 + item_size + gap),
        (box_x + 10 + item_size + gap, box_y + 10 + item_size + gap),
    ]

    for index, item_key in enumerate(group["items"]):
        item_img = pygame.transform.smoothscale(item_images[item_key], (item_size, item_size))
        screen.blit(item_img, positions[index])

def add_item(item_id):
    if item_id and item_id not in collected_items:
        collected_items.append(item_id)

def draw_display_item_groups():
    if current_era not in display_item_groups:
        return
    
    group = display_item_groups[current_era]

    if group["artifact_id"] in completed_quests:
        return
    
    box_x = group["box_col"] * tile_size - camera_x
    box_y = group["box_row"] * tile_size - camera_y

    item_size = 55
    gap = 20

    positions = [
        (box_x + 10, box_y + 10),
        (box_x + 10 + item_size + gap, box_y + 10),
        (box_x + 10, box_y + 10 + item_size + gap),
        (box_x + 10 + item_size + gap, box_y + 10 + item_size + gap),
    ]

    for index, item_key in enumerate(group["items"]):
        item_img = pygame.transform.smoothscale(item_images[item_key], (item_size, item_size))
        screen.blit(item_img, positions[index])

def has_talked_to_all_npcs(era_name):
    required_npcs = required_npcs_by_era.get(era_name, [])

    return bool(required_npcs) and all (
        f"{era_name}:{npc_name}" in talked_to_npcs
        for npc_name in required_npcs
    )

def get_nearby_item_group():
    if current_era not in display_item_groups:
        return None
    
    group = display_item_groups[current_era]

    #player has to talk to every npc first before going to find the artifacts
    if not has_talked_to_all_npcs(current_era):
        return None

    if group["artifact_id"] in completed_quests:
        return None
    
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    box_world_x = group["box_col"] * tile_size
    box_world_y = group["box_row"] * tile_size

    display_rect = pygame.Rect(box_world_x, box_world_y, 160, 160)

    if player_rect.colliderect(display_rect.inflate(100, 100)):
        return current_era

    return None

def open_item_choice(era_name):
    global show_item_choice, current_item_choice_era
    global wrong_choice_text, wrong_choice_timer
    
    show_item_choice = True
    current_item_choice_era = era_name
    wrong_choice_text = ""
    wrong_choice_timer = 0

def choose_artifact_item(item_key):
    global show_item_choice, wrong_choice_text, wrong_choice_timer
    global dialogue_active, current_dialogue, dialogue_index
    global dialogue_text_shown, text_counter
    global current_item_quest

    if current_item_choice_era not in display_item_groups:
        return
    
    group = display_item_groups[current_item_choice_era]

    if item_key != group["correct_item"]:
        wrong_choice_text = "Wrong item. This one belongs here. Look for the item"
        wrong_choice_timer = 120
        return
    
    dialogue_key = group["dialogue_key"]

    if dialogue_key in item_dialogue_data:
        item_data = item_dialogue_data[dialogue_key]

        current_dialogue = item_data["dialogue"]
        current_item_quest = item_data.get("quest")

        dialogue_active = True
        dialogue_index = 0
        dialogue_text_shown = ""
        text_counter = 0

        show_item_choice = False
    
def draw_item_choice_screen():
    global choice_item_rects, wrong_choice_timer

    if not show_item_choice:
        return

    if current_item_choice_era not in display_item_groups:
        return

    group = display_item_groups[current_item_choice_era]

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(230)
    overlay.fill((10, 10, 15))
    screen.blit(overlay, (0, 0))

    title = title_font.render("CHOOSE THE ARTIFACT", True, (255, 220, 120))
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    instruction = small_font.render(
        "Click an item or press 1 - 4. Press ESC to cancel.",
        True,
        (220, 220, 220)
    )
    instruction_rect = instruction.get_rect(center=(WIDTH // 2, 145))
    screen.blit(instruction, instruction_rect)

    choice_item_rects = []

    # THIS LINE FIXES YOUR ERROR
    item_size = 120

    positions = [
        (WIDTH // 2 - 230, 220),
        (WIDTH // 2 + 90, 220),
        (WIDTH // 2 - 230, 450),
        (WIDTH // 2 + 90, 450),
    ]

    for index, item_key in enumerate(group["items"]):
        x, y = positions[index]

        item_box = pygame.Rect(x - 20, y - 20, 180, 180)

        pygame.draw.rect(screen, (35, 35, 45), item_box)
        pygame.draw.rect(screen, (255, 255, 255), item_box, 3)

        item_img = pygame.transform.smoothscale(
            item_images[item_key],
            (item_size, item_size)
        )
        screen.blit(item_img, (x, y))

        number_text = font.render(str(index + 1), True, (255, 255, 0))
        screen.blit(number_text, (item_box.x + 10, item_box.y + 10))

        choice_items_rects.append((item_box, item_key))

    if wrong_choice_timer > 0:
        wrong_surface = font.render(wrong_choice_text, True, (255, 80, 80))
        wrong_rect = wrong_surface.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        screen.blit(wrong_surface, wrong_rect)

        wrong_choice_timer -= 1


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
                        game_state = "profiles"

                    elif credits_button.collidepoint(event.pos):
                        game_state = "credits"

                    elif quit_button.collidepoint(event.pos):
                        save_current_profile()
                        running = False

                elif game_state == "profiles":
                    if profile_1_btn.collidepoint(event.pos):
                        load_profile_data("Profile_1")
                        game_state = "playing"
                        start_self_dialogue(current_era)
                        
                    elif profile_2_btn.collidepoint(event.pos):
                        load_profile_data("Profile_2")
                        game_state = "playing"
                        start_self_dialogue(current_era)
                        
                    elif profile_3_btn.collidepoint(event.pos):
                        load_profile_data("Profile_3")
                        game_state = "playing"
                        start_self_dialogue(current_era)

                    elif back_button.collidepoint(event.pos):
                        game_state = "menu"

                elif game_state == "credits":
                    if back_button.collidepoint(event.pos):
                        game_state = "menu"

                elif game_state == "playing":
                    if show_item_choice:
                        for rect, item_key in choice_items_rects:
                            if rect.collidepoint(event.pos):
                                choose_artifact_item(item_key)
                                break

                    elif game_exit_button.collidepoint(event.pos):
                        save_current_profile()
                        running = False
                
                elif game_state == "pause":
                    if resume_button.collidepoint(event.pos):
                        game_state = "playing"
                    
                    elif main_menu_button.collidepoint(event.pos):
                        game_state = "menu"

                    elif pause_quit_button.collidepoint(event.pos):
                        save_current_profile()
                        running = False

        if game_state == "playing":
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    show_clue_inventory = not show_clue_inventory

                elif event.key == pygame.K_e:
                    if not dialogue_active and not show_clue_inventory and not show_item_choice:

        
                        if can_interact:
                            if current_npc in dialogue_data:
                                npc_data = dialogue_data[current_npc]

                                current_dialogue = npc_data["dialogue"]
                                current_quest = npc_data.get("quest")
                                current_clue = npc_data.get("clue")
                                current_dialogue_npc = current_npc

                                dialogue_active = True
                                dialogue_index = 0
                                dialogue_text_shown = ""
                                text_counter = 0

       
                        elif current_item_group:
                            open_item_choice(current_item_group)
                    
                elif show_item_choice and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    group = display_item_groups[current_item_choice_era]

                    if event.key == pygame.K_1:
                        choose_artifact_item(group["items"][0])
                    elif event.key == pygame.K_2:
                        choose_artifact_item(group["items"][1])
                    elif event.key == pygame.K_3:
                        choose_artifact_item(group["items"][2])
                    elif event.key == pygame.K_4:
                        choose_artifact_item(group["items"][3])

                elif event.key == pygame.K_F3:
                    debug_mode = not debug_mode

                elif event.key == pygame.K_ESCAPE:
                    if show_item_choice:
                        show_item_choice = False
                    else:
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

                                #record the npc after theyve complete their dialogue
                                if current_dialogue_npc:
                                    npc_record = f"{current_era}:{current_dialogue_npc}"

                                    if npc_record not in talked_to_npcs:
                                        talked_to_npcs.append(npc_record)

                                    current_dialogue_npc = None

                                #add quest from the npc dialogue
                                 
                                if current_quest:
                                    quest_log[current_quest] = "started"
                                    add_quest(current_quest)
                                    current_quest = None

                                if current_clue:
                                    add_clue(current_clue)
                                    current_clue = None

                                if current_item_quest:
                                    recovered_item = current_item_quest

                                    add_item(current_item_quest)
                                    complete_quest(current_item_quest)
                                    current_item_quest = None

                                    if(
                                        has_talked_to_all_npcs(current_era)
                                        and current_era in minigames
                                        and current_era not in completed_minigames
                                    ):
                                        minigame_function = minigames[current_era]
                                        minigame_won = minigame_function(screen, clock)
                                        if minigame_won:
                                            completed_minigames.append(current_era)
                                            print(f"Minigame for {current_era} completed!")
                                        else:
                                            print(f"Minigame for {current_era} failed. Try again   .")


                elif event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_n:
                    pygame.mixer.music.unpause()

    #Menu Part
    if game_state == "menu":
        draw_main_menu()
        pygame.display.update()
        continue
    elif game_state == "profiles":        
        draw_profiles_screen()             
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

    if not dialogue_active and not show_clue_inventory and not show_item_choice:
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


    can_interact = False
    current_npc = None

    for npc_row in range(player_row - 1, player_row + 2):
        for npc_col in range(player_col - 1, player_col + 2):

            if 0 <= npc_row < len(game_map) and 0 <= npc_col < len(game_map[0]):

                if game_map[npc_row][npc_col] == "5":
                    npc_key = (current_era, npc_col, npc_row)
                    found_npc = npc_map.get(npc_key)

                    if found_npc:
                        current_npc = found_npc
                        can_interact = True
                        break

        if can_interact:
            break

    current_item_group = get_nearby_item_group()
    can_choose_item = current_item_group is not None



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

        if current_tile == "4" and teleport_is_unlocked(current_era):

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
    
    if current_era in scaled_era_backgrounds:
        bg_img = scaled_era_backgrounds[current_era]
        screen.blit(bg_img, (-camera_x, -camera_y))

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            world_x = col_index * tile_size
            world_y = row_index * tile_size

            screen_x = world_x - camera_x
            screen_y = world_y - camera_y

            if -tile_size < screen_x < WIDTH and -tile_size < screen_y < HEIGHT:
                if tile == "1":
                    if current_era not in era_backgrounds:
                        pygame.draw.rect(screen, (90, 90, 90), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "2":
                    pygame.draw.rect(screen, (101, 67, 33), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "3":
                     if current_era not in era_backgrounds:
                        screen.blit(tree_img, (screen_x, screen_y))
                elif tile == "4":
                    if teleport_is_unlocked(current_era):
                        pygame.draw.rect(
                            screen,
                            (200,150,50),
                            (screen_x, screen_y, tile_size, tile_size)
                        )
                    elif current_era not in era_backgrounds:
                        pygame.draw.rect(
                            screen,
                            (100, 100, 100),
                            (screen_x, screen_y, tile_size, tile_size)
                        )
                    
                elif tile == "5":
                    npc_key = (current_era, col_index, row_index)
                    npc_id = npc_map.get(npc_key)

                    if npc_id in npc_images:
                        npc_img = npc_images[npc_id]
                        npc_rect = npc_img.get_rect(
                            midbottom=(screen_x + tile_size // 2, screen_y + tile_size)
                        )
                        screen.blit(npc_img, npc_rect)
                    else:
                        pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "6":
                    pygame.draw.rect(screen, (255, 20, 147), (screen_x, screen_y, tile_size, tile_size))
                elif tile == "9":
                     if current_era not in era_backgrounds:
                        pygame.draw.rect(screen, (101, 67, 33), (screen_x, screen_y, tile_size, tile_size))
                else:
                    if current_era not in era_backgrounds:
                        pygame.draw.rect(screen, (200, 200, 200), (screen_x, screen_y, tile_size, tile_size))

                # Grid lines
                if current_era not in era_backgrounds:
                    pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, tile_size, tile_size), 1)


    # Draw Player
    draw_display_item_groups()

    screen.blit(
    player_img,
    (player_x - camera_x - 30, player_y - camera_y - 30)
)
    
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
                elif tile == "4" and teleport_is_unlocked(current_era):
                    pygame.draw.rect(screen, (200, 150, 50), (mini_x, mini_y, mini_tile, mini_tile))
                
                    pygame.draw.rect(screen, (70, 70, 70), (mini_x, mini_y, mini_tile, mini_tile))

    player_mini_x = start_x + (player_x // tile_size) * mini_tile
    player_mini_y = start_y + (player_y // tile_size) * mini_tile
    pygame.draw.circle(screen, (0, 255, 0), (player_mini_x + mini_tile // 2, player_mini_y + mini_tile // 2), 3)

    era_label = font.render(f"TIMELINE: {current_era}", True, (255, 255, 0))
    screen.blit(era_label, (20, 20))

    draw_quest_navigation()

    fps_label = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_label, (20, 50))

    if (can_interact or can_choose_item) and not dialogue_active and not show_item_choice:
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

    if show_item_choice:
        draw_item_choice_screen()
        
    pygame.display.update()

pygame.quit()
#4/19/2026 and Earlier dates
#Summary on what I have done in my part for the games:
#Refactored the Architecture, Resolution Upgrade
#Mega Map Installation, Museum and 1920s Jazz Age, Scrolling Camera, Camera Clamping
#Teleportation System, Fog of War Mini-Map, Scene Transitio