import pygame
import random
import time
import sys
import os

def run_minigame (screen,clock):
    #screen setup
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption ("1990s  Archive Puzzle")
    
    #colours
    
    WHITE = (245, 245, 245)
    BLACK = (20, 20, 20)
    DARK = (14, 14, 24)
    PANEL = (30, 30, 42)
    GOLD = (255, 220, 120)
    RED = (220, 70, 70)
    GREEN = (80, 220, 130)
    GRAY = (170, 170, 170)
