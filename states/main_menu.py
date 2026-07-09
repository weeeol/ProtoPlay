import pygame
from states.state import State
from core.scene import Scene
from ui.elements import TextLabel, Button
from core.engine import settings

class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.menu_scene = Scene()

        title = TextLabel(285, 120, "ProtoPlay", 50, settings.COLOR_TEXT)
        start_button = Button(325, 250, 150, 50, "Start", self.start_game)
        quit_button = Button(325, 320, 150, 50, "Quit", self.quit_game)
        footer = TextLabel(350, 500, "By Weeeol", 20, settings.COLOR_TEXT)

        self.menu_scene.add_ui_element(title)
        self.menu_scene.add_ui_element(start_button)
        self.menu_scene.add_ui_element(quit_button)
        self.menu_scene.add_ui_element(footer)

    def start_game(self):
        self.next_state = "GAMEPLAY"
        self.done = True

    def quit_game(self):
        self.quit = True

    def handle_event(self, event):
        self.menu_scene.handle_events(event)

    def update(self, dt):
        self.menu_scene.update(dt)

    def draw(self, screen):
        screen.fill(settings.COLOR_BG_MENU)
        self.menu_scene.draw(screen)
