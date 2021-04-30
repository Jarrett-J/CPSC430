from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds


class Item(Behavior):
    def __init__(self, ammo_type, amount, pickup_sound=None):
        super(Item, self).__init__()

        # ammo type
        self.ammo_type = ammo_type
        self.amount = amount
        self.pickup_sound = pickup_sound

    def tick(self):
        self.game_object._moved = True
        if self.game_object.collisions:
            for other in self.game_object.collisions:
                if other.kind == "player":
                    self.pickup(other)

    def pickup(self, player):
        if self.pickup_sound:
            Sounds.play_sound(self.pickup_sound)

        player.get_behavior(self.ammo_type).ammo_count += self.amount
        pub.sendMessage("refresh-text")

        GameLogic.delete_object(self.game_object)
