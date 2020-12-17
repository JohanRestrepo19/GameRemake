import pygame as pg
import random

from classes.classes import *
from library import *

def level01(screen, clock):
    '''flags'''
    end_game = False
    '''-----'''

    '''Sprite groups'''
    tasters = pg.sprite.Group()
    '''-------------'''

    '''objects'''
    taster = Taster([100,100], BLACK)
    tasters.add(taster)
    '''-------'''

    while not end_game:
        '''Events management''' 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end_game = True
            if event.type == pg.KEYDOWN:
                taster.move(event.key)
                if event.key == pg.K_SPACE:
                    end_game = True
            if event.type == pg.KEYUP:
                taster.stop()
                
        
        '''Groups updating'''
        tasters.update()
        '''---------------'''

        '''Groups drawing'''
        screen.fill(WHITE)
        tasters.draw(screen)
        '''--------------'''

        '''screen updating'''
        
        pg.display.flip()
        clock.tick(60)
        '''---------------''' 
    
    return screen

def level02(screen, clock):
    '''flags'''
    end_game = False
    '''-----'''

    '''Sprite groups'''
    tasters = pg.sprite.Group()
    '''-------------'''

    '''objects'''
    taster = Taster([100,100], BLUE_2)
    tasters.add(taster)
    '''-------'''

    while not end_game:
        '''Events management''' 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                end_game = True
            if event.type == pg.KEYDOWN:
                taster.move(event.key)
                if event.key == pg.K_SPACE:
                    end_game = True
            if event.type == pg.KEYUP:
                taster.stop()
                
        
        '''Groups updating'''
        tasters.update()
        '''---------------'''

        '''Groups drawing'''
        screen.fill(YELLOW)
        tasters.draw(screen)
        '''--------------'''

        '''screen updating'''
        
        pg.display.flip()
        clock.tick(60)
        '''---------------''' 


        
