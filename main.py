import pygame as pg
import random

from library import * 

def level(screen, clock, map_json):
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

    '''map loading'''
    blocks = load_map(map_json)

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
        blocks.update()
        '''---------------'''

        '''Groups drawing'''
        screen.fill(WHITE)
        tasters.draw(screen)
        blocks.draw(screen)
        '''--------------'''

        '''screen updating'''
        
        pg.display.flip()
        clock.tick(FPS)
        '''---------------''' 
    
    return screen


def main():
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    
    #screen = level(screen, clock, 'tiled/level01.json')
    


if __name__ == "__main__":
    main()