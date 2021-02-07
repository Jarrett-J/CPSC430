from OpenGL.GLU import *
from OpenGL.GL import *

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object
        self.load_texture()
        
    def load_texture(self):
        pass
        
    def display(self):
        glPushMatrix()
        
        #pos = self.game_object.position
        glTranslate(*self.game_object.position)
        glRotatef(self.game_object.x_rotation, 1, 0, 0)
        glRotatef(self.game_object.y_rotation, 0, 1, 0)
        glRotatef(self.game_object.z_rotation, 0, 0, 1)
        
        glPushName(self.game_object.id)
        self.draw()
        glPopName()
        
        glPopMatrix()
        
    def draw(self):
        pass