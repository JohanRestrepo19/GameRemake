import pygame as pg
import random

from classes.classes import *
from library import *
from levels.levels import *


def main():
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    
    screen = level01(screen, clock)
    screen = level02(screen, clock)
    


if __name__ == "__main__":
    main()