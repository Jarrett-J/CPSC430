from game_logic import GameLogic
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
    def __init__(self):
        self.view_objects = {}
        self.paused = False
        self.player = None
        self.clock = pygame.time.Clock()
        self.camera_direction = [0.0, 0.0, -1.0]
        self.scale = 5

        self.edit_mode = False
        self.position_mode = False
        self.size_mode = False
        self.input_mode = False
        self.get_name = False
        self.input = ""

        self.position_adjust_amt = 0.1
        self.size_adjust_amt = 0.1

        self.distance = 1.5
        self.textures = []
        self.current_texture = 0

        GameLogic.set_property('paused', True)

        # receive event
        pub.subscribe(self.new_game_object, 'create')
        pub.subscribe(self.delete_game_object, 'delete')

        self.setup()

    def delete_game_object(self, game_object):
        try:
            del self.view_objects[game_object.id]
        except KeyError:
            print("KeyError occured")
            pass

    def tick(self):
        if not self.textures:
            self.find_textures()

        mouseMove = (0, 0)
        clicked = False
        self.apply_texture = False
        self.clear_texture = False
        self.position_adjust = 0.0
        self.size_adjust = 0.0
        self.set_name = False

        self.update_crosshair_texture()

        if self.get_name:
            self.update_hud_texture()

        self.get_name = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameLogic.set_property('quit', True)
                return

            # keyboard
            if event.type == pygame.KEYDOWN:

                if self.input_mode:
                    # input mode
                    if event.key == pygame.K_RETURN:
                        self.input_mode = False
                        self.set_name = True

                    elif event.key == pygame.K_BACKSPACE:
                        self.input = self.input[:-1]
                    else:
                        if self.input is None:
                            self.input = ""

                        self.input += event.unicode

                    self.update_hud_texture()

                if not self.input_mode:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        GameLogic.set_property('paused', self.paused)
                        pygame.mouse.set_pos(self.viewCenter)

                    if event.key == pygame.K_l:
                        # change language
                        self.change_language()

                    if event.key == pygame.K_SPACE:
                        pub.sendMessage("key-jump")

                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        GameLogic.save_world()

                    # edit mode
                    if event.key == pygame.K_e:
                        self.edit_mode = not self.edit_mode

                    # change texture
                    if event.key == pygame.K_t:
                        self.current_texture = (self.current_texture + 1) % len(self.textures)
                        print("Selected texture: " + self.textures[self.current_texture])

                    # apply texture
                    if event.key == pygame.K_r:
                        self.apply_texture = True

                    # clear texture
                    if event.key == pygame.K_z:
                        self.clear_texture = True

                    # position mode
                    if event.key == pygame.K_f:
                        self.position_mode = not self.position_mode
                        print("Position mode " + str(self.position_mode))

                    # sizing mode
                    if event.key == pygame.K_c:
                        self.size_mode = not self.size_mode
                        print("Size mode " + str(self.size_mode))

                    # input mode
                    if event.key == pygame.K_n:
                        self.input_mode = True
                        self.get_name = True
                        self.input = ""

                    if event.key == pygame.K_UP and self.size_mode:
                        self.size_adjust_amt += 0.5
                        print("Size adjust amt: " + str(self.size_adjust_amt))

                    if event.key == pygame.K_DOWN and self.size_mode:
                        self.size_adjust_amt -= 0.5
                        print("Size adjust amt: " + str(self.size_adjust_amt))

                    if event.key == pygame.K_UP and self.position_mode:
                        self.position_adjust_amt += 0.5
                        print("Position adjust amt: " + str(self.position_adjust_amt))

                    if event.key == pygame.K_DOWN and self.position_mode:
                        self.position_adjust_amt -= 0.5
                        print("Position adjust amt: " + str(self.position_adjust_amt))

            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]

                pygame.mouse.set_pos(self.viewCenter)

                if event.type == pygame.MOUSEWHEEL:
                    if self.edit_mode:
                        self.distance = max(1.5, self.distance + event.y)

                    if self.position_mode:
                        self.position_adjust = event.y * self.position_adjust_amt

                    if self.size_mode:
                        self.size_adjust = event.y * self.size_adjust_amt

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True

                    # edit mode placing
                    if self.edit_mode:
                        self.create_object()

        if not self.paused:
            pos = pygame.mouse.get_pos()
            self.handle_click(pos, clicked)
            self.prepare_3d()

            if not self.input_mode:
                keypress = pygame.key.get_pressed()

                if keypress[pygame.K_w]:
                    pub.sendMessage('key-w', camera_direction=self.camera_direction)
                if keypress[pygame.K_s]:
                    pub.sendMessage('key-s', camera_direction=self.camera_direction)
                if keypress[pygame.K_d]:
                    pub.sendMessage('key-d')
                if keypress[pygame.K_a]:
                    pub.sendMessage('key-a')

                pub.sendMessage('rotate-y', amount=mouseMove[0])
                pub.sendMessage('rotate-x', amount=mouseMove[1])

        if self.player:
            glRotate(self.player.x_rotation, 1.0, 0.0, 0.0)
            glRotate(self.player.y_rotation, 0.0, 1.0, 0.0)
            glTranslate(-self.player.position[0], -self.player.position[1], -self.player.position[2])
            self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            camera_direction = numpy.linalg.inv(self.viewMatrix)
            camera_direction = camera_direction[2][0:3]
            camera_direction[0] *= -1
            camera_direction[1] *= -1
            camera_direction[2] *= -1
            self.camera_direction = camera_direction

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        self.display()

        glPopMatrix()

        self.draw_guide()

        self.render_hud()
        pygame.display.flip()

        # fps
        self.clock.tick(60)

    def find_textures(self):
        self.textures = []

        for file in GameLogic.files:
            if GameLogic.files[file].startswith('images/'):
                self.textures.append(file)

    def draw_guide(self):
        if not self.edit_mode:
            return

        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)

        position = (current + self.distance * camera_direction).tolist()

        position[0] = round(position[0])
        position[1] = round(position[1])
        position[2] = round(position[2])

        glPushMatrix()
        glTranslate(*position)

        scale = self.scale

        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5 * scale, 0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5 * scale, -0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5 * scale, -0.5 * scale, 0.5 * scale)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5 * scale, 0.5 * scale, 0.5 * scale)

        glEnd()

        # Back face
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, -1.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5 * scale, 0.5 * scale, -0.5 * scale)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5 * scale, -0.5 * scale, -0.5 * scale)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5 * scale, -0.5 * scale, -0.5 * scale)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5 * scale, 0.5 * scale, -0.5 * scale)

        glEnd()

        # Left face
        glBegin(GL_QUADS)

        glNormal3f(-1.0, 0.0, 0.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5 * scale, 0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(-0.5 * scale, -0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(-0.5 * scale, -0.5 * scale, -0.5 * scale)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5 * scale, 0.5 * scale, -0.5 * scale)

        glEnd()

        # Right face
        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(0.5 * scale, 0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5 * scale, -0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5 * scale, -0.5 * scale, -0.5 * scale)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(0.5 * scale, 0.5 * scale, -0.5 * scale)
        glEnd()

        # Top face
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5 * scale, 0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5 * scale, 0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5 * scale, 0.5 * scale, -0.5 * scale)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5 * scale, 0.5 * scale, -0.5 * scale)
        glEnd()

        # Bottom face
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3d(-0.5 * scale, -0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 0.0)
        glVertex3d(0.5 * scale, -0.5 * scale, 0.5 * scale)

        glTexCoord2f(0.0, 1.0)
        glVertex3d(0.5 * scale, -0.5 * scale, -0.5 * scale)

        glTexCoord2f(1.0, 1.0)
        glVertex3d(-0.5 * scale, -0.5 * scale, -0.5 * scale)

        glEnd()
        glPopMatrix()

    def create_object(self):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)

        position = (current + self.distance * camera_direction).tolist()

        position[0] = round(position[0])
        position[1] = round(position[1])
        position[2] = round(position[2])

        GameLogic.create_object({'size': [self.scale, self.scale, self.scale], 'kind': 'wall', 'position': position})

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

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def update_crosshair_texture(self):
        pass
        #self.screen.blit(self.crosshair_texture, (0, 0))

    def update_hud_texture(self):
        surface = pygame.Surface((800, 30), flags=pygame.SRCALPHA)
        surface.fill(pygame.Color("lightskyblue"))

        text = pygame.font.SysFont('Arial', 28).render(self.input, True, (255, 255, 255))
        surface.blit(text, (0, 0))

        w, h = surface.get_size()

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.hud_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        data = pygame.image.tostring(surface, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def render_hud(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.window_width, self.window_height, 0.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.input_mode:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.hud_texture)

            # build hud
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0)
            glVertex2f(0, 570)
            glTexCoord2f(1.0, 1.0)
            glVertex2f(800, 570)
            glTexCoord2f(1.0, 0.0)
            glVertex2f(800, 600)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(0, 600)
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

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF | OPENGL)

        self.field_of_view = 60
        self.aspect_ratio = self.window_width / self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0

        self.prepare_3d()
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        self.hud_texture = glGenTextures(1)
        # self.crosshair_texture = pygame.image.load("crosshair/crosshair.png")

        #pygame.mouse.set_visible(False)
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

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

        elif game_object.kind == "wall" or game_object.kind == "weapon":
            self.view_objects[game_object.id] = ObjectWall(game_object)

        elif game_object.kind == "sidewall":
            self.view_objects[game_object.id] = ObjectSideWall(game_object)

        elif game_object.kind == "move":
            self.view_objects[game_object.id] = CubeView(game_object)

        elif game_object.kind == "player":
            self.player = game_object

    def handle_click(self, pos, clicked):
        windowX = pos[0]
        windowY = self.window_height - pos[1]

        # if multiple objects under cursor, return up to 200
        glSelectBuffer(200)
        glRenderMode(GL_SELECT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluPickMatrix(windowX, windowY, 1.0, 1.0, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.viewMatrix)
        self.display()

        glMatrixMode(GL_PROJECTION)
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

            # print("closest: " + str(closest))

        if closest:
            # print(closest.faces)
            # closest.hover(self.player)
            if self.set_name:
                closest._name = self.input

            if self.get_name:
                self.input = closest.name

            if self.apply_texture:
                print("apply texture")

                for face in self.get_all_faces(closest):
                    closest.faces[face] = {'type': 'texture', 'value': self.textures[self.current_texture]}

                #for face in self.get_faces(closest):
                    # closest.faces[face] = {'type': 'texture', 'value': self.textures[self.current_texture]}
                    #face = {'type': 'texture', 'value': self.textures[self.current_texture]}

            if self.clear_texture:
                print("clear texture")
                # seems to break when removing a face w/o texture
                for face in self.get_faces(closest):
                    del closest.faces[face]

            if self.position_mode and self.position_adjust:
                for face in self.get_faces(closest):
                    if face == 'front':
                        closest.position[2] += self.position_adjust

                    if face == 'back':
                        closest.position[2] -= self.position_adjust

                    if face == 'left':
                        closest.position[0] += self.position_adjust

                    if face == 'right':
                        closest.position[0] -= self.position_adjust

                    if face == 'top':
                        closest.position[1] -= self.position_adjust

                    if face == 'bottom':
                        closest.position[1] += self.position_adjust

            if self.size_mode and self.size_adjust:
                for face in self.get_faces(closest):
                    if face == 'front' or face == 'back':
                        closest.size[2] += self.size_adjust

                    if face == 'left' or face == 'right':
                        closest.size[0] += self.size_adjust

                    if face == 'top' or face == 'bottom':
                        closest.size[1] += self.size_adjust

            if clicked:
                closest.clicked(self.player)

    def get_faces(self, game_object):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)

        mypos = current + 1.5 * camera_direction

        otherpos = numpy.array(game_object.position)
        distance = numpy.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance

        max_direction = max(direction_vector, key=abs)
        indices = [i for i, j in enumerate(direction_vector) if j == max_direction]

        results = []

        for index in indices:
            if index == 0 and direction_vector[index] < 0:
                results.append('left')
            if index == 0 and direction_vector[index] > 0:
                results.append('right')
            if index == 1 and direction_vector[index] < 0:
                results.append('bottom')
            if index == 1 and direction_vector[index] > 0:
                results.append('top')

            # these might be mixed up
            if index == 2 and direction_vector[index] < 0:
                results.append('back')
            if index == 2 and direction_vector[index] > 0:
                results.append('front')

            return results

    def get_all_faces(self, game_object):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position)

        mypos = current + 1.5 * camera_direction

        otherpos = numpy.array(game_object.position)
        distance = numpy.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance

        max_direction = max(direction_vector, key=abs)
        indices = [i for i, j in enumerate(direction_vector) if j == max_direction]

        results = []

        results.append('left')
        results.append('right')
        results.append('bottom')
        results.append('top')

        results.append('back')
        results.append('front')

        return results

    def clear_objects(self):
        self.view_objects = {}



