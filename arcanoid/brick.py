import pygame

class Brick:
    def __init__(self, x, y, color, health=1):
        self.rect = pygame.Rect(x, y, 70, 20)
        self.color = color
        self.health = health

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.health == 2:
            pygame.draw.rect(screen, (169,169,169), self.rect, 2)  # Серый контур для блока с 2 касаниями