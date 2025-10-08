import pygame

class Scene:
    def __init__(self):
        self.all_entities = []
        self.collidables = pygame.sprite.Group()
        self.ui_elements = [] # New list for UI

    def add_entity(self, entity, collidable=False):
        self.all_entities.append(entity)
        if collidable:
            # Add to the collidable group if specified
            self.collidables.add(entity)

    def add_ui_element(self, element): # New method
        self.ui_elements.append(element)

    def handle_events(self, event): # New method for UI
        for element in self.ui_elements:
            element.handle_event(event)

    def update(self, dt,exclude=None):
        for entity in self.all_entities:
           if entity is not exclude:
                entity.update(dt)
                
        for element in self.ui_elements:
            if hasattr(element, 'update'):
                element.update()

    def draw(self, screen):
        # Draw game entities first
        for entity in self.all_entities:
            entity.draw(screen)
        # Draw UI elements on top
        for element in self.ui_elements:
            element.draw(screen)