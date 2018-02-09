"""
Main file of each setup. Will eventually have login and bootup. 
Redirects based on what character computer it is.
"""
import pygame
import random
import time
import math
import Helpers, Lycron

""" Modes
0: Boot
1: Initial Screens
2: Cascade
3: Fault Tolerance
4+: Post-FT stuff.
10: End
"""

# Important Variables
FrameRate = 30
Name = "Lycron"

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

# Initiate Important Blitting Functions
TaskBar.init()

# Set the file that will be used based on the person
if Name == "Lycron":
    user = Lycron
    Lycron.screen = screen

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

    # Clear the screen
    screen.fill(Helpers.Color("White"))

    # Add Taskbar
    TaskBar.CreateTaskbar()

    # Add Mode_1 Loop
    user.Navigator(mode=1)

    if CountDown > 0:
        TimerRect = pygame.draw.rect(screen, Helpers.Color("Red"), (0, screen_height-30, int(screen_width*CountDown/300), 10))

    if Seconds % 5 == 0 and Frame == 0: # Once every 5 seconds
        user.Navigator(mode=1, unit=5)

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