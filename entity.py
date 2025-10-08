import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__() 
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Entity):
    def __init__(self, x, y, bounds):
        super().__init__(x, y, "assets/player.png") 
        
        self.speed = 200
        self.bounds = pygame.Rect(0, 0, bounds[0], bounds[1])
        self.hitbox = self.rect.inflate(-2, -2) 

    def update(self, dt, collidables):
        prev_x = self.rect.x
        prev_y = self.rect.y

    # --- Horizontal Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt

        self.hitbox.centerx = self.rect.centerx

    # Check for horizontal collisions
        for sprite in collidables:
            if self.hitbox.colliderect(sprite.rect):
                if keys[pygame.K_LEFT]: 
                    self.rect.left = sprite.rect.right - (self.rect.width - self.hitbox.width) / 2
                elif keys[pygame.K_RIGHT]:
                    self.rect.right = sprite.rect.left + (self.rect.width - self.hitbox.width) / 2
                self.hitbox.centerx = self.rect.centerx

        # --- Vertical Movement ---
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt

        self.hitbox.centery = self.rect.centery
            
        # Check for vertical collisions
        for sprite in collidables:
            if self.hitbox.colliderect(sprite.rect):
                if keys[pygame.K_UP]:
                    self.rect.top = sprite.rect.bottom - (self.rect.height - self.hitbox.height) / 2
                elif keys[pygame.K_DOWN]:
                    self.rect.bottom = sprite.rect.top + (self.rect.height - self.hitbox.height) / 2
                self.hitbox.centery = self.rect.centery

        # Boundary Clamping
        if self.rect.left < self.bounds.left: self.rect.left = self.bounds.left
        if self.rect.right > self.bounds.right: self.rect.right = self.bounds.right
        if self.rect.top < self.bounds.top: self.rect.top = self.bounds.top
        if self.rect.bottom > self.bounds.bottom: self.rect.bottom = self.bounds.bottom


class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coin.png")

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/enemy.png")
        self.speed = 50
        self.direction = 1
        self.start_x = x
        self.patrol_range = 80

    def update(self, dt):
        self.rect.x += self.speed * self.direction * dt

          # --- NEW LOGIC TO TURN AROUND ---
        if abs(self.rect.x - self.start_x) >= self.patrol_range:
            # Flip the direction
            self.direction *= -1