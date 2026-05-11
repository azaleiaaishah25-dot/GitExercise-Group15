import pygame

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

can_interact = False
current_npc = None



#1920s arrival dialogue
arrival_1920s_dialogue = [
    {"speaker": "PLAYER", "text": "...Whoa—"},
    {"speaker": "PLAYER", "text": "..Okay.. okay.."},
    {"speaker": "PLAYER", "text": "..This is definitely not the museum anymore."},
    {"speaker": "PLAYER", "text": "Clothes.. hairstyles.. even the way they walk.."},
    {"speaker": "PLAYER", "text": "..1920s. It actually worked."},
    {"speaker": "PLAYER", "text": "I just time traveled.. because someone stole clothes."},
    {"speaker": "PLAYER", "text": "..Alright. Focus."},
    {"speaker": "PLAYER", "text": "If the thief came here.."},
    {"speaker": "PLAYER", "text": "..then the item has to be here too."},
    {"speaker": "PLAYER", "text": "And if it doesn't belong in this era.."},
    {"speaker": "PLAYER", "text": "..it should stand out."}
]

# NPC DATA
dialogue_data = {
    # =========================
    # 1920s NPC 1: Elegant Woman
    # =========================
    ("1920s", 13, 6): {
        "speaker": "Elegant Woman",
        "dialogue": [
            {"speaker": "ELEGANT WOMAN", "text": "Well now, you look like you've walked straight out of a different world."},
            {"speaker": "PLAYER", "text": "..Something like that."},
            {"speaker": "ELEGANT WOMAN", "text": "That outfit.. I don't think I've seen anything like it."},
            {"speaker": "PLAYER", "text": "I could say the same."},
            {"speaker": "ELEGANT WOMAN", "text": "Fair enough."},
            {"speaker": "ELEGANT WOMAN", "text": "You're not from around here, are you?"},
            {"speaker": "PLAYER", "text": "..I'm just passing through."},
            {"speaker": "ELEGANT WOMAN", "text": "Mmm.. mysterious. I like it."},
            {"speaker": "PLAYER", "text": "Have you seen anything.. unusual around here?"},
            {"speaker": "ELEGANT WOMAN", "text": "Unusual? In this city? Always."},
            {"speaker": "PLAYER", "text": "I mean something that doesn't belong."},
            {"speaker": "ELEGANT WOMAN", "text": "..Now that you mention it.."},
            {"speaker": "PLAYER", "text": "What?"},
            {"speaker": "ELEGANT WOMAN", "text": "There was a girl earlier."},
            {"speaker": "PLAYER", "text": "What about her?"},
            {"speaker": "ELEGANT WOMAN", "text": "She didn't quite fit in."},
            {"speaker": "PLAYER", "text": "How so?"},
            {"speaker": "ELEGANT WOMAN", "text": "She looked.. restless. Eyes darting everywhere."},
            {"speaker": "ELEGANT WOMAN", "text": "Like she was hiding something. Or planning something."},
            {"speaker": "PLAYER", "text": "Did you notice anything else?"},
            {"speaker": "ELEGANT WOMAN", "text": "..Her shoes."},
            {"speaker": "PLAYER", "text": "Shoes?"},
            {"speaker": "ELEGANT WOMAN", "text": "They were.. strange."},
            {"speaker": "ELEGANT WOMAN", "text": "Tall. White. Sleek."},
            {"speaker": "ELEGANT WOMAN", "text": "Not like anything we wear."},
            {"speaker": "CLUE", "text": "Clue discovered: Go-Go Boots."},
            {"speaker": "PLAYER", "text": "..That has to be it."},
            {"speaker": "ELEGANT WOMAN", "text": "If you find her, do let me know. I adore a bit of drama."},
            {"speaker": "PLAYER", "text": "I'll keep that in mind."}
        ],
        "quest": "clue_gogo_boots"
    },

    # =========================
    # 1920s NPC 2: Old Tailor
    # =========================
    ("1920s", 19, 11): {
        "speaker": "Old Tailor",
        "dialogue": [
            {"speaker": "OLD TAILOR", "text": "..Hmm."},
            {"speaker": "PLAYER", "text": "..Excuse me?"},
            {"speaker": "OLD TAILOR", "text": "Hold still."},
            {"speaker": "PLAYER", "text": "...What?"},
            {"speaker": "OLD TAILOR", "text": "..That stitching. That cut."},
            {"speaker": "OLD TAILOR", "text": "You remind me of someone."},
            {"speaker": "PLAYER", "text": "I do?"},
            {"speaker": "OLD TAILOR", "text": "Yes.. a young man."},
            {"speaker": "OLD TAILOR", "text": "Always asking questions about garments.. about time."},
            {"speaker": "PLAYER", "text": "..Time?"},
            {"speaker": "OLD TAILOR", "text": "He said clothing tells stories."},
            {"speaker": "OLD TAILOR", "text": "Not just of people.. but of eras."},
            {"speaker": "PLAYER", "text": "..My grandfather."},
            {"speaker": "OLD TAILOR", "text": "Ah. So you know him."},
            {"speaker": "PLAYER", "text": "He.. used to talk like that."},
            {"speaker": "OLD TAILOR", "text": "He had an eye for detail."},
            {"speaker": "OLD TAILOR", "text": "And a habit of noticing things others ignored."},
            {"speaker": "OLD TAILOR", "text": "If you're looking for something.."},
            {"speaker": "OLD TAILOR", "text": "Don't just look at what fits in."},
            {"speaker": "OLD TAILOR", "text": "Look for what doesn't."},
            {"speaker": "PLAYER", "text": "..Yeah."},
            {"speaker": "PLAYER", "text": "That sounds like him."}
        ],
        "quest": "old_tailor_hint"
    },

    # =========================
    # 1950s NPC 3: Gallery Host
    # =========================
    ("1950s", 13, 3): {
        "speaker": "Elegant Woman",
        "dialogue": [
            {"speaker": "GALLERY HOST", "text": "Well, you look a little out of place."},
            {"speaker": "PLAYER", "text": "..That obvious?"},
            {"speaker": "GALLERY HOST", "text": "Just a little."},
            {"speaker": "GALLERY HOST", "text": "Here for the exhibition?"},
            {"speaker": "PLAYER", "text": "..Something like that."},
            {"speaker": "PLAYER", "text": "I’m actually looking for something unusual."},
            {"speaker": "GALLERY HOST", "text": "Oh? In a place full of fashion?"},
            {"speaker": "PLAYER", "text": "Something that doesn’t belong to this time."},
            {"speaker": "GALLERY HOST", "text": "..You know.."},
            {"speaker": "PLAYER", "text": "What?"},
            {"speaker": "GALLERY HOST", "text": "There was a girl earlier."},
            {"speaker": "PLAYER", "text": "..A girl?"},
            {"speaker": "GALLERY HOST", "text": "Yes. Didn’t seem interested in the displays."},
            {"speaker": "GALLERY HOST", "text": "She kept looking around instead.. like she was searching for something."},
            {"speaker": "PLAYER", "text": "Did anything stand out about her?"},
            {"speaker": "GALLERY HOST", "text": "..Her pants."},
            {"speaker": "PLAYER", "text": "What about them?"},
            {"speaker": "GALLERY HOST", "text": "They didn’t match the rest of the era."},
            {"speaker": "GALLERY HOST", "text": "Faded in patches.. uneven coloring."},
            {"speaker": "GALLERY HOST", "text": "Almost like they were.. damaged on purpose."},
            {"speaker": "CLUE", "text": "Clue discovered: Acid Wash Denim"},
            {"speaker": "PLAYER", "text": "..That’s it."},
            {"speaker": "GALLERY HOST", "text": "She wandered deeper into the gallery after that."},
            {"speaker": "GALLERY HOST", "text": "Towards the back exhibits."},
        ],
        "quest": "clue_acid_wash_denim"
    },

    # =========================
    # 1960s NPC 3: Gallery Host
    # =========================
    ("1960s", 4, 7): {
        "speaker": "Fashion Enthusiast",
        "dialogue": [
            {"speaker": "FASHION ENTHUSIAST", "text": "You’re staring."},
            {"speaker": "PLAYER", "text": "..That obvious?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "In here? Yeah."},
            {"speaker": "FASHION ENTHUSIAST", "text": "And that outfit? Completely out of place."},
            {"speaker": "PLAYER", "text": "I get that a lot."},
            {"speaker": "PLAYER", "text": "I’m looking for something specific."},
            {"speaker": "FASHION ENTHUSIAST", "text": "Everyone is. What makes yours special?"},
            {"speaker": "PLAYER", "text": "It doesn’t belong in this era."},
            {"speaker": "FASHION ENTHUSIAST", "text": "..Now that’s interesting."},
            {"speaker": "FASHION ENTHUSIAST", "text": "There was someone like that earlier."},
            {"speaker": "PLAYER", "text": "A girl?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "Yes."},
            {"speaker": "FASHION ENTHUSIAST", "text": "She didn’t blend in."},
            {"speaker": "PLAYER", "text": "How so?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "Everything here is bold, intentional.."},
            {"speaker": "FASHION ENTHUSIAST", "text": "But she felt.. calculated."},
            {"speaker": "PLAYER", "text": "Did you notice what she was wearing?"},
            {"speaker": "FASHION ENTHUSIAST", "text": "..Red dress."},
            {"speaker": "PLAYER", "text": "Red?."},
            {"speaker": "FASHION ENTHUSIAST", "text": "Bright. Hard to miss."},
            {"speaker": "FASHION ENTHUSIAST", "text": "And her hair—tied back."},
            {"speaker": "CLUE", "text": "Clue discovered: Red dress + ponytail"},
            {"speaker": "PLAYER", "text": "..That matches."},
            {"speaker": "FASHION ENTHUSIAST", "text": "But that’s not what stood out most."},
            {"speaker": "PLAYER", "text": "Then what?"},
            {"speaker": "NPC 1", "text": "She was holding something strange."},
            {"speaker": "PLAYER", "text": "What kind of item?"},
            {"speaker": "NPC 1", "text": "A shirt."},
            {"speaker": "NPC 1", "text": "Loose.. patterned.."},
            {"speaker": "NPC 1", "text": "Not fitted like anything here."},
            {"speaker": "CLUE", "text": "Clue discovered: Flannel Shirt"},
            {"speaker": "PLAYER", "text": "Where did she go?"},
            {"speaker": "NPC 1", "text": "Toward the back."},
            {"speaker": "NPC 1", "text": "Near the storage racks."},
        ],
        "quest": "clue_flannel_shirt"
    },

    # ===========================
    # 1960s NPC 4: Gallery Staff
    # ===========================
    ("1960s", 4, 7): {
        "speaker": "Gallery Staff",
        "dialogue": [
            {"speaker": "GALLERY STAFF", "text": "Careful with those racks."},
            {"speaker": "PLAYER", "text": "I won’t touch anything I shouldn’t."},
            {"speaker": "GALLERY STAFF", "text": "..You’re not browsing."},
            {"speaker": "PLAYER", "text": "No."},
            {"speaker": "PLAYER", "text": "I’m looking for something that doesn’t belong here."},
            {"speaker": "GALLERY STAFF", "text": "..Then you think like him."},
            {"speaker": "PLAYER", "text": "My grandfather."},
            {"speaker": "GALLERY STAFF", "text": "Yes."},
            {"speaker": "GALLERY STAFF", "text": "He always said.."},
            {"speaker": "GALLERY STAFF", "text": "Every era has its rhythm. The wrong piece breaks it."},
            {"speaker": "PLAYER", "text": "..That sounds like him."},
            {"speaker": "GALLERY STAFF", "text": "You’ve inherited that awareness."},
            {"speaker": "PLAYER", "text": "A girl came through here."},
            {"speaker": "GALLERY STAFF", "text": "She did."},
            {"speaker": "PLAYER", "text": "What was she carrying?"},
            {"speaker": "GALLERY STAFF", "text": "A shirt."},
            {"speaker": "GALLERY STAFF", "text": "Rough fabric. Checkered pattern."},
            {"speaker": "GALLERY STAFF", "text": "Doesn’t belong in this decade."},
            {"speaker": "PLAYER", "text": "Where is it now?"},
            {"speaker": "GALLERY STAFF", "text": "She tried to hide it among the racks."},
            {"speaker": "GALLERY STAFF", "text": "But it stands out.. if you know what to look for."},
        ],
        "quest": "clue_flannel_shirt"
    },
}

#testing

item_dialogue_data = {
    ("1920s", 10, 4): {
        "dialogue": [
            {"speaker": "PLAYER", "text": "Tall.. white.. doesn't belong.."},
            {"speaker": "PLAYER", "text": "There."},
            {"speaker": "PLAYER", "text": "..Go-Go boots."},
            {"speaker": "PLAYER", "text": "Definitely not from the 1920s."},
            {"speaker": "PLAYER", "text": "So the thief really is scattering items across time.."},
            {"speaker": "PLAYER", "text": "..and not even trying to hide the mismatch."},
            {"speaker": "DEVICE", "text": "Artifact recovered."},
            {"speaker": "DEVICE", "text": "Temporal jump requires stabilization."},
            {"speaker": "PLAYER", "text": "..Which means?"},
            {"speaker": "DEVICE", "text": "Mini-game required to calibrate timeline."},
            {"speaker": "PLAYER", "text": "..Of course there's a catch."},
            {"speaker": "PLAYER", "text": "Nothing can ever be simple."},
            {"speaker": "GAME", "text": "Mini-game starts somewhere here"}
        ],
        "quest": "boots_recovered"
    }
}

quest_log = {}

#Quest System
active_quests = []
completed_quests = []
current_quest = None

quest_popup_text = ""
quest_popup_timer = 0
QUEST_POPUP_DURATION = 150

quest_descriptions = {
    "clue_gogo_boots": "Find the Go-Go Boots",
    "old_tailor_hint": "Use the Tailor's advice to find what does not belong",
    "boots_recovered": "Complete the mini-game to stabilize the timeline"
}

#2. The Maps (Scene to Scene)
museum_map = [
    "111111111111111111111111111111111111111111111111111111111111", # 00
    "100000000000000111111111111111111111111111100000000000000001", 
    "100500000000000100000000000000000000000000100000000000005001",
    "100000333330000000000000000000000000000000000003333300000001",
    "100000333330000000000000000000000000000000000003333300000001", # Ancient Wing
    "100000333330000100000000000000000000000000100003333300000001",
    "111000111110000111111111111111111111111111100001111100011111",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100111111001111111111110000000011111111111111100111111000001", # Row 09
    "100100001001000000000010000000010000000000000100100001000001", # 10
    "100103301001000000000000000000000000000000000100103301000001",
    "100103301001000000000000000000000000000000000100103301000001",
    "100100001001000000000000000000000000000000000100100001000001",
    "100111111001000000000000000000000000000000000100111111000001",
    "100000000000000000000000000000000000000000000000000000000001", # 15 (SPAWN)
    "100000000000000000000000000000000000000000000000000000000001",
    "100111111001000000000000000000000000000000000100111111000001",
    "100100001001000000000000000000000000000000000100100001000001",
    "100106001001000000000000000000000000000000000100106001000001",
    "100100001001000000000000000000000000000000000100100001000001", # 20
    "100111111001111111111110000000011111111111111100111111000001",
    "100000000000000000000001000000010000000000000000000000000001",
    "100000000000000000000001000000010000000000000000000000000001",
    "111111111111100111111111000000011111111100111111111111111111",
    "100000000000100100000000000000000000000100100000000000000001", # 25
    "100000000000100100000000000000000000000100100000000000000001",
    "100333333300000000000000000000000000000000000333333300000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000100100000000000000000000000100100000000000000001",
    "111100111111100111111111110000111111111100111111100111111111", # 30
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "111111111111111111111111110000111111111111111111111111111111", # 35 (EXIT)
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110440111111111111111111111111111111", # 38 (PORTAL)
    "111111111111111111111111111111111111111111111111111111111111"  # 39
]

#Jazz Age

era_1920s_map = [
    "111111111111111111111111111111", 
    "100000000000000000000000000001",
    "101111111000000000011111111101", 
    "101111111000030000011111111101",
    "101112211000000000011122111101", 
    "100000000000000000000000000001", 
    "100000000000050000000000000001", 
    "100000000000000000000000000001",
    "100003000000444400000000030001", 
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "100000000000000000050000000001", 
    "100000000000000000000000000001", 
    "101112211000000000011122111101", 
    "101111111000030000011111111101", 
    "101111111000000000011111111101",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"  
]


interior_1920s_club = [
    "11111111111111111111", 
    "10000000000000000001",
    "10333330000000000001", 
    "10333330000000000001",
    "10000000000000000001",
    "10000000000500000001", 
    "10000000000000000001",
    "11111100000000011111", 
    "10000000000000000001",
    "10000000000000000001", 
    "10003300033000330001", 
    "10003300000000330001",
    "10000000000000000001",
    "11111111221111111111", 
    "11111111111111111111"
]


interior_1920s_warehouse = [
    "11111111111111111111", 
    "10000000000000000001",
    "10111111000011111101", 
    "10000000000000000001",
    "10111100111100000001", 
    "10111100111100000001",
    "10000000000000111101", 
    "10000000000000111101",
    "10110060011000000001", 
    "10111111110000000001",
    "10000000000005000001", 
    "10000000000000000001",
    "10000000000000000001",
    "11111111221111111111", 
    "11111111111111111111"
]


interior_1920s_bank = [
    "11111111111111111111",
    "10000000000000000001",
    "10111100000000111101", 
    "10000000000000000001",
    "10000011111100000001",
    "10000010000100000001", 
    "10000010060100000001", 
    "10000011111100000001",
    "10000000000000000001",
    "10000000000005000001", 
    "10000000000000000001",
    "10000000000000000001",
    "11111111221111111111", 
    "11111111111111111111"
]

era_1960s_map = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "100033300000000000003333000001",
    "100033300000500000003333000001",
    "100000000000000000000000000001",
    "100000000001111100000000000001",
    "100000000001000100000000000001",
    "100050000021000100000005000001",
    "100000000001000100000000000001",
    "100000000001111100000000000001",
    "100000000000000000000000000001",
    "100000000000444400000000000001",
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "100033300000000000003333000001",
    "100033300000500000003333000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"

]

era_1980s_map = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "101111111000000000011111111101",
    "101000001000000000010000001101",
    "101000001020060000010000001101",
    "101000001000000000010000001101",
    "101111111000000000011111111101",
    "100000000000000000000000000001",
    "100000000000444400000000000001",
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "101111111000000000011111111101",
    "101000001000000000010000001101",
    "101000001000050000010000001101",
    "101000001000000000010000001101",
    "101111111000000000011111111101",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"
]

era_1990s_map = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "100000333300000000003333000001",
    "100000333300050000003333000001",
    "100000000000000000000000000001",
    "100011111000000000011111000001",
    "100010001000000000010001000001",
    "100010001000000000010001000001",
    "100011111000000000011111000001",
    "100000000000444400000000000001",
    "100000000000444400000000000001",
    "100000000000000000000000000001",
    "100000002000050000000000000001",
    "100000000000000000000000000001",
    "100033300000000000003333000001",
    "100033300000000000003333000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"
]

