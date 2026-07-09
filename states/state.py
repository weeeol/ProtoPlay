class State:
    def __init__(self):
        self.done = False
        self.next_state = None
        self.quit = False

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def enter_state(self):
        pass

    def exit_state(self):
        pass
