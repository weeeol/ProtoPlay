import pygame
from state_machine import StateMachine
from states import MainMenuState, GameplayState

# 1. Initialize Pygame and set up the display
pygame.init()
pygame.mixer.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ProtoPlay")
clock = pygame.time.Clock()

try:

    icon = pygame.image.load('assets/my_icon.png') 
    pygame.display.set_icon(icon)
except pygame.error as e:
    print(f"Couldn't load icon: {e}")

# --- State Machine Setup ---
states = {
    "MAIN_MENU": MainMenuState(),
    "GAMEPLAY": GameplayState(screen_width, screen_height)
}

# Create the machine and tell it which state to start in.
machine = StateMachine()
machine.setup_states(states, "MAIN_MENU")

# 3. The Game Loop
running = True
while running:
    # Calculate delta time
    dt = min(clock.tick(60) / 1000, 0.05)

    # Process all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        machine.handle_event(event)

    # Update the current state's logic
    machine.update(dt)

    # Draw whatever the current state needs to draw
    machine.draw(screen)

    # Check if a state has told the machine to quit
    if machine.current_state.quit:
        running = False
    
    # Update the entire display
    pygame.display.flip()

# 4. Quit Pygame
pygame.quit()