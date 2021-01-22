import pygame
from pygame.locals import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from PIL.Image import open

rotation = 0.0

def main():
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
                
        display()
        
        pygame.display.flip()
        pygame.time.wait(10)

    return

def init ():
    glEnable(GL_COLOR_MATERIAL);
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    
def wheelBase():
    glBegin(GL_QUADS)
    # Front face
    glColor(0.0, 0.0, 0.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(-0.25, 0.25, 0.0)
    glVertex3d(-0.25, -0.25, 0.0)
    glVertex3d(0.25, -0.25, 0.0)
    glVertex3d(0.25, 0.25, 0.0)
    
    glEnd()

def wheelSides():
    glBegin(GL_TRIANGLES)
    glColor(0.0, 0.0, 0.0, 1.0)
    
    #left of wheel
    glVertex3d(-0.25, -0.25, 0.0)
    glVertex3d(-0.375, 0.0, 0.0)
    glVertex3d(-0.25, 0.25, 0.0)
    
    #right of wheel
    glVertex3d(0.25, -0.25, 0.0)
    glVertex3d(0.375, 0.0, 0.0)
    glVertex3d(0.25, 0.25, 0.0)
    
    #top of wheel
    glVertex3d(-0.25, 0.25, 0.0)
    glVertex3d(0.0, 0.375, 0.0)
    glVertex3d(0.25, 0.25, 0.0)
    
    #bottom of wheel
    glVertex3d(-0.25, -0.25, 0.0)
    glVertex3d(0.0, -0.375, 0.0)
    glVertex3d(0.25, -0.25, 0.0)
    
    glEnd()
    
def carBase():
    glBegin(GL_QUADS)
    
    glColor(1.0, 0.0, 1.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(-2.0, 0.0, 0.0)
    glVertex3d(-2.0, 1.0, 0.0)
    glVertex3d(3.5, 1.0, 0.0)
    glVertex3d(3.5, 0.0, 0.0)
    
    glEnd()
    
def carTop():
    glBegin(GL_QUADS)
    
    glColor(1.0, 0.0, 1.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(-1.0, 0.5, 0.0)
    glVertex3d(-1.0, -0.5, 0.0)
    glVertex3d(1.0, -0.5, 0.0)
    glVertex3d(1.0, 0.5, 0.0)
    
    glEnd()
    
    
def headlight():
    glBegin(GL_QUADS)
    
    glColor(1.0, 1.0, 0.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(-0.25, 0.0, 0.0)
    glVertex3d(-0.25, 0.25, 0.0)
    glVertex3d(0.35, 0.25, 0.0)
    glVertex3d(0.35, 0.0, 0.0)
    
    glEnd()
    
    
def tailLight():
    glBegin(GL_QUADS)
    
    glColor(1.0, 0.0, 0.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(-0.25, 0.0, 0.0)
    glVertex3d(-0.25, 0.25, 0.0)
    glVertex3d(0.35, 0.25, 0.0)
    glVertex3d(0.35, 0.0, 0.0)
    
    glEnd()
    
    
def carWindow():
    glBegin(GL_TRIANGLES)
    glColor(0.0, 1.0, 1.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(0.0, 0.0, 0.0)
    
    glVertex3d(0.0, 1.0, 0.0)
    glVertex3d(-1.0, 0.0, 0.0)
    
    glEnd()
    
    
def carBack():
    glBegin(GL_TRIANGLES)
    glColor(1.0, 0.0, 1.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, 1.0, 0.0)
    glVertex3d(1.0, 0.0, 0.0)
    
    glEnd()
    
    
def background():
    glBegin(GL_QUADS)
    
    glColor(1.0, 1.0, 1.0, 1.0)
    glNormal3f( 0.0, 0.0, -1.0)
    
    glVertex3d(-50.0, -50.0, 0)
    glVertex3d(-50.0, 50.0, 0)
    glVertex3d(50.0, 50.0, 0)
    glVertex3d(50.0, -50.0, 0)
    
    glEnd()
    
    
def display():
    global rotation
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    carSpeed = 0.005
    glTranslate(-carSpeed, 0.0, 0.0)
    
    # push before you draw, pop after you draw

    glPushMatrix()
    
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(-1.0, 0.5, 0.0)
    
    carWindow()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(-1.0, -.5, 0.0)
    carBase()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(0.0, 1.0, 0.0)
    carTop()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(1.0, 0.5, 0.0)
    carBack()

    glPopMatrix()
    glPushMatrix()
    #left wheel
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(-1.5, -0.5, 0.1)
    glRotatef(rotation,0,0,1)
    rotation += 2.5
    
    wheelBase()
    wheelSides()
    
    glPopMatrix()
    glPushMatrix()
    
    #right wheel
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(1.0, -0.5, 0.1)
    glRotatef(rotation,0,0,1)
    rotation += 2.5
    
    wheelBase()
    wheelSides()

    glPopMatrix()
    glPushMatrix()    
    
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(-2.85, 0.2, 0.0)
    
    headlight()
    
    glPopMatrix()
    glPushMatrix()
    
    glTranslate(6.0, 0.0, 0.0)
    glTranslate(2.25, 0.2, 0.0)
    tailLight()
    
    glPopMatrix()
    return

if __name__ == '__main__':
    main()





