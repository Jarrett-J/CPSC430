from behavior import Behavior
from sounds import Sounds


class Melee(Behavior):
    def __init__(self, shoot_sound=None):
        super(Melee, self).__init__()
        self.shoot_sound = shoot_sound
        self.max_cooldown = 20
        self.current_cooldown = 0
        self.reloading = False

    def melee(self):
        if self.reloading:
            return False

        self.reloading = True
        self.current_cooldown = self.max_cooldown

        if self.shoot_sound:
            Sounds.play_sound(self.shoot_sound)

        return True

    def tick(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
        else:
            self.reloading = False
