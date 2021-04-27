from PIL import Image

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


class PlayerView:
    def __init__(self):
        self.view_objects = {}
        self.paused = False
        self.player = None
        self.clock = pygame.time.Clock()

        pub.subscribe(self.new_game_object, 'create')
        pub.subscribe(self.delete_game_object, 'delete')
        pub.subscribe(self.set_ammo_text, 'refresh-text')

        self.setup()
        global ammo_texture
        global health_texture

        global texID
        ammo_texture = None
        health_texture = None
        self.selected_weapon = 1

    def delete_game_object(self, game_object):
        del self.view_objects[game_object.id]

    def tick(self):
        mouseMove = (0, 0)

        if pygame.mouse.get_pressed()[0]:
            self.shoot()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameLogic.set_property('quit', True)
                return

            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]

                pygame.mouse.set_pos(self.viewCenter)

                # CONTROLS
                # mouse
                # change E to activate


            # keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    GameLogic.set_property('paused', self.paused)
                    pygame.mouse.set_pos(self.viewCenter)

                if event.key == pygame.K_l:
                    # change language
                    print("pressed l")
                    self.change_language()

                if event.key == pygame.K_SPACE:
                    pub.sendMessage("key-jump")

                # select melee weapon
                if event.key == pygame.K_1:
                    print("melee selected")
                    self.selected_weapon = 1
                    self.set_ammo_text()

                if event.key == pygame.K_2:
                    print("pistol selected")
                    self.selected_weapon = 2
                    self.set_ammo_text()

                if event.key == pygame.K_3:
                    print("pisotl selected")
                    self.selected_weapon = 3
                    self.set_ammo_text()

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
            # self.display_gun()
            glPopMatrix()

            self.render_hud()
            self.display_weapon()
            pygame.display.flip()

            # fps
            self.clock.tick(60)

    def shoot(self):
        pub.sendMessage("key-shoot")

        pos = pygame.mouse.get_pos()
        self.handle_click(pos)

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

        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    def change_language(self):
        if Localize.lang == "en":
            Localize.set_lang('es')

        elif Localize.lang == "es":
            Localize.set_lang('en')

        print("language is now " + Localize.lang)
        self.set_ammo_text()

        for id in self.view_objects:
            self.view_objects[id].update_text()

    def display(self):
        glInitNames()

        for id in self.view_objects:
            self.view_objects[id].display()

    def surfaceToTexture(self, pygame_surface):
        global texID
        rgb_surface = pygame.image.tostring(pygame_surface, 'RGB')
        glBindTexture(GL_TEXTURE_2D, texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        surface_rect = pygame_surface.get_rect()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE,
                     rgb_surface)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

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
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        self.pistol_image = Image.open('images/pistol/pistol_idle.png')
        self.pistol_shoot = [Image.open('images/pistol/pistol-shoot-1.png'), Image.open('images/pistol/pistol-shoot-2.png'), Image.open('images/pistol/pistol-shoot-3.png'), Image.open('images/pistol/pistol-shoot-4.png'), Image.open('images/pistol/pistol-shoot-5.png')]

        self.shotgun_image = Image.open('images/shotgun.png')
        self.shotgun_reload = [Image.open('images/shotgun-shoot.png'), Image.open('images/shotgun-reload-1.png'), Image.open('images/shotgun-reload-2.png'), Image.open('images/shotgun-reload-3.png')]

        self.melee_image = Image.open('images/melee-idle.png')
        self.melee_attack = [Image.open('images/melee-1.png'), Image.open('images/melee-2.png'), Image.open('images/melee-3.png')]

        self.offscreen_surface = pygame.Surface((self.window_width, self.window_height))
        self.text_font = pygame.font.Font( None, 30 )

        self.reloading = False

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

        elif game_object.kind == "projectile":
            self.view_objects[game_object.id] = ObjectWall(game_object)
            
        elif game_object.kind == "player":
            self.player = game_object
            #self.set_text()

    def handle_click(self, pos):
        if self.selected_weapon == 2:
            self.pistol_behavior = self.player.get_behavior("Pistol")
            if not self.pistol_behavior.shoot():
                return

            self.set_ammo_text()
            print("Clicked. Ammo count is " + str(self.pistol_behavior.ammo_count))

        if self.selected_weapon == 3:
            self.shotgun_behavior = self.player.get_behavior("Shotgun")
            if not self.shotgun_behavior.shoot():
                return

            self.set_ammo_text()
            print("Clicked. Ammo count is " + str(self.shotgun_behavior.ammo_count))

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
        glLoadMatrixf(self.viewMatrix) ###
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

        if self.selected_weapon == 1:
            self.melee(closest, camera)

        else:
            # shoot
            closest.clicked(self.player)

    def melee(self, closest, camera):
        melee = self.player.get_behavior("Melee")

        # returns false if cooling down
        if not melee.melee():
            return

        distance = numpy.linalg.norm(closest.position - camera)
        #print("Distance: " + str(distance))
        if distance < 8:
            #print("in melee range")
            closest.clicked(self.player)

    def display_weapon(self):
        # melee
        if self.selected_weapon == 1:
            self.melee_behavior = self.player.get_behavior("Melee")
            print(str(self.melee_behavior.reloading))
            if self.melee_behavior.reloading:
                if self.melee_behavior.current_cooldown >= 20:
                    self.render_weapon(self.melee_attack[0], 0, 3)
                elif self.melee_behavior.current_cooldown >= 15:
                    self.render_weapon(self.melee_attack[1], 0, 3)
                elif self.melee_behavior.current_cooldown >= 10:
                    self.render_weapon(self.melee_attack[2], 0, 3)
                elif self.melee_behavior.current_cooldown >= 5:
                    self.render_weapon(self.melee_attack[1], 0, 3)
                else:
                    self.render_weapon(self.melee_attack[0], 0, 3)

            else:
                self.render_weapon(self.melee_image, 400, 3)

        # pistol
        if self.selected_weapon == 2:
            # i sure hope this is cached
            self.pistol_behavior = self.player.get_behavior("Pistol")

            offset = 275

            if self.pistol_behavior.reloading:
                if self.pistol_behavior.current_cooldown >= 12:
                    self.render_weapon(self.pistol_shoot[0], offset-22, 3)
                elif self.pistol_behavior.current_cooldown >= 10:
                    self.render_weapon(self.pistol_shoot[1], offset-22, 3)
                elif self.pistol_behavior.current_cooldown >= 8:
                    self.render_weapon(self.pistol_shoot[2], offset-9, 3)
                elif self.pistol_behavior.current_cooldown >= 6:
                    self.render_weapon(self.pistol_shoot[3], offset-3, 3)
                elif self.pistol_behavior.current_cooldown >= 4:
                    self.render_weapon(self.pistol_shoot[3], offset-3, 3)
                else:
                    self.render_weapon(self.pistol_shoot[0], offset-22, 3)

            else:
                self.render_weapon(self.pistol_image, 300, 3)

        # shotgun
        if self.selected_weapon == 3:
            # i sure hope this is cached
            self.shotgun_behavior = self.player.get_behavior("Shotgun")

            if self.shotgun_behavior.reloading:
                if self.shotgun_behavior.current_cooldown >= 75:
                    self.render_weapon(self.shotgun_reload[0], 275, 3)
                elif self.shotgun_behavior.current_cooldown >= 60:
                    self.render_weapon(self.shotgun_reload[1], 400, 3)
                elif self.shotgun_behavior.current_cooldown >= 40:
                    self.render_weapon(self.shotgun_reload[2], 400, 3)
                else:
                    self.render_weapon(self.shotgun_reload[3], 400, 3)

            else:
                self.render_weapon(self.shotgun_image, 275, 3)

    def render_hud(self):
        global ammo_texture
        global health_texture

        if ammo_texture is None:
            self.set_ammo_text()

        if health_texture is None:
            self.set_health_text()


        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.window_width, self.window_height, 0.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, health_texture)

        # build health hud
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

        # build ammo hud
        glBindTexture(GL_TEXTURE_2D, ammo_texture)
        glBegin(GL_QUADS)
        glColor3f(0.0, 1.0, 0.0)

        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, self.window_height - 50);

        glTexCoord2f(1.0, 1.0)
        glVertex2f(200, self.window_height - 50);

        glTexCoord2f(1.0, 0.0)
        glVertex2f(200, self.window_height);

        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, self.window_height);
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def set_ammo_text(self):
        print("setting text")
        global ammo_texture

        if self.selected_weapon == 1:
            img = pygame.font.SysFont('Arial', 50).render("Melee", True, (255, 255, 255),
                                                          (0, 0, 0, 0))
        else:
            ammo = 0

            if self.selected_weapon == 2:
                ammo = self.player.get_behavior("Pistol").ammo_count

            # shotgun
            if self.selected_weapon == 3:
                ammo = self.player.get_behavior("Shotgun").ammo_count

            img = pygame.font.SysFont('Arial', 50).render(language("Ammo: ") + str(ammo), True, (255, 255, 255),
                                                          (0, 0, 0, 0))
        w, h = img.get_size()
        ammo_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, ammo_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def set_health_text(self):
        global health_texture

        img = pygame.font.SysFont('Arial', 50).render(language("Health: ") + str(self.player.get_behavior("PlayerHealth").health), True, (255, 255, 255),
                                                      (0, 0, 0, 0))
        w, h = img.get_size()
        health_texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, health_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    def clear_objects(self):
        self.view_objects = {}

    def render_weapon(self, image, x_offset, scale):
        ix = image.size[0]
        iy = image.size[1]

        image = image.tobytes("raw", "RGBA", 0, -1)

        texture_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture_id)

        # not sure if these are needed
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE);

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.window_width, self.window_height, 0.0)

        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # build hud
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x_offset, self.window_height);
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x_offset + (ix * scale), self.window_height);
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x_offset + (ix * scale), self.window_height - (iy * scale));
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x_offset, self.window_height - (iy * scale));
        glEnd()

        glDisable(GL_TEXTURE_2D)