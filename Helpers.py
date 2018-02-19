import random
import pygame

pygame.font.init()

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
        "DarkWhite": 0xe8e8e8,
        "Teal": 0x1abc9c,
        "Purple": 0x9b59b6,
        "RedOrange": 0xd35400
    }
    if name not in ColorDict:
        raise NameError("Name of color not in list")
    elif name in ColorDict:
        return ColorDict[name]


Possible_Identification = ["POD", "BOT", "COM", "NANO", "LYC", "COMP", "Dom"]
Rare_Possible_Identification = ["Colin", "Liam", "Greyson", "David", "Q", "Katy", 'Mallory',
                               "Grace", "Alyssa", "Serena", "Emily", "Christina", "Abby",
                                "Raden", "Molly", "Michaela"]


def randstr(length, variation):  # HELPER FUNCTION
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
    if random.randint(0, 30) < 3:
        character_name = random.choice(Rare_Possible_Identification)
    else:
        character_name = random.choice(Possible_Identification)
    string = character_name + " " + str(random.randrange(999)) + ":   " + string
    string = string[0:length]

    string = string[0:len(string) - random.randrange(
        variation)].strip()  # Remove a bit from the end to make it random length
    return string


def IdealRandStr(length, UseCaps = False):
    string = ""
    if UseCaps:
        useList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        useList = "abcdefghijklmnopqrstuvwxyz"
    for i in range(length):
        string += random.choice(useList)

    return string


def CenterText(text, font, x_range, y, screen, color):
    text_width, text_height = font.size(text)
    text_x = int((x_range[1] - x_range[0])/2)
    text_pos = (text_x - int(text_width / 2), y)
    final_text = font.render(text, True, color)  # Render the Profile Name
    Sys.screen.blit(final_text, text_pos)  # Blit the name 5pix next to the icon

    return y + text_height


class Font:
    LoadedFonts = {}

    @staticmethod
    def GetFont(size, italics=False, bold=False, semilight=False, semibold=False, light=False):
        """
        Looks for a Font Object with these specifications. If not present, makes one. 
        :param size: Int
        :param italics: Bool
        :param bold: Int, 1, 2, 3
        :param semilight: Bool
        :param semibold: Bool
        :return: 
        """
        FontName = "SegoeUI"
        if bold:  # If user wants full bold:
            if bold > 3:  # Only 3 settings for bold
                raise TypeError("Typeface error: 3 is max boldness")

            FontName += "_" + str(bold) + "b"

            if italics and bold != 3:  # Italics only works on bold 3
                raise TypeError("Typeface error: Bold Italics only on semibold or lvl 3")

            elif italics and bold == 3:
                FontName += "_i"

        elif semilight:
            FontName += "_SL"
            if italics:
                FontName += "_i"
        elif semibold:
            FontName += "_SB"
            if italics:
                FontName += "_i"
        elif light:
            FontName += "_L"
            if italics:
                FontName += "_i"
        elif italics:  # if just normal font and italics:
            FontName += "_i"

        FontName += ".ttf"

        if FontName in Font.LoadedFonts:
            return Font.LoadedFonts["FontName"]
        else:
            Font.LoadedFonts["FontName"] = pygame.font.Font("Assets/Fonts/" + FontName, size)
            return Font.LoadedFonts["FontName"]

# A helper function that shows a message in tehs tatus bar
class StatusBarText:
    ShowingMSG = ""
    TimeRemaining = 0
    position = (0, 0)  # Added by Main.Taskbar()
    screen = None

    SegoeUI = Font.GetFont(30)

    @staticmethod
    def CreateMessage(screen, message: str, time: int):
        """
        Creates a message object to show on the top bar
        :param message:  The string of what to say
        :param time:     The time of how long to show it
        :return:         None
        """
        StatusBarText.ShowingMSG = message
        StatusBarText.TimeRemaining = time
        StatusBarText.screen = screen

    @staticmethod
    def Display():
        if not StatusBarText.TimeRemaining:
            return

        StatusBarText.TimeRemaining -= 1
        Text = StatusBarText.SegoeUI.render(StatusBarText.ShowingMSG, True, (255, 255, 255))  # Render the Profile Name
        StatusBarText.screen.blit(Text, StatusBarText.position)

