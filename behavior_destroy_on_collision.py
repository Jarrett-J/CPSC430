from behavior import Behavior
from game_logic import GameLogic


class DestroyOnCollision(Behavior):
    def __init__(self, ignore=None):
        super(DestroyOnCollision, self).__init__()
        self.ignore = ignore
        self.destroying = False

    def tick(self):
        if self.destroying:
            return

        if self.game_object.collisions:
            for other in self.game_object.collisions:
                if other.kind == self.ignore:
                    return
                else:
                    self.destroying = True
                    print("Collided with " + str(other.kind))
                    GameLogic.delete_object(self.game_object)
