import pygame as pg
import random

import my_modules.classes as cls
import my_modules.library as lib

class Game:
    def __init__(self):
        # Initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((lib.WIDTH, lib.HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        '''Creation of all groups'''
        # Must be replaced by load_map function
        self.all_entities = pg.sprite.Group()
        self.blocks = lib.load_map('tiled/level01.json')
        self.modifiers = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.were_wolf_vipers = pg.sprite.Group()

        '''Creating objects and add them to their corresponding group'''
        self.taster = cls.Taster((300, 0), self, lib.GREEN)
        self.all_entities.add(self.taster)

        self.modifier = cls.HealthModifier((150, 150), self)
        self.modifiers.add(self.modifier)

        self.player = cls.Player((300, 0), self)
        self.all_entities.add(self.player)

        self.igneous_ball = cls.IgneousBall((200, 200), 2, self)
        #self.projectiles.add(self.igneous_ball)

        self.harpy = cls.Harpy((200, 200), self)
        #self.all_entities.add(self.harpy)

        self.dragon = cls.Dragon((600, 30), self)
        self.all_entities.add(self.dragon)

        self.viper = cls.Viper((400, 0), self)
        #self.all_entities.add(self.viper)
        
        self.golem = cls.Golem((400, 0), self)
        self.all_entities.add(self.golem)

        self.were_wolf = cls.WereWolf((400, 0), self)
        #self.all_entities.add(self.were_wolf)

        n = 0

        for i in range(n):
            position = (400, 0)
            self.occultist = cls.Occultist(position, self)
            self.all_entities.add(self.occultist)

        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(lib.FPS)

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_F1:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        # Game loop - update
        self.all_entities.update()
        self.modifiers.update()
        self.projectiles.update()
        self.blocks.update()
        self.were_wolf_vipers.update()

    def draw(self):
        # Game loop - draw
        self.all_entities.draw(self.screen)
        self.blocks.draw(self.screen)
        self.modifiers.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.were_wolf_vipers.draw(self.screen)
        pg.display.flip()
        self.screen.fill(lib.BG_COLOR)

    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass

def main():
    game = Game()
    game.show_start_screen()

    while game.running:
        game.new()

        game.show_game_over_screen()

    pg.quit()

if __name__ == "__main__":
    main()
