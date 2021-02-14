from game_object_rotating import GameObjectRotating
from game_object import GameObject
from game_object_drive import GameObjectDrive
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
    
    def create_driving_object(self, position, kind):
        obj = GameObjectDrive(position, kind, self.next_id)
        self.next_id += 1
        self.game_objects[obj.id] = obj
        
        # send event
        pub.sendMessage('create', game_object=obj)
        return obj
    
    def remove_object(self, id):
        del self._game_objects[id]
        
    
    # Put game objects to spawn here
    def load_world(self):
        self.create_driving_object([0, 0, -10], "vehicle")
        #self.create_object([0, 0, -5], "cube")

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]
        
        return None
    
    def set_property(self, key, value):
        self.properties[key] = value
    
    