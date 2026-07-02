import pygame as pg
import random 
import time

def run_minigame (screen, clock):
    WIDTH,HEIGH =screen.get_size()

    #colours
    BLACK = (10, 10, 20)
    WHITE = (255, 255, 255)
    YELLOW = (255, 220, 120)
    PINK = (255, 80, 180)
    PURPLE = (120, 80, 200)
    GREEN = (60, 220, 120)
    RED = (220, 60, 60)
    BLUE = (80, 160, 255)

    #FONTS
    title_font = pg.font.SysFont(None, 70)
    big_font = pg.font.SysFont(None, 120)
    medium_font = pg.font.SysFont(None, 42)
    small_font = pg.font.SysFont(None, 30)