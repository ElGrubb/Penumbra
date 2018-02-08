"""
February 1st
Very first attempt at making a computer system. This is an attempt at a base model with the 4 areas. 
Here I go!
"""
import pygame
import random
import time
import math
import LycronData

# Important Variables
FrameRate = 30
Name = "Lyrcon"


# Hex Codes and colors
def Color(name):
    """
    Allows us to quickly get colors without having to memorize all the names / numbers
    :param name: String, name of a color. 
    :return: Pygame color object
    """
    ColorDict = {
        "Black": 0x000000,
        "White": 0xFFFFFF,
        "Blue": 0x3498db,
        "Red": 0xe74c3c,
        "Yellow": 0xf1c40f,
        "Green": 0x2ecc71,
        "DarkGray": 0x222222,
        "Gray": 0x2c3e50,
        "LightGray": 0x7f8c8d,
        "DarkWhite": 0xe8e8e8
    }
    if name not in ColorDict:
        raise NameError("Name of color not in list")
    elif name in ColorDict:
        return ColorDict[name]

# Initialize Pygame and clock
pygame.init()
pygame.font.init
clock = pygame.time.Clock()

# Set the height and width of the screen
screen_width = 1280
screen_height = 1080
screen = pygame.display.set_mode([screen_width, screen_height]) #, pygame.FULLSCREEN)


# For in the event loop
def Key(event, key):
    """
    Creates a simpler version of the "if pressed down"
    :param event: The event object
    :param key: The key pressed down
    :return: 
    """
    # Ensure key is a list object
    if type(key) == list: trylist = key
    else: trylist = [key]

    # If it is pressed down, return true. Else, don't.
    for i in trylist:
        if event.type == pygame.KEYDOWN and event.key == i:
            return True
    return False


class TaskBar:
    """
    A class containing the functions for the taskbar to be created and blitted. 
    Need to do TaskBar.init() before ANYTHING ELSE
    """
    ProfileIcon = None   # Will be an object containing the loaded image of the person icon
    Font_SegoeUI = None  # Will be an object with the Font
    SearchBar = None     # Will be an object with the loaded image of the search bar
    @staticmethod
    def init():
        """
        Sets up the images in the TaskBar class
        """
        TaskBar.ProfileIcon = pygame.image.load('Assets/ProfileIcon.png')
        TaskBar.Font_SegoeUI = pygame.font.Font("Assets/Fonts/segoeui.ttf", 30)
        TaskBar.SearchBar = pygame.image.load('Assets/Search.png')

    @staticmethod
    def CreateTaskbar():
        """
        Prepares the Taskbar to be put on the screen
        """
        # Background
        TaskBarBG = pygame.Rect((0, 0, screen_width, 50))  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Color("DarkGray"), TaskBarBG, 0)  # Color it and blit it

        # Icon
        screen.blit(TaskBar.ProfileIcon, (0, 0))  # Blit the image
        Icon_Width, Icon_Height = TaskBar.ProfileIcon.get_size()  # Get the size and height

        # Username
        ProfileName = TaskBar.Font_SegoeUI.render(Name, True, (255, 255, 255))  # Render the Profile Name
        screen.blit(ProfileName, (Icon_Width + 5, 1))  # Blit the name 5pix next to the icon
        text_width, text_height = TaskBar.Font_SegoeUI.size(Name)  # Get the dimensions of the text

        # Search Bar
        screen.blit(TaskBar.SearchBar, (text_width + Icon_Width + 15, 5))  # Put the search bar 15pix from the text


