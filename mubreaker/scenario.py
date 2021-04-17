from random import randint

import pygame

from .items import (Background, Ball, BlueBlock, Heart, Raquet, RedBlock, Sound,
                    WallBlock, YellowBlock)
from .utils import FONTRENDER, SCREENRECT


#####
#
#####


class Scenario(object):

    MAXIMUM_LIFES = 8
    difficulty_level = 0
    inGame = True
    SCORE = 0
    roof_wall_blocks = []
    vertical_wall_blocks = []
    blocks = []
    block_down_animation_time = 10
    change_difficulty_timeoffset = 10

    raquet_list = []
    raquet_list = pygame.sprite.Group()

    ball_list = []
    heart_x = 10
    heart_y = 10
    heart_list = []

    def __init__(self, difficulty, sound):
        self.raquet_list.empty()
        self.SCORE = 0
        self.raquet_list.add(Raquet(difficulty))
        self.set_difficulty(difficulty)
        self.heart_list.append(Heart(self.heart_x, self.heart_y))
        self.roof_wall_blocks, self.vertical_wall_blocks = load_walls()
        self.blocks = load_blocks()
        self.background = Background()
        self.sound = Sound(sound)

    def shot(self):
        if len(self.ball_list) == 0:
            ball = Ball(self.raquet_list.sprites()[0].rect.centerx, self.raquet_list.sprites()[0].rect.centery-25)
            self.ball_list.append(ball)

    def set_difficulty(self, difficulty):
        if difficulty == "EASY":
            self.difficulty_level = 1
        elif difficulty == "MEDIUM":
            self.difficulty_level = 2
        elif difficulty == "HARD":
            self.difficulty_level = 3
        else:
            self.difficulty_level = 1

    def get_difficulty(self):
        if self.difficulty_level == 1:
            return "EASY"
        elif self.difficulty_level == 2:
            return "MEDIUM"
        elif self.difficulty_level == 3:
            return "HARD"
        else:
            return "HARD"

    def change_difficulty(self):
        self.difficulty_level += 1
        if self.difficulty_level <= self.MAXIMUM_LIFES:
            self.heart_x += 28
            if(len(self.heart_list) < 3):
                self.heart_list.insert(0, Heart(self.heart_x, self.heart_y))
            for h in self.heart_list:
                print(h.rect)
        self.background.change_difficulty()
        lastx = self.raquet_list.sprites()[0].rect.centerx
        lasty = self.raquet_list.sprites()[0].rect.centery
        self.raquet_list.empty()
        raquet = Raquet(self.get_difficulty(), lastx, lasty)
        self.raquet_list.add(raquet)
        for ball in self.ball_list:
            ball.speed += 2

    def collision_solid_wall_left(self, obj):
        for w_block in self.vertical_wall_blocks:
            if w_block.rect.centerx < SCREENRECT.width / 2:
                if w_block.rect.colliderect(obj.rect):
                    self.sound.wall_effect()
                    return True
        return False

    def collision_solid_wall_right(self, obj):
        for w_block in self.vertical_wall_blocks:
            if w_block.rect.centerx > SCREENRECT.width / 2:
                if w_block.rect.colliderect(obj.rect):
                    self.sound.wall_effect()
                    return True
        return False

    def collision_block(self, obj):
        for block in self.blocks:
            if block.rect.colliderect(obj.rect):
                block.hitted()
                self.SCORE += 1

                if block.life == 0:
                    self.blocks.remove(block)
                self.sound.block_effect()

                if obj.rect.centery >= block.rect.centery:
                    obj.move_down()
                elif obj.rect.centerx < block.rect.centerx:
                    obj.move_left()
                elif obj.rect.centery < block.rect.centery:
                    obj.move_up()
                elif obj.rect.centerx > block.rect.centerx:
                    obj.move_right()

                return True
        return False

    def collision_with_raquet(self, obj):
        if obj.rect.collidepoint(self.raquet_list.sprites()[0].rect.topleft):
            self.sound.raquet_effect()
            if obj.hdirection == 1:
                obj.hdirection = -1
            return True
        elif obj.rect.collidepoint(self.raquet_list.sprites()[0].rect.topright):
            if obj.hdirection == -1:
                obj.hdirction = 1
                self.sound.raquet_effect()
            return True
        elif obj.rect.colliderect(self.raquet_list.sprites()[0].rect):
            self.sound.raquet_effect()
            return True
        else:
            return False

    def collision_solid_roof(self, obj):
        for roof in self.roof_wall_blocks:
            if roof.rect.colliderect(obj.rect):
                self.sound.wall_effect()
                return True
        return False

    def draw(self, surface):
        self.move_background(surface)
        for wall in self.vertical_wall_blocks:
            wall.draw(surface)
        for roof in self.roof_wall_blocks:
            roof.draw(surface)
        for block in self.blocks:
            block.draw(surface)
        for raquet in self.raquet_list:
            raquet.draw(surface)
        for heart in self.heart_list:
            heart.draw(surface)

    def move_background(self, surface):
        self.background.draw(surface)

    def move_raquet(self, hdirection, vdirection):
        for raquet in self.raquet_list.sprites():
            raquet.move(self, hdirection, vdirection)

    def move_ball(self, surface):
        for ball in self.ball_list:
            ball.move(self)
            ball.draw(surface)
            if ball.rect.top < -10:
                self.ball_list.remove(ball)
            if ball.rect.bottom > SCREENRECT.height+200:
                self.try_to_reload_ball()
                self.ball_list.remove(ball)

    def get_lifes_number(self):
        lifes = 0
        for heart in self.heart_list:
            if heart.image_index == 0:
                lifes += 1

        return lifes

    def try_to_reload_ball(self):
        if self.get_lifes_number() > 1:
            self.heart_list.pop()
        else:
            self.inGame = False

    def game_is_running(self):
        return self.inGame

    def fix_game_clock(self, clock):
        # check for
        if int(clock) > self.block_down_animation_time:
            self.block_down_animation_time = int(clock) + 10
        if int(clock) > self.change_difficulty_timeoffset:
            self.change_difficulty_timeoffset = int(clock) + 10

    def update(self, surface, clock):
        self.fix_game_clock(clock)
        if int(clock) == self.block_down_animation_time:
            self.block_down_animation_time += 10
            for block in self.blocks:
                block.move_down()
            self.generate_new_row()
        if int(clock) == self.change_difficulty_timeoffset:
            self.change_difficulty_timeoffset += 10
            self.change_difficulty()
        self.update_score(surface)

    def generate_new_row(self):
        posy = 30
        for row in range(1):
            posx = 65
            for col in range(9):
                # block = blocks_to_build[get_random_index_in_list(blocks_to_build)]
                block = get_random_block()
                block.rect.left = posx + 5
                block.rect.top = posy + 10
                self.blocks.append(block)
                posx += 55
            posy += 36

    def update_score(self, surface):
        label = FONTRENDER.render("Score: %d" % self.SCORE, 10, (255, 255, 255))
        surface.blit(label, (SCREENRECT.width - 160, 10))


def get_random_block():
    if randint(0, 10) < 4:
        if randint(0, 4) < 3:
            return YellowBlock()
        else:
            return RedBlock()
    else:
        return BlueBlock()


def load_blocks():
    # [] [] [] [] [] [] [] [] []
    # [] [] [] [] [] [] [] [] []
    blocks = []
    posy = 30
    for rows in range(2):
        posx = 65
        for col in range(9):
            block = get_random_block()
            block.rect.left = posx+5
            block.rect.top = posy+10
            blocks.append(block)
            posx += 55

        posy += 34

    return blocks


def load_walls():
    roof_blocks = []
    vertical_blocks = []
    posx = 0
    for i in range(SCREENRECT.width):
        wall_block = WallBlock(posx, 0)
        roof_blocks.append(wall_block)
        posx += 32

    posy = 0
    for i in range(SCREENRECT.height):
        wall_block = WallBlock(0, posy)
        vertical_blocks.append(wall_block)
        wall_block = WallBlock(SCREENRECT.width-30, posy)
        vertical_blocks.append(wall_block)
        posy += 32

    return roof_blocks, vertical_blocks
