from behavior import Behavior

class ZRotation(Behavior):
    def __init__(self, speed):
        super(ZRotation, self).__init__()
        self.speed = speed
        
    def tick(self):
        self.game_object.z_rotation += self.speed