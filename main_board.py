import sys
import random
from collections import defaultdict

from DSA import Board, Chip, Submarine, make_empty_chip, Player, roll_dice
import pygame

from constants import *
from graphics import *


def main():

    # init variables
    tiles = [ChipGraphix(chip, POS_DICT[i], LEVEL_COLOR[chip.level]) for i, chip in enumerate(CHIPS)]
    players = [PlayerGraphix(color, PLAYER_NAME_TEMPLATE.format(i), i) for i, color in enumerate([RED, GREEN, BLUE])]
    board = Board(tiles)

    # init graphics
    pygame.init()
    pygame.display.set_caption('DSA!')
    BOARD_SURF = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    current_player_idx = 0

    # main loop
    while True:
        BOARD_SURF.fill((0, 0, 0))

        for e in board.road + players:
            e.draw(BOARD_SURF)

        for event in pygame.event.get():
            # quit pygame
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # roll dice
            if event.type == pygame.MOUSEBUTTONDOWN:
                dice_roll = roll_dice()
                print(dice_roll)

                current_player = players[current_player_idx]
                current_player.move(dice_roll, board)

                current_player.x, current_player.y = tiles[current_player.position].rect.center
                current_player_idx = (current_player_idx + 1) % len(players)

        pygame.display.update()


if __name__ == '__main__':
    main()
