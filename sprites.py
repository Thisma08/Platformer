import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 2, height * 2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.pos = vec(WIDTH / 2, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.idle_frames = [self.game.spritesheet.get_image(0, 0, 9, 21),
                            self.game.spritesheet.get_image(9, 0, 9, 20)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        self.walking_frames_r = [self.game.spritesheet.get_image(18, 0, 9, 21),
                                 self.game.spritesheet.get_image(27, 0, 10, 21),
                                 self.game.spritesheet.get_image(37, 0, 9, 21),
                                 self.game.spritesheet.get_image(46, 0, 9, 21),
                                 self.game.spritesheet.get_image(55, 0, 9, 20)]

        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame_r = self.game.spritesheet.get_image(73, 0, 17, 20)
        self.jump_frame_r.set_colorkey(BLACK)

        self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)
        self.jump_frame_l.set_colorkey(BLACK)

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x < -20:
            self.pos.x = WIDTH + 20
        if self.pos.x > WIDTH + 20:
            self.pos.x = -20
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:

                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            if self.vel.x >= 0:
                bottom = self.rect.bottom
                self.image = self.jump_frame_r
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            else:
                bottom = self.rect.bottom
                self.image = self.jump_frame_l
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            self.idle = True

        if self.idle:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game,  x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        image = self.game.spritesheet.get_image(0, 21, 25, 8)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < JETPACK_SPAWN_RATE:
            Jetpack(self.game, self)


class Jetpack(pg.sprite.Sprite):
    def __init__(self, game,  plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        image = self.game.spritesheet.get_image(25, 21, 10, 8)
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()






