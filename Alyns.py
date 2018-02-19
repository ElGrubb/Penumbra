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

    SegoeUI_20li = Helpers.Font.GetFont(20, light=True, italics=True)
    SegoeUI_25 = Helpers.Font.GetFont(25)

    selected = "Adriel"
    CharactersInfo = {}
    characters = ["Adriel", "Elik", "Kyr", "Ninmoda", "Lycron", "Yakim", "Rouak", "Usetha", "Alyns"]


    @staticmethod
    def init():
        for i in range(len(Mode_1.characters)):
            Mode_1.CharactersInfo[Mode_1.characters[i]] = {"pos": (0, 50 + 100*i),
                                                           "num": i,
                                                           "name": Mode_1.characters[i],
                                                           "ARIP_id": Helpers.IdealRandStr(15, UseCaps=True)}

        Mode_1.initiated = True
        return

    @staticmethod
    def SidePerson(pos: tuple, info: dict, color: int):
        """
        Creates an object of shapes for a communcation button
        :param pos: A TUPLE containing the position of the box
        :param info: A DICT containing necesaary info for the box. 
        :param color: A BOOL that'll decide the color.  1=Green,  0=Red,   2=Yellow
        :return: updated Info Dict of the object
        """

        # Background:
        BoxPos = pos + (500, 100)

        BoxBackground = pygame.Rect(BoxPos)  # Set the Background for the taskbar rect
        pygame.draw.rect(Sys.screen, color, BoxBackground, 0)  # Color it and blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), BoxBackground, 1)  # Color it and blit it

        # Add Name
        TextPos = (BoxPos[0] + 5, BoxPos[1])
        NameText = Mode_1.SegoeUI_25.render(info["name"], True, (0, 0, 0))  # Create the text
        Sys.screen.blit(NameText, TextPos)  # Add to the Sys.screen

        IDtext = Mode_1.SegoeUI_20li.render("Model:  " + info["ARIP_id"], True, (0, 0, 0))
        Sys.screen.blit(IDtext, (TextPos[0] + 200, TextPos[1]))

        return

    @staticmethod
    def SetUpSideBar():
        for key in Mode_1.CharactersInfo:
            character = Mode_1.CharactersInfo[key]
            if Mode_1.selected == character['name']:
                color = "White"
            else:
                color = "DarkWhite"
            Mode_1.SidePerson(pos=character["pos"], info=character, color=Helpers.Color(color))
        return


    @staticmethod
    def Run():
        Mode_1.SetUpSideBar()

class Mode_5:
    data = {
        "System": "Life Support",
        "Dialogue": ["Listening for ARIPS", "Creating Artificial Brain",
                     "Narrowing Level Fields", "Managing Blood Levels",
                     "Establishing Secure Connections", "Connecting to Mainframe",
                     "Cooking Up Food", "Supporting Life", "Restarting"]
    }


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 0.5:
            pass
