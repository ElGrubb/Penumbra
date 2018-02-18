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

    BoxText = Helpers.Font.GetFont(27, semilight=True)
    PercentText = Helpers.Font.GetFont(20, semilight=True)
    YakimText = None
    EmptyGraph = None

    GraphValues = []

    BBposition = (0, 1050)
    BBimage = None

    TopData = []
    RadarPoints = []

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
        for i in range(Mode_1.TotalFrames):  # For each of the grames
            Mode_1.WaterGraphValues.append(round(GraphSin(150, i, 10)))  # Create Water normal Values
            Mode_1.CarbonGraphValues.append(round(GraphSin(50, i, 3)))
            Mode_1.HumGraphValues.append(round(GraphSin(300, i, 8, UseThird=1)))

        def TopChartWork(Frame):  # Create the positions of the Nitrogen and Oxygen necessary
            # Takes in the Frame number and returns the percentage of each Nitrogen and Oxygen
            Nitrogen = math.radians((360 / 300) * Frame)  # Based on the Frame Int
            Oxygen = math.radians(2*(360 / 300) * Frame)

            f_Nitrogen = round(10 * math.sin(Nitrogen))
            f_Oxygen = round(5 * math.sin(Oxygen))

            return (f_Nitrogen, f_Oxygen)

        for i in range(Mode_1.TotalFrames):  # For each of the frames 
            Mode_1.TopData.append(TopChartWork(i))  # Add to the TopRow cycle values

        Mode_1.YakimText = pygame.image.load('Assets/Yakim01.png')
        Mode_1.EmptyGraph = pygame.image.load("Assets/EmptyGraph.png")

        # Generate 14 values for GraphValues[] for the actual graph
        for i in range(15):  # this is so there are values when the graph starts graphing
            Mode_1.GraphValues.append(Mode_1.CreateGraphPoints(mode=1))

        Mode_1.BBimage = pygame.image.load('Assets/YakimBottomBar.png')

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
        NitrogenLength = 0.75 * TotalLength + Mode_1.TopData[Mode_1.Frame][0]
        NitrogenTotal = NitrogenPosition + (NitrogenLength, TopChartPosition[3])

        NitrogenBox = pygame.Rect(NitrogenTotal)  # Insides of Nitrogen
        pygame.draw.rect(Sys.screen, Helpers.Color("Purple"), NitrogenBox)  # Blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), NitrogenBox, 1)  # Outline it!

        # Oxygen
        OxygenPosition = (NitrogenLength + TopChartPosition[0], TopChartPosition[1])
        OxygenLength = 0.2 * TotalLength + Mode_1.TopData[Mode_1.Frame][1]
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
    def CreateGraphPoints(mode=1, margin=(0, 350)):
        """
        Returns y value of node for point
        """
        if mode == 1:
            mid = margin[1]/2
            range = (mid-30, mid+30)
            return random.randint(range[0], range[1])
        elif mode == 2:
            return random.randint(margin[0], margin[1])

    @staticmethod
    def GenerateNewPoint():
        del Mode_1.GraphValues[0]
        Mode_1.GraphValues.append(Mode_1.CreateGraphPoints(mode=1))

    @staticmethod
    def GenGraph():
        Sys.screen.blit(Mode_1.EmptyGraph, (660, 600))
        poslist = []
        x_pos = 620

        for point in Mode_1.GraphValues:
            x_pos += 40
            pos = (x_pos, 600 + point)
            poslist.append(pos)

        pygame.draw.lines(Sys.screen, Helpers.Color("Black"), False, poslist, 3)

        for point in poslist:
            circledpoint = pygame.draw.circle(Sys.screen, Helpers.Color("Blue"), point, 8)
            circledpoint = pygame.draw.circle(Sys.screen, Helpers.Color("White"), point, 4)

        # Big Text
        Text = "Cloud Pressure Variations"

        TextWidth, TextHeight = Mode_1.BoxText.size(Text)  # Estimate size
        TextPos = (660+int((580-TextWidth)/2), 600)
        TextObj = Mode_1.BoxText.render(Text, True, (0, 0, 0))  # Create text object
        Sys.screen.blit(TextObj, TextPos)  # Blit to screen

    @staticmethod
    def BottomBar():
        Sys.screen.blit(Mode_1.BBimage, Mode_1.BBposition)

    @staticmethod
    def Radar():
        center = (330, 800)
        radius = 200
            # Create the general outline of the radar
        pygame.draw.circle(Sys.screen, Helpers.Color("DarkWhite"), center, radius)
        pygame.draw.circle(Sys.screen, Helpers.Color("White"), center, radius, 8)
        pygame.draw.circle(Sys.screen, Helpers.Color("Black"), center, radius, 4)

            # Generate the sweeping line
        Radians = math.radians(Mode_1.Frame/300*360)
        Coords = (round(200 * math.cos(Radians)), round(200 * math.sin(Radians)))
        final_Coords = (center[0] + Coords[0], center[1] + Coords[1])
        
        # Draw positioning lines
        pygame.draw.line(Sys.screen, Helpers.Color("Black"), (center[0], center[1]-radius),
                         (center[0], center[1]+radius))
        pygame.draw.line(Sys.screen, Helpers.Color("Black"), (center[0] - radius, center[1]),
                         (center[0] + radius, center[1]))
        
            # Draw the Sweeping Line
        pygame.draw.line(Sys.screen, Helpers.Color("Black"), center, final_Coords, 7)
        pygame.draw.line(Sys.screen, Helpers.Color("White"), center, final_Coords, 2)
            
            # Draw circle in the center
        pygame.draw.circle(Sys.screen, Helpers.Color("Black"), center, 10)
        pygame.draw.circle(Sys.screen, Helpers.Color("DarkWhite"), center, 8)

        # Generate a few random points
        if Mode_1.Frame % 60 == 0:  # Every 2 seconds
            dummy_list = []
            for point in Mode_1.RadarPoints:  # For every established point
                if random.randint(0, 1):   # 50% chance itll keep that point
                    dummy_list.append(point)

            # Limits them to 10 points. Fills in remaining points. 
            for i in range(10-len(dummy_list)):  # Make the extra points
                angle = math.radians(random.randint(0, 360))  # Random angle
                scale = random.randint(20, 180)  # Random Vector Length
                Coords = (round(scale * math.cos(angle)), round(scale * math.sin(angle)))  # Generate Coords based on those two
                final_Coords = (center[0] + Coords[0], center[1] + Coords[1])  # Set with (0, 0) in the center of the graph

                dummy_list.append(final_Coords)  # Add the new coord

            Mode_1.RadarPoints = dummy_list  # Save this list

        for point in Mode_1.RadarPoints:  # For each point created / established
            pygame.draw.circle(Sys.screen, Helpers.Color("Black"), point, 5)  # Create Black Outline
            pygame.draw.circle(Sys.screen, Helpers.Color("DarkWhite"), point, 3)  # Create Inside white

            # Create Text to show abovewards
        Text = "Atmospheric Electrostatic Variations"  
        TextWidth, TextHeight = Mode_1.BoxText.size(Text)  # Estimate size
        TextPos = (40 + int((580 - TextWidth) / 2), 560)
        TextObj = Mode_1.BoxText.render(Text, True, (0, 0, 0))  # Create text object
        Sys.screen.blit(TextObj, TextPos)  # Blit to screen
        
        return


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

        # Chart
        Mode_1.GenGraph()
        Mode_1.Radar()

        Mode_1.BottomBar()


class Mode_5:
    data = {
        "System": "Atmospherics",
        "Dialogue": ["Scanning for Clouds", "Checking Radar",
                     "Calculating Storm Percentages", "Checking Rain Requirements",
                     "Regulating Temperature", "Deploying Major Correctment",
                     "Accelorating Desert Storm", "Rebooting to Mainframe"]
    }

def Navigator(mode: int, unit=0):
    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()
        elif unit == 0.5:
            Mode_1.GenerateNewPoint()
