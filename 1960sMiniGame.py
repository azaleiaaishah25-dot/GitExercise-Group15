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

#fonts
font_tittle =pygame.font.SysFont('Arial', 60)
font_bold = pygame.font.SysFont("courier", 22, bold=True)
font_text = pygame.font.SysFont("courier", 18)

# The game variables
score = 0
grid_timer = 0
color_flip_rate = 90

#grid setup

grid_blocks = [
    {"rect": pygame.Rect(100, 150, 280, 180), "color": MOD_ORANGE},
    {"rect": pygame.Rect(420, 150, 280, 180), "color": MUSTARD_YELLOW},
    {"rect": pygame.Rect(100, 360, 280, 180), "color": CHERRY_RED},
    {"rect": pygame.Rect(420, 360, 280, 180), "color": CULTURE_BLACK}
]

target_block_index = random.randint(0,3)
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
player_size = 30
player_speed = 6

#Game loop
while True:
    screen.fill(WHITE)
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#wIN WIN CONDITION
