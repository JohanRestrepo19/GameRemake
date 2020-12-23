import pygame as pg
import random
import my_modules.library as lib


class Taster(pg.sprite.Sprite):
    def __init__(self, position, limit_blocks = None, color = lib.BLACK):
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
        self.limit_blocks =  limit_blocks
    
    def gravity(self, gravity_value = lib.GRAVITY):
        if self.vely != 0:
            self.vely += gravity_value

    def check_collision(self):
        collision_ls = pg.sprite.spritecollide(self, self.limit_blocks, False):
        for block in collision_ls:
            if self.rect.top 

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
            self.vely = -self.velocity * 2
  
    def stop(self):
        self.velx, self.vely = 0, 0

    def update(self):
        self.gravity()
        self.rect.x += self.velx
        self.rect.y += self.vely
        

#ls = list
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
    damage = 10
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
        self.damage = Projectile.damage
    
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

class IgneousBall(Projectile):
    damage = 20
    def __init__(self, position, direction, sprite_route = 'resources/images/sprites/IgneousBall.png'):
        Projectile.__init__(self, position, direction, sprite_route)
        self.damage = IgneousBall.damage
        print(self.damage)

class EnemyIgneousBall(Projectile):
    damage = 20
    def __init__(self, position, direction, sprite_route = 'resources/images/sprites/DragonBreath.png'):
        Projectile.__init__(self, position, direction, sprite_route)
        self.damage = EnemyIgneousBall.damage
        print(self.damage)
        
class Modifier(pg.sprite.Sprite):
    def __init__(self, position, limit_blocks = None, sprite_route = 'resources/images/sprites/Modifiers.png', col = 10, row = 4, sprite_position = [0,0]):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, col, row)
        self.image = self.sprite_mx[sprite_position[0]][sprite_position[1]]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.vely = 0.1
        self.limit_blocks = limit_blocks

    def gravity(self, gravity_value = lib.GRAVITY):
        if self.vely != 0:
            self.vely += gravity_value

    def check_collision(self):
        collision_ls = pg.sprite.spritecollide(self, self.limit_blocks, False)
        
        for block in collision_ls:
            if self.rect.bottom >= block.rect.top:
                self.rect.bottom = block.rect.top
                self.vely = 0
    
    def move(self):
        self.rect.y += self.vely
        
    def update(self):
        self.gravity()
        self.check_collision()
        self.move()

class HealthModifier(Modifier):
    life_increase = 249
    def __init__(self, position, limit_blocks = None, sprite_route = 'resources/images/sprites/Modifiers.png', col = 10, row = 4, sprite_position = [0, 0]):        
        Modifier.__init__(self, position, limit_blocks, sprite_route, col, row, sprite_position)

class IgneousBallModifier(Modifier):
    damage_increase = 20
    change_appearance = 'resources/images/sprites/DragonBreath.png'

    def __init__(self, position, limit_blocks = None, sprite_route = 'resources/images/sprites/Modifiers.png', col = 10, row = 4, sprite_position = [2, 5]):        
        Modifier.__init__(self, position, limit_blocks, sprite_route, col, row, sprite_position)

class Character(pg.sprite.Sprite):
    def __init__(self, position, limit_blocks = None, sprite_route = 'resources/images/sprites/BlackOccultist.png', col = 3, row = 4):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, col, row)
        self.direction = 0
        self.sprite_counter = 0
        self.image = self.sprite_mx[self.direction][self.sprite_counter]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.limit_blocks = limit_blocks
        #Movement counter is used to define the behavior of some enemies
        self.movement_counter = 60   
        self.movement_counter_limit = 60
        self.velocity = 5
        self.velx, self.vely = self.velocity, 0.1
        self.health = 200
        self.collision_damage = 1
        self.reward_score = 10
        self.death_sound = None
        self.damage_sound = None

    def gravity(self, gravity_value = lib.GRAVITY):
        if self.vely != 0: 
            self.vely += gravity_value

    def check_collision(self):
        collision_ls = pg.sprite.spritecollide(self, self.limit_blocks, False)
        pass

    def sprite_animation(self):
        pass

    def move(self):
        pass

    
    def update(self):
        pass