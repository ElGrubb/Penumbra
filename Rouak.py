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
            filepath = "Assets/Rouak/" + filepath + ".jpg"

            Mode_1.SecurityImages.append(pygame.image.load(filepath))

        for i in range(6):
            selected = random.choice(Mode_1.SecurityImages)
            while selected in Mode_1.CurrentlyViewing:
                selected = random.choice(Mode_1.SecurityImages)
            Mode_1.CurrentlyViewing.append(selected)

        Mode_1.initiated = True

    @staticmethod
    def ShowScreens():
        # Display the screens in CurrentlyViewing
        start = (20, 70)
        coords = [(20, 70),  (650, 70),
                  (20, 400), (650, 400),
                  (20, 740), (650, 740)]

        for i in range(6):
            Sys.screen.blit(Mode_1.CurrentlyViewing[i], coords[i])  # Blit the image

        return

    @staticmethod
    def ChangeScreens():
        for i in range(6):
            if random.randrange(5) == 1:
                selected = random.choice(Mode_1.SecurityImages)
                while selected in Mode_1.CurrentlyViewing:
                    selected = random.choice(Mode_1.SecurityImages)
                Mode_1.CurrentlyViewing[i] = selected

    @staticmethod
    def Run():
        Mode_1.ShowScreens()


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 2:
            Mode_1.ChangeScreens()
