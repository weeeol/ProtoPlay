import pygame

class Scene:
    def __init__(self):
        self.all_entities = []
        self.collidables = pygame.sprite.Group()
        self.ui_elements = []

    def add_entity(self, entity, collidable=False):
        self.all_entities.append(entity)
        entity.scene = self
        if collidable:
            self.collidables.add(entity)

    def add_ui_element(self, element):
        self.ui_elements.append(element)
        element.scene = self

    def handle_events(self, event): 
        for element in self.ui_elements:
            element.handle_event(event)

    def update(self, dt):
        for entity in self.all_entities:
            entity.update(dt)
                
        for element in self.ui_elements:
            if hasattr(element, 'update'):
                element.update()

    def draw(self, screen):
        for entity in self.all_entities:
            entity.draw(screen)
        for element in self.ui_elements:
            element.draw(screen)
