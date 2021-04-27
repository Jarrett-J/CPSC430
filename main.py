from game_logic import GameLogic
from player_view import PlayerView
from sounds import Sounds


class Main:
    def __init__(self):
        self.instances = []
        # create instances
        self.instances.append(PlayerView())

    def go(self):
        GameLogic.load_world("level_editor.txt")
        # GameLogic.load_world("level_1.txt")

        while True:
            GameLogic.tick()
            Sounds.tick()

            for instance in self.instances:
                instance.tick()
                
            if GameLogic.get_property("quit"):
                break


if __name__ == '__main__':
    main = Main()
    main.go()
