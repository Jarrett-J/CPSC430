import numpy

from behavior import Behavior
from game_logic import GameLogic


class Spawn(Behavior):
    def __init__(self, max_cooldown, kind, size=None):
        super(Spawn, self).__init__()

        self.max_cooldown = max_cooldown
        self.current_cooldown = max_cooldown
        self.kind = kind
        self.size = size

    def get_projectile_type(self):
        if self.kind == "heatseeking":
            self.behaviors = {"EnemyHealth": [10], "Goto": ["player", 0.1, 0.1], "Projectile": [10, self.game_object], "Gravity": [0.1]}
        else:
            self.behaviors = {"EnemyHealth": [10], "GotoLastPosition": ["player", 0.1, 0.1], "Projectile": [10, self.game_object], "Gravity": [0.01]}

    def spawn(self):
        self.get_projectile_type()

        current = numpy.array(self.game_object.position)
        position = current.tolist()

        #         behaviors = {"EnemyHealth": [10], "Goto": ["player", 0.1, 0.1], "Projectile": [10, 'projectileEnemy']}
        #         data = {'kind': 'projectile', 'position': position, 'behaviors': behaviors}

        data = {'kind': self.kind, 'position': position, 'behaviors': self.behaviors}

        if self.size:
            data['size'] = self.size

        GameLogic.additions.append(data)

    def tick(self):
        if self.current_cooldown <= 0:
            self.spawn()

            self.current_cooldown = self.max_cooldown

        else:
            self.current_cooldown -= 1
