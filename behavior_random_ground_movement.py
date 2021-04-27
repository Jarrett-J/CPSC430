import random
from behavior import Behavior


class RandomGroundMovement(Behavior):
    def __init__(self, speed):
        super(RandomGroundMovement, self).__init__()
        self.can_move = True
        self.speed = speed

        # how long the npc moves
        self.current_move_time = 0
        self.max_move_time = 50

        # the cooldown in between movements
        self.current_move_cooldown = 100
        self.max_move_cooldown = 100

        # the amount moved
        self.x = self.speed
        self.y = 0
        self.z = self.speed

        # the direction moved
        self.x_direction = 0
        self.z_direction = 0

    def randomize_direction(self):
        self.x_direction = random.randint(-1, 1)
        self.z_direction = random.randint(-1, 1)

        # print("New x direction: " + str(self.x_direction))
        # print("New z direction: " + str(self.z_direction))

    def tick(self):
        if self.can_move:
            if self.current_move_cooldown <= 0:
                x_movement = self.x * self.x_direction
                z_movement = self.z * self.z_direction

                # move
                self.game_object.position[0] += x_movement
                self.game_object.position[2] += z_movement
                self.game_object._moved = True

                self.current_move_time -= 1

                if self.current_move_time <= 0:
                    # erratic, long movement
                    self.max_move_cooldown = random.randint(5, 10)
                    self.current_move_cooldown = self.max_move_cooldown
                    self.randomize_direction()

            else:
                self.game_object._moved = False
                self.current_move_time = self.max_move_time
                self.current_move_cooldown -= 1
                # print("cooling down: " + str (self.current_move_cooldown))