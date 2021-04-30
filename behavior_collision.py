from behavior import Behavior
import numpy


class BlockedByObjects(Behavior):
    def __init__(self, ignore_kind=None):
        super(BlockedByObjects, self).__init__()
        self.ignore = ignore_kind

        self.push_amount = .3

    def tick(self):
        if self.game_object.collisions:
            mypos = numpy.array(self.game_object.position)

            for other in self.game_object.collisions:
                if other.kind == self.ignore:
                    return

                otherpos = numpy.array(other.position)
                distance = numpy.linalg.norm(mypos - otherpos)

                if distance == 0:
                    return

                direction_vector = (mypos - otherpos) / distance

                max_direction = max(direction_vector, key=abs)
                indices = [i for i, j in enumerate(direction_vector) if j == max_direction]

                velocity = 0.0

                if not indices:
                    return

                for index in indices:

                    if index == 0:
                        velocity = max(velocity, self.game_object.get_property('x_velocity', self.push_amount))
                    if index == 1:
                        velocity = max(velocity, self.game_object.get_property('y_velocity', self.push_amount))
                    if index == 2:
                        velocity = max(velocity, self.game_object.get_property('z_velocity', self.push_amount))


                face = indices[0]
                thirdpos = numpy.array([0.0, 0.0, 0.0])
                thirdpos[0] = mypos[0] if face != 0 else otherpos[0]
                thirdpos[1] = mypos[1] if face != 1 else otherpos[1]
                thirdpos[2] = mypos[2] if face != 2 else otherpos[2]

                distance = numpy.linalg.norm(mypos - thirdpos)
                direction_vector = (mypos - thirdpos)/distance

                self.game_object.position = (thirdpos+(distance+velocity)*direction_vector).tolist()

"""
                print(self.game_object.kind)

                print("mypos: " + str(mypos))
                print("otherpos: " + str(otherpos))
                print("distance: " + str(distance))
                print("direction vector: " + str(direction_vector))
                print("position: " + str(otherpos + (distance + 0.2) * direction_vector) + "\n")
                """
