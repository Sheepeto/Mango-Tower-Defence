from ursina import *
import numpy as np
import os
import pickle


class Bat(Entity):

    def __init__(self):
        super().__init__(model="cube",
                         texture="Bat1",
                         position=(-26.25, 0, 0),
                         scale=2.5,
                         color=color.green,
                         collider="box")
        self.Health = 10
        self.MoveSpeed = 0.125


        invoke(self.Movement, delay=0.125)

    def Movement(self):
        if self.texture.name == "Bat1.png" or self.texture.name == "Bat2.png" or self.texture.name == "Bat3.png":
            if self.x != 26.25:
                self.x += self.MoveSpeed
                invoke(self.Movement, delay=0.005)

            else:

                self.texture = "mango"
                invoke(self.Movement, delay=0.005)

        else:

            if self.x != -26.25:
                self.x -= self.MoveSpeed
                invoke(self.Movement, delay=0.005)

            else:
                self.texture = "Bat1"
                invoke(self.Movement, delay=0.005)


class LevelOne(Entity):

    def __init__(self):
        super().__init__()

        with open(r'Data\Data.pkl', 'rb') as f:
            self.Data = pickle.load(f)

        self.CurrentWave = 1
        self.TotalWaves = 10
        self.EnemySpawned = 0

        self.EnemyList = []
        self.Units = self.Data["Units"]

        self.Mangoes = self.Data["Mangoes"]
        self.Money = self.Data["Money"]

        # UI

        self.WaveText = Text(text=f"Wave: {self.CurrentWave}/{self.TotalWaves}",
                             scale=1.25,
                             origin=(-4.5, -14))

        self.MoneyText = Text(text=f"Money: {self.Money}",
                              scale=1.25,
                              origin=(-4.75, -13))

        self.MangoText = Text(text=f"Mangoes: {self.Mangoes}",
                              scale=1.25,
                              origin=(-4.375, -12))

        self.ReadyButton = Button(text="Start Wave",
                                  position=(0.75, -0.35),
                                  scale=(0.25, 0.125),
                                  on_click=self.StartWave)

        # Track

        self.Track = Entity(model="cube",
                            scale=(50, 2.5))

        self.ExitTrack = Entity(model="cube",
                                color=color.red,
                                position=(-26.25, 0),
                                scale=2.5,
                                visible=True,
                                collider="box")

        self.MangoTree = Entity(model="cube",
                                texture="mango",
                                position=(26.25, 0),
                                scale=2.5)

        self.Enemy1 = Entity()
        self.Enemy2 = Entity()
        self.Enemy3 = Entity()


    def LoseMango(self):

        self.Mangoes -= 1
        self.MangoText.text = f"Mangoes: {self.Mangoes}"

    def SpawnEnemey(self):

        if self.EnemySpawned == 2:
            self.Enemy2 = Bat()
            self.EnemySpawned = 3

        if self.EnemySpawned == 1:
            self.Enemy2 = Bat()
            invoke(self.SpawnEnemey, delay=0.5)
            self.EnemySpawned = 2

        if self.EnemySpawned == 0:
            self.Enemy1 = Bat()
            invoke(self.SpawnEnemey, delay=0.5)
            self.EnemySpawned = 1


    def StartWave(self):

        if self.Mangoes > 0:

            if self.CurrentWave == 1:

                self.ReadyButton.disable()

                invoke(self.SpawnEnemey, delay=0.5)



    def update(self):
        print(self.Enemy2.position)
        try:
            if self.Enemy1.texture.name == "mango.png":
                if self.Enemy1.position.x == -26.25:
                    print("yes")

                    invoke(self.LoseMango, delay=0.25)

            if self.Enemy2.texture.name == "mango.png":
                if self.Enemy2.position.x == -26.25:
                    print("yes")

                    invoke(self.LoseMango, delay=0.25)

            if self.Enemy3.texture.name == "mango.png":
                if self.Enemy3.position.x == -26.25:
                    print("yes")

                    invoke(self.LoseMango, delay=0.25)
        except AttributeError:
            pass

        if self.Mangoes == 0:
            scene.clear()

