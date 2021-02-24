from game_object import GameObject
from player_view import PlayerView


class GameObjectCounter(GameObject, player_view):
    def __init__(self, position, kind, id):
        super(GameObjectCounter, self).__init__(position, kind, id)
        self.times_clicked = 0

    def tick(self):
        pass

    def clicked(self):
        self.times_clicked += 1
