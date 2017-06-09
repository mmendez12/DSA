from DSA import *
from constants import *
import pygame


class PlayerGraphix(Player):
    def __init__(self, color, name, index):
        Player.__init__(self, name)

        self.color = color
        self.radius = PLAYER_TOKEN_RADIUS
        self.x = (index + 1) * PLAYER_INIT_SPACE
        self.y = 20

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class ChipGraphix(Chip):
    def __init__(self, chip, pos, color, chip_size=CHIP_SIZE):
        Chip.__init__(self, chip.level, chip.value)

        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], chip_size, chip_size)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
