import pygame
from entities.entity import Entity
from core.engine import settings

class Player(Entity):
    def __init__(self, x, y, bounds):
        super().__init__(x, y, "assets/player.png") 
        
        self.bounds = pygame.Rect(0, 0, bounds[0], bounds[1])
        self.hitbox = self.rect.inflate(-2, -2) 

        self.max_health = settings.PLAYER_MAX_HEALTH
        self.health = self.max_health

         # --- Physics Attributes ---
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.jumps_remaining = settings.PLAYER_MAX_JUMPS
        self.jump_key_pressed_last_frame = False
        self.last_hit_time = 0

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > settings.PLAYER_INVINCIBILITY_DURATION:
            self.health -= amount
            print(f"Player took damage! Health is now: {self.health}")
            self.last_hit_time = current_time

    def reset_health(self):
        self.health = self.max_health

    def update(self, dt):
        prev_x = self.rect.x
        prev_y = self.rect.y
        super().update(dt)

        collidables = self.scene.collidables if self.scene else []

        # --- Horizontal Movement & Jumping ---
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.velocity.x = settings.PLAYER_SPEED
            
        jump_key_pressed = keys[pygame.K_UP] or keys[pygame.K_SPACE]
        
        if self.on_ground:
            self.jumps_remaining = settings.PLAYER_MAX_JUMPS
            if jump_key_pressed:
                self.jump()
                self.jumps_remaining -= 1
        else:
            if jump_key_pressed and not self.jump_key_pressed_last_frame and self.jumps_remaining > 0:
                self.jump()
                self.jumps_remaining -= 1
                
        self.jump_key_pressed_last_frame = jump_key_pressed

        # --- Apply Gravity ---
        self.velocity.y += settings.GRAVITY * dt
        if self.velocity.y > 1000:
            self.velocity.y = 1000

        self.rect.x += self.velocity.x * dt
        self.hitbox.centerx = self.rect.centerx

        for sprite in collidables:
            if self.hitbox.colliderect(sprite.rect):
                if self.velocity.x < 0: # moving left
                    self.rect.left = sprite.rect.right - (self.rect.width - self.hitbox.width) / 2
                elif self.velocity.x > 0: # moving right
                    self.rect.right = sprite.rect.left + (self.rect.width - self.hitbox.width) / 2
                self.velocity.x = 0    
                self.hitbox.centerx = self.rect.centerx

        # Vertical movement based on velocity instead of keys (which the old code had left in)
        self.rect.y += self.velocity.y * dt
        self.hitbox.centery = self.rect.centery
        self.on_ground = False
            
        for sprite in collidables:
            if self.hitbox.colliderect(sprite.rect):
                if self.velocity.y >= 0: # Moving down (falling)
                    self.rect.bottom = sprite.rect.top + (self.rect.height - self.hitbox.height) / 2
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0: # Moving up (jumping)
                    self.rect.top = sprite.rect.bottom - (self.rect.height - self.hitbox.height) / 2
                    self.velocity.y = 0 # Bonked head
                self.hitbox.centery = self.rect.centery

        # Boundary Clamping
        if self.rect.left < self.bounds.left: self.rect.left = self.bounds.left
        if self.rect.right > self.bounds.right: self.rect.right = self.bounds.right
        if self.rect.top < self.bounds.top: self.rect.top = self.bounds.top
        if self.rect.bottom > self.bounds.bottom: self.rect.bottom = self.bounds.bottom

        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time < settings.PLAYER_INVINCIBILITY_DURATION:
            if (current_time // 100) % 2 == 0:
                self.image.set_alpha(150)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def jump(self):
        self.velocity.y = settings.PLAYER_JUMP_STRENGTH
