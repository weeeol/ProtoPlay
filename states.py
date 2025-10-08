import pygame
from state_machine import State
from scene import Scene
from ui_element import TextLabel, Button
from entity import Entity, Player, Coin, Enemy

class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.menu_scene = Scene() # Use a Scene object!

        title = TextLabel(285, 120, "ProtoPlay", 50, (255, 255, 255))
        start_button = Button(325, 250, 150, 50, "Start", self.start_game)
        quit_button = Button(325, 320, 150, 50, "Quit", self.quit_game)
        footer = TextLabel(350, 500, "By Weeeol", 20, (255, 255, 255))

        # Add elements to the scene's UI layer
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
        screen.fill((20, 20, 50))
        self.menu_scene.draw(screen)


class GameplayState(State):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_scene = Scene()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.current_level_path = None


# --- NEW: Load the sound effect ---
        try:
            self.coin_sound = pygame.mixer.Sound("assets/coin_collect.wav")
            self.hit_sound = pygame.mixer.Sound("assets/enemy_hit.wav")
        except pygame.error as e:
            print(f"Couldn't load coin sound: {e}")
            self.coin_sound = None
            self.hit_sound = None


        # Load the level from the file
        self.load_level("levels/level_3.txt")

    def load_level(self, file_path):
        self.current_level_path = file_path
        TILE_SIZE = 50 
        try:
            with open(file_path, 'r') as f:
                for y, line in enumerate(f): 
                    for x, char in enumerate(line.strip()): 
                        pos_x = x * TILE_SIZE
                        pos_y = y * TILE_SIZE

                        if char == '#':
                            block = Entity(pos_x, pos_y, "assets/block.png")
                            self.game_scene.add_entity(block, collidable=True)
                        
                        elif char == 'P':
                             self.player = Player(x=pos_x, y=pos_y, bounds=(self.screen_width, self.screen_height))
                             self.game_scene.add_entity(self.player)

                        elif char == 'C':
                            coin = Coin(pos_x, pos_y)
                            self.game_scene.add_entity(coin)
                            self.coins.add(coin)
                        
                        elif char == 'E':
                            enemy = Enemy(pos_x, pos_y)
                            self.game_scene.add_entity(enemy, collidable=False)
                            self.enemies.add(enemy)

        except FileNotFoundError:
            print(f"Error: Could not load level file: {file_path}")
            self.player = Player(x=375, y=500, bounds=(self.screen_width, self.screen_height))
            self.game_scene.add_entity(self.player)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = "MAIN_MENU"
            self.done = True
        self.game_scene.handle_events(event)

    def update(self, dt):
        if hasattr(self, 'player'):
            self.player.update(dt, self.game_scene.collidables)
            self.game_scene.update(dt, exclude=self.player)
        else:
            self.game_scene.update(dt)
        if hasattr(self, 'player'):
            collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
            for coin in collected_coins:
                self.game_scene.all_entities.remove(coin) 
                print("Coin collected!")

             # --- NEW: Play the sound ---
                if self.coin_sound:
                    self.coin_sound.play()

            # Check for collision with enemies
            hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hit_enemies:
                if self.hit_sound:
                    self.hit_sound.play()
                self.reset()
                print("Hit an enemy!")
                self.done = True
                self.next_state = "MAIN_MENU"
                return


    def draw(self, screen):
        screen.fill((173, 216, 230)) 
        self.game_scene.draw(screen)

    def reset(self):
        print("Player died! Resetting level...")
        # Create a fresh, empty scene and sprite groups
        self.game_scene = Scene()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Reload the level from the saved path
        if self.current_level_path:
            self.load_level(self.current_level_path)