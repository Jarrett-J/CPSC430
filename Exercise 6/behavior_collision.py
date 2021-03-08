from behavior import Behavior
from pubsub import pub
import math
import numpy

class BlockedByObjects(Behavior):

    def tick(self):
        if self.game_object.collisions:
            mypos = numpy.array(self.game_object.position)
            
            for other in self.game_object.collisions:
                otherpos = numpy.array(other.position)
                distance = numpy.linalg.norm(mypos - otherpos)
                direction_vector = (mypos - otherpos)/distance
                self.game_object.position = otherpos+(distance+0.2)*direction_vector
                
                """
                print(self.game_object.kind)
                
                
                print("mypos: " + str(mypos))
                print("otherpos: " + str(otherpos))
                print("distance: " + str(distance))
                print("direction vector: " + str(direction_vector))
                print("position: " + str(otherpos+(distance+0.2)*direction_vector) + "\n")
                """

