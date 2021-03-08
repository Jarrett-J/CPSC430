from view_object import ViewObject
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL.Image import open
import pygame
from localize import *

class ObjectVehicle(ViewObject):
    global car_texture
    global text_texture
    global text
    
    def load_texture(self):        
        # initialize as car
        self.game_object.kind = "car"
        
        self.load_text()
        self.texture_init()
        
    def texture_init(self):
        global car_texture
        metalImage = open("metal.jpg")
    
        ix = metalImage.size[0]
        iy = metalImage.size[1]
        metalImage = metalImage.tobytes("raw", "RGB", 0, -1)
        
        car_texture = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, car_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, metalImage)
        
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
        
    def update_text(self):
        self.load_text()
        
    def load_text(self):
        global text_texture
        
        img = pygame.font.SysFont('Arial', 50).render(language(self.game_object.text), True, (255, 255, 255), (0, 0, 0, 0))
        w, h = img.get_size()
        text_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, text_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        
    def draw(self):
        self.load_text()
        if self.game_object.kind == "car":
            self.drawCar()
            
        elif self.game_object.kind == "truck":
            self.drawTruck()
        
    def drawCar(self):
        global text_texture
        global car_texture
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, car_texture)
        offset_X = -3
        offset_Z = -3
        
        #carSpeed = 0.005
        #glTranslate(self.x_translation, 0.0, 0.0)
        
        # push before you draw, pop after you draw

        glPushMatrix()
        
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(-1.0 + offset_X, 0.5, 0.0 + offset_Z)
        
        self.carWindow()
        
        glPopMatrix()
        glPushMatrix()
        
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(-1.0 + offset_X, -.5, 0.0 + offset_Z)
        self.carBase()
        
        glPopMatrix()
        glPushMatrix()
        
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(0.0 + offset_X, 1.0, 0.0 + offset_Z)
        
        glBindTexture(GL_TEXTURE_2D, text_texture)
        self.carTop()
        
        
        glPopMatrix()
        glPushMatrix()
        
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(1.0 + offset_X, 0.5, 0.0 + offset_Z)
        glBindTexture(GL_TEXTURE_2D, car_texture)
        self.carBack()

        glPopMatrix()
        glPushMatrix()
        #left wheel
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(-1.5 + offset_X, -0.5, 0.1 + offset_Z)
        glRotatef(self.game_object.tire_rotation,0,0,1)
        
        self.carWheelBase()
        self.carWheelSides()
        
        glPopMatrix()
        glPushMatrix()
        
        #right wheel
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(1.0 + offset_X, -0.5, 0.1 + offset_Z)
        glRotatef(self.game_object.tire_rotation,0,0,1)
        
        self.carWheelBase()
        self.carWheelSides()

        glPopMatrix()
        glPushMatrix()    
        
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(-2.85 + offset_X, 0.2, 0.0 + offset_Z)
        
        self.headlight()
        
        glPopMatrix()
        glPushMatrix()
        
        glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
        glTranslate(2.25 + offset_X, 0.2, 0.0 + offset_Z)
        self.tailLight()
        
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        
    def drawTruck(self):
        global text_texture
        global car_texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, car_texture)
        offset_Z = -5
        offset_Y = 0.7
        
        #glTranslate(truck_x_translation, 0.0, 0.0)
        
        glPushMatrix()
        glTranslate(-2.2, -1.0 + offset_Y, 0.0 + offset_Z)
        glRotatef(self.game_object.tire_rotation,0,0,1)
        self.truckWheelSides()
        self.truckWheelBase()
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(1.2, -1.0 + offset_Y, 0.0 + offset_Z)
        glRotatef(self.game_object.tire_rotation,0,0,1)
        self.truckWheelSides()
        self.truckWheelBase()
        glPopMatrix()
        
        
        glPushMatrix()
        glTranslate(0, 0.0 + offset_Y, 0.0 + offset_Z)
        
        glBindTexture(GL_TEXTURE_2D, text_texture)
        self.truckBase()
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(-2.0, -0.25 + offset_Y, 0.0 + offset_Z)
        glBindTexture(GL_TEXTURE_2D, car_texture)
        self.truckFront()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        
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
    
    def truckWheelBase(self):
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
    
    def truckWheelSides(self):
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
        
        
    def carWindow(self):
        glBegin(GL_TRIANGLES)
        #glColor(0.0, 1.0, 1.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        #bottom
        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.0, 0.0, 0.0)
        
        #middle (right angle)
        glTexCoord2f(1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.0, 1.0, 0.0)
        
        #
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-1.0, 0.0, 0.0)
        
        glEnd()        
        
    def carWheelBase(self):
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
    
    def carWheelSides(self):
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
        
    def carBase(self):

        glBegin(GL_QUADS)
        
        #glColor(1.0, 0.0, 1.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        #bottom left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2.0, 0.0, 0.0)
        
        #top left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2.0, 1.0, 0.0)
        
        #top right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(3.5, 1.0, 0.0)
        
        #bottom right
        glTexCoord2f(1.0, 0.0)
        glVertex3d(3.5, 0.0, 0.0)
        
        glEnd()
        
        
    def carTop(self):

        glBegin(GL_QUADS)
        
        #glColor(1.0, 0.0, 1.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        #bottom left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-1.0, -0.5, 0.0)
        
        #top left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-1.0, 0.5, 0.0)
        
        #top right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(1.0, 0.5, 0.0)
        
        #bottom right
        glTexCoord2f(1.0, 0.0)
        glVertex3d(1.0, -0.5, 0.0)
            
        glEnd()

        
    def headlight(self):
        glBegin(GL_QUADS)
        
        #glColor(1.0, 1.0, 0.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        #bottom left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.25, 0.0, 0.0)
        
        #top left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.25, 0.25, 0.0)
        
        #top right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.35, 0.25, 0.0)
        
        #bottom right
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.35, 0.0, 0.0)
        
        glEnd()
        
        
    def tailLight(self):
        glBegin(GL_QUADS)
        
        #glColor(1.0, 0.0, 0.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        #bottom left
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.25, 0.0, 0.0)
        
        #top left
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.25, 0.25, 0.0)
        
        #top right
        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.35, 0.25, 0.0)
        
        #bottom right
        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.35, 0.0, 0.0)
        
        glEnd()
         
    def carBack(self):
        glBegin(GL_TRIANGLES)
        #glColor(1.0, 0.0, 1.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        
        #right angle
        glTexCoord2f(0.0, 0.0)
        
        glVertex3d(0.0, 0.0, 0.0)
        
        glTexCoord2f(1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.0, 1.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(1.0, 0.0, 0.0)
        
        glEnd()
