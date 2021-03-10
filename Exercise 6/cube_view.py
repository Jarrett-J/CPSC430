from view_object import ViewObject
from OpenGL.GLU import *
from OpenGL.GL import *
import pygame

class CubeView(ViewObject):
    global front_texture
    global back_texture
        
    def load_texture(self):
        global front_texture
        global back_texture
        
        # front
        img = pygame.font.SysFont('Arial', 50).render("Click me", True, (255, 255, 255), (0, 0, 0, 0))
        w, h = img.get_size()
        front_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, front_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        
        # back
        img = pygame.font.SysFont('Arial', 50).render("Click me", True, (255, 255, 255), (0, 0, 0, 0))
        w, h = img.get_size()
        back_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, back_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, front_texture)
        glPushMatrix()
        glBegin(GL_QUADS)
        
        # Front face
        glNormal3f( 0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5, 0.5, 0.5)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glBegin(GL_QUADS)
        # Left face
        glNormal3f( -1.0, 0.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, back_texture)
        glBegin(GL_QUADS)
        
        # Back face
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
        glDisable(GL_TEXTURE_2D)
        
        glBegin(GL_QUADS)
        # Right face
        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glEnd()
        
        glBegin(GL_QUADS)
        # Top face
        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        
        
        glBegin(GL_QUADS)
        # Bottom face
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)


