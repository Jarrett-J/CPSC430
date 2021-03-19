from behavior import Behavior

class Gravity(Behavior):
    def __init__ (self, speed):
        super(Gravity, self).__init__()
        self.speed = speed
        
        self.old_y = 0.0
        
    def tick(self):              
        if self.old_y != self.game_object.position[1]:
            self.game_object.set_property('falling', True)
        else:
            self.game_object.set_property('falling', False)
            
        self.old_y = self.game_object.position[1]
        
        self.game_object.set_property('y_velocity', self.speed)
        self.game_object.position[1] -= self.speed
        self.game_object._moved = True


