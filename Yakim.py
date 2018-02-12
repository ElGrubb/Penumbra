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
    Frame = 0
    TotalFrames = 600

    WaterGraphValues = []  # Should be around 300 Values
    CarbonGraphValues = []  # Should also be around 300 values
    HumGraphValues = []     # Around 150 as well

    BoxText = pygame.font.Font("Assets/Fonts/segoeuisl.ttf", 27)
    PercentText = pygame.font.Font("Assets/Fonts/segoeuisl.ttf", 20)
    YakimText = None

    TopData = []

    @staticmethod
    def init():
        # Create WaterGraphValues for use
        def GraphSin(FrameRate, Frame, Scale, UseThird=False):  # Uses Trig to create values
            """
            In the form of sin(InnerFirst) + sin(InnerSecond)
            :param FrameRate:  Period of function, essentially
            :param Frame:      Which frame it's on now (x value)
            :return:           rounded to 3 decimal places. 
            """
            First = math.radians(2 * (360 / FrameRate) * Frame)
            Second = math.radians((360 / FrameRate) * Frame)
            Third = math.radians(2 * (360 / FrameRate) * Frame/4) if UseThird else 0
            sin = math.sin(First) + math.sin(Second) + math.sin(Third)
            return round(Scale * sin, 3)

        # Use GraphSin() to generate WaterGraph and CarbonGraph Values
        for i in range(Mode_1.TotalFrames):
            Mode_1.WaterGraphValues.append(round(GraphSin(150, i, 10)))
            Mode_1.CarbonGraphValues.append(round(GraphSin(50, i, 3)))
            Mode_1.HumGraphValues.append(round(GraphSin(300, i, 8, UseThird=1)))

        def TopChartWork(Frame):
            Nitrogen = math.radians((360 / 300) * Frame)
            Oxygen = math.radians(2*(360 / 300) * Frame)

            f_Nitrogen = round(10 * math.sin(Nitrogen))
            f_Oxygen = round(5 * math.sin(Oxygen))

            return (f_Nitrogen, f_Oxygen)

        for i in range(Mode_1.TotalFrames):
            Mode_1.TopData.append(TopChartWork(i))

        Mode_1.YakimText = pygame.image.load('Assets/Yakim01.png')
        Mode_1.initiated = True

    @staticmethod
    def CreateChart(x_position, text, data, color, text_color=None, start=360, y_position=80):
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
        BoxPosition = (x_position, y_position, 80, 400)
        # Set Up Words First
        TextWidth, TextHeight = Mode_1.BoxText.size(text)  # Get estimate of size
        TextPosition = (BoxPosition[0] + (80-TextWidth)/2, y_position - 35)  # Adjust position to center it

        Text = Mode_1.BoxText.render(text, True, (0, 0, 0))  # Create text object
        Sys.screen.blit(Text, TextPosition)   # Blit to screen

        # Now set up the box that moves
        BlueBoxPosition = (x_position, 400 + y_position, 80, -start - data[Mode_1.Frame-1])  # Adjust box pos based on variation
        BlueBox = pygame.Rect(BlueBoxPosition)  # Create object
        pygame.draw.rect(Sys.screen, color, BlueBox)  # Blit it

        BlueBoxOutline = pygame.Rect(BlueBoxPosition) # Outline of the box object
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), BlueBoxOutline, 2)  # Blit it

        Outline = pygame.Rect(BoxPosition)  # Full Outline
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), Outline, 2)  # Blit

        # Percent Text
        Percent = str(round((start+data[Mode_1.Frame-1])*100/400)) + "%"  # Text Percentage
        PercentTextWidth, PercentTextHeight = Mode_1.PercentText.size(Percent)  # Estimate size

        PercentPos = (x_position + (80 - PercentTextWidth)/2, 400 + y_position -start-data[Mode_1.Frame-1])  # Center it
        PercentTextFinal = Mode_1.PercentText.render(Percent, True, text_color)  # Render the Percentage Text
        Sys.screen.blit(PercentTextFinal, PercentPos)  # Blit it

    @staticmethod
    def TopChart():
        """
        The Fundamental Theorem of Yakim
        :return: A bigass chart that tells the composition of the atmosphere
        """
        TopChartPosition = (20, 70, 1240, 60)
        TotalLength = 1240

        # Nitrogen
        NitrogenPosition = (TopChartPosition[0], TopChartPosition[1])
        NitrogenLength = 0.75 * TotalLength + Mode_1.TopData[Mode_1.Frame][0]  # TODO this
        NitrogenTotal = NitrogenPosition + (NitrogenLength, TopChartPosition[3])

        NitrogenBox = pygame.Rect(NitrogenTotal)  # Insides of Nitrogen
        pygame.draw.rect(Sys.screen, Helpers.Color("Purple"), NitrogenBox)  # Blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), NitrogenBox, 1)  # Outline it!

        # Oxygen
        OxygenPosition = (NitrogenLength + TopChartPosition[0], TopChartPosition[1])
        OxygenLength = 0.2 * TotalLength + Mode_1.TopData[Mode_1.Frame][1] # TODO this
        OxygenTotal = OxygenPosition + (OxygenLength, TopChartPosition[3])

        OxygenBox = pygame.Rect(OxygenTotal)  # Insides of Nitrogen
        pygame.draw.rect(Sys.screen, Helpers.Color("Blue"), OxygenBox)  # Blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), OxygenBox, 1)  # Outline it!

        # Remaining
        RemainingLength = TotalLength - OxygenLength - NitrogenLength
        if RemainingLength % 2 != 0:
            RemainingLength = ((RemainingLength-1)/2, (RemainingLength+1)/2)
        else:
            RemainingLength = (RemainingLength/2, RemainingLength/2)

        # Argon
        ArgonPosition = (NitrogenLength + OxygenLength + TopChartPosition[0], TopChartPosition[1])
        ArgonLength = int(RemainingLength[0])
        ArgonTotal = ArgonPosition + (ArgonLength, TopChartPosition[3])

        ArgonBox = pygame.Rect(ArgonTotal)  # Insides of Argon
        pygame.draw.rect(Sys.screen, Helpers.Color("Yellow"), ArgonBox)  # Blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), ArgonBox, 1)  # Outline it!

        # Other
        OtherPosition = (ArgonPosition[0] + ArgonLength, TopChartPosition[1])
        OtherLength = int(RemainingLength[1])
        OtherTotal = OtherPosition + (OtherLength, TopChartPosition[3])

        OtherBox = pygame.Rect(OtherTotal)  # Insides of Argon
        pygame.draw.rect(Sys.screen, Helpers.Color("RedOrange"), OtherBox)  # Blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), OtherBox, 1)  # Outline it!

        # Full Outline
        FullOutline = pygame.Rect(TopChartPosition)  # Outline of the box object
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), FullOutline, 2)  # Blit it

        ### TEXT
        # Nitrogen
        NiSize = Mode_1.BoxText.size("Nitrogen")
        NiPos = (NitrogenTotal[0] + NitrogenLength - NiSize[0]-5, NitrogenTotal[1]+6)
        NiText = Mode_1.BoxText.render("Nitrogen", True, (0, 0, 0))  # Render the Percentage Text
        Sys.screen.blit(NiText, NiPos)  # Blit it

        # Oxygen
        OxySize = Mode_1.BoxText.size("Oxygen")
        OxyPos = (OxygenTotal[0] + OxygenLength - OxySize[0] - 5, OxygenTotal[1] + 6)
        OxyText = Mode_1.BoxText.render("Oxygen", True, (0, 0, 0))  # Render the Percentage Text
        Sys.screen.blit(OxyText, OxyPos)  # Blit it

    @staticmethod
    def GenText():
        pass

    @staticmethod
    def Run():
        if Mode_1.Frame >= 300:  # For all the circular motion, ensure it knows the correct frame
            Mode_1.Frame = 0
        else:
            Mode_1.Frame += 1

        Sys.screen.blit(Mode_1.YakimText, (20, 150))  # Blit the image

        # Set up Graphs on sidebar
        GraphYPos = 170
        Mode_1.CreateChart(1160, "Water", Mode_1.WaterGraphValues, Helpers.Color("Blue"), y_position=GraphYPos)
        Mode_1.CreateChart(1040, "Carbon", Mode_1.CarbonGraphValues, Helpers.Color("Gray"), text_color=(255, 255, 255), y_position=GraphYPos)
        Mode_1.CreateChart(920, "Humidity", Mode_1.HumGraphValues, Helpers.Color("Teal"), start=300, y_position=GraphYPos)

        # Set up Topbar
        Mode_1.TopChart()  # Wowzers


def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 5:
            pass
            # Mode_1.RandColorChange()