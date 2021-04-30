from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds


class WeaponPickup(Behavior):
    def __init__(self, weapon_type, pickup_sound=None):
        super(WeaponPickup, self).__init__()

        self.weapon_type = weapon_type
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

        behavior_to_find = "behavior_" + self.weapon_type
        behavior = player.get_behavior(self.weapon_type)

        if behavior.has_weapon:
            behavior.ammo_count += 10

        else:
            behavior.has_weapon = True

        pub.sendMessage("refresh-text")
        GameLogic.delete_object(self.game_object)
