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


class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def setup_states(self, states, start_state):
        self.states = states
        self.current_state = self.states[start_state]
        self.current_state.enter_state()

    def flip_state(self):
        self.current_state.exit_state()
        
        # Switch to the new state
        next_state_name = self.current_state.next_state
        self.current_state.done = False
        self.current_state = self.states[next_state_name]
        
        # Run the setup method on the new state
        self.current_state.enter_state()

    def update(self, dt):

        if self.current_state.done:
            self.flip_state()
        self.current_state.update(dt)

    def handle_event(self, event):
        self.current_state.handle_event(event)
        
    def draw(self, screen):
        self.current_state.draw(screen)