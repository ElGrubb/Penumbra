import time, pygame
# Initialize Pygame and clock
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
Viewing = -1
pygame.mixer.init(frequency=22050,size=-16,channels=4)


ViewFont = pygame.font.Font("SegoeUI.ttf", 30)


info = [{
    "Name": "BeginningBeep_A:  1",
    "File": "NBeeps_0.wav",
    "Queue": "GRACE: Interpod signals are scattered. Heightened frequency of network transmissions.[NOW]"
}, {
    "Name": "BeginningBeep_C:  2",
    "File": "NBeeps_1.wav",
    "Queue": "USETHA: Nutrient solution temperature increasing, nutrient levels decreasing. [NOW]"
}, {
    "Name": "BeginningBeep_Eb:  3",
    "File": "NBeeps_2.wav",
    "Queue": "ROUAK: Exterior visuals down. POD barriers are beginning collapse. [NOW]"
}, {
    "Name": "BeginningBeep_Gb:  4",
    "File": "NBeeps_3.wav",
    "Queue": "YAKIM: Oxygen concentration levels depreciating by 3%. Nitrogen concentration increased—[NOW]"
}, {
    "Name": "BeginningBeep_A4:  5",
    "File": "NBeeps_4.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}, {
    "Name": "Cascade Imminent",
    "File": "Voice_Cascade.wav",
    "Queue": "[After the last one a few seconds]"

}, {
    "Name": "Convergence Fourthcoming (ANOTHER ONE AFTER QUICK)",
    "File": "ConvergenceFourthcoming_2.wav",
    "Queue": "ADRIEL and ELIK: Failsafe Echo Delta Niner [1s 2s NOW]"
}, {
    "Name": "Shutdown2",
    "File": "Shutdown2.wav",
    "Queue": "[Automatic]",
    "End": ["NBeeps_0.wav", "NBeeps_1.wav", "NBeeps_2.wav", "NBeeps_3.wav", "NBeeps_4.wav", "Voice_Cascade.wav","ConvergenceFourthcoming_2.wav"]
}, {
    "Name": "VoiceCheck1",
    "File": "VoiceCheck1.wav",
    "Queue": "NINMODA: 27 [1, 2, 3, NOW]"
}, {
    "Name": "RouakAlarm",
    "File": "RouakAlarm.wav",
    "Queue": "ELIK and ADRIEL: Understood [NOW]"
}, {
    "Name": "End Rouak Alarm",
    "File": None,
    "Queue": "KILL THE ALARM ( GI DAGA AFTER! )",
    "End": ["RouakAlarm.wav"]
}, {
    "Name": "Gi Daga",
    "File": "Gi Daga.wav",
    "Queue": "ELIK and ADRIEL: Kill the Alarm!"
}, {
    "Name": "End Gi Daga",
    "File": None,
    "Queue": "When Colin hits the Floor",
    "End": ["Gi Daga.wav"]
}, {
    "Name": "Alyns Alarm",
    "File": "AlynsAlarm.wav",
    "Queue": "ELIK: Enough!"
}, {
    "Name": "End Alyns Alarm",
    "File": None,
    "Queue": "Fade out by yourself",
    "End": ["AlynsAlarm.wav"]
}, {
    "Name": "20 Minutes Remaining",
    "File": "VoiceCheck2.wav",
    "Queue": "ROUAK: But I— / ADRIEL: Trust me. [NOW]",
    "Playing": True
}, {
    "Name": "Colins Monologue",
    "File": "AlanParsons.wav",
    "Queue": "ADRIEL: 264 Years",
    "Playing": True
}, {
    "Name": "End Monologue",
    "Queue": "test",
    "File": None,
    "End": ["AlanParsons.wav"]
}, {
    "Name": "15 Minutes Remaining",
    "Queue": "ELIK:Keep to the protocol… [NOW]",
    "File": "Voicecheck3.wav",
}, {
    "Name": "12 Minutes Remaining",
    "Queue": "ELIK: At what expense? ADRIEL: We don’t know. [NOW]",
    "File": "Voicecheck4.wav",
}, {
    "Name": "Noise during linkage",
    "File": "AlanParsons2.wav",
    "Queue": "Forging the Link [NOW]",
    "Playing": True
}, {
    "Name": "End Link Noise",
    "Queue": "before NINMODA: Not Working!",
    "File": None,
    "End": ["AlanParsons2.wav"]
}, {
    "Name": "Buzz During Link",
    "Queue": "When David falls down and gasps",
    "File": "LowHum1.wav"
}, {
    "Name": "End Hum",
    "Queue": "When they link again",
    "File": None,
    "End": ["LowHum1.wav"]
}, {
    "Name": "7 Minutes Remaining",
    "Queue": "NINMODA: I don’t care… I must be allowed to…or maybe it could be… [NOW]",
    "File": "Voicecheck5.wav",
}, {
    "Name": "Buzz before she puts her hands on her ears",
    "Queue": "When she puts her hands on her ears",
    "File": "LowHum2.wav"
}, {
    "Name": "End Hum",
    "Queue": "When the hands are on the ears",
    "File": None,
    "End": ["LowHum2.wav"]
}, {
    "Name": "Tuning Fork C",
    "File": "TuningFork.wav",
    "Queue": "When DAVID (NINMODA) Strikes his tuning fork"
}, {
    "Name": "BeginningBeep_A:  2",
    "File": "EBeep_1.wav",
    "Queue": "GRACE: Interpod signals are scattered. Heightened frequency of network transmissions.[NOW]"
}, {
    "Name": "4 Minutes Remaining",
    "Queue": "KYR: Fault Tolerance still in effect, but…  [NOW]",
    "File": "Voicecheck6.wav",
}, {
    "Name": "BeginningBeep_C:  1",
    "File": "EBeep_2.wav",
    "Queue": "USETHA: Nutrient solution temperature increasing, nutrient levels decreasing. [NOW]"
}, {
    "Name": "1 Minute Remaining",
    "Queue": "USETHA: Hydroponics operational! Central Processing increased to 29%. [NOW]",
    "File": "Voicecheck7.wav",
}, {
    "Name": "BeginningBeep_Eb:  3",
    "File": "EBeep_3.wav",
    "Queue": "ROUAK: Exterior visuals down. POD barriers are beginning collapse. [NOW]"
}, {
    "Name": "BeginningBeep_Gb:  4",
    "File": "EBeep_4.wav",
    "Queue": "YAKIM: Oxygen concentration levels depreciating by 3%. Nitrogen concentration increased—[NOW]"
}, {
    "Name": "BeginningBeep_A4:  5",
    "File": "EBeep_5.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}, {
    "Name": "End all of the Beeping",
    "File": None,
    "Queue": "Whenever you feel like it; before the voice check but like 2 seconds before",
    "End": ["EBeep_5.wav","EBeep_4.wav","EBeep_3.wav","EBeep_2.wav","EBeep_1.wav"],
    "Fadeout": 2
}, {
    "Name": "30 Seconds Remaining",
    "Queue": "ALYNS: All ARIP signatures discharged… but one. [1 2 3 NOW]",
    "File": "Voicecheck8.wav",
}, {
    "Name": "10 Seconds Remaining",
    "Queue": "KYR: I understand now. (beat) Thank you.  [1 2 NOW]",
    "File": "Voicecheck9.wav",
}, {
    "Name": "5",
    "Queue": "-",
    "File": "Voicecheck10_5.wav",
}, {
    "Name": "4",
    "Queue": "-",
    "File": "Voicecheck10_4.wav",
}, {
    "Name": "3",
    "Queue": "-",
    "File": "Voicecheck10_3.wav",
}, {
    "Name": "2",
    "Queue": "-",
    "File": "Voicecheck10_2.wav",
}, {
    "Name": "BeginningBeep_A4:  5",
    "File": "Voicecheck10_1.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]",
    "End": ["EBeep_5.wav", "EBeep_4.wav", "EBeep_3.wav", "EBeep_2.wav", "EBeep_1.wav"]
}, {
    "Name": "BeginningBeep_A4:  5",
    "File": "TuningFork.wav",
    "Queue": "ALYNS: 11.5% degradation in the biosignatures of the ARIP. [NOW]"
}]
pygame.mixer.set_num_channels(len(info))
for i in range(len(info)):  # Adds a tag that none of them have been played yet
    info[i]["played"] = False
    info[i]["Number"] = i

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

        Text = NextUp["Name"]
        TextObj = ViewFont.render(Text, True, (0, 0, 0))  # Render the Profile Name
        screen.blit(TextObj, (5, 70))


