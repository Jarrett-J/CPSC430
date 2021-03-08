from game_object import GameObject


class GameObjectMove(GameObject):
    def __init__(self, position, size, kind, id):
        super(GameObjectMove, self).__init__(position, size, kind, id)
        self.can_move = False
        self.move_left = True
        self.move_amt = 0
        self.x = .25
        self.y = 0
        self.z = 0
        
    def tick(self):
        if self.can_move:
            if self.move_left:
                self.position[0] -= self.x
                self.move_amt += 1
                if self.move_amt > 50:
                    self.move_left = False
                    self.move_amt = 0
                
            else:
                self.position[0] += self.x
                self.move_amt += 1
                if self.move_amt > 50:
                    self.move_left = True
                    self.move_amt = 0
                
    def clicked(self):
        print("Clicked move cube")
        self.can_move = not self.can_move
