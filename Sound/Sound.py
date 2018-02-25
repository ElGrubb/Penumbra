import pyglet, time, pygame
from pyglet.gl import *
pyglet.options['audio'] = ('openal', 'directsound', 'silent')

# Initialize Pygame and clock
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
Viewing = -1
pygame.mixer.init(frequency=22050,size=-16,channels=4)


ViewFont = pygame.font.Font("SegoeUI.ttf", 30)

info = [{
    "Number": 0,
    "Name": "BeginningBeep_A:  1",
    "File": "Beeps_A.wav",
    "Queue": "GRACE: Interpod signals are scattered. Heightened frequency of network transmissions.[NOW]"
}, {
    "Number": 1,
    "Name": "BeginningBeep_C:  2",
    "File": "Beeps_C.wav",
    "Queue": "USETHA: Nutrient solution temperature increasing, nutrient levels decreasing. [NOW]"
}, {
    "Number": 2,
    "Name": "BeginningBeep_Eb:  3",
    "File": "Beeps_Eb.wav",
    "Queue": "ROUAK: Exterior visuals down. POD barriers are beginning collapse. [NOW]"
}, {
    "Number": 3,
    "Name": "BeginningBeep_Gb:  4",
    "File": "Beeps_Gb.wav",
    "Queue": "YAKIM: Oxygen concentration levels depreciating by 3%. Nitrogen concentration increased—[NOW]"
}, {
    "Number": 4,
    "Name": "BeginningBeep_A4:  5",
    "File": "Test01.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}, {
    "Number": 5,
    "Name": "Convergence Fourthcoming",
    "File": "Convergence.wav",
    "Queue": "ADRIEL and ELIK: Failsafe Echo Delta Niner [1s 2s NOW]"
}, {
    "Number": 6,
    "Name": "Shutdown",
    "File": "Shutdown.wav",
    "Queue": "[Automatic]"
}
]

for i in range(len(info)):  # Adds a tag that none of them have been played yet
    info[i]["played"] = False

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



def ShowInfo():
    NextUp = None
    for i in range(len(info)):
        if not info[i]["played"]:
            NextUp = info[i]
            break
    if NextUp:
        Text = "Hit Space at the [NOW]:   "#  + NextUp["Queue"]
        TextObj = ViewFont.render(Text, True, (0, 0, 0))  # Render the Profile Name
        screen.blit(TextObj, (5, 5))

        Text = NextUp["Queue"]
        TextObj = ViewFont.render(Text, True, (0, 0, 0))  # Render the Profile Name
        screen.blit(TextObj, (5, 35))


screen = pygame.display.set_mode((1280, 800))

done = False
Escape = 0
while not done:
    # Keyboard and Mouse Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # On Pressdown of Escape
        if Key(event, pygame.K_ESCAPE):
            Escape += 1
            if Escape >= 30 * 5:
                done = True

        # On Pressdown of Space
        if Key(event, pygame.K_SPACE):
            play = None
            for i in range(len(info)):
                if not info[i]["played"]:
                    play = i
                    info[play]["played"] = True
                    break
            if play != None:
                print("Playing " + info[play]["Name"])
                to_play = pygame.mixer.Sound(info[play]["File"])
                pygame.mixer.Channel(play).set_volume(13.0)
                pygame.mixer.Channel(play).play(to_play)

                print(pygame.mixer.Channel(play).get_volume())

            if play == 5:
                time.sleep(1.1)
                play = 6
                to_play = pygame.mixer.Sound(info[play]["File"])
                pygame.mixer.Channel(7).play(to_play)
                info[play]["played"] = True
                time.sleep(.15)
                for j in range(6):
                    # j = 5-j
                    pygame.mixer.Channel(j).stop()
                    play = 6

    screen.fill(Color("White"))
    ShowInfo()
    pygame.display.flip()
    clock.tick(30)

exit()





music = pyglet.resource.media('Beeps_A.wav')
music.play()
time.sleep(1.5)
music2 = pyglet.resource.media('Beeps_C.wav')
music2.play()

time.sleep(1.5)
music2 = pyglet.resource.media('Beeps_Eb.wav')
music2.play()

time.sleep(3.5)
music2 = pyglet.resource.media('Beeps_Gb.wav')
music2.play()

time.sleep(3.5)
music2 = pyglet.resource.media('Beeps_A4.wav')
music2.play()

time.sleep(5.5)
music2 = pyglet.resource.media('Tornado.wav')
music2.play()

pyglet.app.run()