class Lycron:
    """
    Runs specific functions for Lycron. 
    """
    # Changable Variables
    ChatHeight, ChatWidth = 905, 610  # Vars containing the length and width of the chatbox
    Font_Width = 20  # Font Size
    String_Length, String_Variation, String_Padding_min = 58, 15, 5
    GenerateStatuses = 8  # How many to generate and keep track of
    StatusPositionX, StatusPositionY, StatusBuffer = 650, 70, 105

    # Static Variables
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

    @staticmethod
    def init():
        # Start up all the image files necessary
        Lycron.Font_ChatWindow = pygame.font.Font("Assets/Fonts/segoeui.ttf", Lycron.Font_Width)
        Lycron.PossibleRows = math.floor(Lycron.ChatHeight / (Lycron.Font_ChatWindow.size("Lycron")[1] - 10)) - 11

        Lycron.Lycron00 = pygame.image.load('Assets/Lycron00.png')
        Lycron.Lycron01 = pygame.image.load('Assets/Lycron01.png')
        Lycron.Lycron02 = pygame.image.load('Assets/Lycron02.png')
        Lycron.Lycron03 = pygame.image.load('Assets/Lycron03.png')
        Lycron.LycronImages = [Lycron.Lycron00, Lycron.Lycron01, Lycron.Lycron02, Lycron.Lycron03]

        # Generate Starting Text rows
        for i in range(Lycron.PossibleRows):
            Lycron.PreviousText.append(Lycron.randstr(Lycron.String_Length))  # Generates random strings

        # Generate the Status Lists that'll be used
        StartingStatusPosition = Lycron.StatusPositionY
        for i in range(Lycron.GenerateStatuses):
            status = Lycron.CreateCommuncation((Lycron.StatusPositionX, StartingStatusPosition), {}, color=1)
            Lycron.StatusList.append(status)
            StartingStatusPosition += Lycron.StatusBuffer # Add 100 px for the size of the box and a buffer of 20

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
        Possible_Identification = ["POD", "BOT", "COM", "NANO", "LYC", "COMP", "Dom"]
        string = random.choice(Possible_Identification) + " " + str(random.randrange(999)) + ":   " + string
        string = string[0:length]

        string = string[0:len(string)-random.randrange(Lycron.String_Variation)].strip()  # Remove a bit from the end to make it random length
        return string

    @staticmethod
    def Text():
        # Create Black Box
        ChatBoxBG = pygame.Rect((20, 70, Lycron.ChatWidth, Lycron.ChatHeight))
        pygame.draw.rect(screen, Color("DarkGray"), ChatBoxBG, 0)

        # Add some dialogue
        if random.randrange(7) == 3: # 1/7 chance of text occuring! This way theres no pattern
            Lycron.PreviousText.append(Lycron.randstr(Lycron.String_Length))  # Generates random strings

        if len(Lycron.PreviousText) > Lycron.PossibleRows:  # Limit the number of things said so there's no excess lines
            del Lycron.PreviousText[0]

        # Generate text objects now
        printList = []  # List of the objects
        CurrentDistance = 0  # How far down the scren we have gone
        for line in Lycron.PreviousText:  # For each line in it
            # Iterates through each line of text, formatting it and adding to printList
            while Lycron.Font_ChatWindow.size(line)[0] > Lycron.ChatWidth:  # Ensures each is not too long
                line = line[0:len(line)-1]  # If it is, removes 1 from it until it's not too long
            ChatText = Lycron.Font_ChatWindow.render(line, True, (255, 255, 255))  # Create the text
            screen.blit(ChatText, (25, 70 + CurrentDistance))  # Add to the screen
            CurrentDistance += Lycron.Font_ChatWindow.size(line)[1] - Lycron.String_Padding_min  # Create new distance

    @staticmethod
    def Images():
        tempList = []
        for status in Lycron.StatusList:
            new_status = Lycron.CreateCommuncation(status["pos"], status, color=status["Color"])
            tempList.append(new_status)
        Lycron.StatusList = tempList

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
            string = random.choice(PreNames) + " " + random.choice(LycronData.Military_Alphabet) + "-"
            string += random.choice(LycronData.Military_Alphabet) + "-"
            string += random.choice(LycronData.Military_Alphabet)
            info["Name"] = string

            # ID Number:
            info["ID"] = str(random.randrange(100000, 999999)) + str(random.randrange(100000, 999999))

            # Status
            info["CurrentStatus"] = random.choice(LycronData.Good_Statuses)
        # Cleanup
        if color == 0 and info["JustChanged"]:
            info["ConnectedText"] = "Not Connected To: "
            info['CurrentStatus'] = random.choice(LycronData.Bad_Statuses)
            info["JustChanged"] = False

        if random.randrange(400) == 100: # todo add mode
            if color == 0:
                info['CurrentStatus'] = random.choice(LycronData.Bad_Statuses)
                color = 1
            elif color == 1:
                info['CurrentStatus'] = random.choice(LycronData.Good_Statuses)
            elif color == 2:
                info['CurrentStatus'] = random.choice(LycronData.Bad_Statuses)
                color = 1

        # Background:
        BoxSize = (610, 100)

        BoxBackground = pygame.Rect(pos, BoxSize)  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Color("DarkWhite"), BoxBackground, 0)  # Color it and blit it
        pygame.draw.rect(screen, Color("Black"), BoxBackground, 1)  # Color it and blit it

        # Colored Box
        StatusPos = (pos[0] + 5, pos[1] + 5)
        StatusSize = (9, 90)
        if color == 0:
            StatusColor = Color("Red")
        elif color == 1:
            StatusColor = Color("Green")
        elif color == 2:
            StatusColor = Color("Yellow")

        Status = pygame.Rect(StatusPos, StatusSize)  # Create the object
        pygame.draw.rect(screen, StatusColor, Status, 0)  # Color it and blit it
        #Outline
        StatusOutline = pygame.Rect((pos[0] + 4, pos[1] + 4), (11, 92))  # Create the object
        pygame.draw.rect(screen, Color("Black"), StatusOutline, 1)  # Color it and blit it

        # Text
        ConnectedToPos = (pos[0] + 20, pos[1] + 0)
        ConnectedTo = Lycron.SegoeUI_Small.render(info["ConnectedText"], True, (0, 0, 0))  # Create the text
        screen.blit(ConnectedTo, ConnectedToPos)  # Add to the screen
        ConnectedTo_Width, ConnectedTo_Height = Lycron.SegoeUI_Small.size(info["ConnectedText"])

        ServerName = Lycron.SemiboldSegoeUI_Small.render(info["Name"], True, (0, 0, 0))
        screen.blit(ServerName, (ConnectedToPos[0] + ConnectedTo_Width, ConnectedToPos[1]))

        # -== Extra Text ==-
          # ID
        IDPos = (pos[0] + 20, pos[1] + ConnectedTo_Height)
        IDText = "Identification Number: " + info["ID"]
        ID = Lycron.SegoeUI_Small.render(IDText, True, (0, 0, 0))
        screen.blit(ID, IDPos)
        ID_Width, ID_Height = Lycron.SegoeUI_Small.size(IDText)
          # Current Status
        CurrentStatusPos = (pos[0] + 20, IDPos[1] + ID_Height)
        CurrentStatusText = "Current Status: " + info["CurrentStatus"]
        CurrentStatus = Lycron.SegoeUI_Small.render(CurrentStatusText, True, (0, 0, 0))
        screen.blit(CurrentStatus, CurrentStatusPos)
        CurrentStatus_Width, CurrentStatus_Height = Lycron.SegoeUI_Small.size(CurrentStatusText)


        info['Color'] = color
        return info

    @staticmethod
    def RandColorChange():  # Runs every 5 seconds //todo add if mode is red
        if random.randrange(4) == 1:  # so like 3 per minute?
            StatusList = Lycron.StatusList
            selected_int = random.randint(0, len(StatusList)-1)

            # Randomly chooses either red or orange
            StatusList[selected_int]["Color"] = random.choice([0, 2])
            StatusList[selected_int]["JustChanged"] = True

            SelectedStatus = StatusList[selected_int]  # Make dedicated Variable
            StatusList.remove(SelectedStatus)          # Remove from List
            StatusList =[SelectedStatus] + StatusList  # Move to the top of the list

            # Redo Positions
            starting = Lycron.StatusPositionY
            for status in StatusList:
                status["pos"] = (Lycron.StatusPositionX, starting)
                starting += Lycron.StatusBuffer

            Lycron.StatusList = StatusList




