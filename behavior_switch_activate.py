from pubsub import pub

from behavior import Behavior


class SwitchActivate(Behavior):
    def __init__(self, message):
        super(SwitchActivate, self).__init__()

        self.message = message

    def activated(self, game_object):
        pub.sendMessage(self.message)