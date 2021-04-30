from game_logic import GameLogic
from movies import Movies
from player_view_editor import PlayerView
from sounds import Sounds


class Main:
    def __init__(self):
        self.instances = []
        # create instances
        self.instances.append(PlayerView())

    def go(self):
        GameLogic.load_world("level_2.txt")
        
        while True:
            GameLogic.tick()
            Sounds.tick()
            Movies.tick()
            for instance in self.instances:
                instance.tick()
                
            if GameLogic.get_property("quit"):
                break
            
    
if __name__ == '__main__':
    main = Main()
    main.go()