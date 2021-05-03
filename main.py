# Music :
# 8Bit Title Screen by https://opengameart.org/users/joth
# 8Bit Style Music by https://opengameart.org/users/tom-peter

import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.snd_dir = path.join(self.dir, "snd")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump.wav'))
        self.jetpack_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jetpack.wav'))
        self.g_o_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Fail.wav'))


    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        pg.mixer.music.load(path.join(self.snd_dir, 'Bob&#039;s Adventures - back34.ogg'))
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        jet_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for jet in jet_hits:
            self.jetpack_sound.play()
            self.player.vel.y = -JETPACK_POWER
            self.player.jumping = False

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        while len(self.platforms) < 8:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30),)
            #for plat in self.platforms:
                #overlapping = pg.sprite.spritecollide(plat, self.platforms, False)
                #for overlapping_plat in overlapping:
                    #overlapping_plat.kill()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, '8Bit Title Screen.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Bienvenue sur", 22, YELLOW, WIDTH / 2, HEIGHT * 1 / 4)
        self.draw_text(TITLE, 50, YELLOW, WIDTH / 2, HEIGHT * 1.3 / 4)
        self.draw_text("Utilisez les flèches pour vous déplacer et Espace pour sauter ", 20, WHITE, WIDTH / 2, HEIGHT * 2 / 4)
        self.draw_text("Appuyez sur n'importe quelle touche pour jouer", 20, WHITE, WIDTH / 2, HEIGHT * 2.5 / 4)
        self.draw_text("Meilleur Score: " + str(self.highscore), 20, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_g_o_screen(self):
        if not self.running:
            return
        self.g_o_sound.play()
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER !", 50, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Appuyez sur n'importe quelle touche pour rejouer", 22, WHITE, WIDTH / 2, HEIGHT * 2.5 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NOUVEAU RECORD !", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 30)
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text("Meilleur Score: " + str(self.highscore), 20, WHITE, WIDTH / 2, HEIGHT / 2 + 30)

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_g_o_screen()

pg.quit()
