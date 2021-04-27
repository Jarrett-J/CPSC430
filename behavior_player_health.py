from pubsub import pub

from behavior import Behavior
from sounds import Sounds


class PlayerHealth(Behavior):
    def __init__(self, health, sound=None):
        super(PlayerHealth, self).__init__()
        self.health = health
        self.sound = "sounds/player-oof.wav"

        #pub.subscribe(self.hit_player, "damage-player")

    # for use with pub
    # def hit_player(self, game_object):

    def hit_player(self, damage):
        print("Player took a hit")

        self.health -= damage
        print("Health: " + str(self.health))
        if self.sound:
            Sounds.play_sound(self.sound)

        if self.health <= 0:
            print("Player died")
            # play death sound
            # restart level
            # prohibit control
            pass
