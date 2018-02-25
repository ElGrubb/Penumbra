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
    SegoeUI_20l  = Helpers.Font.GetFont(20, light=True)
    SegoeUI_25b   = Helpers.Font.GetFont(25, bold=1)
    SegoeUI_50b = Helpers.Font.GetFont(50, bold=1)

    selected = "Adriel"
    CharactersInfo = {}
    characters = ["Adriel", "Elik", "Kyr", "Ninmoda", "Lycron", "Yakim", "Rouak", "Usetha", "Alyns"]

    AdvanceFrames = 0

    ARIPDrawings = []

    @staticmethod
    def init():
        for i in range(len(Mode_1.characters)):
            Mode_1.CharactersInfo[Mode_1.characters[i]] = {"pos": (0, 50 + 100*i),
                                                           "num": i,
                                                           "name": Mode_1.characters[i],
                                                           "ARIP_id": Helpers.IdealRandStr(15, UseCaps=True),
                                                           "Second_id": Helpers.IdealRandStr(20),
                                                           "Third_id": Helpers.IdealRandStr(5),
                                                           "JustChanged": 0}

        Mode_1.ARIPDrawings.append(pygame.image.load("Assets/ARIP Diagram 1.png"))
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
        NameText = Mode_1.SegoeUI_25b.render(info["name"], True, (0, 0, 0))  # Create the text
        Sys.screen.blit(NameText, TextPos)  # Add to the Sys.screen

        IDtext = Mode_1.SegoeUI_20li.render("Model:  " + info["ARIP_id"], True, (0, 0, 0))
        Sys.screen.blit(IDtext, (TextPos[0] + 200, TextPos[1]))

        SecondText = Mode_1.SegoeUI_20l.render("Working ID: " + info["Second_id"], True, (0, 0, 0))
        Sys.screen.blit(SecondText, (TextPos[0], TextPos[1] + 45))

        ThirdText = Mode_1.SegoeUI_20l.render("Status:  Connected to Central Processing", True, (0, 0, 0))
        Sys.screen.blit(ThirdText, (TextPos[0], TextPos[1] + 70))
        return

    @staticmethod
    def PersonalInfo():
        info = Mode_1.CharactersInfo[Mode_1.selected]
        BigName = Mode_1.SegoeUI_50b.render(info["name"] + "'s ARIP Information", True, (0, 0, 0))
        Sys.screen.blit(BigName, (525, 50))


        return

    @staticmethod
    def SetUpSideBar():
        for key in Mode_1.CharactersInfo:
            character = Mode_1.CharactersInfo[key]
            if Mode_1.selected == character['name']:
                color = "White"
            else:
                color = "Gray"
            Mode_1.SidePerson(pos=character["pos"], info=character, color=Helpers.Color(color))
        return

    @staticmethod
    def GeneralInfo():  # Displays the right hand stuff about the person
        character = Mode_1.CharactersInfo[Mode_1.selected]
        if character["JustChanged"] > 0:  # Ensure there's like 1/6th of a second of whiteness when changing characters
            character["JustChanged"] -= 1
            return

        Sys.screen.blit(random.choice(Mode_1.ARIPDrawings), (500, 100))

    @staticmethod
    def Advance():
        Mode_1.AdvanceFrames += 1
        # Set up Data for Cataclysm


    @staticmethod
    def Run():
        Mode_1.SetUpSideBar()
        Mode_1.PersonalInfo()
        Mode_1.GeneralInfo()
        return

class Mode_5:
    data = {
        "System": "Life Support",
        "Dialogue": ["Listening for ARIPS", "Creating Artificial Brain",
                     "Narrowing Level Fields", "Managing Blood Levels",
                     "Establishing Secure Connections", "Connecting to Mainframe",
                     "Supporting Life", "Restarting"]
    }


def Navigator(mode: int, unit=0):
    if mode == 1 or mode == 1.5:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
            Mode_1.Advance()
        elif unit == 0.5:
            pass
