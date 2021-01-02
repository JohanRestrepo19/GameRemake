import pygame as pg
import random
import my_modules.library as lib


class Taster(pg.sprite.Sprite):
    def __init__(self, position, game, color = lib.BLACK):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([50, 50])
        self.image.fill(color)
        self.direction = 0
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.velocity = 7
        self.velx, self.vely = 0, 0
        self.health = 200
        self.on_ground = False
        self.collision_damage = 0

    def gravity(self, gravity_value = lib.GRAVITY):
        if not self.on_ground:
            self.vely += gravity_value

    def move(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.velx = -self.velocity
        if keys[pg.K_d]:
            self.velx = self.velocity
        if keys[pg.K_w] and self.on_ground:
            self.vely = -12
        if keys[pg.K_s]:
            self.vely = self.velocity


    def update(self):
        self.velx = 0
        self.gravity()
        self.move()

        self.rect.x += self.velx
        #Check collision on the x-axis
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)
        for block in collision_ls:
            if (self.rect.right >= block.rect.left) and (self.velx > 0):
                self.rect.right = block.rect.left
                self.velx = 0

            if self.rect.left <= block.rect.right and (self.velx < 0):
                self.rect.left = block.rect.right
                self.velx = 0

        self.rect.y += self.vely

        # Check collision on the y-axis
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)

        # if there is not collision with any block below then self.on_ground
        # must be False because the character is not on the floor
        if not collision_ls:
            self.on_ground = False

        for block in collision_ls:
            if (self.rect.bottom >= block.rect.top) and (self.vely > 0):
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.vely = 0

            if (self.rect.top <= block.rect.bottom) and (self.vely < 0):
                self.rect.top = block.rect.bottom
                self.vely = 0
                self.on_ground = False

#ls = list
# mx = matrix
class Block(pg.sprite.Sprite):
    def __init__(self, position, sprite_route, sprite_position):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, 5, 1)
        self.image = self.sprite_mx[sprite_position[0]][sprite_position[1]].convert()
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

    def get_damage(self):
        return self.damage

class Projectile(pg.sprite.Sprite):
    damage = 10
    def __init__(self, position, direction, game, sprite_route = 'resources/images/sprites/IgneousBall.png'):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, 4, 2)
        self.sprite_size = 1
        self.direction = direction
        self.sprite_direction = 0
        self.game = game
        self.image = self.sprite_mx[self.sprite_size][self.sprite_direction]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.velocity = 4
        self.velx, self.vely = 0, 0
        self.damage = Projectile.damage
    
    def get_damage(self):
        return self.damage

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

        '''Blocks collision'''
        # Check if projectile collides with any block and then kills it
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)
        if collision_ls:
            self.kill()

        '''Projectile out of screen'''
        # Since the projectile only moves in the x-axis then only that direction is checked
        if (self.rect.x > lib.WIDTH) or (self.rect.x < 0):
            self.kill()
            print(f'Igneous balls on screen {len(self.game.projectiles)}')

class IgneousBall(Projectile):
    damage = 20
    def __init__(self, position, direction, game,sprite_route = 'resources/images/sprites/IgneousBall.png'):
        Projectile.__init__(self, position, direction, game, sprite_route)
        self.damage = IgneousBall.damage
        
    def update(self):
        Projectile.update(self)

        '''Check collision with enemies and enemy igneous ball'''
        # Collision with enemies
        collision_ls = pg.sprite.spritecollide(self, self.game.all_entities, False)

        for enemy in collision_ls:
            # The Igneous ball will hit only the enemies in the all entities group
            if not isinstance(enemy, Player):
                enemy.health -= self.damage
                self.kill()

class EnemyIgneousBall(Projectile):
    damage = 20
    def __init__(self, position, direction, game, sprite_route = 'resources/images/sprites/DragonBreath.png'):
        Projectile.__init__(self, position, direction, game, sprite_route)
        self.damage = EnemyIgneousBall.damage
        

    def update(self):
        Projectile.update(self)

        '''Check collision with player'''
        collision_ls = pg.sprite.spritecollide(self, self.game.all_entities, False)
        for player in collision_ls:
            if isinstance(player, Player):
                player.health -= self.damage
                self.kill()
                print(f"(EnemyIgenousBall) Player's health: {player.health}")


