import pygame as pg
import random
import json
import os

import my_modules.classes as cls

WIDTH = 800
HEIGHT = 600
RIGHT_LIMIT = WIDTH - 200
LEFT_LIMIT = 200
UPPER_LIMIT = 100
LOWER_LIMIT = HEIGHT - 100

FPS = 60
GRAVITY = 0.5

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLUE_2 = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
CYAN = (0, 176, 246)
BG_COLOR = CYAN

def crop_image(image_route, columns, rows):
    image = pg.image.load(image_route)
    image_info = image.get_rect()
    image_width = image_info[2]
    image_height = image_info[3]

    sprite_width = image_width // columns
    sprite_height = image_height // rows

    sprites_row = []
    sprites_matrix = []

    for row in range(rows):
        for column in range(columns):
            sprite = image.subsurface(column*sprite_width, row*sprite_height, sprite_width, sprite_height)
            sprites_row.append(sprite)
        sprites_matrix.append(sprites_row)
        sprites_row = []

    return sprites_matrix


def load_json(route):
    with open(route) as content:
        json_information = json.load(content)
    content.close()
    return json_information

# dc: dictionary
# ls: list


def load_map(json_route, game):
    #sprite groups
    all_entities = pg.sprite.Group()
    blocks = pg.sprite.Group()
    spikes = pg.sprite.Group()
    modifiers = pg.sprite.Group()
    projectiles = pg.sprite.Group()
    were_wolf_vipers = pg.sprite.Group()
    groups_dc = {}

    #json information
    map_information = load_json(json_route)
    map_dc = map_information['layers'][0]
    map_ls = map_dc['data']
    row_limit = map_dc['height']
    column_limit = map_dc['width']
    block_counter = 0

    # Creating all objects and add them to their corresponding group
    for row in range(row_limit):
        for column in range(column_limit):
            position = [column*32, row*32]
            if map_ls[block_counter] == 1:
                block = cls.LimiterBlock(position, 'resources/images/sprites/Blocks.jpg', [0,0])
                blocks.add(block)
            elif map_ls[block_counter] == 6:
                dragon = cls.Dragon(position, game)
                all_entities.add(dragon)
            elif map_ls[block_counter] == 18:
                golem = cls.Golem(position, game)
                all_entities.add(golem)
            elif map_ls[block_counter] == 30:
                harpy = cls.Harpy(position, game)
                all_entities.add(harpy)
            elif map_ls[block_counter] == 42:
                occultist = cls.Occultist(position, game)
                all_entities.add(occultist)
            elif map_ls[block_counter] == 54:
                viper = cls.Viper(position, game)
                all_entities.add(viper)
            elif map_ls[block_counter] == 66:
                were_wolf = cls.WereWolf(position, game)
                all_entities.add(were_wolf)
            elif map_ls[block_counter] == 78:
                sprite_route = os.path.join("resources", "images", "sprites", "BlueSpike.png")
                spike = cls.Spike(position, sprite_route, (0, 1))
                spikes.add(spike)
            block_counter += 1

    groups_dc['all_entities'] = all_entities
    groups_dc['blocks'] = blocks
    groups_dc['spikes'] = spikes
    groups_dc['modifiers'] = modifiers
    groups_dc['projectiles'] = projectiles
    groups_dc['were_wolf_vipers'] = were_wolf_vipers

    return groups_dc

def draw_text(screen, font, text, color, dimensions, position):
    font = pg.font.Font(font, dimensions)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    screen.blit(surface, position)
