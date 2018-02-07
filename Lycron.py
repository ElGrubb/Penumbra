"""
February 1st
Very first attempt at making a computer system. This is an attempt at a base model with the 4 areas. 
Here I go!
"""
import pygame
import random
import time

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
        "LightGray": 0x7f8c8d
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
screen = pygame.display.set_mode([screen_width, screen_height], pygame.FULLSCREEN)


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
    ProfileIcon = None
    Font_SegoeUI = None
    SearchBar = None
    @staticmethod
    def init():
        TaskBar.ProfileIcon = pygame.image.load('Assets/ProfileIcon.png')
        TaskBar.Font_SegoeUI = pygame.font.Font("Assets/Fonts/segoeui.ttf", 30)
        TaskBar.SearchBar = pygame.image.load('Assets/Search.png')

    @staticmethod
    def CreateTaskbar():
        """
        Prepares the Taskbar to be put on the screen
        :return: 
        """
        # Background
        TaskBarBG = pygame.Rect((0, 0, screen_width, 50))
        pygame.draw.rect(screen, Color("DarkGray"), TaskBarBG, 0)

        # Icon
        screen.blit(TaskBar.ProfileIcon, (0, 0))
        Icon_Width, Icon_Height = TaskBar.ProfileIcon.get_size()

        # Username
        ProfileName = TaskBar.Font_SegoeUI.render(Name, True, (255, 255, 255))
        screen.blit(ProfileName, (Icon_Width + 5, 1))
        text_width, text_height = TaskBar.Font_SegoeUI.size(Name)

        # Search Bar
        screen.blit(TaskBar.SearchBar, (text_width + Icon_Width + 15, 5))


class LycronLoop:
    PreviousText = []
    ChatHeight = 800
    ChatWidth = 500
    AvgSize = []
    Font_ChatWindow = None
    Font_Width = 20
    PossibleRows = 0

    Lycron00 = None
    Lycron01 = None
    Lycron02 = None
    Lycron03 = None
    LycronImages = [Lycron00, Lycron01, Lycron02, Lycron03]

    CurrentImage = 0

    @staticmethod
    def init():
        LycronLoop.Font_ChatWindow = pygame.font.Font("Assets/Fonts/segoeui.ttf", LycronLoop.Font_Width)
        LycronLoop.PossibleRows = int(LycronLoop.ChatHeight / (LycronLoop.Font_ChatWindow.size("Lycron")[1]-10))

        LycronLoop.Lycron00 = pygame.image.load('Assets/Lycron00.png')
        LycronLoop.Lycron01 = pygame.image.load('Assets/Lycron01.png')
        LycronLoop.Lycron02 = pygame.image.load('Assets/Lycron02.png')
        LycronLoop.Lycron03 = pygame.image.load('Assets/Lycron03.png')
        LycronLoop.LycronImages = [LycronLoop.Lycron00, LycronLoop.Lycron01, LycronLoop.Lycron02, LycronLoop.Lycron03]

    @staticmethod
    def randstr(length):  # Create random strings for display
        string = ''
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ    1234567890    abcdefghijklmnopqrstuvwxyz.!/"
        for i in range(0, length):
            string += random.choice(characters)
        string = string[0:len(string)-random.randrange(16)].strip()
        return string

    @staticmethod
    def Text():
        # Create Black Box
        ChatBoxBG = pygame.Rect((20, 70, LycronLoop.ChatWidth, LycronLoop.ChatHeight))
        pygame.draw.rect(screen, Color("DarkGray"), ChatBoxBG, 0)

        # Add some dialogue
        if random.randrange(7) == 3: # 1/7 chance of text occuring! This way theres no pattern
            LycronLoop.PreviousText.append(LycronLoop.randstr(30))  # Generates random strings

        if len(LycronLoop.PreviousText) > LycronLoop.PossibleRows:  # Limit the number of things said
            del LycronLoop.PreviousText[0]

        if not LycronLoop.PreviousText:  # If it just booted up
            for i in range(LycronLoop.PossibleRows):
                LycronLoop.PreviousText.append(LycronLoop.randstr(30))  # Generates random strings

        # Generate text
        printList = []
        CurrentDistance = 0
        for line in LycronLoop.PreviousText:
            while TaskBar.Font_SegoeUI.size(line)[0] > LycronLoop.ChatWidth:  # Ensures each is not too long
                line = line[0:len(line)-2]
            ChatText = LycronLoop.Font_ChatWindow.render(line, True, (255, 255, 255))
            screen.blit(ChatText, (25, 70 + CurrentDistance))
            # Distance Shit
            CurrentDistance += LycronLoop.Font_ChatWindow.size(line)[1] - 10

    @staticmethod
    def Images():
        image = LycronLoop.LycronImages[LycronLoop.CurrentImage]
        screen.blit(image, (550, 70))


# Initiate Important Blitting Functions
TaskBar.init()
LycronLoop.init()

# Variables for loop
mode = 0
done = False
CountDown = 0
Frame = 0
Seconds = 0
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if Key(event, pygame.K_ESCAPE):
            done = True
        if Key(event, pygame.K_SPACE):
            if Name == "John Qualters":
                Name = "Lycron"
            else:
                Name = "John Qualters"

    # Clear the screen
    if mode == 0:
        screen.fill(Color("White"))
    elif mode == 1:
        screen.fill(Color("Red"))

    # Add Taskbar
    TaskBar.CreateTaskbar()

    # Add Lycron Loop
    LycronLoop.Text()
    LycronLoop.Images()

    if CountDown > 0:
        TimerRect = pygame.draw.rect(screen, Color("Red"), (0, screen_height-30, int(screen_width*CountDown/300), 10))

    if Seconds % 5 == 0 and Frame == 0: # Once every 5 seconds
        LycronLoop.CurrentImage += 1
        if LycronLoop.CurrentImage >= len(LycronLoop.LycronImages):
            LycronLoop.CurrentImage = 0

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
