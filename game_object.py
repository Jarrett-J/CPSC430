from pubsub import pub


class GameObject:
    def __init__(self, id, data):
        self.properties = {}

        self.position = data['position']
        self.kind = data['kind']

        if 'size' not in data:
            self.size = [1.0, 1.0, 1.0]
        else:
            self.size = data['size']

        if 'name' not in data:
            self._name = None
        else:
            self._name = data['name']

        if 'faces' in data:
            self.faces = data['faces']
        else:
            self.faces = {}

        self.id = id

        self._x_rotation = 0
        self._y_rotation = 0
        self._z_rotation = 0
        
        self.behaviors = {}
        
        self.collisions = []
        self._moved = False

        pub.subscribe(self.clicked, "clicked-"+str(id))

       # if 'name' in data:
        if 'name' in data and self._name is not None:
            print(str(type) + "subscribed to clicked-" + str(data['name']))
            pub.subscribe(self.clicked, "clicked-"+data['name'])

    @property
    def name(self):
        return self._name

    @property
    def moved(self):
        return self._moved
    
    # string
    @property
    def kind(self):
        return self._kind
    
    @kind.setter
    def kind(self, value):
        self._kind = value
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value
        
    # int
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
        
    #x, y, z
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
        
    @property
    def x_rotation(self):
        return self._x_rotation
    
    @x_rotation.setter
    def x_rotation(self, value):
        self._x_rotation = value
        
    @property
    def y_rotation(self):
        return self._y_rotation
    
    @y_rotation.setter
    def y_rotation(self, value):
        self._y_rotation = value
        
    @property
    def z_rotation(self):
        return self._z_rotation
    
    @z_rotation.setter
    def z_rotation(self, value):
        self._z_rotation = value
        
    def add_behavior(self, behavior):
        self.behaviors[behavior.__class__.__name__] = behavior
        behavior.connect(self)
    
    def tick(self):
        from game_logic import GameLogic
        
        if GameLogic.get_property('paused'):
            return

        self._moved = False

        for behavior in self.behaviors:
            self.behaviors[behavior].tick()

        self.collisions = []
        
    def get_property(self, key, default=None):
        if key in self.properties:
            return self.properties[key]
        
        return default
    
    def set_property(self, key, value):
        self.properties[key] = value
            
    def clicked(self, game_object):
        for behavior in self.behaviors:
            self.behaviors[behavior].clicked(game_object)

    def get_behavior(self, key, default=None):
        if key in self.behaviors:
            return self.behaviors[key]

        return default
