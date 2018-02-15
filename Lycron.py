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

Military_Alphabet = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliet",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Wiskey",
    "X-Ray",
    "Yankee",
    "Zulu"
]

Good_Statuses = [
    "All systems operational. Communication is natural.",
    "Chirrup Systems Correcting...",
    "Usual System Cleaning",
    "Open Gateway, High Speeds",
    "High Speeds, All systems operational.",
    "Minor Delays, Channel Open",
]

Bad_Statuses = [
    "Cannot Connect to Host",
    "No Reception",
    "Lost Signal",
    "Fix Immediately",
    "0.000 Nanobot Receptors Open. System Failure",
    "System Failure, send repairs now",
    "Repair Microtransation Server right now",
    "Lost connection to host. Retrying 12.02/s"
]

Possible_Identification = ["POD", "BOT", "COM", "NANO", "LYC", "COMP", "Dom"]
Rare_Possible_Identification = ["Colin", "Liam", "Greyson", "David", "Q", "Katy", 'Mallory',
                               "Grace", "Alyssa", "Serena", "Emily", "Christina", "Abby"]


class Mode_1:
    """
    Runs specific functions for Mode_1. 
    """
    # Changable Variables
    ChatHeight, ChatWidth = 925, 610  # Vars containing the length and width of the chatbox
    Font_Width = 20  # Font Size
    String_Length, String_Variation, String_Padding_min = 58, 15, 5
    GenerateStatuses = 9  # How many to generate and keep track of
    StatusPositionX, StatusPositionY, StatusBuffer = 650, 70, 105

    # Static Variables
    initiated = False
    PreviousText = []  # A list for the previous words that were added
    PossibleRows = 0  # Will contain how many rows of text can be fit
    Font_ChatWindow = None  # Object that will contain the Chat Window
    Lycron00 = None
    Lycron01 = None
    Lycron02 = None
    Lycron03 = None
    LycronImages = [Lycron00, Lycron01, Lycron02, Lycron03]
    CurrentImage = 0
    SegoeUI_Small = pygame.font.Font("Assets/Fonts/segoeui.ttf", 15)
    SemiboldSegoeUI_Small = pygame.font.Font("Assets/Fonts/seguisb.ttf", 15)
    StatusList = []
    BBposition = (0, 1050)
    BBimage = None

    @staticmethod
    def init():
        # Start up all the image files necessary
        Mode_1.Font_ChatWindow = pygame.font.Font("Assets/Fonts/segoeui.ttf", Mode_1.Font_Width)
        Mode_1.PossibleRows = math.floor(Mode_1.ChatHeight / (Mode_1.Font_ChatWindow.size("Mode_1")[1] - 10)) - 11

        Mode_1.Lycron00 = pygame.image.load('Assets/Lycron00.png')
        Mode_1.Lycron01 = pygame.image.load('Assets/Lycron01.png')
        Mode_1.Lycron02 = pygame.image.load('Assets/Lycron02.png')
        Mode_1.Lycron03 = pygame.image.load('Assets/Lycron03.png')
        Mode_1.LycronImages = [Mode_1.Lycron00, Mode_1.Lycron01, Mode_1.Lycron02, Mode_1.Lycron03]

        # Generate Starting Text rows
        for i in range(Mode_1.PossibleRows):
            Mode_1.PreviousText.append(Mode_1.randstr(Mode_1.String_Length))  # Generates random strings

        # Generate the Status Lists that'll be used
        StartingStatusPosition = Mode_1.StatusPositionY
        for i in range(Mode_1.GenerateStatuses):
            status = Mode_1.CreateCommuncation((Mode_1.StatusPositionX, StartingStatusPosition), {}, color=1)
            Mode_1.StatusList.append(status)
            StartingStatusPosition += Mode_1.StatusBuffer # Add 100 px for the size of the box and a buffer of 20
        Mode_1.BBimage = pygame.image.load('Assets/LycronBottomBar.png')

        Mode_1.initiated = True

    @staticmethod
    def randstr(length):  # HELPER FUNCTION
        """
        Create a random string of characters under a specific length
        :param length: How long the max string can be
        :return: The string
        """
        string = ''
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ      1234567890      abcdefghijklmnopqrstuvwxyz.!/"  # Characters to use
        for i in range(0, length):  # For each character until the length
            string += random.choice(characters)  # Add a random character

        # Add Identification:
        if random.randint(0,30) < 3:
            character_name = random.choice(Rare_Possible_Identification)
        else:
            character_name = random.choice(Possible_Identification)
        string = character_name + " " + str(random.randrange(999)) + ":   " + string
        string = string[0:length]

        string = string[0:len(string)-random.randrange(Mode_1.String_Variation)].strip()  # Remove a bit from the end to make it random length
        return string

    @staticmethod
    def Text(mode=1):
        # Create Black Box
        ChatBoxBG = pygame.Rect((20, 70, Mode_1.ChatWidth, Mode_1.ChatHeight))
        pygame.draw.rect(Sys.screen, Helpers.Color("DarkGray"), ChatBoxBG, 0)

        # Delay Time
        if mode == 1:
            Delay = 10
        elif mode == 2:
            Delay = 2

        # Add some dialogue
        if random.randrange(Delay) == 1: # 1/7 chance of text occuring! This way theres no pattern
            Mode_1.PreviousText.append(Mode_1.randstr(Mode_1.String_Length))  # Generates random strings

        if len(Mode_1.PreviousText) > Mode_1.PossibleRows:  # Limit the number of things said so there's no excess lines
            del Mode_1.PreviousText[0]

        # Generate text objects now
        printList = []  # List of the objects
        CurrentDistance = 0  # How far down the scren we have gone
        for line in Mode_1.PreviousText:  # For each line in it
            # Iterates through each line of text, formatting it and adding to printList
            while Mode_1.Font_ChatWindow.size(line)[0] > Mode_1.ChatWidth:  # Ensures each is not too long
                line = line[0:len(line)-1]  # If it is, removes 1 from it until it's not too long
            ChatText = Mode_1.Font_ChatWindow.render(line, True, (255, 255, 255))  # Create the text
            Sys.screen.blit(ChatText, (25, 70 + CurrentDistance))  # Add to the Sys.screen
            CurrentDistance += Mode_1.Font_ChatWindow.size(line)[1] - Mode_1.String_Padding_min  # Create new distance

    @staticmethod
    def Images():
        tempList = []
        for status in Mode_1.StatusList:
            new_status = Mode_1.CreateCommuncation(status["pos"], status, color=status["Color"])
            tempList.append(new_status)
        Mode_1.StatusList = tempList

    @staticmethod
    def CreateCommuncation(pos: tuple, info: dict, color: int):
        """
        Creates an object of shapes for a communcation button
        :param pos: A TUPLE containing the position of the box
        :param info: A DICT containing necesaary info for the box. 
        :param color: A BOOL that'll decide the color.  1=Green,  0=Red,   2=Yellow
        :return: updated Info Dict of the object
        """
        # info
        if not info: # Generate information for each object
            info = {
                "ConnectedText": "Connected To: ",
                "Name": "",  # To be filled in with the next step
                "pos": pos,
                "JustChanged": False
            }
            # Get Name of Station
            PreNames = ["Station", "POD", "NanoSystem", "Control Panel"]
            string = random.choice(PreNames) + " " + random.choice(Military_Alphabet) + "-"
            string += random.choice(Military_Alphabet) + "-"
            string += random.choice(Military_Alphabet)
            info["Name"] = string

            # ID Number:
            info["ID"] = str(random.randrange(100000, 999999)) + str(random.randrange(100000, 999999))

            # Status
            info["CurrentStatus"] = random.choice(Good_Statuses)
        # Cleanup
        if color == 0 and info["JustChanged"]:  # If it just changed from Green to Red
            info["ConnectedText"] = "Not Connected To: "
            info['CurrentStatus'] = random.choice(Bad_Statuses)
            info["JustChanged"] = False
        elif color == 1 and info["JustChanged"]:  # If it just changed from Red to Green
            info["ConnectedText"] = "Connected To: "
            info['CurrentStatus'] = random.choice(Good_Statuses)
            info["JustChanged"] = False

        if random.randrange(400) == 100: # todo add mode
            if color == 0:
                info['CurrentStatus'] = random.choice(Bad_Statuses)
                color = 1
                info["JustChanged"] = True
            elif color == 1:
                info['CurrentStatus'] = random.choice(Good_Statuses)
            elif color == 2:
                info['CurrentStatus'] = random.choice(Bad_Statuses)
                color = 1
                info["JustChanged"] = True

        # Background:
        BoxSize = (610, 100)

        BoxBackground = pygame.Rect(pos, BoxSize)  # Set the Background for the taskbar rect
        pygame.draw.rect(Sys.screen, Helpers.Color("DarkWhite"), BoxBackground, 0)  # Color it and blit it
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), BoxBackground, 1)  # Color it and blit it

        # Colored Box
        StatusPos = (pos[0] , pos[1] )  # (pos[0] + 5, pos[1] + 5)
        StatusSize = (15, 100)          # (9, 90)
        if color == 0:
            StatusColor = Helpers.Color("Red")
        elif color == 1:
            StatusColor = Helpers.Color("Green")
        elif color == 2:
            StatusColor = Helpers.Color("Yellow")

        Status = pygame.Rect(StatusPos, StatusSize)       # (pos[0] + 4, pos[1] + 4)  (11, 92)
        pygame.draw.rect(Sys.screen, StatusColor, Status, 0)
        #Outline
        StatusOutline = pygame.Rect(StatusPos, StatusSize)  # Create the object
        pygame.draw.rect(Sys.screen, Helpers.Color("Black"), StatusOutline, 1)  # Color it and blit it

        # Text
        ConnectedToPos = (pos[0] + 20, pos[1] + 0)
        ConnectedTo = Mode_1.SegoeUI_Small.render(info["ConnectedText"], True, (0, 0, 0))  # Create the text
        Sys.screen.blit(ConnectedTo, ConnectedToPos)  # Add to the Sys.screen
        ConnectedTo_Width, ConnectedTo_Height = Mode_1.SegoeUI_Small.size(info["ConnectedText"])

        ServerName = Mode_1.SemiboldSegoeUI_Small.render(info["Name"], True, (0, 0, 0))
        Sys.screen.blit(ServerName, (ConnectedToPos[0] + ConnectedTo_Width, ConnectedToPos[1]))

        # -== Extra Text ==-
          # ID
        IDPos = (pos[0] + 20, pos[1] + ConnectedTo_Height)
        IDText = "Identification Number: " + info["ID"]
        ID = Mode_1.SegoeUI_Small.render(IDText, True, (0, 0, 0))
        Sys.screen.blit(ID, IDPos)
        ID_Width, ID_Height = Mode_1.SegoeUI_Small.size(IDText)
          # Current Status
        CurrentStatusPos = (pos[0] + 20, IDPos[1] + ID_Height)
        CurrentStatusText = "Current Status: " + info["CurrentStatus"]
        CurrentStatus = Mode_1.SegoeUI_Small.render(CurrentStatusText, True, (0, 0, 0))
        Sys.screen.blit(CurrentStatus, CurrentStatusPos)
        CurrentStatus_Width, CurrentStatus_Height = Mode_1.SegoeUI_Small.size(CurrentStatusText)

        info['Color'] = color
        return info

    @staticmethod
    def RandColorChange():  # Runs every 5 seconds //todo add if mode is red
        if random.randrange(4) == 1:  # so like 3 per minute?
            StatusList = Mode_1.StatusList
            selected_int = random.randint(0, len(StatusList)-1)

            # Randomly chooses either red or orange
            StatusList[selected_int]["Color"] = random.choice([0, 2])
            StatusList[selected_int]["JustChanged"] = True

            SelectedStatus = StatusList[selected_int]  # Make dedicated Variable
            StatusList.remove(SelectedStatus)          # Remove from List
            StatusList =[SelectedStatus] + StatusList  # Move to the top of the list

            # Redo Positions
            starting = Mode_1.StatusPositionY
            for status in StatusList:
                status["pos"] = (Mode_1.StatusPositionX, starting)
                starting += Mode_1.StatusBuffer

            Mode_1.StatusList = StatusList


    @staticmethod
    def BottomBar():
        Sys.screen.blit(Mode_1.BBimage, Mode_1.BBposition)

    @staticmethod
    def Run():
        Mode_1.Text()
        Mode_1.Images()
        Mode_1.BottomBar()


def Navigator(mode: int, unit=0):

    if mode == 1:
        if not Mode_1.initiated:
            Mode_1.init()

        if not unit:
            Mode_1.Run()

        elif unit == 5:
            Mode_1.RandColorChange()

