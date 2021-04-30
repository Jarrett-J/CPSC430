from behavior import Behavior


class Shoot(Behavior):
    def __init__(self):
        super(Shoot, self).__init__()
        self.damage = 10
