import pygame
import random
import time
import math
import Helpers

pygame.font.init()


class Sys:
    screen = None
    screen_height, screen_width = None, None

    FrameRate = None


class Mode_1:
    initiated = False

    @staticmethod
    def init():
        pass

    @staticmethod
    def Run():
        pass

class Mode_5:
    data = {
        "System": "Hydropponics",
        "Dialogue": ["Reconfiguring Hydroponics", "Starting Eco-Lights",
                     "Configuring Gardening Data", "Testing Sprinkler System",
                     "Success...", "Planting Abby Berries"]
    }


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 0.5:
            pass
