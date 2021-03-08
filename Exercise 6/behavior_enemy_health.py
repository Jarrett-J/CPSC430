from behavior import Behavior
from pubsub import pub
import math
import numpy

class EnemyHealth(Behavior):
    def __init__(self, health):
        super(EnemyHealth, self).__init__()
        self.falling = False
        self.health = health
        
    def tick(self):
        if self.falling:
            self.game_object.position[1] -= 500
            self.falling = False
        
    
    def clicked(self):
        self.health -= 10
        print("Health: " + str(self.health))
        if (self.health <= 0):
            self.falling = True
            #destroy    
        
        