import pygame as pg
import random
import json

WIDTH = 800
HEIGHT = 600
GREEN = [0,255,0]
RED = [255,0,0]
BLUE = [0,0,255]
YELLOW = [255,255,0]
BLUE_2 = [0,255,255]
BLACK = [0,0,0]
WHITE = [255,255,255]
GRAY = [180,180,180]

def crop_image(image_route, columns, rows):
    image = pg.image.load  (image_route)
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