from textures import Textures
from view_object import ViewObject
from OpenGL.GL import *


class ObjectGround(ViewObject):

    def draw(self):

        self.ground()

    def get_texture(self, face):
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'texture':
                Textures.activate_texture(self.game_object.faces[face]['value'])

    def ground(self):
        self.get_texture("front")
        glBegin(GL_QUADS)
        
        # front

        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, 0.5)
        glEnd()
        Textures.deactivate_texture()

        # Left face
        self.get_texture("left")
        glBegin(GL_QUADS)
        glNormal3f(-1.0, 0.0, 0.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5, 0.5, -0.5)
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

        # Right face
        self.get_texture("right")
        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
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
        glDisable(GL_TEXTURE_2D)
        Textures.deactivate_texture()