class Modifier(pg.sprite.Sprite):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Modifiers.png', col = 10, row = 4, sprite_position = [0,0]):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, col, row)
        self.image = self.sprite_mx[sprite_position[0]][sprite_position[1]]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.vely = 0.1
        self.game = game

    def gravity(self, gravity_value = lib.GRAVITY):
        if self.vely != 0:
            self.vely += gravity_value

    def check_collision(self):
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)

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
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Modifiers.png', col = 10, row = 4, sprite_position = [0, 0]):
        Modifier.__init__(self, position, game, sprite_route, col, row, sprite_position)

class IgneousBallModifier(Modifier):
    damage_increase = 20
    change_appearance = 'resources/images/sprites/DragonBreath.png'

    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Modifiers.png', col = 10, row = 4, sprite_position = [2, 5]):
        Modifier.__init__(self, position, game, sprite_route, col, row, sprite_position)

class Character(pg.sprite.Sprite):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/BlackOccultist.png', col = 3, row = 4):
        pg.sprite.Sprite.__init__(self)
        self.sprite_mx = lib.crop_image(sprite_route, col, row)
        self.direction = 0
        self.sprite_counter = 0
        self.image = self.sprite_mx[self.direction][self.sprite_counter]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.game = game
        #Movement counter is used to define the behavior of some enemies
        self.movement_counter = 60
        self.movement_counter_limit = lib.FPS * 3
        self.velocity = 2
        self.velx, self.vely = 0, 0
        self._health = 200
        self._collision_damage = 1
        self.reward_score = 10
        self.death_sound = None
        self.damage_sound = None
        self.on_ground = False

    '''I'm using decorators just for try them out'''
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health):
        #fprint('Taking damage')
        self._health = health

    @property
    def collision_damage(self):
        return self._collision_damage


    def gravity(self, gravity_value = lib.GRAVITY):
        if not self.on_ground:
            self.vely += gravity_value
        if self.on_ground:
            self.vely = 0

    def move(self):
        if self.movement_counter > self.movement_counter_limit:
            self.direction = random.randint(1, 2)

            # move to the left direction
            if self.direction == 1:
                self.velx = -self.velocity
            # move to the right direction
            if self.direction == 2:
                self.velx = self.velocity

            self.movement_counter = 0
        else:
            # self.movement_counter increases with the len of the actions list that the character is currently doing
            self.movement_counter += len(self.sprite_mx[self.direction])

    def sprite_animation(self):
        if (self.velx != 0):
            if self.sprite_counter < lib.FPS:
                self.sprite_counter += 1
            else:
                self.sprite_counter = 0

            # sprite_divider is the number which is used to divide the counter of the sprites
            # in base of the FPS

            sprite_divider = (lib.FPS // len(self.sprite_mx[self.direction])) + 1
            self.image = self.sprite_mx[self.direction][self.sprite_counter // sprite_divider]

    def check_health(self):
        # Check if the character is still alive, if the health is less than zero it dies
        if self.health < 0:
            self.kill()

    def update(self):
        self.gravity()
        self.move()
        self.sprite_animation()

        self.rect.x += self.velx
        # Check collision on the x-axis
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)
        for block in collision_ls:
            # Check collision with blocks to the right of the character
            if (self.rect.right >= block.rect.left) and (self.velx > 0):
                self.rect.right = block.rect.left
                self.velx = 0
            # Check collision with blocks to the left of the character
            if (self.rect.left <= block.rect.right) and (self.velx < 0):
                self.rect.left = block.rect.right
                self.velx = 0

        self.rect.y += self.vely

        # Check collision on the y-axis
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)

        # if there is not collision with any block below then self.on_ground
        # must be False because the character is not on the floor
        if not collision_ls:
            self.on_ground = False

        for block in collision_ls:
            # Check collision with blocks below the character
            if (self.rect.bottom >= block.rect.top) and (self.vely > 0):
                self.rect.bottom = block.rect.top
                self.on_ground = True
                self.vely = 0

            #Check collision with block above the character
            if (self.rect.top <= block.rect.bottom) and (self.vely < 0):
                self.rect.top = block.rect.bottom
                self.vely = 0
                self.on_ground = False
        
        self.check_health()        

