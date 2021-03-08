from localize import *
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
from object_ground import ObjectGround
from object_wall import ObjectWall
from object_sidewall import ObjectSideWall
import random


class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}
        self.paused = False
        self.player = None
        self.clock = pygame.time.Clock()
        # receive event
        pub.subscribe(self.new_game_object, 'create')

        self.setup()
        global clicks_texture
        global numClicks
        numClicks = -1
        self.set_text()
        self.user_clicked()
        

    def tick(self):
        mouseMove = (0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property('quit', True)
                return

            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]

                pygame.mouse.set_pos(self.viewCenter)

            # CONTROLS
            # mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)

            # keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    pygame.mouse.set_pos(self.viewCenter)

                if event.key == pygame.K_SPACE:
                    self.spawn_car_randomly()

                if event.key == pygame.K_l:
                    # change language
                    print("pressed l")
                    self.change_language()

        if not self.paused:
            self.prepare_3d()
            keypress = pygame.key.get_pressed()
            
            if keypress[pygame.K_w]:
                pub.sendMessage('key-w')
            if keypress[pygame.K_s]:
                pub.sendMessage('key-s')
            if keypress[pygame.K_d]:
                pub.sendMessage('key-d')
            if keypress[pygame.K_a]:
                pub.sendMessage('key-a')
            if keypress[pygame.K_SPACE]:
                pub.sendMessage('key-space')
                
            pub.sendMessage('rotate-y', amount=mouseMove[0])
            pub.sendMessage('rotate-x', amount=mouseMove[1])

            if self.player:
                glRotate(self.player.x_rotation, 1.0, 0.0, 0.0)
                glRotate(self.player.y_rotation, 0.0, 1.0, 0.0)
                glTranslate(-self.player.position[0], -self.player.position[1], -self.player.position[2])
                self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPushMatrix()

            self.display()
        
            glPopMatrix()
            
            self.render_hud()
            pygame.display.flip()
            
            # fps
            self.clock.tick(60)

    def prepare_3d(self):
        glViewport(0, 0, self.window_width, self.window_height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.field_of_view, self.aspect_ratio, 0.1, 100.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_COLOR_MATERIAL)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

    def render_hud(self):
        global clicks_texture
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.window_width, self.window_height, 0.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, clicks_texture)

        # build hud
        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, 0)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(200, 0)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(200, 50)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, 50)
        glEnd()

        glDisable(GL_TEXTURE_2D)



    def change_language(self):
        if Localize.lang == "en":
            Localize.set_lang('es')

        elif Localize.lang == "es":
            Localize.set_lang('en')

        print("language is now " + Localize.lang)
        self.set_text()

        for id in self.view_objects:
            self.view_objects[id].update_text()

    def spawn_car_randomly(self):
        pass
        #pos = [random.uniform(-10, 10), random.uniform(-10, 10), -10]
        #self.game_logic.test_create_object(pos, "vehicle", GameObjectDrive)

    def display(self):
        glInitNames()

        for id in self.view_objects:
            self.view_objects[id].display()

    def setup(self):
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        # // gives division integer result
        self.viewCenter = (self.window_width // 2, self.window_height // 2)
        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF | OPENGL)
        self.field_of_view = 60
        self.aspect_ratio = self.window_width / self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0

        self.prepare_3d()
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    def reset_opengl(self):
        glViewport(0, 0, self.window_width, self.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
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

        elif game_object.kind == "ground":
            self.view_objects[game_object.id] = ObjectGround(game_object)

        elif game_object.kind == "wall":
            self.view_objects[game_object.id] = ObjectWall(game_object)

        elif game_object.kind == "sidewall":
            self.view_objects[game_object.id] = ObjectSideWall(game_object)

        elif game_object.kind == "move":
            self.view_objects[game_object.id] = CubeView(game_object)
            
        elif game_object.kind == "player":
            self.player = game_object

        print(game_object.kind)

    def handle_click(self, pos):
        self.user_clicked()
        
        print("handle click")
        windowX = pos[0]
        windowY = self.window_height - pos[1]

        # if multiple objects under cursor, return up to 20
        glSelectBuffer(20)
        glRenderMode(GL_SELECT)

        glMatrixMode(GL_PROJECTION);
        glPushMatrix()
        glLoadIdentity();

        gluPickMatrix(windowX, windowY, 1.0, 1.0, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.viewMatrix) ###
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

            #print("closest: " + str(closest))
        closest.clicked()

    # HUD stuff below
    def user_clicked(self):
        global numClicks
        global clicks_texture
        numClicks += 1
        self.set_text()
        
    def set_text(self):
        global clicks_texture
        global numClicks
        
        img = pygame.font.SysFont('Arial', 50).render(language("Clicks: ") + str(numClicks), True, (255, 255, 255),
                                                      (0, 0, 0, 0))
        w, h = img.get_size()
        clicks_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, clicks_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        





