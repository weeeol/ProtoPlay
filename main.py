import pygame
from core.engine import settings
from core import resource_manager
from core.state_machine import StateMachine
from core.editor_ui import EditorUI
from states.main_menu import MainMenuState
from states.gameplay import GameplayState
from states.game_over import GameOverState

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("ProtoPlay")
clock = pygame.time.Clock()

icon = resource_manager.get_image('assets/my_icon.png') 
if icon:
    pygame.display.set_icon(icon)

# --- State Machine Setup ---
states = {
    "MAIN_MENU": MainMenuState(),
    "GAMEPLAY": GameplayState(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
    "GAME_OVER": GameOverState()
}

machine = StateMachine()
machine.setup_states(states, "MAIN_MENU")

editor = EditorUI(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

running = True
while running:
    # Calculate delta time
    dt = min(clock.tick(settings.FPS) / 1000, 0.05)

    # Process all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            editor.toggle()

        # Pass event to editor. If it's active, it might consume clicks.
        handled_by_editor = editor.handle_event(event)
        
        # In edit mode, don't process player inputs via machine.handle_event if it was a mouse click?
        # Actually, let's just let the state handle it if it knows it's in edit_mode.
        machine.handle_event(event)
        
    if editor.save_level_requested:
        if hasattr(machine.current_state, 'save_level'):
            machine.current_state.save_level()
        editor.save_level_requested = False
        
    if hasattr(machine.current_state, 'edit_mode'):
        # Only GameplayState will have this
        machine.current_state.edit_mode = editor.active
        machine.current_state.current_brush = editor.current_brush

    # --- Handle Dynamic Screen Resizing ---
    current_width, current_height = screen.get_size()
    if current_width != settings.SCREEN_WIDTH or current_height != settings.SCREEN_HEIGHT:
        # Update display
        screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        
        # Update Editor UI
        editor.manager.set_window_resolution((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        editor.window.set_position((settings.SCREEN_WIDTH - 430, 20))
        editor.window.set_dimensions((420, settings.SCREEN_HEIGHT - 40))
        
        # Update Gameplay State dependencies
        gameplay_state = states["GAMEPLAY"]
        gameplay_state.screen_width = settings.SCREEN_WIDTH
        gameplay_state.screen_height = settings.SCREEN_HEIGHT
        gameplay_state.pause_overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        gameplay_state.pause_overlay.fill(settings.COLOR_PAUSE_OVERLAY)
        
        if hasattr(gameplay_state, 'player'):
            gameplay_state.player.bounds = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

    machine.update(dt)
    editor.update(dt)

    machine.draw(screen)
    editor.draw(screen)

    if machine.current_state.quit:
        running = False
    
    pygame.display.flip()

pygame.quit()