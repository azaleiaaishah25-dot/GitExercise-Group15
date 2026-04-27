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


#2. The Maps (Scene to Scene)
museum_map = [
    "111111111111111111111111111111111111111111111111111111111111", #1 is wall, 3 is tree(temporary), 4 is teleportation
    "100000000000000000000000000011110000000000000000000000000001",
    "100050000000000000000000000011110000000000000000000500000001",
    "100000000333000003330000000000000000000333000003330000000001",
    "100000000333000003330000000000000000000333000003330000000001",
    "111111100000000000000001111100111110000000000000000011111111",
    "100000000000000000000001111100111110000000000000000010000001",
    "100000000000000000000000000000000000000000000000000010000001",
    "100333000000000000000000000000000000000000000000000010033301",
    "100333000000000000000000000000000000000000000000000010033301",
    "100000000000011111111111000000000000111111111111000010000001",
    "100000000000011111111111000000000000111111111111000010000001",
    "111110011111111111111111111100111111111111111111110011111111",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100111111111111100111111111100111111111100111111111111100001",
    "100111111111111100111111111100111111111100111111111111100001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100050000000000000000000000000000000000000000000000050000001",
    "111111111111111111110011111100111111001111111111111111111111",
    "100000000000000000000011111100111111000000000000000000000001",
    "100000000000000000000011111100111111000000000000000000000001",
    "100333000003330000000000000000000000000000003330000033300001",
    "100333000003330000000000000000000000000000003330000033300001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "111111111111111111110011111100111111001111111111111111111111",
    "100000000000000000000011111100111111000000000000000000000001",
    "100000000000000000000011111100111111000000000000000000000001",
    "100333000003330000000000000000000000000000003330000033300001",
    "100333000003330000000000000000000000000000003330000033300001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110000111111111111111111111111111111",
    "111111111111111111111111110440111111111111111111111111111111",
    "111111111111111111111111111111111111111111111111111111111111"
]

#Jazz Age
era_1920s_map = [
    "111111111111111111111111111111111111111111111111111111111111", 
    "100000000000000000000000000000000000000000000000000000000001",
    "100300000000000000000030000000000003000000000000000000300001",
    "100111111111111111111110000000000001111111111111111111100001", 
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000050000001111111111111111111100001", 
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100501",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111771111111110000000000001111111112211111111100001", 
    "100000000000000000000000000000000000000000000000000000000001", 
    "100330000000000000000000000000000000000000000000000000000001", 
    "100000000000000000000000000000000000000000000000000330000001",
    "100000000000000000000000000000000000000000000000000000000001", 
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000003300000000000000000000000000000000000000000000001", 
    "100000000000000000000000000000000000000000000000000000000001", 
    "100111111111881111111110000000000001111111111111111111100001", 
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000050000001111111111111111111100001", 
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001",
    "100111111111111111111110000000000001111111111111111111100001", 
    "100300000000000000000030000000000003000000000000000000300001",
    "100000000000000000000000000000000000000000000000000000000001", 
    "100000000000000000000000000000000000000000000000000000000001",
    "100000000000000000000000000000000000000000000000000000000001",
    "100111111111111111111111111111111110000000000000000000000001",
    "100111111111111111111111111111111110000000000000000000000001", 
    "100111111111111111111111111111111190000000000000000000000001",
    "100111111111111111111111111111111190000000000044440000000001", 
    "100111111111111111111111111111111110000000000044440000000001", 
    "100111111111111111111111111111111110000000000000000000000001", 
    "100000000000000000000000000000000000000000000000000000000001", 
    "111111111111111111111111111111111111111111111111111111111111"  
]

interior_1920s_club = [
    "111111111111111111111111111111",
    "100000000000000000000000000001",
    "100000050000000000000000000001", 
    "100111111110000000011111111001", 
    "100000000000000000000000000001",
    "100033300003330000333000000001", 
    "100033300003330000333000000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "111111111111112211111111111111", 
    "111111111111111111111111111111"
]

