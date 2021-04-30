import numpy

from behavior import Behavior
from pubsub import pub
import math

class KeyFly(Behavior):
    def __init__(self, speed):
        super(KeyFly, self).__init__()
        self.speed = speed
        self.speed = 1
        
        pub.subscribe(self.key_w, 'key-w')
        pub.subscribe(self.key_s, 'key-s')
        pub.subscribe(self.key_a, 'key-a')
        pub.subscribe(self.key_d, 'key-d')

    def key_w(self, camera_direction):
        camera_direction = numpy.array(camera_direction)
        current = numpy.array(self.game_object.position)

        position = (current + self.speed * camera_direction).tolist()

        self.game_object.position = position
        self.game_object._moved = True
        
    def key_s(self, camera_direction):
        camera_direction = numpy.array(camera_direction)
        current = numpy.array(self.game_object.position)

        position = (current - self.speed * camera_direction).tolist()

        self.game_object.position = position
        self.game_object._moved = True
    
    def key_a(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object._y_rotation-90))
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object._y_rotation-90))
        self.game_object._moved = True
        
    def key_d(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object._y_rotation+90))
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object._y_rotation+90))
        self.game_object._moved = True