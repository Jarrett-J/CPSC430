from pubsub import pub

from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds


class PlayerHealth(Behavior):
    def __init__(self, health, sound=None):
        super(PlayerHealth, self).__init__()
        self.health = health
        self.sound = sound

    def hit_player(self, damage):
        self.health -= damage
        pub.sendMessage("player-damage")

        if self.sound:
            Sounds.play_sound(self.sound)

        if self.health <= 0:
            print("Player died")
            GameLogic.load_world(GameLogic.current_level)
            pub.sendMessage('refresh-text')
            pub.sendMessage('refresh-health')
            pass
