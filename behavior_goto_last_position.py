import numpy
from pubsub import pub

from behavior import Behavior
from game_logic import GameLogic


# go to last position of destination object
class GotoLastPosition(Behavior):
    def __init__(self, destination, speed, distance, event=None):
        super(GotoLastPosition, self).__init__()
        self.destination = destination
        self.speed = speed
        self.distance = distance
        self.event = event
        self.sent_event = False
        self.last_position = self.get_destination()
        self.calculated = False

    def calculate_direction(self, destination):
        current = numpy.array(self.game_object.position)
        distance = numpy.linalg.norm(destination - current)
        direction_vector = (destination - current) / distance

        return direction_vector

    def get_destination(self):
        result = None
        if type(self.destination) == list:
            result = self.destination

        if type(self.destination) == str:
            obj = GameLogic.get_object(self.destination)
            if obj:
                # create copy, not reference
                result = obj.position[:]

        return result

    def tick(self):
        # only calculate direction_vector once, so projectile doesnt stop at object location
        if not self.calculated:
            self.direction_vector = self.calculate_direction(self.last_position)
            self.calculated = True

        current = numpy.array(self.game_object.position)

        self.game_object.position = (current+self.speed*self.direction_vector).tolist()
        self.game_object._moved = True
