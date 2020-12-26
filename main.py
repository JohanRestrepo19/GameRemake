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
        self.all_sprites = pg.sprite.Group()
        self.blocks = lib.load_map('tiled/level01.json')

        self.taster = cls.Taster((300, 0), self.blocks, lib.GREEN)
        self.modifier = cls.Modifier((150, 150), self.blocks)
        self.player = cls.Player((300, 0), self.blocks)
        self.all_sprites.add(self.player, self.taster, self.modifier)


        n = 10

        for i in range(n):
            position = (400, 0)
            self.character = cls.Character(position, self.blocks)
            self.all_sprites.add(self.character)



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

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        self.blocks.update()


    def draw(self):
        # Game loop - draw
        self.screen.fill(lib.WHITE)
        self.all_sprites.draw(self.screen)
        self.blocks.draw(self.screen)
        pg.display.flip()

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
