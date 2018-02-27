"""
Main file of each setup. Will eventually have login and bootup. 
Redirects based on what character computer it is.
"""
# TODO Login and Bootup
# TODO More FAILED screens
# TODO PERCENTAGE ON MODE_5
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
import Helpers, Lycron, Yakim, Rouak, Alyns, Usetha, Mainframe
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
with open("CurrentUser.txt", "r") as file:
    Name = file.read()
mode = 0    # Starting Mode!
bootSeconds = 1  # How many seconds to wait before booting
EscapeTime = 3   # How many seconds to wait before escaping

# Initialize Pygame and clock
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Set the height and width of the screen
screen_width = 1280
screen_height = 1080
if monitor:
    screen = pygame.display.set_mode() #, pygame.FULLSCREEN, 32)
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

    EndSearchBar = (0, 0)

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

        TaskBar.EndSearchBar = (text_width + Icon_Width + 15 + 370 + 15, 0)
        Helpers.StatusBarText.position = TaskBar.EndSearchBar

        Helpers.StatusBarText.Display()

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
    SegoeUI_150i = Helpers.Font.GetFont(150, italics=True)

    BlackLogo = None
    WhiteLogo = None


    @staticmethod
    def init():
        Boot.PODName = pygame.image.load('Assets/PODName.png')
        Boot.BlackLogo = pygame.image.load('Assets/BootLogoBlack.png')
        Boot.WhiteLogo = pygame.image.load('Assets/BootLogoWhite.png')

    @staticmethod
    def Start():
        screen.fill(Helpers.Color("Black"))
        Boot.counter += 1

        # screen.fill(Helpers.Color("DarkGray"))
        screen.blit(Boot.WhiteLogo, (1280 / 2 - 250, 1080 / 2 - 370))

        Helpers.CenterText("PodOS", Boot.SegoeUI_150i, (0, 1280), 650, screen, (255, 255, 255))

        if int(Boot.counter / FrameRate) >= bootSeconds:
            return False
        else:
            return True

# The general items of Mode_2
class Mode_2:
    # Contains functions helpful in constructing each mode 2
    PreviousText = []
    SegoeUI_20 = Helpers.Font.GetFont(20)

    Failure = pygame.image.load('Assets/Failure.png')
    Denied = pygame.image.load('Assets/Denied.png')
    Error = pygame.image.load('Assets/Error.png')
    ShowingFailure = {"showing": None, "time": 0}

    ShowTerminal = False
    PreviousText = []

    @staticmethod
    def Text():
        # Add some machine text
        rows = 17
        pos = (150, 400, 1000)
        Delay = 5
        ChatWidth = 1000

        if random.randrange(Delay) == 1:  # 1/5 chance of text occuring! This way theres no pattern
            Mode_2.PreviousText.append(
                Helpers.randstr(100, 15))  # Generates random strings

        if len(Mode_2.PreviousText) > rows:  # Limit the number of things said so there's no excess lines
            del Mode_2.PreviousText[0]

        # Generate text objects now
        printList = []  # List of the objects
        CurrentDistance = -90  # How far down the scren we have gone
        for line in Mode_2.PreviousText:  # For each line in it
            # Iterates through each line of text, formatting it and adding to printList
            while Mode_2.SegoeUI_20.size(line)[0] > ChatWidth:  # Ensures each is not too long
                line = line[0:len(line) - 1]  # If it is, removes 1 from it until it's not too long
            ChatText = Mode_2.SegoeUI_20.render(line, True, (0, 0, 0))  # Create the text
            screen.blit(ChatText, (pos[0], pos[1] + 70 + CurrentDistance))  # Add to the Sys.screen

            CurrentDistance += Mode_2.SegoeUI_20.size(line)[1] - 5  # Create new distance
        return

    @staticmethod
    def ErrorMessage(show=False):
        # if show is True, blit it on
        if show:
            Mode_2.ShowingFailure["time"] = 180
            Mode_2.ShowingFailure["showing"] = Mode_2.Denied


        # If there's a failure message to be shown
        if Mode_2.ShowingFailure["time"]:
            Mode_2.ShowingFailure["time"] -= 1
            screen.blit(Mode_2.ShowingFailure["showing"], (265, 450))

    @staticmethod
    def Terminal():
        if not Mode_2.ShowTerminal:
            return
        BlackBox = pygame.draw.rect(screen, Helpers.Color("Black"),(240, 200, 800, 400))
        WhiteInside = pygame.draw.rect(screen, Helpers.Color("White"), (240, 200, 800, 400), 2)
        WhiteInside = pygame.draw.rect(screen, Helpers.Color("White"), (244, 204, 794, 394), 1)

        # Add some machine text
        rows = 17
        pos = (245, 225, 800)
        Delay = 2
        ChatWidth = 800

        if random.randrange(Delay) == 1:  # 1/5 chance of text occuring! This way theres no pattern
            Mode_2.PreviousText.append(
                Helpers.randstr(80, 15))  # Generates random strings

        if len(Mode_2.PreviousText) > rows:  # Limit the number of things said so there's no excess lines
            del Mode_2.PreviousText[0]

        # Generate text objects now
        printList = []  # List of the objects
        CurrentDistance = -90  # How far down the scren we have gone
        for line in Mode_2.PreviousText:  # For each line in it
            # Iterates through each line of text, formatting it and adding to printList
            while Mode_2.SegoeUI_20.size(line)[0] > ChatWidth:  # Ensures each is not too long
                line = line[0:len(line) - 1]  # If it is, removes 1 from it until it's not too long
            ChatText = Mode_2.SegoeUI_20.render(line, True, (255, 255, 255))  # Create the text
            screen.blit(ChatText, (pos[0], pos[1] + 70 + CurrentDistance))  # Add to the Sys.screen

            CurrentDistance += Mode_2.SegoeUI_20.size(line)[1] - 5  # Create new distance

        if Mode_2.ShowingFailure["time"]:
            Mode_2.ShowingFailure["time"] -= 1
            screen.blit(Mode_2.ShowingFailure["showing"], (265, 450))
        return

    @staticmethod
    def ShowFailure():
        # Show the failure Message
        Mode_2.ShowingFailure["time"] = 120
        Mode_2.ShowingFailure["showing"] = Mode_2.Denied
        return

