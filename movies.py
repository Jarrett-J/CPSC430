from PIL import Image

from game_logic import GameLogic
import cv2
from OpenGL.GL import *


class Movies:
    movies = {}

    @staticmethod
    def get_frame(tag):
        if tag not in Movies.movies:
            return None

        """
        if tag not in Movies.movies:
            Movies.play_movie(tag)

            if tag not in Movies.movies:
                return None
        """
        if Movies.movies[tag]['texture']:
            glBindTexture(GL_TEXTURE_2D, Movies.movies[tag]['texture'])
            glEnable(GL_TEXTURE_2D)

    @staticmethod
    def play_movie(tag, loop=False):
        # print("playing movie")
        if tag in Movies.movies:
            Movies.movies[tag]['paused'] = False
        else:
            if tag not in GameLogic.files:
                return

            capture = cv2.VideoCapture()
            capture.open(GameLogic.files[tag])

            Movies.movies[tag] = {'capture': capture, 'paused': False, 'texture': None, 'loop': loop}

    @staticmethod
    def pause_movie(tag):
        if tag in Movies.movies:
            Movies.movies[tag]['paused'] = True

    @staticmethod
    def stop_movie(tag):
        if tag in Movies.movies:
            if Movies.movies[tag]['texture']:
                delete = [Movies.movies[tag]['texture']]
                glDeleteTextures(delete)

            Movies.movies[tag]['capture'].release()

            print("deleting movie" + str(Movies.movies[tag]))
            del Movies.movies[tag]

    @staticmethod
    def tick():
        to_delete = []

        for tag in Movies.movies:
            if Movies.movies[tag]['paused']:
                continue

            success, frame = Movies.movies[tag]['capture'].read()

            if not success and not Movies.movies[tag]['loop']:
                to_delete.append(tag)
                continue

            if not success:
                Movies.movies[tag]['capture'].set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = Movies.movies[tag]['capture'].read()

                if not success:
                    to_delete.append(tag)
                    continue
            frame = Image.fromarray(frame)
            ix = frame.size[0]
            iy = frame.size[1]
            frame = frame.tobytes("raw", "RGB", 0, -1)
           # print("still playing movie")
            #texture_id = glGenTextures(1)

            if Movies.movies[tag]['texture']:
                texture_id = Movies.movies[tag]['texture']
            else:
                texture_id = glGenTextures(1)
                Movies.movies[tag]['texture'] = texture_id

            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)

        for deletion in to_delete:
            Movies.stop_movie(deletion)
