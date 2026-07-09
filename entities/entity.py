import pygame
from core import resource_manager

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__() 
        self.image = resource_manager.get_image(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scene = None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
