from behavior import Behavior


class EnemyMelee(Behavior):
    def __init__(self, damage):
        super(EnemyMelee, self).__init__()
        self.damage = damage
        self.max_cooldown = 50
        self.current_cooldown = 0


    def tick(self):
        if self.current_cooldown <= 0:
            if self.game_object.collisions:
                for other in self.game_object.collisions:
                    if other.kind == "player":
                        other.get_behavior("PlayerHealth").hit_player(self.damage)
                        self.current_cooldown = self.max_cooldown

        else:
            self.current_cooldown -= 1
