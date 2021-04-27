from behavior import Behavior
from pubsub import pub


class Jump(Behavior):
    def __init__(self, speed, adjust):
        super(Jump, self).__init__()

        self.jumping = False
        self.speed = speed
        self.adjust = adjust
        self.current = self.speed

        pub.subscribe(self.jump, 'key-jump')

    def jump(self):
        if not self.game_object.get_property('falling'):
            self.jumping = True

    def tick(self):
        if not self.jumping:
            return

        if self.current <= 0.0:
            self.jumping = False
            self.current = self.speed
            return

        self.game_object.set_property('y_velocity', self.game_object.get_property('y_velocity', 0.0) + self.current)
        self.game_object.position[1] += self.current
        self.game_object._moved = True
        self.current -= self.adjust
