import pygame

class Paddle:
    def __init__(self, width, height):
        self.rect = pygame.Rect(400 - width // 2, 570, width, height)
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.move_ip(self.speed, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
