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

    NanobotLevels = []  # Should be around 300 Values
    Frame = 0
    SegoeUI27sl = Helpers.Font.GetFont(27, semilight=True)
    SegoeUI20sl = Helpers.Font.GetFont(20, semilight=True)
    CurrentColor = Helpers.Color("RedOrange")

    CautionTriangle = None
    Cautioned = False
    Degredation = None

    @staticmethod
    def init():
        for i in range(len(Mode_1.characters)):
            Mode_1.CharactersInfo[Mode_1.characters[i]] = {"pos": (0, 50 + 100*i),
                                                           "num": i,
                                                           "name": Mode_1.characters[i],
                                                           "ARIP_id": Helpers.IdealRandStr(15, UseCaps=True),
                                                           "Second_id": Helpers.IdealRandStr(20),
                                                           "Third_id": Helpers.IdealRandStr(5),
                                                           "JustChanged": 0,
                                                           "Caution": False}
       # Create GraphValues for use
        def GraphSin(FrameRate, Frame, Scale, UseThird=False):  # Uses Trig to create values
            """
            In the form of sin(InnerFirst) + sin(InnerSecond)
            :param FrameRate:  Period of function, essentially
            :param Frame:      Which frame it's on now (x value)
            :return:           rounded to 3 decimal places. 
            """
            First = math.radians(2 * (360 / FrameRate) * Frame)
            Second = math.radians((360 / FrameRate) * Frame)
            Third = math.radians(2 * (360 / FrameRate) * Frame / 4) if UseThird else 0
            sin = math.sin(First) + math.sin(Second) + math.sin(Third)
            return round(Scale * sin, 3)

        for i in range(300):  # For each of the grames
            Mode_1.NanobotLevels.append(round(GraphSin(300, i, 40, UseThird=True)))

        Mode_1.ARIPDrawings.append(pygame.image.load("Assets/ARIP Diagram 1.png"))
        Mode_1.initiated = True
        Mode_1.CautionTriangle = pygame.image.load("Assets/CautionTriangle.png")
        Mode_1.Degredation = pygame.image.load("Assets/Degredation.png")
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

        # Add Caution Triangle
        if info["Caution"]:
            Sys.screen.blit(Mode_1.CautionTriangle, (pos[0]+ 400, pos[1]))
        return

    @staticmethod
    def PersonalInfo(mode=1):
        info = Mode_1.CharactersInfo[Mode_1.selected]
        BigName = Mode_1.SegoeUI_50b.render(info["name"] + "'s ARIP Information", True, (0, 0, 0))
        Sys.screen.blit(BigName, (525, 50))

        character = Mode_1.CharactersInfo[Mode_1.selected]
        if character["JustChanged"] > 0:  # Ensure there's like 1/6th of a second of whiteness when changing characters
            character["JustChanged"] -= 1
            Mode_1.CurrentColor = Helpers.Color(random.choice(["Red", "RedOrange", "Yellow", "Green", "Blue"]))
            return

        Sys.screen.blit(random.choice(Mode_1.ARIPDrawings), (500, 100))
        Mode_1.CreateChart(1120, "Activity", Mode_1.NanobotLevels, Mode_1.CurrentColor, y_position=150)
        Mode_1.Frame = Mode_1.Frame + 1 if Mode_1.Frame < 300 else 0

        if mode == 2:
            Sys.screen.blit(Mode_1.Degredation, (630, 400))

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
    def CreateChart(x_position, text, data, color, text_color=None, start=300, y_position=80, length=530):
        """
        Used 3 times, can create the individual charts on the top right that slowly fill and decrease
        :param x_position:  Where each one should start, x wise
        :param text:        What the text should read above it
        :param data:        What it should use for the variations
        :param color:       Its color
        :param text_color:  The color of the text (defaults to black)
        :param start:       What value should it start at? 0-400 (recommended: 360)
        :param y_position:  Where should the y position be (defaults to 80)
        :return: One of the item boxes
        """
        if not text_color:  # Set default text color to black
            text_color = (0, 0, 0)
        BoxPosition = (x_position, y_position, 80, length)
        # Set Up Words First
        TextWidth, TextHeight = Mode_1.SegoeUI27sl.size(text)  # Get estimate of size
        TextPosition = (BoxPosition[0] + (80-TextWidth)/2, y_position - 35)  # Adjust position to center it

        Text = Mode_1.SegoeUI27sl.render(text, True, (0, 0, 0))  # Create text object
        Sys.screen.blit(Text, TextPosition)   # Blit to screen

        # Now set up the box that moves
        BlueBoxPosition = (x_position, length + y_position, 80, -start - data[Mode_1.Frame-1])  # Adjust box pos based on variation
        BlueBox = pygame.Rect(BlueBoxPosition)  # Create object
        pygame.draw.rect(Sys.screen, color, BlueBox)  # Blit it

        BlueBoxOutline = pygame.Rect(BlueBoxPosition) # Outline of the box object
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), BlueBoxOutline, 2)  # Blit it

        Outline = pygame.Rect(BoxPosition)  # Full Outline
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), Outline, 2)  # Blit

        # Percent Text
        Percent = str(round((start+data[Mode_1.Frame-1])*100/length)) + "%"  # Text Percentage
        PercentTextWidth, PercentTextHeight = Mode_1.SegoeUI20sl.size(Percent)  # Estimate size

        PercentPos = (x_position + (80 - PercentTextWidth)/2, length + y_position -start-data[Mode_1.Frame-1])  # Center it
        PercentTextFinal = Mode_1.SegoeUI20sl.render(Percent, True, text_color)  # Render the Percentage Text
        Sys.screen.blit(PercentTextFinal, PercentPos)  # Blit it


    @staticmethod
    def Advance(type=1):
        NextPosition = Mode_1.CharactersInfo[Mode_1.selected]["num"] + type # Int to where you are
        if NextPosition == 9:
            NextPosition = 0
        if NextPosition == -1:
            NextPosotion = 8
        Mode_1.selected = Mode_1.characters[NextPosition]
        Mode_1.CharactersInfo[Mode_1.selected]["JustChanged"] = 5

    @staticmethod
    def Mode_2():
        if Mode_1.Cautioned:
            return
        for character in Mode_1.CharactersInfo:  # For each person
            if not Mode_1.CharactersInfo[character]["Caution"]:
                if random.choice([0, 0, 0]*4 + [1]):
                    Mode_1.CharactersInfo[character]["Caution"] = True
                    return
                else:
                    return
        # If it makes it the whole way
        Mode_1.Cautioned = True


    @staticmethod
    def Run(mode=1):
        Mode_1.SetUpSideBar()
        Mode_1.PersonalInfo(mode=mode)

        if mode == 2:
            Mode_1.Mode_2()
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
    if mode == 1 or mode == 2:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run(mode=mode)
        if unit == 5:
            Mode_1.Advance()
        elif unit == 0.5:
            pass

def Key(type):
    if type == "UP":
        Mode_1.Advance(type=-1)
    if type == "DOWN":
        Mode_1.Advance(type=1)