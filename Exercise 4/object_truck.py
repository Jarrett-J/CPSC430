from view_object import ViewObject
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL.Image import open

class ObjectTruck(ViewObject):
    
    def load_texture(self):
        print("loading truck texture")
        metalImage = open("metal.jpg")
    
        ix = metalImage.size[0]
        iy = metalImage.size[1]
        metalImage = metalImage.tobytes("raw", "RGB", 0, -1)
        
        carTexture = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, carTexture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, metalImage)
        
        glEnable(GL_TEXTURE_2D);
        
        
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
    
    def draw(self):
        offset_Z = 0
        offset_Y = 0
        
        #glTranslate(truck_x_translation, 0.0, 0.0)
        
        glPushMatrix()
        glTranslate(-2.2, -1.0 + offset_Y, 0.0 + offset_Z)
        #glRotatef(rotation,0,0,1)
        #rotation += truck_rotation_amt
        self.wheelSides()
        self.wheelBase()
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(1.2, -1.0 + offset_Y, 0.0 + offset_Z)
        #glRotatef(rotation,0,0,1)
        #rotation += truck_rotation_amt
        self.wheelSides()
        self.wheelBase()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslate(0, 0.0 + offset_Y, 0.0 + offset_Z)
        self.truckBase()
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(-2.0, -0.25 + offset_Y, 0.0 + offset_Z)
        self.truckFront()
        glPopMatrix()
    
    def truckBase(self):
        glBegin(GL_QUADS)
        
        glNormal3f(0.0, 0.0, -1.0)
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, -1.0, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, 1.0, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3d(2.0, 1.0, 0.0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3d(2.0, -1.0, 0.0)
        

        glEnd()
    
    
    def truckFront(self):
        glBegin(GL_QUADS)
        
        glNormal3f(0.0, 0.0, -1.0)
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-1.0, -0.75, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-1.0, 0.75, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3d(1.0, 0.75, 0.0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3d(1.0, -0.75, 0.0)
        
        
        glEnd()
    
    def wheelBase(self):
        glBegin(GL_QUADS)
        # Front face
        #glColor(0.0, 0.0, 0.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.25, 0.25, 0.0)
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.25, -0.25, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.25, -0.25, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.25, 0.25, 0.0)
        
        glEnd()
    
    def wheelSides(self):
        glBegin(GL_TRIANGLES)
        #glColor(0.0, 0.0, 0.0, 1.0)
        
        #left of wheel
        
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.25, -0.25, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.375, 0.0, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.25, 0.25, 0.0)
        
        #right of wheel
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.25, -0.25, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.375, 0.0, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.25, 0.25, 0.0)
        
        #top of wheel
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.25, 0.25, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.0, 0.375, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.25, 0.25, 0.0)
        
        #bottom of wheel
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.25, -0.25, 0.0)
        
        glTexCoord2f(1.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.0, -0.375, 0.0)
        
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.25, -0.25, 0.0)
        
        glEnd()