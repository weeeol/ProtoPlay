import pygame
import pygame_gui
from core.engine import settings

class InspectorWindow(pygame_gui.elements.UIWindow):
    def __init__(self, editor_ui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor_ui = editor_ui

    def on_close_window_button_pressed(self):
        self.hide()

class EditorUI:
    def __init__(self, screen_width, screen_height):
        self.manager = pygame_gui.UIManager((screen_width, screen_height), theme_path='assets/theme.json')
        self.active = False
        
        self.window = InspectorWindow(
            editor_ui=self,
            rect=pygame.Rect(screen_width - 430, 20, 420, screen_height - 40),
            manager=self.manager,
            window_display_title="Property Inspector"
        )
        self.window.hide()
        
        self.level_window = InspectorWindow(
            editor_ui=self,
            rect=pygame.Rect(10, 20, 200, 350),
            manager=self.manager,
            window_display_title="Level Tools"
        )
        self.level_window.hide()
        
        self.current_brush = '#'
        self.save_level_requested = False
        self.file_dialog = None
        
        self.slider_to_key = {}
        self.entry_to_key = {}
        self.key_to_slider = {}
        self.key_to_entry = {}
        
        self.build_property_list()
        self.build_level_tools()

    def build_level_tools(self):
        self.brush_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['# (Block)', 'C (Coin)', 'E (Enemy)', 'P (Player)', '  (Eraser)'],
            starting_option='# (Block)',
            relative_rect=pygame.Rect(10, 10, 150, 30),
            manager=self.manager,
            container=self.level_window
        )
        self.save_level_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 60, 150, 40),
            text="Save Level",
            manager=self.manager,
            container=self.level_window
        )
        self.asset_browser_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 120, 150, 40),
            text="Import Asset",
            manager=self.manager,
            container=self.level_window
        )

    def build_property_list(self):
        y_offset = 5
        
        config = {
            "SCREEN_WIDTH": (400, 1920), "SCREEN_HEIGHT": (300, 1080), "FPS": (30, 144),
            "GRAVITY": (0, 2000), "PLAYER_SPEED": (0, 1000), "PLAYER_JUMP_STRENGTH": (-1000, 0),
            "PLAYER_MAX_HEALTH": (1, 100), "PLAYER_INVINCIBILITY_DURATION": (100, 5000),
            "PLAYER_MAX_JUMPS": (1, 10), "ENEMY_SPEED": (0, 500), "ENEMY_PATROL_RANGE": (10, 500),
            "TILE_SIZE": (10, 100)
        }
        
        sections = [
            ("Display", ["SCREEN_WIDTH", "SCREEN_HEIGHT", "FPS", "TILE_SIZE"]),
            ("Physics", ["GRAVITY"]),
            ("Player", ["PLAYER_SPEED", "PLAYER_JUMP_STRENGTH", "PLAYER_MAX_HEALTH", "PLAYER_INVINCIBILITY_DURATION", "PLAYER_MAX_JUMPS"]),
            ("Enemy", ["ENEMY_SPEED", "ENEMY_PATROL_RANGE"])
        ]
        
        for section_name, keys in sections:
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(10, y_offset, 360, 20),
                text=f"--- {section_name} ---",
                manager=self.manager,
                container=self.window
            )
            y_offset += 25
            
            for key in keys:
                value = settings.get(key)
                if value is not None:
                    pygame_gui.elements.UILabel(
                        relative_rect=pygame.Rect(10, y_offset, 235, 25),
                        text=key,
                        manager=self.manager,
                        container=self.window
                    )
                    min_v, max_v = config.get(key, (0, max(100, value * 2)))
                    slider = pygame_gui.elements.UIHorizontalSlider(
                        relative_rect=pygame.Rect(250, y_offset, 90, 25),
                        start_value=value,
                        value_range=(min_v, max_v),
                        manager=self.manager,
                        container=self.window
                    )
                    entry = pygame_gui.elements.UITextEntryLine(
                        relative_rect=pygame.Rect(345, y_offset, 50, 25),
                        manager=self.manager,
                        container=self.window
                    )
                    entry.set_text(str(value))
                    
                    self.slider_to_key[slider] = key
                    self.entry_to_key[entry] = key
                    self.key_to_slider[key] = slider
                    self.key_to_entry[key] = entry
                    
                    y_offset += 30
            y_offset += 5

        # Save Button
        self.save_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, y_offset + 10, 385, 35),
            text="Save Settings",
            manager=self.manager,
            container=self.window
        )

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.window.show()
            self.level_window.show()
        else:
            self.window.hide()
            self.level_window.hide()
            if self.file_dialog:
                self.file_dialog.hide()

    def handle_event(self, event):
        if not self.active:
            return False
            
        self.manager.process_events(event)
        
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element in self.slider_to_key:
                key = self.slider_to_key[event.ui_element]
                orig_val = settings.get(key)
                if isinstance(orig_val, int):
                    new_val = int(event.value)
                else:
                    new_val = float(event.value)
                settings.set(key, new_val)
                self.key_to_entry[key].set_text(str(new_val))
                
        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element in self.entry_to_key:
                key = self.entry_to_key[event.ui_element]
                try:
                    orig_val = settings.get(key)
                    if isinstance(orig_val, int):
                        new_val = int(event.text)
                    else:
                        new_val = float(event.text)
                    settings.set(key, new_val)
                    self.key_to_slider[key].set_current_value(new_val)
                except ValueError:
                    event.ui_element.set_text(str(settings.get(key)))
                    
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_btn:
                settings.save()
                print("Settings saved to project.json")
            elif event.ui_element == self.save_level_btn:
                self.save_level_requested = True
            elif event.ui_element == self.asset_browser_btn:
                import os
                self.file_dialog = pygame_gui.windows.UIFileDialog(
                    rect=pygame.Rect(160, 50, 440, 500),
                    manager=self.manager,
                    window_title='Import Asset',
                    initial_file_path='.',
                    allow_picking_directories=False
                )
                
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.brush_dropdown:
                self.current_brush = event.text[0]
                
        elif event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            if self.file_dialog and event.ui_element == self.file_dialog:
                import shutil, os
                filepath = event.text
                filename = os.path.basename(filepath)
                dest = os.path.join("assets", filename)
                if not os.path.exists("assets"):
                    os.makedirs("assets")
                try:
                    shutil.copy2(filepath, dest)
                    print(f"Imported asset: {dest}")
                except Exception as e:
                    print(f"Failed to import asset: {e}")
                
        return True # Handled

    def update(self, dt):
        if self.active:
            self.manager.update(dt)

    def draw(self, screen):
        if self.active:
            self.manager.draw_ui(screen)
