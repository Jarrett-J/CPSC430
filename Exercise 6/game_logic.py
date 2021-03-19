from game_object_rotating import GameObjectRotating
from game_object import GameObject
from game_object_drive import GameObjectDrive
from game_object_ground import GameObjectGround
from game_object_move import GameObjectMove
from player import Player
from pubsub import pub
import numpy
import json
import importlib

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
    def load_world(self, filename):
        # send event to view to delete game objects
        self.game_objects = { }
        
        with open(filename) as infile:
            level_data = json.load(infile)
            
            if not 'objects' in level_data:
                return False
            
            for game_object in level_data['objects']:
                size = [1.0, 1.0, 1.0]
                if 'size' in game_object:
                    size = game_object['size']
                    
                obj = self.create_object(game_object['position'], size, game_object['kind'])
        
                if 'behaviors' not in game_object:
                    continue
                
                for behavior in game_object['behaviors']:
                    module = importlib.import_module(level_data['behaviors'][behavior])
                    class_ = getattr(module, behavior)
                    instance = class_(*game_object['behaviors'][behavior])
                    
                    obj.add_behavior(instance)


    def get_property(self, key, default=None):
        if key in self.properties:
            return self.properties[key]
        
        return default

    def set_property(self, key, value):
        self.properties[key] = value


