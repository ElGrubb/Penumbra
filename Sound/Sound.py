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
    "File": "NBeeps_0.wav",
    "Queue": "GRACE: Interpod signals are scattered. Heightened frequency of network transmissions.[NOW]"
}, {
    "Number": 1,
    "Name": "BeginningBeep_C:  2",
    "File": "NBeeps_1.wav",
    "Queue": "USETHA: Nutrient solution temperature increasing, nutrient levels decreasing. [NOW]"
}, {
    "Number": 2,
    "Name": "BeginningBeep_Eb:  3",
    "File": "NBeeps_2.wav",
    "Queue": "ROUAK: Exterior visuals down. POD barriers are beginning collapse. [NOW]"
}, {
    "Number": 3,
    "Name": "BeginningBeep_Gb:  4",
    "File": "NBeeps_3.wav",
    "Queue": "YAKIM: Oxygen concentration levels depreciating by 3%. Nitrogen concentration increased—[NOW]"
}, {
    "Number": 4,
    "Name": "BeginningBeep_A4:  5",
    "File": "NBeeps_4.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}, {
    "Number": 5,
    "Name": "Convergence Fourthcoming",
    "File": "ConvergenceFourthcoming_2.wav",
    "Queue": "ADRIEL and ELIK: Failsafe Echo Delta Niner [1s 2s NOW]"
}, {
    "Number": 6,
    "Name": "Shutdown2",
    "File": "Shutdown2.wav",
    "Queue": "[Automatic]",
    "End": [0, 1, 2, 3, 4, 5]
}, {
    "Number": 7,
    "Name": "VoiceCheck1",
    "File": "VoiceCheck1.wav",
    "Queue": "NINMODA: 27 [1, 2, 3, NOW]"
}, {
    "Number": 8,
    "Name": "RouakAlarm",
    "File": "RouakAlarm.wav",
    "Queue": "ELIK and ADRIEL: Understood [NOW]"
}, {
    "Number": 9,
    "Name": "End Gi Daga",
    "File": None,
    "Queue": "When Colin Hits the Floor",
    "End": [8]
}, {
    "Number": 10,
    "Name": "Gi Daga",
    "File": "Gi Daga.wav",
    "Queue": "ELIK and ADRIEL: Kill the Alarm!"


}, {
    "Number": 11,
    "Name": "Alyns Beep",
    "File": "AlynsBeep.wav",
    "Queue": "ELIK: Enough!",
    "End": [10]
}, {
    "Number": 12,
    "Name": "20 Minutes Remaining",
    "File": "VoiceCheck2.wav",
    "Queue": "ROUAK: But I— / ADRIEL: Trust me. [NOW]",
    "Playing": True
}, {
    "Number": 13,
    "Name": "Colins Monologue",
    "File": "AlanParsons.wav",
    "Queue": "ADRIEL: 264 Years",
    "Playing": True
}, {
    "Number": 14,
    "Name": "End Monologue",
    "Queue": "test",
    "File": None,
    "End": [13]
}, {
    "Number": 14,
    "Name": "15 Minutes Remaining",
    "Queue": "ELIK:Keep to the protocol… [NOW]",
    "File": "Voicecheck3.wav",
}, {
    "Number": 16,
    "Name": "12 Minutes Remaining",
    "Queue": "ELIK: At what expense? ADRIEL: We don’t know. [NOW]",
    "File": "Voicecheck4.wav",
}, {
    "Number": 17,
    "Name": "Linkage Sadness",
    "File": "AlanParsons.wav",
    "Queue": "Forging the Link [NOW]",
    "Playing": True
}, {
    "Number": 18,
    "Name": "End Monologue",
    "Queue": "test",
    "File": None,
    "End": [17]


}, {
    "Number": 19,
    "Name": "7 Minutes Remaining",
    "Queue": "NINMODA: I don’t care… I must be allowed to…or maybe it could be… [NOW]",
    "File": "Voicecheck5.wav",
}, {
    "Number": 20,
    "Name": "Tuning Fork C",
    "File": "TuningFork.wav",
    "Queue": "When DAVID (NINMODA) Strikes his tuning fork"
}, {
    "Number": 21,
    "Name": "BeginningBeep_A:  2",
    "File": "EBeep_1.wav",
    "Queue": "GRACE: Interpod signals are scattered. Heightened frequency of network transmissions.[NOW]"
}, {
    "Number": 22,
    "Name": "4 Minutes Remaining",
    "Queue": "KYR: Fault Tolerance still in effect, but…  [NOW]",
    "File": "Voicecheck6.wav",
}, {
    "Number": 23,
    "Name": "BeginningBeep_C:  1",
    "File": "EBeep_2.wav",
    "Queue": "USETHA: Nutrient solution temperature increasing, nutrient levels decreasing. [NOW]"
}, {
    "Number": 24,
    "Name": "1 Minute Remaining",
    "Queue": "USETHA: Hydroponics operational! Central Processing increased to 29%. [NOW]",
    "File": "Voicecheck7.wav",
}, {
    "Number": 25,
    "Name": "BeginningBeep_Eb:  3",
    "File": "EBeep_3.wav",
    "Queue": "ROUAK: Exterior visuals down. POD barriers are beginning collapse. [NOW]"
}, {
    "Number": 26,
    "Name": "BeginningBeep_Gb:  4",
    "File": "EBeep_4.wav",
    "Queue": "YAKIM: Oxygen concentration levels depreciating by 3%. Nitrogen concentration increased—[NOW]"
}, {
    "Number": 27,
    "Name": "BeginningBeep_A4:  5",
    "File": "EBeep_5.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}, {
    "Number": 28,
    "Name": "30 Seconds Remaining",
    "Queue": "ALYNS: All ARIP signatures discharged… but one. [1 2 3 NOW]",
    "File": "Voicecheck8.wav",
}, {
    "Number": 29,
    "Name": "10 Seconds Remaining",
    "Queue": "KYR: I understand now. (beat) Thank you.  [1 2 NOW]",
    "File": "Voicecheck9.wav",
}, {
    "Number": 30,
    "Name": "5",
    "Queue": "-",
    "File": "Voicecheck10_5.wav",
}, {
    "Number": 31,
    "Name": "4",
    "Queue": "-",
    "File": "Voicecheck10_4.wav",
}, {
    "Number": 32,
    "Name": "3",
    "Queue": "-",
    "File": "Voicecheck10_3.wav",
}, {
    "Number": 33,
    "Name": "2",
    "Queue": "-",
    "File": "Voicecheck10_2.wav",
}, {
    "Number": 34,
    "Name": "BeginningBeep_A4:  5",
    "File": "Voicecheck10_1.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]",
    "End": [27, 26, 25, 23, 21]
}, {
    "Number": 35,
    "Name": "BeginningBeep_A4:  5",
    "File": "TuningFork.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}]

pygame.mixer.set_num_channels(len(info))
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
            for i in range(len(info)):  # Find out which sound is queued
                if not info[i]["played"]:
                    play = i
                    info[play]["played"] = True
                    break

            if play != None and info[play]["File"]:  # If there's something to play
                print("Playing " + info[play]["Name"])
                to_play = pygame.mixer.Sound(info[play]["File"])
                pygame.mixer.Channel(play).set_volume(13.0)
                pygame.mixer.Channel(play).play(to_play)

                print(pygame.mixer.Channel(play).get_volume())

            try:
                endlist = info[play]["End"]
                # If there's an endlist:
                for item in endlist:
                    pygame.mixer.Channel(item).stop()
            except:
                pass

# if play == 9: # Kill the Alarm!
#                 pygame.mixer.Channel(8).stop()
#                 # time.sleep(2)
                # to_play = pygame.mixer.Sound(info[8]["File"])
                # pygame.mixer.Channel(9).play(to_play)

    screen.fill(Color("White"))
    ShowInfo()
    pygame.display.flip()
    clock.tick(30)

exit()