import pygame as pg
import random

from library import *

class Taster(pg.sprite.Sprite):
    def __init__(self, position, color=WHITE):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([50,50])
        self.image.fill(color)
        self.direction = 0
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.velocity = 7
        self.velx = 0 
        self.vely = 0
        self.health = 200
        self.limit_blocks = None
    
    def gravity(self, gravity_value = 1):
        pass

    def check_collision(self):
        pass

    def move(self, key):
        if key == pg.K_DOWN:
            self.direction = 0
            self.velx = 0
            self.vely = self.velocity
        if key == pg.K_LEFT:
            self.direction = 1
            self.velx = -self.velocity
            self.vely = 0
        if key == pg.K_RIGHT:
            self.direction = 2
            self.velx = self.velocity
            self.vely = 0
        if key == pg.K_UP:
            self.direction = 3
            self.velx = 0
            self.vely = -self.velocity
    
    def stop(self):
        self.velx = 0
        self.vely = 0

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