# Fault Tolerance
class Mode_3:
    frame = 0
    initiated = False

    SegoeUI_100 = Helpers.Font.GetFont(100)
    SegoeUI_125i = Helpers.Font.GetFont(125, italics=True)

    LoadingBar = 0

    @staticmethod
    def init():
        Mode_3.initiated = True

    @staticmethod
    def Background():
        if Mode_3.frame < 31:
            Mode_3.frame += .5
            BlackFade = pygame.draw.rect(screen, Helpers.Color("DarkGray"), (0, 0, 1280, int(Mode_3.frame/30 * 1080)))
            TaskBar.CreateTaskbar(0)
            return
        screen.fill(Helpers.Color("DarkGray"))
        TaskBar.CreateTaskbar(0)

        Helpers.CenterText("Fault Tolerance Activated:", Mode_3.SegoeUI_100, (0, 1280), 300, screen, (255, 255, 255))
        Helpers.CenterText(user.Mode_5.data["System"], Mode_3.SegoeUI_125i, (0, 1280), 400, screen, (255, 255, 255))

        Mode_3.LoadingBar = Mode_3.LoadingBar + 1 if Mode_3.LoadingBar < 60 else -60

        if Mode_3.LoadingBar < 0:
            WhiteBox = pygame.draw.rect(screen, Helpers.Color("White"), (0, 50, 1280, 20))
            y_length = int((60 + Mode_3.LoadingBar)/60 * 1280)
            MovingBox = pygame.draw.rect(screen, Helpers.Color("DarkGray"), (0, 50, y_length, 20))
        else:
            y_length = int((Mode_3.LoadingBar)/60 * 1280)
            MovingBox = pygame.draw.rect(screen, Helpers.Color("White"), (0, 50, y_length, 20))


    @staticmethod
    def run():
        if not Mode_3.initiated:
            Mode_3.init()

        Mode_3.Background()

