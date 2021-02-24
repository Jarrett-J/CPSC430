from game_object import GameObject

class GameObjectCounter(GameObject):
    def __init__(self, position, kind, id):
        super(GameObjectSpawner, self).__init__(position, kind, id)
        self.times_clicked = 0
        
    def tick(self):
        pass
            
    def clicked(self):
        self.times_clicked += 1    
