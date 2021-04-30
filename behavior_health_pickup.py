from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds


class HealthPickup(Behavior):
    def __init__(self, amount, pickup_sound=None):
        super(HealthPickup, self).__init__()

        self.amount = amount
        self.pickup_sound = pickup_sound

    def tick(self):
        self.game_object._moved = True
        if self.game_object.collisions:
            for other in self.game_object.collisions:
                if other.kind == "player":
                    self.pickup(other)

    def pickup(self, player):
        health_behavior = player.get_behavior("PlayerHealth")

        if health_behavior.health >= 100:
            return

        if self.pickup_sound:
            Sounds.play_sound(self.pickup_sound)

        health_behavior.health += self.amount

        if health_behavior.health > 100:
            health_behavior.health = 100

        pub.sendMessage("refresh-health")

        GameLogic.delete_object(self.game_object)
