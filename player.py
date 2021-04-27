from game_object import GameObject
from pubsub import pub
import math
import numpy


class Player(GameObject):
    def __init__(self, position, size, kind, id):
        super(Player, self).__init__(position, size, kind, id)

        pub.subscribe(self.key_w, 'key-w')
        pub.subscribe(self.key_s, 'key-s')
        pub.subscribe(self.key_a, 'key-a')
        pub.subscribe(self.key_d, 'key-d')
        
        pub.subscribe(self.rotate_y, 'rotate-y')
        pub.subscribe(self.rotate_x, 'rotate-x')
        pub.sendMessage("refresh-text")
        self.speed = 1

    def key_w(self):
        self.position[2] -= self.speed * math.cos(math.radians(self._y_rotation))
        self.position[0] += self.speed * math.sin(math.radians(self._y_rotation))
        self._moved = True
        
    def key_s(self):
        self.position[2] += self.speed * math.cos(math.radians(self._y_rotation))
        self.position[0] -= self.speed * math.sin(math.radians(self._y_rotation))
        self._moved = True
    
    def key_a(self):
        self.position[2] -= self.speed * math.cos(math.radians(self._y_rotation-90))
        self.position[0] += self.speed * math.sin(math.radians(self._y_rotation-90))
        self._moved = True
        
    def key_d(self):
        self.position[2] -= self.speed * math.cos(math.radians(self._y_rotation+90))
        self.position[0] += self.speed * math.sin(math.radians(self._y_rotation+90))
        self._moved = True
        
    def rotate_y(self, amount):
        self.y_rotation += amount
    
    def rotate_x(self, amount):
        self.x_rotation += amount
    
    def tick(self):
        print("a")
        if self.collisions:
            mypos = numpy.array(self.position)
            
            for other in self.collisions:
                otherpos = numpy.array(other.position)
                distance = numpy.linalg.norm(mypos - otherpos)
                direction_vector = (mypos - otherpos)/distance
                self.position = otherpos+(distance+0.1)*direction_vector

    def clicked(self, game_object):
        print("Player was clicked!!!!!!!!!!!!!!!!")
