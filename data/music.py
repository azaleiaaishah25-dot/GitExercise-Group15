import pygame
import os

pygame.mixer.init()

current_music = None

music_tracks = {
    "Museum": "Audio/museum_theme_original.wav",
    "1920s": "Audio/jazz_1920s_original.wav",
    "1950s": "Audio/gallery_1950s_original.wav",
    "1960s": "Audio/sixties_theme_original.wav",
    "1980s": "Audio/eighties_theme_original.wav",
    "1990s": "Audio/nineties_theme_original.wav",
}

def play_music(era_name):
    global current_music

    if era_name not in music_tracks:
        return
    
    music_path = music_tracks[era_name]

    if current_music == music_path:
        return
    
    if not os.path.exists(music_path):
        print("Music file not found:", music_path)
        return

    pygame.mixer.music.fadeout(500)
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

    current_music = music_path

def stop_music():
    pygame.mixer.music.fadeout(800)

def set_music_volume(volume):
    pygame.mixer.music.set_volume(volume)