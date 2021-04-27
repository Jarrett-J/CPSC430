from behavior import Behavior
from game_logic import GameLogic
import numpy

class Platform(Behavior):
    def __init__(self, finish, speed, transport):
        super(Platform, self).__init__()

        self.start = None
        self.finish = numpy.array(finish)
        self.speed = speed
        self.transport = transport

    def connect(self, game_object):
        super(Platform, self).connect(game_object)

        self.start = numpy.array(game_object.position)
        self.distance = numpy.linalg.norm(self.finish - self.start)
        self.direction_vector = (self.finish - self.start) / self.distance

    def tick(self):
        current = numpy.array(self.game_object.position)
        distance = numpy.linalg.norm(self.start-current)

        riders = []

        if self.transport:
            self.game_object.position[1] += 0.1

            for other in GameLogic.game_objects:
                if not GameLogic.collide(self.game_object, GameLogic.game_objects[other]):
                    continue

                if GameLogic.game_objects[other] in self.game_object.collisions:
                    continue

                #todo recursively add riders that are stack on top of each other
                riders.append(GameLogic.game_objects[other])

            self.game_object.position[1] -= 0.1

        if distance >= self.distance:
            self.direction_vector = -(1/numpy.linalg.norm(self.direction_vector)) * self.direction_vector
            self.game_object.position = (self.finish).tolist()
            temp = self.start
            self.start = self.finish
            self.finish = temp
        else:
            self.game_object.position = (self.start + (distance+self.speed) * self.direction_vector).tolist()
            self.move_riders(riders, self.direction_vector, self.speed)

        self.game_object._moved = True

    def move_riders(self, riders, direction_vector, speed):
        for rider in riders:
            rider.position = (rider.position+direction_vector*speed).tolist()