building_data = {
    
    ("1920s", 5, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},
    ("1920s", 6, 4): {"name": "Club", "target_map": interior_1920s_club, "spawn": (9, 11)},

    ("1920s", 22, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},
    ("1920s", 23, 4): {"name": "Bank", "target_map": interior_1920s_bank, "spawn": (9, 11)},

    ("1920s", 22, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    ("1920s", 23, 13): {"name": "Warehouse", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},
    

    
    ("1960s", 10, 7): {"name": "Cafe", "target_map": interior_1920s_club, "spawn": (9, 11)},  # placeholder interior

    ("1980s", 10, 4): {"name": "Office", "target_map": interior_1920s_bank, "spawn": (9, 11)},  # placeholder interior
    
    ("1990s", 8, 12): {"name": "Mall", "target_map": interior_1920s_warehouse, "spawn": (9, 11)},  # placeholder interior

    # INTERIOR EXITS

    # Club / Cafe 
    ("Club", 9, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (5, 5)},
    ("Cafe", 8, 13): {"name": "1960s", "target_map": era_1960s_map, "spawn": (10, 8)},


    # Bank / Office
    ("Bank", 8, 12): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 5)},
    ("Bank", 9, 12): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 5)},
    ("Office", 8, 12): {"name": "1980s", "target_map": era_1980s_map, "spawn": (10, 5)},
    ("Office", 9, 12): {"name": "1980s", "target_map": era_1980s_map, "spawn": (10, 5)},

    # Warehouse / Mall 
    ("Warehouse", 8, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 12)},
    ("Warehouse", 9, 13): {"name": "1920s", "target_map": era_1920s_map, "spawn": (22, 12)},
    ("Mall", 8, 13): {"name": "1990s", "target_map": era_1990s_map, "spawn": (8, 13)},
    ("Mall", 9, 13): {"name": "1990s", "target_map": era_1990s_map, "spawn": (8, 13)},
}

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

                if event.key == pygame.K_e:
                    if not dialogue_active and can_interact:
                        if current_npc in dialogue_data:
                            npc_data = dialogue_data[current_npc]

                            current_dialogue = npc_data["dialogue"]
                            current_quest = npc_data.get("quest")

                            dialogue_active = True
                            dialogue_index = 0
                            dialogue_text_shown = ""
                            text_counter = 0

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

    if not dialogue_active:
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
                transition_to(era_1920s_map, "1920s", 14, 10)
            elif current_era == "1920s":
                transition_to(era_1960s_map, "1960s", 14, 10)
            elif current_era == "1960s":
                transition_to(era_1980s_map, "1980s", 14, 10)
            elif current_era == "1980s":
                transition_to(era_1990s_map, "1990s", 14, 10)
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

        
    pygame.display.update()

pygame.quit()
#4/19/2026 and Earlier dates
#Summary on what I have done in my part for the games:
#Refactored the Architecture, Resolution Upgrade
#Mega Map Installation, Museum and 1920s Jazz Age, Scrolling Camera, Camera Clamping
#Teleportation System, Fog of War Mini-Map, Scene Transitions