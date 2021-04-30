from pubsub import pub

from behavior import Behavior
from game_logic import GameLogic


class LoadLevel(Behavior):
    def __init__(self, level):
        super(LoadLevel, self).__init__()
        self.level = level

    def activated(self, game_object):
        GameLogic.load_world(self.level)

