import pygame as pg
import random
import my_modules.library as lib


class Taster(pg.sprite.Sprite):
    def __init__(self, position, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([50, 50])
        self.image.fill(color)
        self.direction = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.velocity = 7
        self.velx = 0
        self.vely = 0
        self.health = 200
        self.limit_blocks = None
    
    def gravity(self, gravity_value=1):
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

# mx = matrix
class Block(pg.sprite.Sprite):
    def __init__(self, position, sprite_route, sprite_position):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, 5, 1)
        self.image = self.sprite_mx[sprite_position[0]][sprite_position[1]]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        
    def update(self):
        pass

class LimiterBlock(Block):
    def __init__(self, position, sprite_route, sprite_position):
        Block.__init__(self, position, sprite_route, sprite_position)

class Spike(Block):
    def __init__(self, position, sprite_route, sprite_position):
        Block.__init__(self, position, sprite_route, sprite_position)
        self.sprite_mx = lib.crop_image(sprite_route, 2, 1)
        self.image = self.sprite_mx[sprite_position[0]][sprite_position[1]]
        self.damage = 1

class Projectile(pg.sprite.Sprite):
    def __init__(self, position, direction, sprite_route = 'resources/images/sprites/IgneousBall.png'):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, 4, 2)
        self.sprite_size = 1
        self.direction = direction
        self.sprite_direction = 0
        self.image = self.sprite_mx[self.sprite_size][self.sprite_direction]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.velocity = 4
        self.velx, self.vely = 0, 0
        self.damage = 10
    
    def move(self):
        # if direction equals to 1 that means that projectile will head to left direction
        if self.direction == 1:
            self.velx = -self.velocity
            self.sprite_direction = 1
        
        # if direction equals to 2 that means that projectile will head to right direction
        if self.direction == 2:
            self.velx = self.velocity
            self.sprite_direction = 0

        self.rect.x += self.velx
        self.rect.y += self.vely

    def sprite_draw(self):
        self.image = self.sprite_mx[self.sprite_size][self.sprite_direction]

    def update(self):
        self.move()
        self.sprite_draw()
        