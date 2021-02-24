from game_object_rotating import GameObjectRotating
from game_object import GameObject
from game_object_drive import GameObjectDrive
from game_object_ground import GameObjectGround
from game_object_move import GameObjectMove
from pubsub import pub


class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}
        self.next_id = 0

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, position, kind):
        obj = GameObject(position, kind, self.next_id)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        # send event
        pub.sendMessage('create', game_object=obj)
        return obj

    def remove_object(self, id):
        del self._game_objects[id]

    # Put game objects to spawn here
    def load_world(self):
        # self.create_driving_object([0, 0, -10], "vehicle")
        # self.create_object([0, 0, -5], "cube")
        self.test_create_object([0, 0, -10], "cube", GameObjectRotating)
        self.test_create_object([15, 0, -10], "move", GameObjectMove)

        self.test_create_object([-10, 0, -5], "vehicle", GameObjectDrive)

        # ground
        self.test_create_object([0, 0, 0], "ground", GameObjectGround)
        self.test_create_object([0, 0, -10], "ground", GameObjectGround)
        self.test_create_object([0, 0, 10], "ground", GameObjectGround)

        self.test_create_object([10, 0, 0], "ground", GameObjectGround)
        self.test_create_object([10, 0, -10], "ground", GameObjectGround)
        self.test_create_object([10, 0, 10], "ground", GameObjectGround)

        self.test_create_object([-10, 0, 0], "ground", GameObjectGround)
        self.test_create_object([-10, 0, -10], "ground", GameObjectGround)
        self.test_create_object([-10, 0, 10], "ground", GameObjectGround)

        self.test_create_object([-20, 0, 0], "ground", GameObjectGround)
        self.test_create_object([-20, 0, -10], "ground", GameObjectGround)
        self.test_create_object([-20, 0, 10], "ground", GameObjectGround)

        self.test_create_object([20, 0, 0], "ground", GameObjectGround)
        self.test_create_object([20, 0, -10], "ground", GameObjectGround)
        self.test_create_object([20, 0, 10], "ground", GameObjectGround)

        # ceiling
        self.test_create_object([0, 10, 0], "ground", GameObjectGround)
        self.test_create_object([0, 10, -10], "ground", GameObjectGround)
        self.test_create_object([0, 10, 10], "ground", GameObjectGround)

        self.test_create_object([10, 10, 0], "ground", GameObjectGround)
        self.test_create_object([10, 10, -10], "ground", GameObjectGround)
        self.test_create_object([10, 10, 10], "ground", GameObjectGround)

        self.test_create_object([-10, 10, 0], "ground", GameObjectGround)
        self.test_create_object([-10, 10, -10], "ground", GameObjectGround)
        self.test_create_object([-10, 10, 10], "ground", GameObjectGround)

        self.test_create_object([-20, 10, 0], "ground", GameObjectGround)
        self.test_create_object([-20, 10, -10], "ground", GameObjectGround)
        self.test_create_object([-20, 10, 10], "ground", GameObjectGround)

        self.test_create_object([20, 10, 0], "ground", GameObjectGround)
        self.test_create_object([20, 10, -10], "ground", GameObjectGround)
        self.test_create_object([20, 10, 10], "ground", GameObjectGround)

        # walls
        self.test_create_object([20, -1, 15], "wall", GameObjectGround)
        self.test_create_object([10, -1, 15], "wall", GameObjectGround)
        self.test_create_object([0, -1, 15], "wall", GameObjectGround)
        self.test_create_object([-10, -1, 15], "wall", GameObjectGround)
        self.test_create_object([-20, -1, 15], "wall", GameObjectGround)

        self.test_create_object([20, -1, -15], "wall", GameObjectGround)
        self.test_create_object([10, -1, -15], "wall", GameObjectGround)
        self.test_create_object([0, -1, -15], "wall", GameObjectGround)
        self.test_create_object([-10, -1, -15], "wall", GameObjectGround)
        self.test_create_object([-20, -1, -15], "wall", GameObjectGround)

        # side walls
        self.test_create_object([25, -1, 10], "sidewall", GameObjectGround)
        self.test_create_object([25, -1, 0], "sidewall", GameObjectGround)
        self.test_create_object([25, -1, -10], "sidewall", GameObjectGround)

        self.test_create_object([-25, -1, 10], "sidewall", GameObjectGround)
        self.test_create_object([-25, -1, 0], "sidewall", GameObjectGround)
        self.test_create_object([-25, -1, -10], "sidewall", GameObjectGround)

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value

    def test_create_object(self, position, kind, objectType):
        obj = objectType(position, kind, self.next_id)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        # send event
        pub.sendMessage('create', game_object=obj)
        return obj
