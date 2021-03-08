from behavior import Behavior

class MoveOnClick(Behavior):
    def __init__(self, move_direction):
        super(MoveOnClick, self).__init__()
        self.can_move = False
        self.move_left = True
        self.move_amt = 0
        self.x = move_direction[0]
        self.y = move_direction[1]
        self.z = move_direction[2]
        
    def tick(self):
        if self.can_move:
            if self.move_left:
                self.game_object.position[0] -= self.x
                self.game_object.position[1] -= self.y
                self.game_object.position[2] -= self.z
                
                self.move_amt += 1
                if self.move_amt > 50:
                    self.move_left = False
                    self.move_amt = 0
                
            else:
                self.game_object.position[0] += self.x
                self.game_object.position[1] += self.y
                self.game_object.position[2] += self.z
            
                self.move_amt += 1
                if self.move_amt > 50:
                    self.move_left = True
                    self.move_amt = 0
                
    def clicked(self):
        print("Clicked move cube")
        self.can_move = not self.can_move
