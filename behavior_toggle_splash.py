from pubsub import pub

from behavior import Behavior


class ToggleSplash(Behavior):
    def __init__(self):
        super(ToggleSplash, self).__init__()
        pub.sendMessage('splash')
