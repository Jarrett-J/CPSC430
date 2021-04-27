from behavior import Behavior
from game_logic import GameLogic


class Gravity(Behavior):
    def __init__(self, speed):
        super(Gravity, self).__init__()

        self.speed = speed
        self.old_y = 0.0
        
    def tick(self):
        #print("y velocity: " + str(self.game_object.get_property('y_velocity', 0.0)))
        #print("falling is " + str(self.game_object.get_property('falling')))
        """
        # virtual floor
        if self.game_object.position[1] <= 0.0:
            self.game_object.set_property("falling", False)
            self.game_object.position[1] = 0.0
            return
        """

        self.old_y = self.game_object.position[1]
        self.game_object.position[1] -= self.speed

        for other in GameLogic.game_objects:
            # ignore non-collision
            if not GameLogic.collide(self.game_object, GameLogic.game_objects[other]):
                continue

            # ignore existing collision
            if GameLogic.game_objects[other] in self.game_object.collisions:
                continue

            # gravity-related collision
            self.game_object.position[1] += self.speed
            self.game_object.set_property('falling', False)

            #print("setting y velocity to 0 (this gets called)")
            self.game_object.set_property('y_velocity', 0.0)
            return

        # falling
        #print("old y: " + str(self.old_y))
       # print("y pos: " + str(self.game_object.position[1]))
        if self.old_y != self.game_object.position[1]:
            self.game_object.set_property('falling', True)
            self.game_object.set_property('y_velocity', self.game_object.get_property('y_velocity', 0.0) + self.speed)
        else:
            self.game_object.set_property('falling', False)
            print("SETTING Y VELOCITY TO 0! (this never gets called)")
            self.game_object.set_property('y_velocity', 0.0)

        self.game_object._moved = True


        """
        if self.old_y != self.game_object.position[1]:
            self.game_object.set_property('falling', True)
        else:
            self.game_object.set_property('falling', False)
            
        self.old_y = self.game_object.position[1]
        
        self.game_object.set_property('y_velocity', self.speed)
        self.game_object.position[1] -= self.speed
        self.game_object._moved = True
        """

