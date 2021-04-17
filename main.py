# coding=utf-8
import json
import os

import pygame
import pygameMenu
from pygameMenu.locals import *

from mubreaker import gameconfig
from mubreaker.Game import main

ABOUT = ['MUBreakout V0.33',
         'Author: Iker Ocio Zuazo',
         'Mondragon Unibertsitatea']

COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (640, 480)

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

# -----------------------------------------------------------------------------
# Init pygame
pygame.mixer.pre_init(30100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
pygame.display.set_icon(pygame.image.load("mubreaker/res/icon.png"))
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('MUBreakout - Main Menu')
clock = pygame.time.Clock()
dt = 1 / FPS

# Global variables
DIFFICULTY = ['EASY']
SOUND = ['ENABLED']


pygame.mixer.music.load("mubreaker/res/main_sound.mp3")
if gameconfig.sound:
    pygame.mixer.music.play(-1)
    sound_option_selection = [('Enabled', 'ENABLED'),
                              ('Disabled', 'DISABLED')]
else:
    sound_option_selection = [('Disabled', 'DISABLED'),
                              ('Enabled', 'ENABLED')]

if gameconfig.difficulty == "EASY":
    difficulty_option_selection = [('Easy', 'EASY'),
                                   ('Medium', 'MEDIUM'),
                                   ('Hard', 'HARD')]
elif gameconfig.difficulty == "MEDIUM":
    difficulty_option_selection = [('Medium', 'MEDIUM'),
                                   ('Easy', 'EASY'),
                                   ('Hard', 'HARD')]
elif gameconfig.difficulty == "HARD":
    difficulty_option_selection = [('Hard', 'HARD'),
                                   ('Easy', 'EASY'),
                                   ('Medium', 'MEDIUM')]

# -----------------------------------------------------------------------------


def change_difficulty(d):
    modify_config(difficulty=d)
    DIFFICULTY[0] = d


def change_sound(d):
    if d == "ENABLED":
        modify_config(sound=True)
        pygame.mixer.music.play()
    else:
        modify_config(sound=False)
        pygame.mixer.music.pause()
    SOUND[0] = d


def open_rank():
    f = open("mubreaker/ranking.txt", "r")
    json_data = json.loads(f.readline())
    content_list = []
    for item in json_data:
        content_list.append("{} - {}    with    {}    points.".format(item['position'], item['name'], item['score']))
    return content_list


def modify_config(sound=None, difficulty=None):
    if sound is not None:
        gameconfig.sound = sound
    if difficulty is not None:
        gameconfig.difficulty = difficulty
    f = open("mubreaker/gameconfig.py", "w")
    f.write("sound={}\ndifficulty='{}' # easy, medium, hard".format(gameconfig.sound, gameconfig.difficulty))
    f.close


def main_background():
    surface.fill(COLOR_BACKGROUND)
    surface.blit(pygame.image.load("mubreaker/res/breakout_bg.png"), (0, 0))
    surface.blit(pygame.image.load("mubreaker/res/instructions.png"), (0, 0))
    surface.blit(pygame.image.load("mubreaker/res/logo.png"), ((WINDOW_SIZE[0]/2)-150, 10))


about_menu = pygameMenu.TextMenu(surface,
                                 window_width=WINDOW_SIZE[0],
                                 window_height=WINDOW_SIZE[1],
                                 font=pygameMenu.fonts.FONT_BEBAS,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 font_size_title=30,
                                 title='About',
                                 menu_alpha=70,
                                 # Disable menu close (ESC button)
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 font_color=COLOR_BLACK,
                                 text_fontsize=20,
                                 menu_color_title=COLOR_WHITE,
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 option_shadow=False,
                                 color_selected=COLOR_WHITE,
                                 text_color=COLOR_BLACK,
                                 bgfun=main_background)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(TEXT_NEWLINE)
about_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# -----------------------------------------------------------------------------
# OPTION MENU
option_menu = pygameMenu.Menu(surface,
                              window_width=WINDOW_SIZE[0],
                              window_height=WINDOW_SIZE[1],
                              font=pygameMenu.fonts.FONT_BEBAS,
                              font_title=pygameMenu.fonts.FONT_8BIT,
                              font_size_title=30,
                              title='Optionsmenu',
                              menu_alpha=70,
                              font_size=30,
                              menu_width=int(WINDOW_SIZE[0] * 0.6),
                              menu_height=int(WINDOW_SIZE[1] * 0.6),
                              bgfun=main_background,
                              menu_color=MENU_BACKGROUND_COLOR,
                              option_shadow=False,
                              font_color=COLOR_BLACK,
                              color_selected=COLOR_WHITE,
                              onclose=PYGAME_MENU_DISABLE_CLOSE)

option_menu.add_selector('Select Difficulty', difficulty_option_selection,
                         onreturn=None,
                         onchange=change_difficulty)

option_menu.add_selector('Sound', sound_option_selection,
                         onreturn=None,
                         onchange=change_sound)

option_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# -----------------------------------------------------------------------------
# RANKING MENU
ranking_menu = pygameMenu.TextMenu(surface,
                                   window_width=WINDOW_SIZE[0],
                                   window_height=WINDOW_SIZE[1],
                                   font=pygameMenu.fonts.FONT_BEBAS,
                                   font_title=pygameMenu.fonts.FONT_8BIT,
                                   font_size_title=30,
                                   title='Ranking',
                                   menu_alpha=90,
                                   onclose=PYGAME_MENU_DISABLE_CLOSE,
                                   font_color=COLOR_BLACK,
                                   text_fontsize=20,
                                   menu_color_title=COLOR_WHITE,
                                   menu_color=MENU_BACKGROUND_COLOR,
                                   menu_width=int(WINDOW_SIZE[0] * 0.6),
                                   menu_height=int(WINDOW_SIZE[1] * 0.85),
                                   option_shadow=False,
                                   color_selected=COLOR_WHITE,
                                   text_color=COLOR_BLACK,
                                   bgfun=main_background)
for m in open_rank():
    ranking_menu.add_line(m)
ranking_menu.add_line("")
ranking_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_title=pygameMenu.fonts.FONT_8BIT,
                            font_size_title=30,
                            draw_region_x=50,
                            draw_region_y=60,
                            title='Menu',
                            menu_alpha=70,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.3),
                            menu_height=int(WINDOW_SIZE[1] * 0.55),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,  # ESC disabled
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            )
main_menu.add_option('Play', main)
main_menu.add_option('Ranking', ranking_menu)
main_menu.add_option('Options', option_menu)
main_menu.add_option('About', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
# Main loop
while True:
    # Tick
    clock.tick(60)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Main menu
    # quitar lo de mainloop

    main_menu.mainloop(events)
    # Flip surface
    pygame.display.flip()
