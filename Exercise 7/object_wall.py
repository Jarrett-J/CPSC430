from view_object import ViewObject
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL.Image import open

class ObjectWall(ViewObject):
    global texture
    
    def load_texture(self):
        global texture
        
        image = open("wall.jpg")
    
        ix = image.size[0]
        iy = image.size[1]
        image = image.tobytes("raw", "RGB", 0, -1)
        
        texture = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
        
        glEnable(GL_TEXTURE_2D);
        
        """
        light_ambient = [0.5, 0.5, 0.5, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_position = [0.0, 1.0, 1.0, 1.0]
        
        glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT1, GL_POSITION, light_position)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT1)
        
        glEnable(GL_COLOR_MATERIAL);
        
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        """
        
    def draw(self):
        global texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        
        glPushMatrix()
        glColor3f(1, 1, 1)
        self.wall()
        glPopMatrix()
        
    def wall(self):
        scale = 1
        glBegin(GL_QUADS)
        
        # front
        glNormal3f(0.0, 0.0, 1.0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-1.0 * scale, 1.0 * scale, 1 * scale)
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-1.0 * scale, -1.0 * scale, 1 * scale)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(1.0 * scale, -1.0 * scale, 1 * scale)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3d(1.0 * scale, 1.0 * scale, 1 * scale)
        
        glEnd()
        
        # Left face
        glBegin(GL_QUADS)
        glNormal3f( -1.0, 0.0, 0.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        glEnd()
        
        # Back face
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 0.0, -1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(1.0, -1.0, -1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(1.0, 1.0, -1.0)
        glEnd()
        
        # Right face
        glBegin(GL_QUADS)
        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3d(1.0, 1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(1.0, 1.0, -1.0)
        glEnd()
        
        # Top face
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(1.0, 1.0, 1.0)
        glVertex3d(1.0, 1.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        glEnd()
        
        # Bottom face
        glBegin(GL_QUADS)
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glEnd()
        glDisable(GL_TEXTURE_2D)