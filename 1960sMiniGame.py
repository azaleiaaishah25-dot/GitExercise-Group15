import pygame
import random 
import sys
 
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colours for the game
BLACK          = (10, 10, 12)
WHITE          = (255, 255, 255)
MOD_ORANGE     = (242, 100, 25)
MUSTARD_YELLOW = (246, 190, 0)
CHERRY_RED     = (213, 0, 50)
CULTURE_BLACK  = (20, 20, 20)

# Fonts
font_title = pygame.font.SysFont('Arial', 60)
font_bold = pygame.font.SysFont("courier", 22, bold=True)
font_text = pygame.font.SysFont("courier", 18)

# The game variables
score = 0
grid_timer = 0
color_flip_rate = 90

# Grid setup
grid_blocks = [
    {"rect": pygame.Rect(100, 150, 280, 180), "color": MOD_ORANGE},
    {"rect": pygame.Rect(420, 150, 280, 180), "color": MUSTARD_YELLOW},
    {"rect": pygame.Rect(100, 360, 280, 180), "color": CHERRY_RED},
    {"rect": pygame.Rect(420, 360, 280, 180), "color": CULTURE_BLACK}
]

target_block_index = random.randint(0, 3)
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
player_size = 30
player_speed = 6

# --- MAIN GAME LOOP ---
while True:
    screen.fill(WHITE)
    events = pygame.event.get()

    # Handle close window event
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- WIN CONDITION STATE ---
    if score >= 10:
        screen.fill(MOD_ORANGE)
        win_lbl = font_title.render("1960s ERA CLEARED!", True, WHITE)
        sub_lbl = font_text.render("Artifact Secured: Mod Go-Go Boots", True, BLACK)
        prompt = font_text.render("Loading 1980s Timeline Engine...", True, WHITE)
            
        screen.blit(win_lbl, (WIDTH//2 - win_lbl.get_width()//2, HEIGHT//2 - 60))
        screen.blit(sub_lbl, (WIDTH//2 - sub_lbl.get_width()//2, HEIGHT//2 - 10))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 40))

        pygame.display.flip()
        pygame.time.wait(5000)  # Show win screen for 5 seconds
        pygame.quit()
        sys.exit()

    # --- COLOR FLIP TIMER ---
    grid_timer += 1
    if grid_timer >= color_flip_rate:
        grid_timer = 0
        # Shuffle colors to create the shifting geometric illusion
        colors = [MOD_ORANGE, MUSTARD_YELLOW, CHERRY_RED, CULTURE_BLACK]
        random.shuffle(colors)
        for i in range(4):
            grid_blocks[i]["color"] = colors[i]
            
        # Change which grid cell holds the artifact
        target_block_index = random.randint(0, 3)

    # --- INPUT PROCESSING (PLAYER MOVEMENT) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos.x > 0: player_pos.x -= player_speed
    if keys[pygame.K_RIGHT] and player_pos.x < WIDTH - player_size: player_pos.x += player_speed
    if keys[pygame.K_UP] and player_pos.y > 120: player_pos.y -= player_speed
    if keys[pygame.K_DOWN] and player_pos.y < HEIGHT - player_size: player_pos.y += player_speed

    player_rect = pygame.Rect(player_pos.x, player_pos.y, player_size, player_size)

    # --- RENDER THE GAME INTERFACE ---
    # 1. Header & Text Info
    title_text = font_title.render("1960s TIME SYNC: POP ART PUZZLE", True, BLACK)
    instruction = font_text.render("Find the hidden target item before the layout shifts!", True, CHERRY_RED)
    intruction_2 = font_text.render("Move your arrow keys to navigate.", True, CHERRY_RED)
    score_text = font_bold.render(f"Boots Found: {score}/10", True, BLACK)
        
    screen.blit(title_text, (30, 20))
    screen.blit(instruction, (30, 55))
    screen.blit(score_text, (WIDTH - 240, 35))

    # 2. Draw the 4 Op-Art Color Blocks
    for index, block in enumerate(grid_blocks):
        pygame.draw.rect(screen, block["color"], block["rect"])
        # Give them a sharp, heavy border typical of 60s illustration layout
        
        pygame.draw.rect(screen, BLACK, block["rect"], 4)
            
        # 3. Handle Item Logic and Display Indicators
        if index == target_block_index:
            # Render the goal text inside the designated box
            lbl_item = font_bold.render("👔👔 Flannel shirt", True, WHITE if block["color"] == CULTURE_BLACK else BLACK)
            text_x = block["rect"].x + (block["rect"].width // 2) - (lbl_item.get_width() // 2)
            text_y = block["rect"].y + (block["rect"].height // 2) - (lbl_item.get_height() // 2)
            screen.blit(lbl_item, (text_x, text_y))
                
            # Check if player stepped into the correct zone
            if block["rect"].colliderect(player_rect):
                score += 1
                grid_timer = color_flip_rate # Force a color re-shuffle instantly

        else:
            # Decoy / Bad item warning indicator text
            lbl_decoy = font_text.render("[ 1950s Fad ]", True, WHITE if block["color"] == CULTURE_BLACK else BLACK)
            text_x = block["rect"].x + (block["rect"].width // 2) - (lbl_decoy.get_width() // 2)
            text_y = block["rect"].y + (block["rect"].height // 2) - (lbl_decoy.get_height() // 2)
            screen.blit(lbl_decoy, (text_x, text_y))
                
            # Penalty check: Standing on a decoy when colors change slows player down
            if block["rect"].colliderect(player_rect) and grid_timer == 0:
                score = max(0, score - 1)

    # 4. Render Player Token (Drawn cleanly on top of the blocks)
    center_p = (int(player_pos.x + player_size//2), int(player_pos.y + player_size//2))
    pygame.draw.circle(screen, BLACK, center_p, 18)
    pygame.draw.circle(screen, WHITE, center_p, 12)
    pygame.draw.circle(screen, CHERRY_RED, center_p, 6)

    # Refresh screen and regulate FPS
    pygame.display.flip()
    clock.tick(FPS)