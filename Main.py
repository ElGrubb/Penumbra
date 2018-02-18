"""
Main file of each setup. Will eventually have login and bootup. 
Redirects based on what character computer it is.
"""
# TODO Login and Bootup
import pygame
import random
import time
import math
try:
    import git, os, sys
    monitor = False
except:
    monitor = True
    time.sleep(2)
    import os, sys
import Helpers, Lycron, Yakim, Rouak, Alyns
""" Modes
0: Boot
1: Initial Screens
2: Cascade
3: Fault Tolerance
4+: Post-FT stuff.
10: End
"""
# Check for Updates
# g = git.cmd.Git(os.getcwd())
# output = g.pull()
# if "Already" not in output:
#     os.execv(sys.executable, ['python'] + sys.argv)

# Important Variables
FrameRate = 30
Name = "Alyns"
mode = 0    # Starting Mode!
bootSeconds = 1  # How many seconds to wait before booting
EscapeTime = 3   # How many seconds to wait before escaping

# Initialize Pygame and clock
pygame.init()
pygame.font.init
clock = pygame.time.Clock()

# Set the height and width of the screen
screen_width = 1280
screen_height = 1080
if monitor:
    screen = pygame.display.set_mode()#, pygame.FULLSCREEN, 32)
    w, h = pygame.display.get_surface().get_size()
    screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
elif not monitor:
    screen = pygame.display.set_mode((screen_width, screen_height))

# Set the file that will be used based on the person
if Name == "Lycron":
    user = Lycron
elif Name == "Yakim":
    user = Yakim
elif Name == "Rouak":
    user = Rouak
elif Name == "Alyns":
    user = Alyns
elif Name == "Usetha":
    user = Usetha
elif Name == "Mainframe":
    user = Mainframe
user.Sys.screen = screen
user.Sys.screen_height, user.screen_width = screen_height, screen_width
user.Sys.FrameRate = FrameRate

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

# Sets up the User's TaskBar
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
        TaskBar.Font_SegoeUI = Helpers.Font.GetFont(30)
        TaskBar.SearchBar = pygame.image.load('Assets/Search.png')

    @staticmethod
    def CreateTaskbar(Escape=None):
        """
        Prepares the Taskbar to be put on the screen
        """
        # Background
        TaskBarBG = pygame.Rect((0, 0, screen_width, 50))  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Helpers.Color("DarkGray"), TaskBarBG, 0)  # Color it and blit it

        # Icon
        screen.blit(TaskBar.ProfileIcon, (0, 0))  # Blit the image
        Icon_Width, Icon_Height = TaskBar.ProfileIcon.get_size()  # Get the size and height

        # Username
        ProfileName = TaskBar.Font_SegoeUI.render(Name, True, (255, 255, 255))  # Render the Profile Name
        screen.blit(ProfileName, (Icon_Width + 5, 1))  # Blit the name 5pix next to the icon
        text_width, text_height = TaskBar.Font_SegoeUI.size(Name)  # Get the dimensions of the text

        # Search Bar
        screen.blit(TaskBar.SearchBar, (text_width + Icon_Width + 15, 5))  # Put the search bar 15pix from the text

        # Escape
        if Escape > 2:
            percentage = int(Escape/(FrameRate*EscapeTime)*100)

            EscapeLocation = text_width + Icon_Width + 15 + 370 + 15
            EscapeBarBG = pygame.Rect((EscapeLocation, 5, 100, 37))  # Set the Background for the taskbar rect
            pygame.draw.rect(screen, Helpers.Color("White"), EscapeBarBG, 2)  # Color it and blit it

            EscapeBarBG = pygame.Rect((EscapeLocation, 5, percentage, 37))  # Set the Background for the taskbar rect
            pygame.draw.rect(screen, Helpers.Color("White"), EscapeBarBG, 0)
            if percentage >= 95:
                EscapeWords = TaskBar.Font_SegoeUI.render("Escape", True, (0, 0, 0))  # Render the Profile Name
                screen.blit(EscapeWords, (EscapeLocation+5, 0))  # Blit the name 5pix next to the icon

# The Small Loading Screen
class Boot:
    counter = 0
    PODName = None
    @staticmethod
    def init():
        Boot.PODName = pygame.image.load('Assets/PODName.png')


    @staticmethod
    def Start():
        screen.fill(Helpers.Color("Black"))
        Boot.counter += 1

        screen.blit(Boot.PODName, (0, 404))  # Blit the image

        if int(Boot.counter / FrameRate) >= bootSeconds:
            return False
        else:
            return True

