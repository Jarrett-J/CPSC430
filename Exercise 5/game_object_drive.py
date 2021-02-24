from game_object import GameObject
import pygame
from pygame.locals import *

class GameObjectDrive(GameObject):
    def __init__(self, position, kind, id):
        super(GameObjectDrive, self).__init__(position, kind, id)
        self.tire_rotation = 0;
        self.text = "Car"
        self.driveEnabled = False
        
    def tick(self):
        keys = pygame.key.get_pressed()
        
        if (self.driveEnabled):
            if keys[K_a]:          
                self.position = [self.position[0] - 0.09, self.position[1], self.position[2]]
                self.tire_rotation += 6
                
            elif keys[K_d]:
                self.position = [self.position[0] + 0.09, self.position[1], self.position[2]]
                self.tire_rotation -= 6
            
    def clicked(self):
        print("Clicked vehicle")
        if self.kind == "car":
            self.kind = "truck"
            self.text = "Truck"
            
        elif self.kind == "truck":
            self.kind = "car"
            self.text = "Car"
