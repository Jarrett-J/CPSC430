from behavior import Behavior
from pubsub import pub

class CanJump(Behavior):
    def __init__(self, jump_amt):
        super(CanJump, self).__init__()
        self.can_jump = True
        self.jumping = False
        self.falling = False
        self.jump_amt = jump_amt
        
        self.jump_time = 20
        
        pub.subscribe(self.key_space, 'key-space')

    def tick(self):
        if self.jumping:
            if not self.falling:
                if self.jump_time > 0:
                    self.can_jump = False
                    self.game_object.position[1] += self.jump_amt
                    self.jump_time -= 1
                else:
                    self.falling = True
                    self.jump_time = 20
            
            else:
                if self.jump_time > 0:
                    self.can_jump = False
                    self.game_object.position[1] -= self.jump_amt
                    self.jump_time -= 1
                else:
                    self.falling = False
                    self.jumping = False
                    self.jump_time = 20
        
    def key_space(self):
        self.jumping = True
        
