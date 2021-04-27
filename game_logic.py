from game_object import GameObject
from pubsub import pub
import json
import importlib


class GameLogic:
    properties = {}
    game_objects = {}
    name_index = {}
    files = {}
    level_data = {}
    filename = None

    deletions = []
    additions = []
    next_id = 0

    @staticmethod
    def tick():
        for game_object in GameLogic.game_objects:
            if GameLogic.game_objects[game_object].moved:
                for other in GameLogic.game_objects:
                    if GameLogic.collide(GameLogic.game_objects[game_object], GameLogic.game_objects[other]):
                        GameLogic.game_objects[game_object].collisions.append(GameLogic.game_objects[other])

        for id in GameLogic.game_objects:
            if GameLogic.loading_level:
                GameLogic.loading_level = False
                break

            GameLogic.game_objects[id].tick()

        GameLogic.process_deletions()
        GameLogic.process_additions()

    @staticmethod
    def collide(object1, object2):
        if object1 == object2:
            return False

        minx1 = object1.position[0] - object1.size[0]/2
        maxx1 = object1.position[0] + object1.size[0]/2
        miny1 = object1.position[1] - object1.size[1]/2
        maxy1 = object1.position[1] + object1.size[1]/2
        minz1 = object1.position[2] - object1.size[2]/2
        maxz1 = object1.position[2] + object1.size[2]/2

        minx2 = object2.position[0] - object2.size[0]/2
        maxx2 = object2.position[0] + object2.size[0]/2
        miny2 = object2.position[1] - object2.size[1]/2
        maxy2 = object2.position[1] + object2.size[1]/2
        minz2 = object2.position[2] - object2.size[2]/2
        maxz2 = object2.position[2] + object2.size[2]/2

        return minx1 < maxx2 and minx2 < maxx1 and miny1 < maxy2 and miny2 < maxy1 and minz1 < maxz2 and minz2 < maxz1

    @staticmethod
    def delete_object(obj):
        GameLogic.deletions.append(obj)

    @staticmethod
    def process_deletions():
        for obj in GameLogic.deletions:
            if obj.name:
                del GameLogic.name_index[obj.name]

            try:
                del GameLogic.game_objects[obj.id]
            except KeyError:
                print("KeyError in process_deletions()")
                pass

            pub.sendMessage('delete', game_object=obj)

        GameLogic.deletions = []

    @staticmethod
    def process_additions():
        for obj in GameLogic.additions:
            print("adding object: " + str(obj))
            GameLogic.create_object(obj)

        GameLogic.additions = []

    @staticmethod
    def get_object(id):
        result = None
        if id in GameLogic.name_index:
            result = GameLogic.name_index[id]

        if id in GameLogic.game_objects:
            result = GameLogic.game_objects[id]

        return result

    @staticmethod
    def load_world(filename):
        GameLogic.loading_level = True
        pub.sendMessage('clear_view_objects')

        GameLogic.game_objects = { }
        GameLogic.filename = filename

        with open(filename) as infile:
            level_data = json.load(infile)
            GameLogic.level_data = level_data
            
            if not 'objects' in level_data:
                return False
            
            for game_object in level_data['objects']:
                if 'size' not in game_object:
                    game_object['size'] = [1.0, 1.0, 1.0]

                if 'name' not in game_object:
                    game_object['name'] = None
                    
                obj = GameLogic.create_object(game_object)
        
                if 'behaviors' not in game_object:
                    continue
                
                for behavior in game_object['behaviors']:
                    module = importlib.import_module(level_data['behaviors'][behavior])
                    class_ = getattr(module, behavior)
                    instance = class_(*game_object['behaviors'][behavior])
                    instance.arguments = game_object['behaviors'][behavior]

                    obj.add_behavior(instance)

            for file in level_data['files']:
                GameLogic.files[file] = level_data['files'][file]

            if 'level' in level_data:
                if 'music' in level_data['level']:
                    from sounds import Sounds
                    Sounds.play_music(level_data['level']['music'])

    @staticmethod
    def create_object(data):
        obj = GameObject(GameLogic.next_id, data)
        GameLogic.next_id += 1
        GameLogic.game_objects[obj.id] = obj

        if 'name' in data:
            GameLogic.name_index[data['name']] = obj

        for behavior in data['behaviors']:
            module = importlib.import_module(GameLogic.level_data['behaviors'][behavior])
            class_ = getattr(module, behavior)
            instance = class_(*data['behaviors'][behavior])
            instance.arguments = data['behaviors'][behavior]

            obj.add_behavior(instance)

        # send event
        pub.sendMessage('create', game_object=obj)
        return obj

    @staticmethod
    def get_property(key, default=None):
        if key in GameLogic.properties:
            return GameLogic.properties[key]
        
        return default

    @staticmethod
    def set_property(key, value):
        GameLogic.properties[key] = value

    @staticmethod
    def save_world():
        print("Saving world")

        if 'objects' in GameLogic.level_data:
            del GameLogic.level_data['objects']

        GameLogic.level_data['objects'] = []

        for game_object in GameLogic.game_objects:
            GameLogic.save_object(GameLogic.game_objects[game_object])

        with open(GameLogic.filename, 'w') as outfile:
            outfile.write(GameLogic.jsonprint(GameLogic.level_data))

    @staticmethod
    def save_object(game_object):
        data = {}

        data['kind'] = game_object.kind
        data['position'] = game_object.position
        data['size'] = game_object.size

        if game_object.faces:
            data['faces'] = game_object.faces

        if game_object.name:
            data['name'] = game_object.name

        data['behaviors'] = {}

        for behavior in game_object.behaviors:
            data['behaviors'][behavior] = game_object.behaviors[behavior].arguments

        GameLogic.level_data['objects'].append(data)

    @staticmethod
    def replace(data):
        import uuid

        replacements = []
        objects = []

        for obj in data['objects']:
            replacement = uuid.uuid4().hex
            replacements.append((f'"{replacement}"', json.dumps(obj)))

            objects.append(f'{replacement}')

        data['objects'] = objects

        return data, replacements

    @staticmethod
    def jsonprint(data):
        import copy

        data = copy.deepcopy(data)

        data, replacements = GameLogic.replace(data)
        result = json.dumps(data, indent=4)

        for old, new in replacements:
            result = result.replace(old, new)

        return result