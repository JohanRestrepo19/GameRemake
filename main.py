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
        self.player = None

    def map_movement(self, *groups):
        # Checking the limits on the x-axis
        if self.player.rect.right >= lib.RIGHT_LIMIT:
            self.player.rect.right = lib.RIGHT_LIMIT
            # Background
            # Access to each group
            for group in groups:
                # Change the position of each entity
                for entity in group:
                    entity.rect.x -= self.player.velx
        elif self.player.rect.left <= lib.LEFT_LIMIT:
            self.player.rect.left = lib.LEFT_LIMIT
            # Background
            for group in groups:
                for entity in group:
                    entity.rect.x += abs(self.player.velx)

        # Checking the limits on the y-axis
        if self.player.rect.top <= lib.UPPER_LIMIT:
            self.player.rect.top = lib.UPPER_LIMIT
            # Background
            for group in groups:
                for entity in group:
                    entity.rect.y += abs(self.player.vely)
        elif self.player.rect.bottom >= lib.LOWER_LIMIT:
            self.player.rect.bottom = lib.LOWER_LIMIT
            # Background
            for group in groups:
                for entity in group:
                    entity.rect.y -= abs(self.player.vely)

    def new(self, map_json):
        # start a new game
        '''Creation of all groups'''
        # Must be replaced by load_map function
        groups_dc = lib.load_map(map_json, self)

        self.all_entities = groups_dc['all_entities']
        self.blocks = groups_dc['blocks']
        self.spikes = groups_dc['spikes']
        self.modifiers = groups_dc['modifiers']
        self.projectiles = groups_dc['projectiles']
        self.were_wolf_vipers = groups_dc['were_wolf_vipers']


        '''self.all_entities = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.modifiers = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.were_wolf_vipers = pg.sprite.Group()'''

        '''Creating objects and add them to their corresponding group'''
        self.taster = cls.Taster((300, 0), self, lib.GREEN)
        self.all_entities.add(self.taster)

        self.player = cls.Player((300, 0), self)
        self.all_entities.add(self.player)



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
        self.spikes.update()
        self.were_wolf_vipers.update()
        self.map_movement(self.all_entities, self.modifiers, self.projectiles, self.blocks, self.spikes, self.were_wolf_vipers)

    def draw(self):
        # Game loop - draw
        self.all_entities.draw(self.screen)
        self.blocks.draw(self.screen)
        self.spikes.draw(self.screen)
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
        game.new('tiled/level01.json')

        game.show_game_over_screen()

    pg.quit()

if __name__ == "__main__":
    main()
