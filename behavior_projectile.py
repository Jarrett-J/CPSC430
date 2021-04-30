from behavior import Behavior
from game_logic import GameLogic


class Projectile(Behavior):
    def __init__(self, damage, summoner_game_object, ignore_kind=None):
        super(Projectile, self).__init__()
        self.damage = damage
        self.ignore = ignore_kind
        self.summoner_game_object = summoner_game_object
        self.destroying = False

        # print("ignoring " + str(self.summoner_game_object))

    def tick(self):
        if self.destroying:
            return

        if self.game_object.collisions:
            for other in self.game_object.collisions:
                if other.id == self.summoner_game_object.id:
                    return

                if other.kind == self.ignore:
                    return
                else:
                    self.destroying = True

                    if other.kind == "player":
                        other.get_behavior("PlayerHealth").hit_player(self.damage)

                    # print("Collided with " + str(other.kind))
                    self.delete_object()

    def delete_object(self):
        if not self.destroying:
            return
        self.destroying = True
        GameLogic.delete_object(self.game_object)

    def clicked(self, game_object):
        pass