# --- THE MAPS: 1920s INTERIORS (MEGA-PIER EXPANSION) ---
interior_1920s_warehouse = [
    "11111111111111111111111111111111111111111111111111111111111111111111111111111111", 
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001",
    "10111100111100111100111101111111100111100111100111100111101111111110011111111001", 
    "10111100111100111100111101111111100111100111100111100111101111111110011111111001",
    "10000000000000000000000001000000000000000000000000000000010000000000000000000001",
    "10111111111111111110000001000111111111111111111111100000010001111111111111111001", 
    "10000000000000000000000001000000000000000000000000000000010000000000000000000001",
    "10000000000000000000000001000000000000000000000000000000010000000000000000000001",
    "10111111111111111110011111111111111111111111111111100111111111111111111111111001",
    "10111111111111111110011111111111111111111111111111100111111111111111111111111001",
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001", 
    "10050000500005000050000000000000000050000500005000050000000000000000500005000001", 
    "10000000000000000000000111111111110000000000000000000001111111111100000000000001",
    "10111111111100000000000100000000010000000001111111110001000000000100001111111001",
    "10111111111100000000000100006000010000000001111111110001000060000100001111111001", 
    "10000000000000000000000100000000010000000000000000000001000000000100000000000001", 
    "10000000000000000000000111122111110000000000000000000001111221111100000000000001", 
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001",
    "10111100001111000011110000111100001111000011110000111100001111000011110000111101", 
    "10111100001111000011110000111100001111000011110000111100001111000011110000111101",
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001",
    "10111100001111000011110000111100001111000011110000111100001111000011110000111101", 
    "10111100001111000011110000111100001111000011110000111100001111000011110000111101",
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001",
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001",
    "10000000000000000000000000000000000000000000000000000000000000000000000000000001",
    "11111111111111111111111111111111111000000111111111111111111111111111111111111111",
    "11111111111111111111111111111111111000000111111111111111111111111111111111111111",
    "11111111111111111111111111111111111009999111111111111111111111111111111111111111", 
    "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
]

current_era = "Museum"
game_map = museum_map #Starting at the Museum

#Fog of war 
visited_map = [[False for _ in range(len(museum_map[0]))] for _ in range(len(museum_map))]


#3. Player Variables
player_size = tile_size
player_size = 60
player_x = 1500
player_y = 1600
speed = 6 #pixels per movements in a frame = FPS


#4. Images
duck_img = pygame.image.load("Images/duck_with_knife.jpg").convert_alpha()
duck_img = pygame.transform.scale(duck_img, (player_size, player_size))

tree_img = pygame.image.load("Images/pixel_tree.jpg").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size))

#5. Functions (Logic)

def check_collision(x, y, current_map):
    player_rect = pygame.Rect(x, y, player_size, player_size)
    for row_index, row in enumerate(current_map):
        for col_index, tile in enumerate(row):
            if tile in ["1", "3"]:
                wall_rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                if player_rect.colliderect(wall_rect):
                    return True
                
    return False


