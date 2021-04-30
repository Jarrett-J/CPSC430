from pubsub import pub

from behavior import Behavior
from game_logic import GameLogic


class LoadLevelOnTimer(Behavior):
    def __init__(self, level, wait_time, cutscene, event=None):
        super(LoadLevelOnTimer, self).__init__()
        self.level = level
        self.wait_time = wait_time
        self.cutscene = cutscene
        self.called = False
        self.event = event

    def tick(self):
        if not self.called:
            pub.sendMessage("play" + str(self.cutscene))
            self.called = True

        if self.wait_time:
            if self.wait_time <= 1:
                GameLogic.load_world(self.level)
                pub.sendMessage("stop" + str(self.cutscene))

                if self.event:
                    pub.sendMessage(self.event)
            else:
                self.wait_time -= 1