# The "Restarting" Phase
class Mode_5:
    data = None
    SegoeUI_20 = Helpers.Font.GetFont(20)
    SegoeUI_35 = Helpers.Font.GetFont(35)
    SegoeUI_50 = Helpers.Font.GetFont(50)
    SegoeUI_100 = Helpers.Font.GetFont(100)
    SegoeUI_125i = Helpers.Font.GetFont(125, italics=True)
    SegoeUI_100sli = Helpers.Font.GetFont(100, semilight=True, italics=True)
    SegoeUI_150i = Helpers.Font.GetFont(150, italics=True)

    initiated = False

    PreviousText = []

    LoadingPercentage = 0
    PercentageSpeed = 80
    PercentageText = "Restarting"
    PercentageColor = Helpers.Color("RedOrange")

    Failure = None
    Denied = None
    Error = None
    ShowingFailure = {"showing": None, "time": 0}

    Transition = 0
    BlackLogo = None
    WhiteLogo = None

    @staticmethod
    def init():
        Mode_5.data = user.Mode_5.data  # Retrieve data from user

        Mode_5.Failure = pygame.image.load('Assets/Failure.png')
        Mode_5.Denied = pygame.image.load('Assets/Denied.png')
        Mode_5.Error = pygame.image.load('Assets/Error.png')

        Mode_5.BlackLogo = pygame.image.load('Assets/BootLogoBlack.png')
        Mode_5.WhiteLogo = pygame.image.load('Assets/BootLogoWhite.png')

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
        return

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
        return

    @staticmethod
    def LoadingText():
        add_to_loading = random.randrange(Mode_5.PercentageSpeed)  # Add a random amount each time
        Mode_5.LoadingPercentage += add_to_loading/100  # Add to the loading bar

        if Mode_5.LoadingPercentage >= 100:  # If the loading bar is above 100%
            Mode_5.LoadingPercentage = 0  # Set to 0
            Mode_5.PercentageSpeed = random.choice([75, 50, 125, 100, 25, 78, 80])  # Set next time's speed
            Mode_5.PercentageText = random.choice(Mode_5.data["Dialogue"])  # Change text
            Mode_5.PercentageColor = Helpers.Color(random.choice(["RedOrange", "Blue", "Green", "Yellow"])) # Change color

            Mode_5.ShowingFailure["showing"] = random.choice([Mode_5.Failure, Mode_5.Error, Mode_5.Denied])
            Mode_5.ShowingFailure["time"] = 90  # Show the failure message for 3 seconds (90 frames)

        # Arrange the colored box
        x_pos = int(800 * Mode_5.LoadingPercentage/100)
        PercentagePos = (240, 840, x_pos, 80)
        PercentageBox = pygame.Rect(PercentagePos)  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Mode_5.PercentageColor, PercentageBox)

        # Draw the Outline
        OutlineBox = pygame.Rect((240, 840, 800, 80))  # Set the Background for the taskbar rect
        pygame.draw.rect(screen, Helpers.Color("Black"), OutlineBox, 3)
        pygame.draw.line(screen, Helpers.Color("Black"), (x_pos + 240, 840), (x_pos + 240, 840 + 80), 3)

        # Add the Text
        Helpers.CenterText(Mode_5.PercentageText, Mode_5.SegoeUI_50, (0, 1280), 775, screen, (0, 0, 0))

        # Add Percentage Text
        PercentageText = str(round(Mode_5.LoadingPercentage, 1)) + "%"
        PercentageWidth, PercentageHeight = Mode_5.SegoeUI_35.size(PercentageText)
        if Mode_5.LoadingPercentage > 50:
            pos = (x_pos + 240 - PercentageWidth - 5, 855)
        else:
            pos = (x_pos + 240 + 5, 855)

        # Actually Show the text
        PercentageTextBox = Mode_5.SegoeUI_35.render(PercentageText, True, (0, 0, 0))  # Create the text
        screen.blit(PercentageTextBox, pos)  # Add to the Sys.screen

        # If there's a failure message to be shown
        if Mode_5.ShowingFailure["time"]:
            Mode_5.ShowingFailure["time"] -= 1
            screen.blit(Mode_5.ShowingFailure["showing"], (265, 450))
        return

    @staticmethod
    def RunTransition():
        if Mode_5.Transition < 30:
            screen.fill(Helpers.Color("DarkGray"))
            return
        if Mode_5.Transition < 45:
            screen.fill(Helpers.Color("DarkGray"))
            screen.blit(Mode_5.WhiteLogo, (1280/2-250, 1080/2-370))
            return
        if Mode_5.Transition < 90:
            screen.fill(Helpers.Color("DarkGray"))
            screen.blit(Mode_5.WhiteLogo, (1280/2-250, 1080/2-370))

            Helpers.CenterText("PodOS", Mode_5.SegoeUI_150i, (0, 1280), 650, screen, (255, 255, 255))
            if Mode_5.Transition > 55:
                Helpers.CenterText("Loading...", Mode_5.SegoeUI_50, (0, 1280), 830, screen, (255, 255, 255))
            return
        if Mode_5.Transition  > 90:
            screen.fill(Helpers.Color("LightGray"))

            WhiteBox = pygame.Rect((140, 140, 1000, 800))  # Set the Background for the taskbar rect

            pygame.draw.rect(screen, Helpers.Color("White"), WhiteBox, 0)
            pygame.draw.rect(screen, Helpers.Color("Black"), WhiteBox, 5)

            screen.blit(Mode_5.BlackLogo, (1280 / 2 - 250, 1080 / 2 - 370))

            Helpers.CenterText("PodOS", Mode_5.SegoeUI_150i, (0, 1280), 650, screen, (0, 0, 0))
            Helpers.CenterText("Loading...", Mode_5.SegoeUI_50, (0, 1280), 830, screen, (0, 0, 0))
            return

    @staticmethod
    def run():
        if not Mode_5.initiated:
            Mode_5.init()

        if not Mode_5.Transition == 150:
            Mode_5.Transition += 1
            Mode_5.RunTransition()
            return

        Mode_5.Background()
        Mode_5.Text()
        Mode_5.LoadingText()
        return

