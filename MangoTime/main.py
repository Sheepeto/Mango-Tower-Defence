
# General Modules
from ursina import *
import os
import pickle
import numpy as np

# Levels
from Levels.LevelOne import *

App = Ursina()


class Game(Entity):

    def __init__(self):

        super().__init__()

        if os.path.exists(r'Data\Data.pkl'):
            with open(r'Data\Data.pkl', 'rb') as f:
                self.Data = pickle.load(f)

        camera.orthographic = True

        self.Playing = False

        if self.Data["Level"] == 0:
            self.Prologue()

        else:
            self.LevelSelection()

    def LevelSelection(self):
        scene.clear()

        if self.Data["Level"] == 1:
            with open(r'Data\Data.pkl', 'wb') as f:

                pickle.dump(self.Data, f)
            self.CurrentLevel = LevelOne()

    def PrologueCheck(self):

        if self.PrologueText.text == "This is my story of how my \ntribe became the most feared tribe in the land":

            self.Data["Level"] = 1
            self.LevelSelection()

        if self.PrologueText.text == "And in this land Mangoes are\nthe most sought-after resource and must defend it\nat all cost":

            self.PrologueText.text = "This is my story of how my \ntribe became the most feared tribe in the land"
            self.PrologueText.origin = (0.725, 3.75)

        if self.PrologueText.text == f"My name is {self.Data['Username']} and i'm the leader of the tribe {self.Data['Tribe Name']}":

            self.PrologueText.text = "And in this land Mangoes are\nthe most sought-after resource and must defend it\nat all cost"
            self.PrologueText.origin = (0.65, 2.5)




    def Prologue(self):

        self.Box = Entity(model="cube",
                          color=color.rgb(217, 160, 102),
                          position=(-5, -15),
                          scale=(55, 10, 1))

        self.PrologueText = Text(
            f"My name is {self.Data['Username']} and i'm the leader of the tribe {self.Data['Tribe Name']}",
            origin=(0.125, 7.5),
            scale=2)
        Button(text="Next",
               scale=0.125,
               position=(0.7, -0.375),
               on_click=self.PrologueCheck)

