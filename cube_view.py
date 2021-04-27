from textures import Textures
from view_object import ViewObject
from OpenGL.GL import *


class CubeView(ViewObject):
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

    def draw(self):
        glColor3f(1, 1, 1)
        self.get_texture("back")
        glBegin(GL_QUADS)

        # Front face
        glColor(*self.get_color("back"))
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

        self.get_texture('left')
        glBegin(GL_QUADS)
        # Left face
        glColor(*self.get_color("left"))
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()

        self.get_texture('back')
        glBegin(GL_QUADS)
        
        # Back face
        glColor(*self.get_color("front"))
        glNormal3f(0.0, 0.0, -1.0)
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

        self.get_texture("right")
        glBegin(GL_QUADS)

        # Right face
        glColor(*self.get_color("right"))
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()

        self.get_texture("top")
        glBegin(GL_QUADS)

        # Top face
        glColor(*self.get_color("top"))
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()

        self.get_texture("bottom")
        glBegin(GL_QUADS)

        # Bottom face
        glColor(*self.get_color("bottom"))
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        Textures.deactivate_texture()
