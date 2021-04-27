import numpy
from pubsub import pub

from behavior import Behavior
from game_logic import GameLogic


class Goto(Behavior):
    def __init__(self, destination, speed, distance, event=None):
        super(Goto, self).__init__()
        self.destination = destination
        self.speed = speed
        self.distance = distance
        self.event = event
        self.sent_event = False

    def get_destination(self):
        result = None
        if type(self.destination) == list:
            result = self.destination

        if type(self.destination) == str:
            obj = GameLogic.get_object(self.destination)
            if obj:
                result = obj.position

        return result

    def tick(self):
        destination = self.get_destination()
        if not destination:
            return

        destination = numpy.array(destination)
        current = numpy.array(self.game_object.position)
        distance = numpy.linalg.norm(destination-current)

        if distance <= self.distance:
            if self.event and not self.sent_event:
                pub.sendMessage(self.event, game_object=self.game_object)
                self.sent_event = True

            return

        self.sent_event = False
        direction_vector = (destination-current)/distance
        self.game_object.position = (current+self.speed*direction_vector).tolist()
        self.game_object._moved = True
