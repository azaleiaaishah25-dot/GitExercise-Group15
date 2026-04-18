import pygame

#Master switch 
pygame.init() 

#1. Setup & Variables
tile_size = 50
WIDTH, HEIGHT = 1200, 720  
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Style Heist - Detective Game")
clock = pygame.time.Clock() #limit the pc fps 
font = pygame.font.SysFont(None, 30)


#2. The Maps (Scene to Scene)
museum_map = [
    "111111111111111111",
    "100000000000000001",
    "100000000333000001",   
    "100011111110000001",
    "100330000000000001",
    "111110000000111111",   
    "000000000000000000",   
    "000033300000050000",   
    "111100000000011111",
    "111400000000011111" # 4 is the Teleporter
]

era_1920s_map = [
    "1111111111",
    "1000000001",
    "1000400001", # 4 takes you back to Museum
    "1111111111"
]

current_era = "Museum"
game_map = museum_map #Starting at the Museum


#3. Player Variables
player_size = tile_size
player_size = 50
player_x = 100
player_y = 100
speed = 5 #pixels per movements in a frame = FPS


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

    #C. Teleportation Logic 
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    #Step on Tile 4

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if tile == "4":
                portal_rect = pygame.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size)
                if player_rect.colliderect(portal_rect):
                    #Scenes to Scenes
                    if current_era == "Museum":
                        current_era = "1920s"
                        game_map = era_1920s_map
                    else:
                        current_era = "Museum"
                        game_map = museum_map

                    player_x, player_y = 100, 100

    #D. Drawing
    screen.fill((10, 20, 20))

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * tile_size, row_index * tile_size
            
            if tile == "1":
                pygame.draw.rect(screen, (90, 90, 90), (x, y, tile_size, tile_size))
            elif tile == "3":
                screen.blit(tree_img, (x, y))
            elif tile == "4":
                pygame.draw.rect(screen, (200, 150, 50), (x, y, tile_size, tile_size)) # Portal
            elif tile == "5":
                pygame.draw.rect(screen, (0, 0, 255), (x, y, tile_size, tile_size)) # NPC Placeholder
            else:
                pygame.draw.rect(screen, (200, 200, 200), (x, y, tile_size, tile_size))
            
            # Grid lines
            pygame.draw.rect(screen, (0, 0, 0), (x, y, tile_size, tile_size), 1)

    # Draw Player
    screen.blit(duck_img, (player_x, player_y))

    pygame.display.update()

pygame.quit()



