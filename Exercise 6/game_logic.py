from game_object_rotating import GameObjectRotating
from game_object import GameObject
from game_object_drive import GameObjectDrive
from game_object_ground import GameObjectGround
from game_object_move import GameObjectMove
from player import Player
from behavior_x_rotation import XRotation
from behavior_y_rotation import YRotation
from behavior_z_rotation import ZRotation
from behavior_key_move import KeyMove
from behavior_mouse_rotation import MouseRotation
from behavior_collision import BlockedByObjects
from behavior_move_on_click import MoveOnClick
from behavior_enemy_health import EnemyHealth
from behavior_jump import CanJump
from behavior_rotate_on_click import RotateOnClick
from pubsub import pub
import numpy

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        self.next_id = 0

    def tick(self):
        for game_object in self.game_objects:
            if self.game_objects[game_object].moved:
                for other in self.game_objects:
                    if self.game_objects[game_object] == self.game_objects[other]:
                        continue
                    
                    if self.collide(self.game_objects[game_object], self.game_objects[other]):
                        self.game_objects[game_object].collisions.append(self.game_objects[other])
        
        for id in self.game_objects:
            self.game_objects[id].tick()

    def collide(self, object1, object2):
        radius1 = max(object1.size)
        
        mypos = numpy.array(object1.position)
        otherpos = numpy.array(object2.position)
        
        distance = numpy.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos)/distance
        
        max_direction = max(direction_vector, key=abs)
        
        indices = [i for i, j in enumerate(direction_vector) if j == max_direction]
        sizes = [object2.size[j] for i, j in enumerate(indices)]
        radius2 = max(sizes)

        return distance < radius1+radius2
    
    def create_object(self, position, size, kind):
        obj = GameObject(position, size, kind, self.next_id)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        # send event
        pub.sendMessage('create', game_object=obj)
        return obj
    
    def remove_object(self, id):
        del self._game_objects[id]

    # Put game objects to spawn here
    def load_world(self):
        player = self.create_object([0, 0, 0], [1, 1, 1], "player")
        cube = self.create_object([-2, 0, -10], [1, 1, 1], "cube")
        moveCube = self.create_object([2, 0, -10], [1, 1, 1,], "move")
        enemyCube = self.create_object([5, 0, -10], [1, 1, 1,], "cube")
        
        enemyCube.add_behavior(EnemyHealth(20))
        player.add_behavior(KeyMove(0.1))
        player.add_behavior(MouseRotation(0.1))
        player.add_behavior(BlockedByObjects())
        player.add_behavior(CanJump(0.2))
        cube.add_behavior(ZRotation(0.5))
        cube.add_behavior(RotateOnClick())
        moveCube.add_behavior(MoveOnClick([0, .1, 0]))
        
        #self.create_object([-10, 0, -5], [1.0, 1.0, 1.0], "vehicle", GameObjectDrive)

        # ground
        self.create_object([0, 0, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([0, 0, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([0, 0, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([10, 0, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([10, 0, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([10, 0, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([-10, 0, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([-10, 0, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([-10, 0, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([-20, 0, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([-20, 0, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([-20, 0, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([20, 0, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([20, 0, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([20, 0, 10], [1.0, 1.0, 1.0], "ground")

        # ceiling
        self.create_object([0, 10, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([0, 10, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([0, 10, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([10, 10, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([10, 10, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([10, 10, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([-10, 10, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([-10, 10, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([-10, 10, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([-20, 10, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([-20, 10, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([-20, 10, 10], [1.0, 1.0, 1.0], "ground")

        self.create_object([20, 10, 0], [1.0, 1.0, 1.0], "ground")
        self.create_object([20, 10, -10], [1.0, 1.0, 1.0], "ground")
        self.create_object([20, 10, 10], [1.0, 1.0, 1.0], "ground")

        x = 5
        y = 5
        z = 5
        
        
        # walls
        
        self.create_object([20, -1, 15], [x, y, z], "wall")
        self.create_object([10, -1, 15], [x, y, z], "wall")
        self.create_object([0, -1, 15], [x, y, z], "wall")
        self.create_object([-10, -1, 15], [x, y, z], "wall")
        self.create_object([-20, -1, 15], [x, y, z], "wall")
        
        
        self.create_object([20, -1, -15], [x, y, z], "wall")
        self.create_object([10, -1, -15], [x, y, z], "wall")
        self.create_object([0, -1, -15], [x, y, z], "wall")
        self.create_object([-10, -1, -15], [x, y, z], "wall")
        self.create_object([-20, -1, -15], [x, y, z], "wall")
        
        
        # side walls
        self.create_object([25, -1, 10], [1.0, 1.0, 1.0], "sidewall")
        self.create_object([25, -1, 0], [1.0, 1.0, 1.0], "sidewall")
        self.create_object([25, -1, -10], [1.0, 1.0, 1.0], "sidewall")

        self.create_object([-25, -1, 10], [1.0, 1.0, 1.0], "sidewall")
        self.create_object([-25, -1, 0], [1.0, 1.0, 1.0], "sidewall")
        self.create_object([-25, -1, -10], [1.0, 1.0, 1.0], "sidewall")
        
        
    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value


