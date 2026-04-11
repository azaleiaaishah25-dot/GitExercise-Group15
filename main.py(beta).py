import pygame

pygame.init() #"master switch" 


tile_size = 50

game_map = [
    "111111111111111111",
    "100000000000000001",
    "100000000333000001",   
    "100011111110000001",
    "100000000000000001",
    "111110000000111111",   
    "000000000000000000",   #Outside Area
    "000033300000000000",
    "000000040000000000" 
]


#screen aka display
WIDTH, HEIGHT = 1200, 720 #Dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #window, open physical window. Takes a tuple
pygame.display.set_caption("2D Game") #Window with name, cosmetic

#Player aka Character
#player_x / player_y = player variable
player_size = 50
player_x = 100
player_y = 100
speed = 5 #pixels per movements in a frame = FPS

clock = pygame.time.Clock() #limit the pc fps 

player_size = tile_size

running = True
while running: #game is still live if still running
    clock.tick(60) #fps, frame per second

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 20, 20))
    
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size

            if tile == "1":
                color = (90, 90, 90)
            elif tile == "3":
                color = (0, 150, 0) #tree
            elif tile == "4": 
                color = (200, 150, 50)
            else:
                color = (200, 200, 200)

            pygame.draw.rect(screen, color, (x,y, tile_size, tile_size))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, tile_size, tile_size), 1)
    #Draw
    pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_size, player_size))

    pygame.display.update()
           
    running = True
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

    #Movement hot keys
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
    if not check_collision(new_x, player_y):
        player_x = new_x

    #Move Y
    if not check_collision(player_x, new_y):
        player_y = new_y

player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

for row_index, row in enumerate(game_map):
    for col_index, tile in enumerate(game_map):
        if tile == "4":
            tile_rect = pygame.Rect(
                col_index * tile_size,
                row_index * tile_size,
                tile_size,
                tile_size
            )

            if player_rect.collidedict(tile_rect):
                print("Entered building!") 


#2D game from python feels like minecraft world but with blocks
#Example: 111111 - wall
#sample test 1 with tile_size

pygame.quit()



