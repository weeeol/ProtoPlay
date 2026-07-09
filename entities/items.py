from entities.entity import Entity

class Coin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "assets/coin.png")
