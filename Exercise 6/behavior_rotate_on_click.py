from behavior import Behavior

class RotateOnClick(Behavior):
    def __init__(self):
        super(RotateOnClick, self).__init__()
        self.allow_rotation = True
        self.rotation_speed = 0
        
    def tick(self):
        if self.allow_rotation:
            self.game_object.x_rotation += self.rotation_speed
            self.game_object.y_rotation += self.rotation_speed
            self.game_object.z_rotation += self.rotation_speed
                
    def clicked(self):
        self.rotation_speed += 0.5
        print("Clicked rotate cube")

