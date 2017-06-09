import sys
import random
from collections import defaultdict

from DSA import Board, Chip, Submarine, make_empty_chip, Player, roll_dice
import pygame as pg

from constants import *
from graphics import *


def screen_controls(surface, player):
    player_font = pg.font.SysFont('Sans Serif', 12)
    label = player_font.render(str(player), 1, (255, 255, 255))
    label_rect = label.get_rect()
    label_rect.bottomright = (BOARD_WIDTH, BOARD_HEIGHT)
    surface.blit(label, label_rect.topleft)



def main():

    # init variables
    fpsClock = pg.time.Clock()

    tiles = [ChipGraphix(chip, POS_DICT[i], LEVEL_COLOR[chip.level]) for i, chip in enumerate(CHIPS)]
    players = [PlayerGraphix(color, PLAYER_NAME_TEMPLATE.format(i), i) for i, color in enumerate([RED, GREEN, BLUE])]
    board = Board(tiles)

    # init graphics
    pg.init()
    pg.display.set_caption('DSA!')
    BOARD_SURF = pg.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    current_player_idx = 0

    # main loop
    while True:
        BOARD_SURF.fill((0, 0, 0))
        current_player = players[current_player_idx]
        screen_controls(BOARD_SURF, current_player)

        for e in board.road + players:
            e.draw(BOARD_SURF)

        for event in pg.event.get():
            # quit pg
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # roll dice
            if event.type == pg.MOUSEBUTTONDOWN:
                dice_roll = roll_dice()
                print(dice_roll)

                current_player.move(dice_roll, board)

                current_player.x, current_player.y = tiles[current_player.position].rect.center
                current_player_idx = (current_player_idx + 1) % len(players)

        pg.display.update()

        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
