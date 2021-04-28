from movies import Movies
from textures import Textures
from view_object import ViewObject
from OpenGL.GL import *


class ObjectWall(ViewObject):
    def get_color(self, face):
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'color':
                return self.game_object.faces[face]['value']

        # default color
        return [0.25, 0.25, 0.25, 1.0]

    def get_texture(self, face):
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'texture':
                Textures.activate_texture(self.game_object.faces[face]['value'])

            if self.game_object.faces[face]['type'] == 'movie':
                Movies.get_frame(self.game_object.faces[face]['value'])

    def draw(self):
        glColor3f(1, 1, 1)
        self.wall()

    def wall(self):
        scale = 1

        # Front face
        self.get_texture("front")
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, 0.5)
        
        glEnd()
        Textures.deactivate_texture()

        # Back face
        self.get_texture("back")
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 0.0, -1.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5, -0.5, -0.5)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, -0.5, -0.5)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, 0.5, -0.5)

        glEnd()
        Textures.deactivate_texture()

        # Left face
        self.get_texture("left")
        glBegin(GL_QUADS)

        glNormal3f(-1.0, 0.0, 0.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, -0.5)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)

        glEnd()
        Textures.deactivate_texture()

        # Right face
        self.get_texture("right")
        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, 0.5)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, -0.5, -0.5)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, 0.5, -0.5)

        glEnd()
        Textures.deactivate_texture()

        # Top face
        self.get_texture("top")
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 1.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()

        # Bottom face
        self.get_texture("bottom")
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)

        glTexCoord2f(1.0, 0.0)

        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
