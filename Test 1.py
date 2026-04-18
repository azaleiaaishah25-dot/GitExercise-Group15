import pygame

pygame.init()

tile_size = 50

game_map = [
    "111111111111111111",
    "100000000000000001",
    "100000000333000001",   
    "100011111110000001",
    "100330000000000001",
    "111110000000111111",   
    "000000000000000000",
    "000033300000050000",   # 5 = NPC
    "000000000003300000",
    "110000011000011000",
    "11110001111111101111",
    "000000000011111111",
    "111100000033311111",
    "1114000000003111111"
]

# Screen
WIDTH, HEIGHT = 1200, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game")

# Player
player_size = tile_size
player_x = 100
player_y = 100
speed = 5

clock = pygame.time.Clock()

# Images
duck_img = pygame.image.load("Images/duck_with_knife.jpg").convert_alpha()
duck_img = pygame.transform.scale(duck_img, (player_size, player_size))

tree_img = pygame.image.load("Images/pixel_tree.jpg").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (tile_size, tile_size))

# NPC from map
npc_positions = []
for row_index, row in enumerate(game_map):
    for col_index, tile in enumerate(row):
        if tile == "5":
            npc_positions.append((col_index * tile_size, row_index * tile_size))

# Font
font = pygame.font.SysFont(None, 30)

# Collision function
def check_collision(x, y):
    player_rect = pygame.Rect(x, y, player_size, player_size)

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if tile in ["1", "3"]:
                wall_rect = pygame.Rect(
                    col_index * tile_size,
                    row_index * tile_size,
                    tile_size,
                    tile_size
                )
                if player_rect.colliderect(wall_rect):
                    return True
    return False

# Game loop
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 20, 20))

    # Draw map
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size

            if tile == "1":
                pygame.draw.rect(screen, (90, 90, 90), (x, y, tile_size, tile_size))

            elif tile == "3":
                screen.blit(tree_img, (x, y))

            elif tile == "4":
                pygame.draw.rect(screen, (200,150,50), (x,y, tile_size, tile_size))

            else:
                pygame.draw.rect(screen, (200,200,200), (x, y, tile_size, tile_size))

            pygame.draw.rect(screen, (0, 0, 0), (x, y, tile_size, tile_size), 1)

    # Movement
    keys = pygame.key.get_pressed()

    new_x = player_x
    new_y = player_y

    if keys[pygame.K_w]:
        new_y -= speed
    if keys[pygame.K_s]:
        new_y += speed
    if keys[pygame.K_a]:
        new_x -= speed
    if keys[pygame.K_d]:
        new_x += speed

    if not check_collision(new_x, player_y):
        player_x = new_x
    if not check_collision(player_x, new_y):
        player_y = new_y

    # Draw NPCs
    for npc_x, npc_y in npc_positions:
        pygame.draw.rect(screen, (255, 0, 0), (npc_x, npc_y, tile_size, tile_size))

    # Draw player
    screen.blit(duck_img, (player_x, player_y))

    # Interaction
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    interacting = False
    

    for npc_x, npc_y in npc_positions:
        npc_rect = pygame.Rect(npc_x, npc_y, tile_size, tile_size)

        if player_rect.colliderect(npc_rect):
            if keys[pygame.K_e]:
                interacting = False

                for npc_x, npc_y in npc_positions:
                    npc_rect = pygame.Rect(npc_x, npc_y, tile_size, tile_size)

                    interaction_rect = npc_rect.inflate(40, 40) #increase size
                    
                    if player_rect.colliderect(interaction_rect):
                        hint = font.render("Press E to interact", True, (255, 255, 0))
                        screen.blit(hint, (npc_x - 20, npc_y - 30))

                        if keys[pygame.K_e]:
                            interacting = True

    # Dialogue
    if interacting:
        text = font.render("WELCOME TO THE GAME!", True, (255, 255, 255))
        screen.blit(text, (50, 50))

    pygame.display.update()

pygame.quit()