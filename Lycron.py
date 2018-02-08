"""
February 1st
Very first attempt at making a computer system. This is an attempt at a base model with the 4 areas. 
Here I go!
"""
import pygame
import random
import time
import math

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
        "DarkWhite": 0xecf0f1
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
        # image = Lycron.LycronImages[Lycron.CurrentImage]
        # screen.blit(image, (550, 70))

        TaskBarBG = pygame.Rect((650, 70, 610, 100))  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Color("DarkWhite"), TaskBarBG, 0)  # Color it and blit it

    @staticmethod
    def CreateCommuncation():
        pass


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
        Lycron.CurrentImage += 1
        if Lycron.CurrentImage >= len(Lycron.LycronImages):
            Lycron.CurrentImage = 0

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
