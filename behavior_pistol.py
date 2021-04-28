from behavior import Behavior
from sounds import Sounds


class Pistol(Behavior):
    def __init__(self, shoot_sound=None, empty_sound=None):
        super(Pistol, self).__init__()
        self.ammo_count = 5
        self.shoot_sound = shoot_sound
        self.empty_sound = empty_sound
        self.max_cooldown = 15
        self.current_cooldown = 0
        self.reloading = False

    def shoot(self):
        if self.reloading:
            return False

        if self.ammo_count <= 0:
            Sounds.play_sound(self.empty_sound)
            # we set a cooldown so the sound isnt spammed
            self.reloading = True
            self.current_cooldown = 8
            return False

        self.reloading = True
        self.current_cooldown = self.max_cooldown
        self.ammo_count -= 1

        if self.shoot_sound:
            Sounds.play_sound(self.shoot_sound)

        return True

    def tick(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
        else:
            self.reloading = False

    def has_ammo(self):
        return self.ammo_count
