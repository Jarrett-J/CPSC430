from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic
from movies import Movies


class Movie(Behavior):
    def __init__(self, movie, playevent, pauseevent, stopevent, loop=None):
        super(Movie, self).__init__()
        self.loop = loop
        self.movie = movie

        pub.subscribe(self.play, playevent)
        pub.subscribe(self.pause, pauseevent)
        pub.subscribe(self.stop, stopevent)

    def play(self):
        print("play")
        Movies.play_movie(self.movie, self.loop)

    def pause(self):
        Movies.pause_movie(self.movie)

    def stop(self):
        Movies.stop_movie(self.movie)
        GameLogic.delete_object(self.game_object)
