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
    TotalFrames = 300

    TemperatureGraph = []
    PressureGraph =    []
    NutrientsGraph =   []

    SegoeUI27sl = Helpers.Font.GetFont(27, semilight=True)
    SegoeUI20sl = Helpers.Font.GetFont(20, semilight=True)

    GeneralText = None

    Advanced = False
    HydroponicsImage = None


    @staticmethod
    def init():
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

        # Use GraphSin() to generate Values
        for i in range(Mode_1.TotalFrames):  # For each of the grames
            Mode_1.TemperatureGraph.append(round(GraphSin(150, i, 10)))  # Create Water normal Values
            Mode_1.PressureGraph.append(round(GraphSin(50, i, 3)))
            Mode_1.NutrientsGraph.append(round(GraphSin(300, i, 8, UseThird=1)))

        Mode_1.GeneralText = pygame.image.load("Assets/Usetha01.png")
        Mode_1.HydroponicsImage = pygame.image.load("Assets/hydroponics.jpg")

        Mode_1.initiated = True

    @staticmethod
    def CreateChart(x_position, text, data, color, text_color=None, start=300, y_position=80, length=850):
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
    def Advance():
        if Mode_1.Advanced:
            return
        if Mode_1.Frame == 0:
            for i in range(Mode_1.TotalFrames):
                Mode_1.TemperatureGraph[i] = Mode_1.TemperatureGraph[i] * 3
                Mode_1.PressureGraph[i] = Mode_1.PressureGraph[i] * 2
                Mode_1.NutrientsGraph[i] = Mode_1.NutrientsGraph[i] * 4

            Mode_1.Advanced = True


    @staticmethod
    def Run():
        Mode_1.Frame += 1  # Ensure the frames are cyclical
        if Mode_1.Frame > Mode_1.TotalFrames:
            Mode_1.Frame = 0

        GraphYPos = 100
        Mode_1.CreateChart(1160, "Temp.", Mode_1.TemperatureGraph, Helpers.Color("Red"), y_position=GraphYPos)
        Mode_1.CreateChart(1040, "Pressure", Mode_1.PressureGraph, Helpers.Color("Blue"), text_color=(255, 255, 255),
                           y_position=GraphYPos, start=500)
        Mode_1.CreateChart(920, "Nutrients", Mode_1.NutrientsGraph, Helpers.Color("Green"), start=700,
                           y_position=GraphYPos)

        Sys.screen.blit(Mode_1.GeneralText, (20, 70))
        Sys.screen.blit(Mode_1.HydroponicsImage, (50, 425))


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

    if mode == 2:
        Mode_1.Advance()
        Mode_1.Run()
