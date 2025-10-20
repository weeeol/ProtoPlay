import pygame

class UIElement:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def handle_event(self, event):
        pass

    def draw(self, screen):
        pass

pygame.font.init()

class TextLabel(UIElement):
    def __init__(self, x, y, text, font_size, color):
        # Create a font object
        self.font = pygame.font.Font('font/DejaVuSans.ttf', font_size)
        self.text = text
        self.color = color
        
        text_surface = self.font.render(text, True, color)
        super().__init__(x, y, text_surface.get_width(), text_surface.get_height())
        
        self.text_surface = text_surface

    def set_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect.width = self.text_surface.get_width()
        self.rect.height = self.text_surface.get_height()

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)


class Button(UIElement):
    def __init__(self, x, y, width, height, text, on_click):
        super().__init__(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.is_hovering = False
        self.is_pressed = False 

        # Basic styling
        self.font = pygame.font.Font('font/DejaVuSans.ttf', 24) 
        self.text_color = (255, 255, 255)
        self.bg_color = (50, 50, 50)
        self.hover_color = (100, 100, 100)
        self.pressed_color = (20, 20, 20) 

        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.is_hovering = True
        else:
            self.is_hovering = False
            self.is_pressed = False 

    def handle_event(self, event):
        if self.is_hovering:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.is_pressed = True 
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pressed:
                self.on_click()
                self.is_pressed = False 
            
    def draw(self, screen):
        if self.is_pressed:
            current_color = self.pressed_color
        elif self.is_hovering:
            current_color = self.hover_color
        else:
            current_color = self.bg_color
        
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        screen.blit(self.text_surface, self.text_rect)