# The "Restarting" Phase
class Mode_5:
    data = None
    SegoeUI_20 = Helpers.Font.GetFont(20)
    SegoeUI_50 = Helpers.Font.GetFont(50)
    SegoeUI_100 = Helpers.Font.GetFont(100)
    SegoeUI_125i = Helpers.Font.GetFont(125, italics=True)
    SegoeUI_100sli = Helpers.Font.GetFont(100, semilight=True, italics=True)
    initiated = False

    PreviousText = []

    LoadingPercentage = 0
    PercentageSpeed = 80
    PercentageText = "Restarting"
    PercentageColor = Helpers.Color("RedOrange")

    Failure = None
    ShowingFailure = 0

    @staticmethod
    def init():
        Mode_5.data = user.Mode_5.data  # Retrieve data from user

        Mode_5.Failure = pygame.image.load('Assets/Failure.png')
        Mode_5.initiated = True
        return

    @staticmethod
    def Background():
        screen.fill(Helpers.Color("LightGray"))
        WhiteBox = pygame.Rect((140, 140, 1000, 800))  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Helpers.Color("White"), WhiteBox, 0)
        pygame.draw.rect(screen, Helpers.Color("Black"), WhiteBox, 5)

        PodOS_text = "PodOS"
        Helpers.CenterText(PodOS_text, Mode_5.SegoeUI_100, (0, 1280), 140-10, screen, (0, 0, 0))
        end_y = Helpers.CenterText(Mode_5.data["System"], Mode_5.SegoeUI_125i, (0, 1280), 210, screen, (0, 0, 0))

        line = pygame.draw.line(screen, (0, 0, 0), (140, end_y), (1140, end_y), 5)

    @staticmethod
    def Text():
        # Add some machine text
        rows = 17
        pos = (150, 400, 1000)
        Delay = 5
        ChatWidth = 1000

        if random.randrange(Delay) == 1:  # 1/5 chance of text occuring! This way theres no pattern
            Mode_5.PreviousText.append(
                Helpers.randstr(100, 15))  # Generates random strings

        if len(Mode_5.PreviousText) > rows:  # Limit the number of things said so there's no excess lines
            del Mode_5.PreviousText[0]

        # Generate text objects now
        printList = []  # List of the objects
        CurrentDistance = -90  # How far down the scren we have gone
        for line in Mode_5.PreviousText:  # For each line in it
            # Iterates through each line of text, formatting it and adding to printList
            while Mode_5.SegoeUI_20.size(line)[0] > ChatWidth:  # Ensures each is not too long
                line = line[0:len(line) - 1]  # If it is, removes 1 from it until it's not too long
            ChatText = Mode_5.SegoeUI_20.render(line, True, (0, 0, 0))  # Create the text
            screen.blit(ChatText, (pos[0], pos[1] + 70 + CurrentDistance))  # Add to the Sys.screen

            CurrentDistance += Mode_5.SegoeUI_20.size(line)[1] - 5  # Create new distance

    @staticmethod
    def LoadingText():
        add_to_loading = random.randrange(Mode_5.PercentageSpeed)
        Mode_5.LoadingPercentage += add_to_loading/100
        if Mode_5.LoadingPercentage >= 100:
            Mode_5.LoadingPercentage = 0
            Mode_5.PercentageSpeed = random.choice([75, 50, 125, 100, 25, 78, 80])
            Mode_5.PercentageText = random.choice(Mode_5.data["Dialogue"])
            Mode_5.PercentageColor = Helpers.Color(random.choice(["RedOrange", "Blue", "Green", "Yellow"]))

            Mode_5.ShowingFailure = 90

        x = int(800 * Mode_5.LoadingPercentage/100)
        PercentagePos = (240, 840, x, 80)
        PercentageBox = pygame.Rect(PercentagePos)  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Mode_5.PercentageColor, PercentageBox)

        OutlineBox = pygame.Rect((240, 840, 800, 80))  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Helpers.Color("Black"), OutlineBox, 3)

        Helpers.CenterText(Mode_5.PercentageText, Mode_5.SegoeUI_50, (0, 1280), 775, screen, (0, 0, 0))

        if Mode_5.ShowingFailure:
            Mode_5.ShowingFailure -= 1
            screen.blit(Mode_5.Failure, (265, 450))




    @staticmethod
    def run():
        if not Mode_5.initiated:
            Mode_5.init()

        Mode_5.Background()
        Mode_5.Text()
        Mode_5.LoadingText()

        return


# Initiate Important Blitting Functions
TaskBar.init()
Boot.init()

# Variables for loop
done = False
CountDown = 0
Frame = 0
Seconds = 0
Escape = 0  # How long they've been holding escape
pygame.key.set_repeat(500, 30)
# -------- Main Program Loop -----------
while not done:
    # Keyboard and Mouse Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    done = True
        if Key(event, pygame.K_ESCAPE):
            Escape += 1
            if Escape >= FrameRate * EscapeTime:
                done = True

        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            Escape = 0

    # Clear the screen
    screen.fill(Helpers.Color("White"))

    if mode == 1 or mode == 2:
        # Add Taskbar
        TaskBar.CreateTaskbar(Escape=Escape)

        # Add Mode_1 Loop
        user.Navigator(mode=mode)

        if CountDown > 0:
            TimerRect = pygame.draw.rect(screen, Helpers.Color("Red"), (0, screen_height-30, int(screen_width*CountDown/300), 10))

        if Frame % 15 == 0 and Frame != 0:  # Twice a Second
            user.Navigator(mode=mode, unit=0.5)
        if Seconds % 5 == 0 and Frame == 0:  # Once every 2 seconds
            user.Navigator(mode=mode, unit=2)
        if Seconds % 5 == 0 and Frame == 0: # Once every 5 seconds
            user.Navigator(mode=mode, unit=5)

    if mode == 5:
        Mode_5.run()

    elif mode == 0:
        if not Boot.Start():
            mode = 1

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
