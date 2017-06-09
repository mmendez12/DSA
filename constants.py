from collections import defaultdict
from DSA import Chip
# from myutil import *
import random

def get_chip_loc(idx):
    """
    :param idx:
    :return: the location of the chip on the grid

     >>> place_chip_on_board(3)
     (0, 3)
     >>> place_chip_on_board(4)
     (1, 3)
     >>> place_chip_on_board(5)
     (1, 2)
     >>> place_chip_on_board(8)
     (2, 0)
     >>> place_chip_on_board(9)
     (2, 1)
    """
    row_idx = int(idx/N_COL)

    if row_idx % 2 == 0:
        col_idx = idx % N_COL
    else:
        col_idx = (N_COL - 1) - (idx % N_COL)

    return row_idx, col_idx


def loc_to_pos(row, col):
    x = MARGIN_WIDTH + col * (CHIP_SIZE + SPACE_SIZE)
    y = MARGIN_HEIGHT + row * (CHIP_SIZE + SPACE_SIZE)

    return [int(e) for e in (x, y)]


BOARD_WIDTH = 300
BOARD_HEIGHT = 300
CHIP_SIZE = 20
SPACE_SIZE = 5
N_CHIP = 4*8
N_COL = 4
N_ROW = 8
CHIP_MAX_VALUE = 15
N_LEVEL = 4

PLAYER_NAME_TEMPLATE = 'Player {}'
PLAYER_TOKEN_RADIUS = 5
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLAYER_INIT_SPACE = 20

MARGIN_WIDTH = (BOARD_WIDTH - (N_COL * CHIP_SIZE + SPACE_SIZE * (N_COL - 1))) / 2
MARGIN_HEIGHT = (BOARD_HEIGHT - (N_ROW * CHIP_SIZE + SPACE_SIZE * (N_ROW - 1))) / 2

LEVEL_COLOR = [(255, 255, 255), (172, 218, 207), (43, 206, 175), (8, 170, 139), (0, 65, 105)]

CHIPS = []

for value in range(CHIP_MAX_VALUE + 1):
    level = int(value / N_LEVEL) + 1
    CHIPS.append(Chip(level, value))
    CHIPS.append(Chip(level, value))

random.shuffle(CHIPS)
CHIPS.sort(key=lambda x: x.level)

POS_DICT = {i: loc_to_pos(*get_chip_loc(i)) for i in range(len(CHIPS))}