class MainMenu(Entity):

    def __init__(self):

        super().__init__()

        window.color = color.rgba(0.25, 0.25, 0.25, 1)

        self.TitleText = Text(text="Mango Time",
                              origin=(0, -5),
                              scale=3)

        self.VersionText = Text(text="Version: 1",
                                origin=(-3.25, 9),
                                scale=2)

        self.PlayGameButton = Button(text="Play Game",
                                     origin=(0, -0.5),
                                     scale=(0.5, 0.125))
        self.PlayGameButton.on_click = self.Setup

        self.CreditsButton = Button(text="Credits",
                                    origin=(0, 0.75),
                                    scale=(0.5, 0.125))
        self.CreditsButton.on_click = self.Credits

        self.ExitButton = Button(text="Exit",
                                 origin=(0, 2),
                                 scale=(0.5, 0.125))
        self.ExitButton.on_click = application.quit

        self.SettingsButton = Button(texture="SettingsIcon",
                                     color=color.rgba(1, 1, 1, 1),
                                     origin=(8.4, -4.5),
                                     scale=0.1)
        self.SettingsButton.on_click = self.Settings

    def Setup(self):

        if not os.path.exists(r'Data\Data.pkl'):

            scene.clear()

            self.UsernameText = Text(text="Enter a Username",
                                     origin=(0, -5),
                                     scale=3)

            self.UsernameField = InputField()

            self.ConfirmButton = Button(text="Confirm",
                                        position=(0, -0.125, 0),
                                        scale=0.125,
                                        on_click=self.Setup2)

            self.ErrorText = Text(text="",
                                  color=color.red,
                                  scale=2,
                                  origin=(0, -2))

        else:

            self.PlayGame()

    def Setup2(self):

        if self.UsernameField.text == "":

            self.ErrorText.text = "Name Can't be blank"

        else:

            self.Username = self.UsernameField.text
            scene.clear()

            self.TribeText = Text(text="Enter a name for the tribe",
                                  origin=(0, -5),
                                  scale=3)

            self.TribeField = InputField()

            self.ConfirmButton = Button(text="Confirm",
                                        position=(0, -0.125, 0),
                                        scale=0.125,
                                        on_click=self.SetupFinalizing)

            self.ErrorText2 = Text(text="",
                                   color=color.red,
                                   scale=2,
                                   origin=(0, -2))

    def SetupFinalizing(self):

        if self.TribeField.text == "":

            self.ErrorText2.text = "Tribe name Can't be blank"

        else:
            self.TribeName = self.TribeField.text

            Data = {"Username": self.Username,
                    "Tribe Name": self.TribeName,
                    "Level": 0,
                    "Mangoes": 2,
                    "Money": 10,
                    "Units": ["Spearman"]
                    }

            with open(r'Data\Data.pkl', 'wb') as f:

                pickle.dump(Data, f)

            f.close()

            self.PlayGame()

    def PlayGame(self):

        scene.clear()

        Game()

    def Credits(self):

        self.PlayGameButton.text = ""
        self.CreditsButton.text = ""
        self.ExitButton.text = ""
        self.SettingsButton.disable()

        self.CreditsPanel = Panel(color=color.rgba(0, 0, 0, 255))

        self.CreditsText = Text("Credits",
                                parent=self.CreditsPanel,
                                origin=(0, -17))

        self.CreditsListText = Text("All Assets come from opengameart.org",
                                    parent=self.CreditsPanel,
                                    origin=(0, 0))

        self.CreditsExitButton = Button(texture="Exit",
                                        color=color.rgba(1, 1, 1, 1),
                                        origin=(8.4, -4.5),
                                        scale=0.1)
        self.CreditsExitButton.on_click = self.ExitCredits

    def ExitCredits(self):

        self.PlayGameButton.text = "Play Game"
        self.CreditsButton.text = "Credits"
        self.ExitButton.text = "Exit"
        self.SettingsButton.enable()

        self.CreditsPanel.disable()
        self.CreditsText.disable()
        self.CreditsExitButton.disable()
        self.CreditsListText.disable()

    def Settings(self):

        self.PlayGameButton.text = ""
        self.CreditsButton.text = ""
        self.ExitButton.text = ""
        self.SettingsButton.disable()

        self.SettingsPanel = Panel(color=color.rgba(0, 0, 0, 255))

        self.SettingsText = Text("Settings",
                                 parent=self.SettingsPanel,
                                 origin=(0, -17))

        self.SettingsExitButton = Button(texture="Exit",
                                         color=color.rgba(1, 1, 1, 1),
                                         origin=(8.4, -4.5),
                                         scale=0.1)
        self.SettingsExitButton.on_click = self.ExitSettings

    def ExitSettings(self):

        self.PlayGameButton.text = "Play Game"
        self.CreditsButton.text = "Credits"
        self.ExitButton.text = "Exit"
        self.SettingsButton.enable()

        self.SettingsPanel.disable()
        self.SettingsText.disable()
        self.SettingsExitButton.disable()


def SplashScreen():
    window.color = color.black

    def EndIntro(IntroTransparency):

        if UrsinaImage.color != color.rgba(255, 255, 255, 0):

            UrsinaImage.color = color.rgba(255, 255, 255, IntroTransparency)
            PythonImage.color = color.rgba(255, 255, 255, IntroTransparency)
            UrsinaText.color = color.rgba(255, 255, 255, IntroTransparency)

            IntroTransparency -= 1
            invoke(EndIntro, IntroTransparency, delay=0.005)

        else:

            scene.clear()
            MainMenu()

    def StartIntro(IntroTransparency):

        if UrsinaImage.color != color.rgba(255, 255, 255, 255):

            UrsinaImage.color = color.rgba(255, 255, 255, IntroTransparency)
            PythonImage.color = color.rgba(255, 255, 255, IntroTransparency)

            IntroTransparency += 1

            invoke(StartIntro, IntroTransparency, delay=0)

        else:

            invoke(EndIntro, IntroTransparency, delay=0)

    IntroTransparency = 1

    UrsinaText = Text("Made With Ursina and Python",
                      origin=(0, -5),
                      scale=2)

    UrsinaImage = Sprite(texture="ursinalogo",
                         origin=(1, 0),
                         color=color.rgba(255, 255, 255, 0))

    PythonImage = Sprite(texture="pythonlogo",
                         origin=(-1, 0),
                         color=color.rgba(255, 255, 255, 0))

    invoke(StartIntro, IntroTransparency, delay=0.005)


SplashScreen()

App.run()
