import pygame
from pygame.locals import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PIL.Image import open

rotation = 0.0
rotationAmt = 0.0
truck_rotation_amt = 0.0
x_translation = 0.0
truck_x_translation = 0.0

def main():
    global x_translation
    global truck_x_translation
    global rotationAmt
    global truck_rotation_amt

    pygame.init()
    windowSize = (800,600)
    pygame.display.set_mode(windowSize, DOUBLEBUF|OPENGL)
    
    gluPerspective(60, (windowSize[0]/windowSize[1]), 0.1, 100.0)

    glTranslatef(0.0, 0.0, -5)

    init ()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and x_translation <= 0:
                    print("left key up")
                    x_translation += 0.03
                    rotationAmt -= 1.5
                    
                if event.key == pygame.K_RIGHT and x_translation >= 0:
                    print("right key up")
                    x_translation -= 0.03
                    rotationAmt += 1.5
                
                    
            keys = pygame.key.get_pressed()
            

            if keys[K_LEFT] and x_translation >= 0:
                print("left key down")
                x_translation -= 0.03
                rotationAmt += 1.5
                
            elif keys[K_RIGHT] and x_translation <= 0:
                print("right key down")
                x_translation += 0.03
                rotationAmt -= 1.5
                
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and truck_x_translation <= 0:
                    print("left key up")
                    truck_x_translation += 0.03
                    truck_rotation_amt -= 1.5
                    
                if event.key == pygame.K_d and truck_x_translation >= 0:
                    print("right key up")
                    truck_x_translation -= 0.03
                    truck_rotation_amt += 1.5
                
                    
            keys = pygame.key.get_pressed()
            

            if keys[K_a] and truck_x_translation >= 0:
                print("left key down")
                truck_x_translation -= 0.03
                truck_rotation_amt += 1.5
                
            elif keys[K_d] and truck_x_translation <= 0:
                print("right key down")
                truck_x_translation += 0.03
                truck_rotation_amt -= 1.5
                
                    
        display()
        
        pygame.display.flip()
        pygame.time.wait(10)

    return

    

def init ():
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
    
    
def wheelBase():
    
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
    

def wheelSides():
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
    
def carBase():
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
    
def carTop():
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
    
    
def headlight():
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
    
    
def tailLight():
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
    
    
def carWindow():
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
    
    
def carBack():
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
    

def truckBase():
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
    
    
def truckFront():
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
    
    
def display():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    createCar()
    createTruck()
    
    return


def createTruck():
    global rotation
    global truck_rotation_Amt
    global truck_x_translation
    offset_Z = -3
    offset_Y = -3
    
    glTranslate(truck_x_translation, 0.0, 0.0)
    
    glPushMatrix()
    glTranslate(-2.2, -1.0 + offset_Y, 0.0 + offset_Z)
    glRotatef(rotation,0,0,1)
    rotation += truck_rotation_amt
    wheelSides()
    wheelBase()
    glPopMatrix()
    
    glPushMatrix()
    glTranslate(1.2, -1.0 + offset_Y, 0.0 + offset_Z)
    glRotatef(rotation,0,0,1)
    rotation += truck_rotation_amt
    wheelSides()
    wheelBase()
    glPopMatrix()
    
    
    glPushMatrix()
    glTranslate(0, 0.0 + offset_Y, 0.0 + offset_Z)
    truckBase()
    glPopMatrix()
    
    glPushMatrix()
    glTranslate(-2.0, -0.25 + offset_Y, 0.0 + offset_Z)
    truckFront()
    glPopMatrix()
        

def createCar():
    global rotation
    global rotationAmt
    global x_translation
    
    offset_X = -3
    offset_Z = -3
    
    #carSpeed = 0.005
    glTranslate(x_translation, 0.0, 0.0)
    
    # push before you draw, pop after you draw

    glPushMatrix()
    
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(-1.0 + offset_X, 0.5, 0.0 + offset_Z)
    
    carWindow()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(-1.0 + offset_X, -.5, 0.0 + offset_Z)
    carBase()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(0.0 + offset_X, 1.0, 0.0 + offset_Z)
    carTop()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(1.0 + offset_X, 0.5, 0.0 + offset_Z)
    carBack()

    glPopMatrix()
    glPushMatrix()
    #left wheel
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(-1.5 + offset_X, -0.5, 0.1 + offset_Z)
    glRotatef(rotation,0,0,1)
    rotation += rotationAmt
    
    wheelBase()
    wheelSides()
    
    glPopMatrix()
    glPushMatrix()
    
    #right wheel
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(1.0 + offset_X, -0.5, 0.1 + offset_Z)
    glRotatef(rotation,0,0,1)
    rotation += rotationAmt
    
    wheelBase()
    wheelSides()

    glPopMatrix()
    glPushMatrix()    
    
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(-2.85 + offset_X, 0.2, 0.0 + offset_Z)
    
    headlight()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0 + offset_X, 0.0, 0.0 + offset_Z)
    glTranslate(2.25 + offset_X, 0.2, 0.0 + offset_Z)
    tailLight()
    
    glPopMatrix()
    
    

if __name__ == '__main__':
    main()