class Player(Character):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Player.png', col = 3, row = 2):
        Character.__init__(self, position, game, sprite_route, col, row)
        self.velocity = 5
        self.score = 0
        self.shot_counter = lib.FPS
        self.cool_down_shot = lib.FPS // 2

    def move(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.velx = -self.velocity
            self.direction = 0
        if keys[pg.K_RIGHT]:
            self.velx = self.velocity
            self.direction = 1
        if keys[pg.K_UP] and self.on_ground:
            self.vely = -12

    def shoot(self):
        keys = pg.key.get_pressed()
        if (self.shot_counter > self.cool_down_shot) and keys[pg.K_SPACE]:
            self.shot_counter = 0
            position = (self.rect.x, self.rect.y)
            #Check the direction the player is heading
            if self.direction == 0:                #
                # Direction 0 means the player is moving to the left
                # and the left direction of the igneous ball is 1
                direction = 1
            if self.direction == 1:
                # Direction 1 means the player is moving to the right
                # and the right direction of the igneous ball is 2
                direction = 2

            new_igneous_ball = IgneousBall(position, direction, self.game)
            self.game.projectiles.add(new_igneous_ball)
            print(f'Number of igneous balls on screen {len(self.game.projectiles)}')
        else:
            self.shot_counter += 1


    def update(self):
        #print(f"Player's velocity: ({self.velx}, {self.vely})")
        self.velx = 0
        self.move()
        Character.update(self)
        self.shoot()

        '''Check collision with normal enemies'''
        collision_ls = pg.sprite.spritecollide(self, self.game.all_entities, False)
        for enemy in collision_ls:
            if not isinstance(enemy, (Player, Block, Modifier, IgneousBall, Dragon, WereWolf, Taster)):
                self.health -= enemy.collision_damage
                #self.set_health(self.get_health() - enemy.get_collision_damage())
                print(f"Player's health {self.health}")

        '''Check collision with modifiers'''
        collision_ls = pg.sprite.spritecollide(self, self.game.modifiers, True)
        for modifier in collision_ls:
            if isinstance(modifier, HealthModifier):
                self.health += HealthModifier.life_increase
                print(f"Player's increase life to : {self.health}")
            elif isinstance(modifier, IgneousBallModifier):
                IgneousBall.damage += IgneousBallModifier.damage_increase
                print(f"Igenous ball's damage: {IgneousBall.damage}")

        '''Check collision with special enemies'''
        # Dragon, Were-wolf
        collision_ls = pg.sprite.spritecollide(self, self.game.all_entities, False)
        for enemy in collision_ls:
            if isinstance(enemy, (Dragon, WereWolf)):
                self.health -= enemy.collision_damage
                print(f"(Special enemy) Player's health {self.health}")

        # Due to the fact that the Werewolf's vipers are in a different gruop
        # it is necessary to check them in another collision check

        collision_ls = pg.sprite.spritecollide(self, self.game.were_wolf_vipers, False)
        for viper in collision_ls:
            self.health -= viper.collision_damage
            print(f"(Viper) Player's health {self.health}")

class Occultist(Character):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Occultist.png'):
        Character.__init__(self, position, game, sprite_route)

class Harpy(Character):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Harpy.png'):
        Character.__init__(self, position, game, sprite_route)
        self.movement_counter_limit = lib.FPS * 2

    def move(self):
        if self.movement_counter > self.movement_counter_limit:
            self.direction = random.randint(0, 3)

            # move down direction
            if self.direction == 0:
                self.vely = self.velocity

            # move left direction
            if self.direction == 1 :
                self.velx = -self.velocity

            # move right direction
            if self.direction == 2:
                self.velx = self.velocity

            # move up direction
            if self.direction == 3:
                self.vely = -self.velocity

            self.movement_counter = 0
        else:
            self.movement_counter += len(self.sprite_mx[self.direction])

    def update(self):
        self.move()
        self.sprite_animation()

        self.rect.x += self.velx
        # Check collision on the x-axis
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)
        for block in collision_ls:
            if (self.rect.right >= block.rect.left) and (self.velx > 0):
                self.rect.right = block.rect.left
                self.velx = 0
            if (self.rect.left <= block.rect.right) and (self.velx < 0):
                self.rect.left = block.rect.right
                self.velx = 0

        self.rect.y += self.vely
        # Checko collision on the y-axis
        collision_ls = pg.sprite.spritecollide(self, self.game.blocks, False)
        for block in collision_ls:
            if (self.rect.bottom >= block.rect.top) and (self.vely > 0):
                self.rect.bottom = block.rect.top
                self.vely = 0
            if (self.rect.top <= block.rect.bottom) and (self.vely < 0):
                self.rect.top = block.rect.bottom
                self.vely = 0
        
        Character.check_health(self)

