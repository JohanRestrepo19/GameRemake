import pygame as pg
import random

from classes.classes import *
from library import *


def main():
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    '''Flags'''
    end = False
    '''-----'''

    '''Sprite groups'''
    tasters = pg.sprite.Group()
    '''-------------'''

    '''objects'''
    taster = Taster([100,100])
    tasters.add(taster)
    '''-------'''

    while not end:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end = True
            if event.type == pg.KEYDOWN:
                taster.move(event.key)
            if event.type == pg.KEYUP:
                taster.stop()

        '''Groups updating'''
        tasters.update()
        '''---------------'''

        '''Groups drawing'''
        screen.fill(BLACK)
        tasters.draw(screen)
        '''--------------'''

        '''screen updating'''
        
        pg.display.flip()
        clock.tick(60)
        '''---------------''' 


if __name__ == "__main__":
    main()