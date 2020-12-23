import pygame as pg
import random

import my_modules.classes as cls
import my_modules.library as lib


def level(screen, clock, map_json):
    '''flags'''
    end_game = False
    '''-----'''

    '''map loading'''
    blocks = lib.load_map(map_json)

    '''Sprite groups'''
    tasters = pg.sprite.Group()
    projectiles = pg.sprite.Group()
    modifiers = pg.sprite.Group()
    '''-------------'''

    '''objects'''
    taster = cls.Taster([100,100], blocks)
    tasters.add(taster)

    igneous_ball = cls.IgneousBall([lib.WIDTH // 2, lib.HEIGHT // 2], 1)
    projectiles.add(igneous_ball)
    enemy_igneous_ball = cls.EnemyIgneousBall([lib.WIDTH // 2, lib.HEIGHT // 2], 2)
    projectiles.add(enemy_igneous_ball)

    health_modifier = cls.HealthModifier([250, 250], blocks)
    damage_modifier = cls.IgneousBallModifier((290, 250), blocks)
    modifiers.add(health_modifier, damage_modifier)
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
        blocks.update()
        projectiles.update()
        modifiers.update()
        '''---------------'''

        '''Groups drawing'''
        screen.fill(lib.WHITE)
        tasters.draw(screen)
        blocks.draw(screen)
        projectiles.draw(screen)
        modifiers.draw(screen)
        '''--------------'''

        '''screen updating'''
        
        pg.display.flip()
        clock.tick(lib.FPS)
        '''---------------''' 
    
    return screen


def main():
    pg.init()
    screen = pg.display.set_mode([lib.WIDTH, lib.HEIGHT])
    clock = pg.time.Clock()

    
    screen = level(screen, clock, 'tiled/level01.json')
    


if __name__ == "__main__":
    main()