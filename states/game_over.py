import pygame
from states.state import State
from core.scene import Scene
from ui.elements import TextLabel, Button
from core.engine import settings

class GameOverState(State):
    def __init__(self):
        super().__init__()
        self.game_over_scene = Scene()

        title = TextLabel(260, 120, "Game Over", 50, settings.COLOR_TEXT)
        retry_button = Button(325, 250, 150, 50, "Retry", self.retry_game)
        menu_button = Button(325, 320, 150, 50, "Main Menu", self.go_to_menu)

        self.game_over_scene.add_ui_element(title)
        self.game_over_scene.add_ui_element(retry_button)
        self.game_over_scene.add_ui_element(menu_button)

    def retry_game(self):
        self.next_state = "GAMEPLAY"
        self.done = True

    def go_to_menu(self):
        self.next_state = "MAIN_MENU"
        self.done = True

    def handle_event(self, event):
        self.game_over_scene.handle_events(event)

    def update(self, dt):
        self.game_over_scene.update(dt)

    def draw(self, screen):
        screen.fill(settings.COLOR_BG_GAMEOVER)
        self.game_over_scene.draw(screen)
