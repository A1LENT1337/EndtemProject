import pygame
import random


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = [random.choice([-4, 4]), -4]

    def move(self):
        self.rect.move_ip(self.speed[0], self.speed[1])

    def bounce_x(self):
        self.speed[0] = -self.speed[0]

    def bounce_y(self):
        self.speed[1] = -self.speed[1]

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)
