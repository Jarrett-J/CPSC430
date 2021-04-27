from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds


class EnemyHealth(Behavior):
    def __init__(self, health):
        super(EnemyHealth, self).__init__()
        self.health = health
        self.sound = "sounds/enemy-hit-1.wav"
        
    def clicked(self, game_object):
        self.health -= 10
        print("Health: " + str(self.health))
        if self.sound:
            Sounds.play_sound(self.sound)

        if self.health <= 0:
            # play death sound

            GameLogic.delete_object(self.game_object)