# Initiate Important Blitting Functions
TaskBar.init()
Lycron.init()

# Variables for loop
mode = 0
done = False
CountDown = 0
Frame = 0
Seconds = 0
# -------- Main Program Loop -----------
while not done:
    # Keyboard and Mouse Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    done = True
        if Key(event, pygame.K_ESCAPE):  done = True
        if Key(event, pygame.K_SPACE):
            if Name == "John Qualters":
                Name = "Lycron"
            else:
                Name = "John Qualters"

    # Clear the screen
    screen.fill(Color("White"))

    # Add Taskbar
    TaskBar.CreateTaskbar()

    # Add Lycron Loop
    Lycron.Text()
    Lycron.Images()

    if CountDown > 0:
        TimerRect = pygame.draw.rect(screen, Color("Red"), (0, screen_height-30, int(screen_width*CountDown/300), 10))

    if Seconds % 5 == 0 and Frame == 0: # Once every 5 seconds
        Lycron.RandColorChange()

    # Update the screen
    pygame.display.flip()
    if CountDown > 1:
        CountDown -= 1
    elif CountDown == 1:
        CountDown = 0
        mode = 1

    # Do frame stuff
    Frame += 1
    if Frame > FrameRate:
        Frame = 0
        Seconds = Seconds + 1 if Seconds < 60 else 0
    clock.tick(FrameRate)

pygame.quit()