#!/usr/bin/env python
import json
import os.path

import pygame

from . import gameconfig
from .items import ROBOT_IA
from .scenario import Scenario
from .utils import FONTRENDER, SCREENRECT, screenRECT

global SCORE


def draw_list(surface, actor_list):
    for actor in actor_list:
        actor.draw(surface)


def get_font_from_str(name, text):
    return FONTRENDER.render("{}:{}".format(text, name), True, (255, 255, 255))


def DEAD():
    return FONTRENDER.render("GAME OVER", True, (255, 255, 255))


def save_to_file(json_data):
    output = open('mubreaker/ranking.txt', 'w')
    output.write(json_data)
    output.close()


def open_ranking_from_file():
    ranking = open("mubreaker/ranking.txt", "r")
    return json.loads(ranking.readline())


def name_is_in_list(list, name):
    for item in list:
        if name == item["name"]:
            return True
    return False


def get_ordered_score_list(list):
    list.sort(key=lambda x: x["score"], reverse=True)
    index = 1
    for item in list:
        item['position'] = index
        index += 1
    if len(list) > 10:
        list.pop()
    return list


def save_score(name, score):
    all_data = open_ranking_from_file()
    if not name_is_in_list(all_data, name):
        data = {}
        data['position'] = 0
        data['name'] = name
        data['score'] = score
        all_data.append(data)
        all_data = get_ordered_score_list(all_data)
        json_data = json.dumps(all_data)
        save_to_file(json_data)
        print("Exiting...")
        return True
    else:
        return False


def game_over(surface, background, clock, score, retry=False):
    writing_name = True
    flag_retry = False
    press_enter = FONTRENDER.render("Press enter to continue", True, (255, 255, 255))
    press_esc = FONTRENDER.render("Press ESC to restart", True, (255, 255, 255))
    POINTS = FONTRENDER.render("SCORE: {}".format(score), True, (255, 255, 255))
    name = ""
    if retry:
        PRETEXT = "Write another name"
    else:
        PRETEXT = "Please, enter your name"
    get_font_from_str("", PRETEXT)
    while writing_name and not flag_retry:
        # clear/erase the last drawn
        surface.fill((0, 0, 0))
        surface.blit(background.background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    writing_name = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    flag_retry = True
                else:
                    name += str(chr(event.key))
        if len(name) > 3:
            name = name[0:3]
        surface.blit(press_enter, (SCREENRECT.width/2-200, SCREENRECT.height-100))
        surface.blit(press_esc, (SCREENRECT.width/2-200, SCREENRECT.height-80))
        surface.blit(POINTS, (SCREENRECT.width/2-200, SCREENRECT.height/2-20))
        surface.blit(get_font_from_str(name, PRETEXT), ((SCREENRECT.width/2)-200, SCREENRECT.height/2))
        pygame.display.flip()
        clock.tick(2000)
    if flag_retry:
        main()
    else:
        if not save_score(name, score):
            game_over(surface, background, clock, score, True)


def main(winstyle=0):
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('MUBreakout')
    pygame.mouse.set_visible(0)
    winstyle = 0
    bestdepth = pygame.display.mode_ok(screenRECT.size, winstyle, 32)
    pygame.display.set_icon(pygame.image.load("mubreaker/res/icon.png"))
    surface = pygame.display.set_mode(screenRECT.size, winstyle, bestdepth)

    pygame.display.flip()

    inGame = True
    # ACTOR
    scenario = Scenario(gameconfig.difficulty, gameconfig.sound)
    clock = pygame.time.Clock()
    robot = ROBOT_IA(False)
    while inGame:
        time = pygame.time.get_ticks()/1000
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    robot.toggle_IA()
        scenario.shot()
        keystate = pygame.key.get_pressed()
        if robot.is_working():
            hdirection = robot.move_raquet(scenario)
        else:
            hdirection = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]

        # clear/erase the last drawn
        surface.fill((0, 0, 0))

        scenario.draw(surface)
        scenario.move_raquet(hdirection, 0)
        scenario.update(surface, time)
        scenario.move_ball(surface)
        inGame = scenario.game_is_running()
        pygame.display.flip()
        clock.tick(40)

    game_over(surface, scenario.background, clock, scenario.SCORE)
    pygame.time.wait(1000)
    pygame.quit()


main()
