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

    SecurityImages = []
    CurrentlyViewing = []

    @staticmethod
    def init():
        for i in range(26):
            if i < 10:
                SaidString = "0" + str(i)
            else:
                SaidString = str(i)
            filepath = "Rouak" + SaidString
            filepath = "Assets/Rouak/" + filepath + ".png"

            Mode_1.SecurityImages.append(pygame.image.load(filepath))



    @staticmethod
    def Run():
        pass


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 0.5:
            pass
