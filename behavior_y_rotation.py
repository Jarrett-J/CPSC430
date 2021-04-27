from behavior import Behavior

class YRotation(Behavior):
    def __init__(self, speed):
        super(YRotation, self).__init__()
        self.speed = speed
        
    def tick(self):
        self.game_object.y_rotation += self.speed