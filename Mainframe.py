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
    Mainframe0 = None
    Mainframe1 = None
    Mainframe2 = None
    Mainframe3 = None
    Mainframe4 = None

    GoodList = []
    BadList = []
    CurrentlyShowing = None

    SegoeUI_20 = Helpers.Font.GetFont(20)
    PreviousText = []

    initiated = False

    @staticmethod
    def init():
        Mode_1.Mainframe0 = pygame.image.load("Assets/Mainframe01.png")
        Mode_1.Mainframe1 = pygame.image.load("Assets/Mainframe01.png")
        Mode_1.Mainframe2 = pygame.image.load("Assets/Mainframe02.png")
        Mode_1.Mainframe3 = pygame.image.load("Assets/Mainframe03.png")
        Mode_1.Mainframe4 = pygame.image.load("Assets/Mainframe04.png")

        Mode_1.GoodList = [Mode_1.Mainframe0, Mode_1.Mainframe1, Mode_1.Mainframe2]
        Mode_1.BadList = [Mode_1.Mainframe3, Mode_1.Mainframe4]

        Mode_1.CurrentlyShowing = random.choice(Mode_1.GoodList)

        Mode_1.initiated = True

    @staticmethod
    def Terminal(mode=1):
        BlackBox = pygame.draw.rect(Sys.screen, Helpers.Color("Black"), (960, 70, 300, 900))
        # WhiteInside = pygame.draw.rect(Sys.screen, Helpers.Color("White"), (960, 70, 800, 400), 2)
        # WhiteInside = pygame.draw.rect(Sys.screen, Helpers.Color("White"), (964, 24, 794, 394), 1)

        # Add some machine text
        rows = 40
        pos = (960, 70, 900)
        ChatWidth = 300

        if mode == 2:
            delay = 1
        elif mode == 1:
            delay = 10

        if random.randrange(Delay) == 1:  # 1/5 chance of text occuring! This way theres no pattern
            Mode_1.PreviousText.append(
                Helpers.randstr(80, 15))  # Generates random strings
            if mode == 2:
                Mode_1.PreviousText.append(
                    Helpers.randstr(80, 15))

        while len(Mode_1.PreviousText) > rows:  # Limit the number of things said so there's no excess lines
            del Mode_1.PreviousText[0]

        # Generate text objects now
        printList = []  # List of the objects
        CurrentDistance = -90  # How far down the scren we have gone
        for line in Mode_1.PreviousText:  # For each line in it
            # Iterates through each line of text, formatting it and adding to printList
            while Mode_1.SegoeUI_20.size(line)[0] > ChatWidth:  # Ensures each is not too long
                line = line[0:len(line) - 1]  # If it is, removes 1 from it until it's not too long
            ChatText = Mode_1.SegoeUI_20.render(line, True, (255, 255, 255))  # Create the text
            Sys.screen.blit(ChatText, (pos[0], pos[1] + -5 +70 + CurrentDistance))  # Add to the Sys.screen

            CurrentDistance += Mode_1.SegoeUI_20.size(line)[1] - 5  # Create new distance

        return

    @staticmethod
    def Run(mode=1):
        if random.randrange(150) == 4:
            if mode == 1:
                Mode_1.CurrentlyShowing = random.choice(Mode_1.GoodList)
            elif mode == 2:
                Mode_1.CurrentlyShowing = random.choice(Mode_1.BadList)

        Sys.screen.blit(Mode_1.CurrentlyShowing, (10, 50))
        Mode_1.Terminal(mode=mode)


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 0.5:
            pass
    if mode == 2:
        Mode_1.Run(mode=2)

class Mode_5:
    data = {
        "System": "Processing",
        "Dialogue": ["Listening for ARIPS", "Connecting Signals",
                     "Creating System Links", "Saying Hi to Robbi",
                     "Qualters"]
    }