#6. Main Game Loop
running = True
while running: 
    clock.tick(60) #fps, frame per second

    #A. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     #B. Movement Logic
    hotkeys = pygame.key.get_pressed()

    new_x = player_x
    new_y = player_y

    if hotkeys[pygame.K_w]:
        new_y -= speed
    if hotkeys[pygame.K_s]:
        new_y += speed
    if hotkeys[pygame.K_a]:
        new_x -= speed
    if hotkeys[pygame.K_d]:
        new_x += speed

    #Move X
    if not check_collision(new_x, player_y, game_map):
        player_x = new_x
    #Move Y
    if not check_collision(player_x, new_y, game_map):
        player_y = new_y
    
    camera_x = player_x - (WIDTH // 2)
    camera_y = player_y - (HEIGHT // 2)

    map_pixel_width = len(game_map[0]) * tile_size
    map_pixel_height = len(game_map) * tile_size

    camera_x = max(0, min(camera_x, map_pixel_width - WIDTH))
    camera_y = max(0, min(camera_y, map_pixel_height - HEIGHT))

    player_col = player_x // tile_size
    player_row = player_y // tile_size

    #What Player can see
    reveal_radius = 3
    for row in range(player_row - reveal_radius, player_row + reveal_radius + 1):
        for col in range(player_col - reveal_radius, player_col + reveal_radius + 1):
            if 0 <= row < len(game_map) and 0 <= col < len (game_map[0]):
                visited_map[row][col] = True


    #C. Teleportation Logic & Door logic
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):

            if tile in ["4", "2", "9"]:
                trigger_rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)

                if player_rect.colliderect(trigger_rect):

        
                    if tile == "4": 
                        if current_era == "Museum":
                            current_era = "1920s"
                            game_map = era_1920s_map
                        elif current_era == "1920s":
                            current_era = "1950s"
                            game_map = era_1950s_map
                        elif current_era == "1950s":
                            current_era = "1960s"
                            game_map = era_1960s_map
                        elif current_era == "1960s":
                            current_era = "1980s"
                            game_map = era_1980s_map
                        elif current_era == "1980s":
                            current_era = "1990s"
                            game_map = era_1990s_map
                        elif current_era == "1990s":
                            current_era = "Museum"
                            game_map = museum_map

                        player_x, player_y = 1800, 900

                    elif tile == "2":
                        if current_era == "1920s":

                            current_era = "1920s_Club"
                            game_map = interior_1920s_club
                            player_x = 14 * tile_size
                            player_y = 11 * tile_size

                        elif current_era == "1920s_Club":
                            current_era = "1920s"
                            game_map = era_1920s_map
                        
                    elif tile == "9":
                        if current_era == "1920s":

                            current_era = "1920s_Warehouse"
                            game_map = interior_1920s_warehouse
                            player_x = 14 * tile_size
                            player_y = 11 * tile_size
                        
                        elif current_era == "1920s_Club":
                            current_era = "1920s"
                            game_map = era_1920s_map

                            player_x, player_y = 1800, 900


                    visited_map = [[False for _ in range(len(game_map[0]))] for _ in range(len(game_map))]

                    pygame.time.delay(200)
                    break
                    
    #D. Drawing
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
                    pygame.draw.rect(screen, (200, 150, 50), (screen_x, screen_y, tile_size, tile_size)) # Portal
                elif tile == "5":
                    pygame.draw.rect(screen, (0, 0, 255), (screen_x, screen_y, tile_size, tile_size)) # NPC Placeholder
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

    # ---Mini-Map---
    mini_tile = 5
    map_width = len(game_map[0]) * mini_tile
    start_x = WIDTH - map_width - 20
    start_y = 20

    #1. Mini Map
    pygame.draw.rect(screen, (30, 30, 30), (start_x - 2, start_y -2, map_width + 4, len(game_map) * mini_tile + 4))

    #2. Draw Tiles
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if visited_map[row_index][col_index]:
                mini_x = start_x + (col_index * mini_tile)
                mini_y = start_y + (row_index * mini_tile)

                if tile == "1": #wall
                    pygame.draw.rect(screen, (150, 150, 150), (mini_x, mini_y, mini_tile, mini_tile))
                elif tile == "4": #Portal
                    pygame.draw.rect(screen, (200, 150, 50), (mini_x, mini_y, mini_tile, mini_tile))
                else:
                    pygame.draw.rect(screen, (70, 70, 70), (mini_x, mini_y, mini_tile, mini_tile))


    player_mini_x = start_x + (player_x // tile_size) * mini_tile
    player_mini_y = start_y + (player_y // tile_size) * mini_tile
    pygame.draw.circle(screen, (0, 255, 0 ), (player_mini_x + mini_tile//2, player_mini_y + mini_tile//2), 3)

    era_label = font.render(f"TIMELINE: {current_era}", True, (255, 255, 0)) #Yellow Color
    screen.blit(era_label, (20, 20))

    pygame.display.update()

pygame.quit()

#4/19/2026 and Earlier dates
#Summary on what I have done in my part for the games:
#Refactored the Architecture, Resolution Upgrade
#Mega Map Installation, Museum and 1920s Jazz Age, Scrolling Camera, Camera Clamping
#Teleportation System, Fog of War Mini-Map, Scene Transitions

