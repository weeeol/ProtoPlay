import pygame
from states.state import State
from core.scene import Scene
from ui.elements import TextLabel, Button
from entities.player import Player
from entities.enemy import Enemy
from entities.items import Coin
from entities.entity import Entity
from core.engine import settings
from core import resource_manager

class GameplayState(State):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.score = 0
        self.score_label = TextLabel(x=10, y=10, text=f"Score: {self.score}", font_size=24, color=settings.COLOR_TEXT)
        self.health_label = TextLabel(x=10, y=40, text="", font_size=24, color=settings.COLOR_TEXT)

        self.levels = ["levels/level_1.txt", "levels/level_2.txt", "levels/level_3.txt"]
        self.current_level_index = 0
        self.level_grid = []
        self.edit_mode = False
        self.current_brush = '#'
        
        self.game_scene = Scene()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.current_level_path = None

        self.is_paused = False
        self.pause_scene = Scene()
        
        self.pause_overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.pause_overlay.fill(settings.COLOR_PAUSE_OVERLAY) 

        pause_title = TextLabel(300, 150, "Paused", 50, settings.COLOR_TEXT)
        resume_button = Button(325, 250, 150, 50, "Resume", self.resume_game)
        menu_button = Button(325, 320, 150, 50, "Main Menu", self.quit_to_menu)
        
        self.pause_scene.add_ui_element(pause_title)
        self.pause_scene.add_ui_element(resume_button)
        self.pause_scene.add_ui_element(menu_button)


        # --- Load the sound effect ---
        self.coin_sound = resource_manager.get_sound("assets/coin_collect.wav")
        self.hit_sound = resource_manager.get_sound("assets/enemy_hit.wav")

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
        
        self.level_grid = []
        try:
            with open(file_path, 'r') as f:
                for y, line in enumerate(f): 
                    row = list(line.rstrip('\n'))
                    self.level_grid.append(row)
                    for x, char in enumerate(row): 
                        pos_x = x * settings.TILE_SIZE
                        pos_y = y * settings.TILE_SIZE

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

    def save_level(self):
        if not self.current_level_path: return
        with open(self.current_level_path, 'w') as f:
            for row in self.level_grid:
                line = "".join(row).rstrip()
                f.write(line + "\n")
        print(f"Level saved to {self.current_level_path}")

    def place_entity(self, grid_x, grid_y, brush):
        while len(self.level_grid) <= grid_y:
            self.level_grid.append([' '] * (settings.SCREEN_WIDTH // settings.TILE_SIZE))
        while len(self.level_grid[grid_y]) <= grid_x:
            self.level_grid[grid_y].extend([' '] * (grid_x - len(self.level_grid[grid_y]) + 1))
            
        self.remove_entity_at(grid_x, grid_y)
        self.level_grid[grid_y][grid_x] = brush
        
        pos_x = grid_x * settings.TILE_SIZE
        pos_y = grid_y * settings.TILE_SIZE
        
        if brush == '#':
            block = Entity(pos_x, pos_y, "assets/block.png")
            self.game_scene.add_entity(block, collidable=True)
        elif brush == 'P':
            self.player = Player(x=pos_x, y=pos_y, bounds=(self.screen_width, self.screen_height))
            self.game_scene.add_entity(self.player)
        elif brush == 'C':
            coin = Coin(pos_x, pos_y)
            self.game_scene.add_entity(coin)
            self.coins.add(coin)
        elif brush == 'E':
            enemy = Enemy(pos_x, pos_y)
            self.game_scene.add_entity(enemy, collidable=False)
            self.enemies.add(enemy)

    def remove_entity_at(self, grid_x, grid_y):
        pos_x = grid_x * settings.TILE_SIZE
        pos_y = grid_y * settings.TILE_SIZE
        for entity in list(self.game_scene.all_entities):
            if hasattr(entity, 'rect') and entity.rect.x == pos_x and entity.rect.y == pos_y:
                self.game_scene.all_entities.remove(entity)
                if entity in self.game_scene.collidables:
                    self.game_scene.collidables.remove(entity)
                if entity in self.coins:
                    self.coins.remove(entity)
                if entity in self.enemies:
                    self.enemies.remove(entity)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
                
        if self.edit_mode and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if mx > 210 and mx < settings.SCREEN_WIDTH - 410:
                grid_x = mx // settings.TILE_SIZE
                grid_y = my // settings.TILE_SIZE
                self.place_entity(grid_x, grid_y, self.current_brush)
                
        if self.is_paused:
            self.pause_scene.handle_events(event)
        else:
            self.game_scene.handle_events(event)

    def update(self, dt):
        if self.is_paused or self.edit_mode:
            if self.is_paused:
                self.pause_scene.update(dt)
            return 
        
        # Simple update call for scene (exclude hack removed)
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
        screen.fill(settings.COLOR_BG_GAMEPLAY) 
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