screen = pygame.display.set_mode((1280, 800))

done = False
Escape = 0
EndBeepChannels = []
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

                if not info[play]["File"].startswith("EBeep"):
                    to_play.set_volume(13.0)
                elif info[play]["File"].startswith("Shutdown2.wav"):
                    to_play.set_volume(50)
                    print("BASS BOOSTED")
                elif info[play]["File"].startswith("NBeep"):
                    to_play.set_volume(.1)
                    print(to_play.get_volume())
                else:
                    to_play.set_volume(2)
                    EndBeepChannels.append(pygame.mixer.Channel(play))


                pygame.mixer.Channel(play).play(to_play)

                print(pygame.mixer.Channel(play).get_volume())
                if info[play]["Name"].startswith("Voice"):
                    pygame.mixer.Channel(play).set_volume(40.0)

            try:
                endlist = info[play]["End"]
                # If there's an endlist:
                for item in endlist:
                    itemnumber = 0
                    for infoitem in info:
                        # For each object file
                        # print(infoitem["File"], item)
                        if infoitem["File"] == item:  # If the name is equal to this
                            itemnumber = infoitem["Number"]

                    try:
                        fadeout = item[play]["Fadeout"]
                        pygame.mixer.Channel(itemnumber).fadeout(fadeout)
                        print("FADING OUT")
                    except:
                        pygame.mixer.Channel(itemnumber).stop()
            except:
                pass

    screen.fill(Color("White"))
    ShowInfo()
    pygame.display.flip()
    clock.tick(30)

exit()