class Dragon(Harpy):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Dragon.png'):
        Harpy.__init__(self, position, game, sprite_route)
        self.cool_down_shot = lib.FPS * 2
        self.shot_counter = 0
        self.health = 200
        # The dragon boss is always heading to the left
        self.direction = 1

    def shoot(self):
        if (self.shot_counter > self.cool_down_shot):
            self.shot_counter = 0
            position = (self.rect.midleft)
            direction = self.direction

            new_igneous_ball = EnemyIgneousBall(position, direction, self.game)
            self.game.projectiles.add(new_igneous_ball)
        else:
            self.shot_counter += 1

    def move(self):
        if (self.movement_counter > self.movement_counter_limit):
            # Since the dragon is always heading to the left
            # it is not necessary to define the new direction
            # the dragon will be heading
            self.movement_counter = 0
            move_direction = random.randint(0, 1)

            # Move up
            if move_direction == 0:
                self.vely = -self.velocity
            # Move down
            if move_direction == 1:
                self.vely = self.velocity

        else:
            self.movement_counter += len(self.sprite_mx[self.direction])

    def sprite_animation(self):
        if (self.vely != 0):
            if self.sprite_counter < lib.FPS:
                self.sprite_counter += 1
            else: self.sprite_counter = 0

            sprite_divider = (lib.FPS // len(self.sprite_mx[self.direction])) + 1
            self.image = self.sprite_mx[self.direction][self.sprite_counter // sprite_divider]

    def update(self):
        Harpy.update(self)
        self.shoot()

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vely = 0

class Viper(Character):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Viper.png'):
        Character.__init__(self,position, game, sprite_route)
        self.jump_distance = -12
        self.cool_down_jump = lib.FPS * 2
        self.jump_counter = random.randint(0, self.cool_down_jump)

    def jump(self):
        if self.jump_counter > self.cool_down_jump:
            self.jump_counter = 0
            self.vely = self.jump_distance
        else:
            self.jump_counter += 1
    
    def update(self):
        self.jump()
        Character.update(self)

class Golem(Character):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/Golem.png'):
        Character.__init__(self, position, game, sprite_route)
        self.cool_down_shot = lib.FPS
        self.shot_counter = self.cool_down_shot

    def shoot(self):        
        if self.shot_counter > self.cool_down_shot:
            self.shot_counter = 0
            if self.velx > 0:
                position = (self.rect.right, self.rect.y)
                direction = 2
                new_igneous_ball = EnemyIgneousBall(position, direction, self.game)
                self.game.projectiles.add(new_igneous_ball)
            
            if self.velx < 0:
                position = (self.rect.left, self.rect.y)
                direction = 1
                new_igneous_ball = EnemyIgneousBall(position, direction, self.game)
                self.game.projectiles.add(new_igneous_ball)
        else:
            self.shot_counter += 1

    def update(self):
        self.shoot()
        Character.update(self)

class WereWolf(Character):
    def __init__(self, position, game = None, sprite_route = 'resources/images/sprites/WereWolf.png'):
        Character.__init__(self, position, game, sprite_route)
        self.viper_limit = 5

    def invoke(self):
        if (len(self.game.were_wolf_vipers) < self.viper_limit):
            position = self.rect.center
            new_viper = Viper(position, self.game)
            self.game.were_wolf_vipers.add(new_viper)
            print(f"Were-wolf's viper amount {len(self.game.were_wolf_vipers)}")
    
    def update(self):
        self.invoke()
        Character.update(self)
        
