import pygame
import random
from pygame.math import Vector2

from utils.constants import CELL_NUMBER, CELL_SIZE

apple_image = pygame.image.load('graphics/apple.png')


class Fruit:

    def __init__(self):
        # Position
        self.randomize_position()

    def draw_food(self, window):
        # Create rectangle
        fruit_rect = pygame.Rect(
            self.position.x * CELL_SIZE - 3,
            self.position.y * CELL_SIZE - 3,
            CELL_SIZE,
            CELL_SIZE,
        )
        # Draw the rectangle
        window.blit(apple_image, fruit_rect)

    def randomize_position(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.position = Vector2(self.x, self.y)
        