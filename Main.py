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
    done = 100
except:
    print(str(done))
    time.sleep(1)
    done += 1
    import os, sys
import Helpers, Lycron, Yakim

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
Name = "Yakim"
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
screen = pygame.display.set_mode()#, pygame.FULLSCREEN, 32)
w, h = pygame.display.get_surface().get_size()
screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)

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


class Boot:
    counter = 0
    Font_SegoeUI = pygame.font.Font("Assets/Fonts/segoeui.ttf", 5000)
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

# Initiate Important Blitting Functions
TaskBar.init()
Boot.init()

# Set the file that will be used based on the person
if Name == "Lycron":
    user = Lycron
elif Name == "Yakim":
    user = Yakim
user.Sys.screen = screen
user.Sys.screen_height, user.screen_width = screen_height, screen_width
user.Sys.FrameRate = FrameRate


# Variables for loop
mode = 0
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

        if Seconds % 5 == 0 and Frame == 0: # Once every 5 seconds
            user.Navigator(mode=mode, unit=5)

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
