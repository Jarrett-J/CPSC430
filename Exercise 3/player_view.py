import pygame
import numpy
from pygame.locals import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pubsub import pub

from cube_view import CubeView
from object_car import ObjectCar
from object_truck import ObjectTruck
from object_vehicle import ObjectVehicle
import random

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}
        
        # receive event
        pub.subscribe(self.new_game_object, 'create')
        
        self.setup()
        
    def new_game_object(self, game_object):
        print(game_object.kind)
        
    def tick(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property('quit', True)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spawn_car_randomly()

        glClearColor(1.0, 1.0, 1.0, 1.0)            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.display()
        
        pygame.display.flip()
        pygame.time.wait(10)
        
    def spawn_car_randomly(self):
        pos = [random.uniform(-10, 10), random.uniform (-10, 10), -10]
        self.game_logic.create_driving_object(pos, "vehicle")

    def display(self):
        glInitNames()
        
        for id in self.view_objects:
            self.view_objects[id].display()
        
    def setup(self):
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF|OPENGL)
        self.field_of_view = 60
        self.aspect_ratio = self.window_width/self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0
        
        self.reset_opengl()
        
    def reset_opengl(self):
        glViewport(0, 0, self.window_width, self.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glEnable(GL_COLOR_MATERIAL)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        
    # Define game objects
    def new_game_object(self, game_object):
        if game_object.kind == "cube":
            self.view_objects[game_object.id] = CubeView(game_object)
            
        elif game_object.kind == "car":
            self.view_objects[game_object.id] = ObjectCar(game_object)
            
        elif game_object.kind == "truck":
            self.view_objects[game_object.id] = ObjectTruck(game_object)
            
        elif game_object.kind == "vehicle":
            self.view_objects[game_object.id] = ObjectVehicle(game_object)
            
        print(game_object.kind)
        
    def handle_click(self, pos):
        windowX = pos[0]
        windowY = self.window_height - pos[1]
        
        # if multiple objects under cursor, return up to 20
        glSelectBuffer(20)
        
        glRenderMode(GL_SELECT)
        
        glMatrixMode(GL_PROJECTION);
        glPushMatrix()
        glLoadIdentity();
        
        gluPickMatrix(windowX, windowY, 20.0, 20.0, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)
        
        glMatrixMode(GL_MODELVIEW)
        self.display()
        
        glMatrixMode(GL_PROJECTION);
        glPopMatrix()
        
        buffer = glRenderMode(GL_RENDER)
        
        objects = []
        for record in buffer:
            min_depth, max_depth, name = record
            objects += name
            
        if not objects:
            return
        
        camera = numpy.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX))
        camera = camera[3][0:3]
        
        closest = None
        
        for id in objects:
            obj_pos = self.view_objects[id].game_object.position
            
            if not closest or numpy.linalg.norm(obj_pos - camera) < numpy.linalg.norm(closest.position - camera):
                closest = self.view_objects[id].game_object
                
            closest.clicked()
    