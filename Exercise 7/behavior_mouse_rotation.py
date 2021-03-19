from behavior import Behavior
from pubsub import pub

class MouseRotation(Behavior):
    def __init__(self, sensitivity):
        super(MouseRotation, self).__init__()
        self.sensitivity = sensitivity
        
        pub.subscribe(self.rotate_y, 'rotate-y')
        pub.subscribe(self.rotate_x, 'rotate-x')
        
    def rotate_y(self, amount):
        self.game_object.y_rotation += amount * self.sensitivity
    
    def rotate_x(self, amount):
        self.game_object.x_rotation += amount * self.sensitivity      