# The Final Restart
class Mode_6:
    SegoeUI_100 = Helpers.Font.GetFont(100)
    SegoeUI_125i = Helpers.Font.GetFont(125, italics=True)

    frames = 0

    @staticmethod
    def run():
        Mode_6.frames += 1

        if Mode_6.frames < 30:
            Mode_5.Background()
        elif Mode_6.frames < 60:
            screen.fill(Helpers.Color("LightGray"))
        elif Mode_6.frames < 90:
            screen.fill(Helpers.Color("Black"))
        else:
            screen.fill(Helpers.Color("Black"))
            Helpers.CenterText("Restarting", Mode_6.SegoeUI_100, (0, 1280), 300, screen, (255, 255, 255))
            Helpers.CenterText(user.Mode_5.data["System"], Mode_6.SegoeUI_125i, (0, 1280), 400, screen, (255, 255, 255))


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
        if event.type == pygame.QUIT:
            done = True

        # On Pressdown of Escape
        if Key(event, pygame.K_ESCAPE):
            Escape += 1
            if Escape >= FrameRate * EscapeTime:
                done = True

        # On Pressup of Escape
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            Escape = 0

        # Up and Down for Alyns
        if Name == "Alyns":
            if Key(event, pygame.K_UP):
                user.Key("UP")
            if Key(event, pygame.K_DOWN):
                user.Key("DOWN")

        if mode == 1:  # Begin Convergence
            if Key(event, pygame.K_F2):
                mode = 2
                Helpers.StatusBarText.CreateMessage(screen, "Beginning Failure", 90)

        if mode == 2:
            if Key(event, pygame.K_TAB):
                Mode_2.ShowTerminal = True
                Helpers.StatusBarText.CreateMessage(screen, "Opening Terminal", 60)
            if Mode_2.ShowTerminal and Key(event, pygame.K_RETURN):
                Mode_2.ShowFailure()

            if Key(event, pygame.K_F3):
                time.sleep(1)
                mode = 3

        if mode == 3:
            if Key(event, pygame.K_F5):
                mode = 5

        if mode == 5:  # Keys to transition mode 5 to mode 6
            if Key(event, pygame.K_F6):
                time.sleep(2)
                mode = 6
        if mode == 6:
            if Key(event, pygame.K_SPACE):
                mode = 7

    if 1 <= mode <= 2:
        screen.fill(Helpers.Color("White"))
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

        # If they want terminal showing
        if Mode_2.ShowTerminal:
            Mode_2.Terminal()

    if mode == 3:
        Mode_3.run()

    if mode == 5:
        Mode_5.run()

    if mode == 6:
        Mode_6.run()

    if mode == 7:
        screen.fill(Helpers.Color("Black"))

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
