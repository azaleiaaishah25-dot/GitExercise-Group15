npc_size = tile_size

npc_x = 300
npc_y = 200

font = pygame.font.SysFont(None, 30)
interacting = False

pygame.draw.rect(screen, (255, 0, 0), (npc_x, npc_y, npc_size, npc_size))

player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
npc_rect = pygame.Rect(npc_x, npc_y, npc_size, npc_size)

keys = pygame.key.get_pressed()

if player_rect.colliderect(npc_rect):
    if keys[pygame.K_q]:
        interacting = True
else:
    interacting = False

    if interacting:
        text = font.render("Welcome to the museum!", True, (255, 255, 255))
        screen.blit(text, (50, 50))

