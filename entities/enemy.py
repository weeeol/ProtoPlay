from entities.entity import Entity
from core.engine import settings

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/enemy.png")
        self.direction = 1
        self.start_x = float(x)
        self.exact_x = float(x)

    def update(self, dt):
        self.exact_x += settings.ENEMY_SPEED * self.direction * dt
        self.rect.x = round(self.exact_x)

        if abs(self.exact_x - self.start_x) >= settings.ENEMY_PATROL_RANGE:
            self.direction *= -1
