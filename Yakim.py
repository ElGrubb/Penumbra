import pygame
import random
import time
import math
import Helpers

pygame.font.init()

screen = None
screen_height, screen_width = None, None


class Mode_1:
    initiated = False
    pass


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 5:
            Mode_1.RandColorChange()