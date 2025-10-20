import pygame
from state_machine import State
from scene import Scene
from ui_element import TextLabel, Button
from entity import Entity, Player, Coin, Enemy

class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.menu_scene = Scene()

        title = TextLabel(285, 120, "ProtoPlay", 50, (255, 255, 255))
        start_button = Button(325, 250, 150, 50, "Start", self.start_game)
        quit_button = Button(325, 320, 150, 50, "Quit", self.quit_game)
        footer = TextLabel(350, 500, "By Weeeol", 20, (255, 255, 255))

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

class GameOverState(State):
    def __init__(self):
        super().__init__()
        self.game_over_scene = Scene()

        title = TextLabel(260, 120, "Game Over", 50, (255, 255, 255))
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
        screen.fill((50, 20, 20))
        self.game_over_scene.draw(screen)


class GameplayState(State):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.score = 0
        self.score_label = TextLabel(x=10, y=10, text=f"Score: {self.score}", font_size=24, color=(255, 255, 255))
        self.health_label = TextLabel(x=10, y=40, text="", font_size=24, color=(255, 255, 255))

        self.levels = ["levels/level_1.txt", "levels/level_2.txt", "levels/level_3.txt"]
        self.current_level_index = 0
        
        self.game_scene = Scene()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.current_level_path = None

        self.is_paused = False
        self.pause_scene = Scene()
        
        self.pause_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.pause_overlay.fill((0, 0, 0, 150)) 

        pause_title = TextLabel(300, 150, "Paused", 50, (255, 255, 255))
        resume_button = Button(325, 250, 150, 50, "Resume", self.resume_game)
        menu_button = Button(325, 320, 150, 50, "Main Menu", self.quit_to_menu)
        
        self.pause_scene.add_ui_element(pause_title)
        self.pause_scene.add_ui_element(resume_button)
        self.pause_scene.add_ui_element(menu_button)


# --- Load the sound effect ---
        try:
            self.coin_sound = pygame.mixer.Sound("assets/coin_collect.wav")
            self.hit_sound = pygame.mixer.Sound("assets/enemy_hit.wav")
        except pygame.error as e:
            print(f"Couldn't load coin sound: {e}")
            self.coin_sound = None
            self.hit_sound = None


        # Load the level from the file
        self.load_level(self.levels[self.current_level_index])
    
    def resume_game(self):
        self.is_paused = False
    
    def quit_to_menu(self):
        self.is_paused = False
        self.reset()
        self.current_level_index = 0
        self.next_state = "MAIN_MENU"
        self.done = True

    def load_level(self, file_path):
        self.game_scene = Scene()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.game_scene.add_ui_element(self.score_label)
        self.game_scene.add_ui_element(self.health_label)
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
                             self.health_label.set_text(f"Health: {self.player.health}")

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
                
        if self.is_paused:
            self.pause_scene.handle_events(event)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    if hasattr(self, 'player'):
                        self.player.jump()
            self.game_scene.handle_events(event)

    def update(self, dt):
        if self.is_paused:
            self.pause_scene.update(dt)
            return 
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

             # --- Play the sound ---
                if self.coin_sound:
                    self.coin_sound.play()
                
                self.score += 10
                self.score_label.set_text(f"Score: {self.score}")
            
            if not self.coins:
                self.go_to_next_level()

            # Check for collision with enemies
            hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hit_enemies:
                enemy = hit_enemies[0]
                self.player.take_damage(1)
                self.health_label.set_text(f"Health: {self.player.health}")
                if self.hit_sound:
                    self.hit_sound.play()

                dx = self.player.rect.centerx - enemy.rect.centerx
                dy = self.player.rect.centery - enemy.rect.centery

                
                if abs(dx) > abs(dy):
                    if dx > 0: 
                        self.player.rect.x += 50 # Knock right
                    else:
                        self.player.rect.x -= 50 # Knock left
                else:
                    if dy > 0:
                        self.player.rect.y += 50 # Knock down
                    else: # Player is above the enemy
                        self.player.rect.y -= 50 # Knock up
                if self.player.health <= 0:
                    print("You ran out of health! Game Over.")
                    self.reset() # Reset the level data first
                    print("Hit an enemy!")
                    self.done = True
                    self.next_state = "GAME_OVER" 
                    return

    def go_to_next_level(self):
        self.current_level_index += 1
        
        if self.current_level_index < len(self.levels):
            print(f"Loading level {self.current_level_index + 1}...")
            self.load_level(self.levels[self.current_level_index])
        else:
            print("You won the game!")
            self.current_level_index = 0
            self.reset()
            self.done = True
            self.next_state = "MAIN_MENU"

    def draw(self, screen):
        screen.fill((173, 216, 230)) 
        self.game_scene.draw(screen)
        if self.is_paused:
            screen.blit(self.pause_overlay, (0, 0))
            self.pause_scene.draw(screen)

    def reset(self):
        print("Player died! Resetting level...")
        self.score = 0
        self.game_scene = Scene()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        if self.current_level_path:
            self.load_level(self.current_level_path)

        self.score_label.set_text(f"Score: {self.score}")