import pygame

from .utils import SCREENRECT, load_image, load_images


class Background(pygame.sprite.Sprite):

    def __init__(self, difficulty_index=0):
        pygame.sprite.Sprite.__init__(self)
        self.difficulty = difficulty_index
        self.heading = 0  # N: 0 / E: 1 / S: 2 / W: 3
        self.x = -10
        self.y = -10
        self.image_index = self.difficulty
        self.images = load_images(['breakout_bg1.png', 'breakout_bg2.png', 'breakout_bg3.png'])
        self.background = self.images[0]

    def change_difficulty(self):
        if self.difficulty < 2:
            self.difficulty += 1
            self.image_index += 1

    def draw(self, surface):
        self.calculate_next_step()
        surface.blit(self.images[self.image_index], (self.x, self.y))

    def calculate_next_step(self):
        if self.heading == 0:
            if self.y == -10:
                self.heading = 1
            else:
                self.y -= 1
        elif self.heading == 1:
            if self.x == 0:
                self.heading = 2
            else:
                self.x += 1
        elif self.heading == 2:
            if self.y == 0:
                self.heading = 3
            else:
                self.y += 1
        elif self.heading == 3:
            if self.x == -10:
                self.heading = 0
            else:
                self.x -= 1


class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def move_down(self):
        self.rect.move_ip(0, 36)


class RedBlock(Block):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.images = load_images(['50x32red.png', '50x32redBroken1.png',
                                   '50x32redBroken2.png', '50x32redBroken.png'])

        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENRECT.width / 2
        self.rect.centery = 60
        self.life = 4

    def draw(self, surface):
        self.image = self.images[self.image_index]
        surface.blit(self.image, self.rect)

    def hitted(self):
        self.life -= 1
        if self.life == 3:
            self.image_index = 1
        elif self.life == 2:
            self.image_index = 2
        elif self.life == 1:
            self.image_index = 3
        elif self.life == 0:
            self.kill()


class YellowBlock(Block):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.images = load_images(['50x32yellow.png', '50x32yellowBroken1.png', '50x32yellowBroken.png'])
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENRECT.width / 2
        self.rect.centery = 60
        self.life = 3

    def draw(self, surface):
        self.image = self.images[self.image_index]
        surface.blit(self.image, self.rect)

    def hitted(self):
        self.life -= 1
        if self.life == 2:
            self.image_index = 1
        elif self.life == 1:
            self.image_index = 2
        elif self.life == 0:
            self.kill()


class BlueBlock(Block):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.images = load_images(['50x32blue.png', '50x32blueBroken.png'])
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREENRECT.width / 2
        self.rect.centery = 60
        self.life = 1

    def draw(self, surface):
        if self.life == 1:
            self.image = self.images[self.image_index]
        surface.blit(self.image, self.rect)

    def hitted(self):
        self.life -= 1
        if self.life == 1:
            self.image_index = 1
        elif self.life == 0:
            self.kill()


class ROBOT_IA(object):

    def __init__(self, GAME_MODE):
        self.raquet_speed = 3
        self.game_mode = GAME_MODE

    def move_raquet(self, scenario):
        if len(scenario.ball_list) == 0:
            scenario.shot()
        for ball in scenario.ball_list:
            for raquet in scenario.raquet_list.sprites():
                if ball.rect.centerx >= raquet.rect.centerx+10 and ball.vdirection == 1:
                    return 1
                elif ball.rect.centerx < raquet.rect.centerx-10 and ball.vdirection == 1:
                    return -1
        return 0

    def toggle_IA(self):
        if self.game_mode:
            self.game_mode = False
        else:
            self.game_mode = True

    def is_working(self):
        return self.game_mode


class Sound(object):

    def __init__(self, sound):
        # LOAD SOUND
        pygame.mixer.pre_init(54100, 16, 2, 4096)  # frequency, size, channels, buffersize
        pygame.init()  # turn all of pygame on.
        self.sound = True
        self._raquet_effect = pygame.mixer.Sound('mubreaker/res/raquet_touch.wav')
        self._wall_effect = pygame.mixer.Sound('mubreaker/res/wall_touch.wav')
        self._block_effect = pygame.mixer.Sound('mubreaker/res/block_touch.wav')

    def raquet_effect(self):
        if self.sound:
            self._raquet_effect.play()

    def wall_effect(self):
        if self.sound:
            self._wall_effect.play()

    def block_effect(self):
        if self.sound:
            self._block_effect.play()


class WallBlock(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.image = load_image('block_undestroyable.png')
        self.rect = self.image.get_rect()
        self.rect.left = posx
        self.rect.top = posy
        self.animation_time = 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Heart(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = load_images(['heart_red.png', 'heart_blank.png'])
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = (x, y)

    def draw(self, surface):
        surface.blit(self.images[self.image_index], self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 8
        self.image = load_image('balls/ball1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        self.hdirection = -1  # -1: left / 1: right
        self.vdirection = -1  # -1:up 1: down

    def move_up(self):
        self.vdirection = -1

    def move_down(self):
        self.vdirection = 1

    def move_left(self):
        self.hdirection = -1

    def move_right(self):
        self.hdirection = 1

    def move(self, scenario):
        if scenario.collision_solid_wall_left(self):
            self.move_right()
        elif scenario.collision_solid_wall_right(self):
            self.move_left()
        elif scenario.collision_solid_roof(self):
            self.move_down()
        elif scenario.collision_with_raquet(self):
            self.move_up()
        elif scenario.collision_block(self):
            pass

        self.rect.move_ip(self.hdirection * self.speed, 0)
        self.rect.move_ip(0, self.vdirection * self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Raquet(pygame.sprite.Sprite):

    def __init__(self, difficulty, posx=0, posy=0):
        pygame.sprite.Sprite.__init__(self)
        self.images = load_images(['paleta_easy.png', 'paleta_medium.png'])
        self.image_index = 0
        self.speed = 14
        if difficulty == "EASY":
            self.image_index = 0
        elif difficulty == "MEDIUM":
            self.image_index = 1
        elif difficulty == "HARD":
            self.image_index = 1

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        if posx == 0 and posy == 0:
            self.rect.centerx = SCREENRECT.width/2
            self.rect.centery = SCREENRECT.height-10
        else:
            self.rect.centerx = posx
            self.rect.centery = posy

        self.alive = True

    def move(self, scenario, hdirection, vdirection):
        if scenario.collision_solid_wall_left(self):
            self.rect.move_ip(10, 0)
        elif scenario.collision_solid_wall_right(self):
            self.rect.move_ip(-10, 0)
        else:
            self.rect.move_ip(hdirection*self.speed, 0)
            self.rect.move_ip(0, vdirection * self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
