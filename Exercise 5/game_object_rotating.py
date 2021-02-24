from game_object import GameObject

class GameObjectRotating(GameObject):
    def __init__(self, position, kind, id):
        super(GameObjectRotating, self).__init__(position, kind, id)
        self.allow_rotation = True
        self.rotation_speed = 0
        
    def tick(self):
        if self.allow_rotation:
            self.x_rotation += self.rotation_speed
            self.y_rotation += self.rotation_speed
            self.z_rotation += self.rotation_speed
            
    def clicked(self):
        #self.allow_rotation = not self.allow_rotation
        self.rotation_speed += 0.5
        print("Clicked rotate cube")
        
        