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

    WaterGraphValues = []  # Should be around 300 Values
    CarbonGraphValues = []  # Should also be around 300 values
    HumGraphValues = []     # Around 150 as well

    BoxText = pygame.font.Font("Assets/Fonts/segoeuisl.ttf", 27)
    PercentText = pygame.font.Font("Assets/Fonts/segoeuisl.ttf", 20)


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
            Third = math.radians(2 * (360 / FrameRate) * Frame/3) if UseThird else 0
            sin = math.sin(First) + math.sin(Second) + math.sin(Third)
            return round(Scale * sin, 3)

        # Use GraphSin() to generate WaterGraph and CarbonGraph Values
        for i in range(Sys.FrameRate*10):
            Mode_1.WaterGraphValues.append(round(GraphSin(150, i, 10)))
            Mode_1.CarbonGraphValues.append(round(GraphSin(50, i, 3)))
            Mode_1.HumGraphValues.append(round(GraphSin(300, i, 8, UseThird=1)))

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

        # Full Outline
        FullOutline = pygame.Rect(TopChartPosition)  # Outline of the box object
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), FullOutline, 2)  # Blit it

    @staticmethod
    def Run():
        if Mode_1.Frame >= 300:  # For all the circular motion, ensure it knows the correct frame
            Mode_1.Frame = 0
        else:
            Mode_1.Frame += 1

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