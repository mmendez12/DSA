from DSA import Chip
import random


def get_chip_loc(idx):
    """
    :param idx:
    :return: the location of the chip on the grid

     >>> get_chip_loc(3)
     (0, 3)
     >>> get_chip_loc(4)
     (1, 3)
     >>> get_chip_loc(5)
     (1, 2)
     >>> get_chip_loc(8)
     (2, 0)
     >>> get_chip_loc(9)
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


FPS = 30
SCALE = 3
BOARD_WIDTH = 300 * SCALE
BOARD_HEIGHT = 300 * SCALE
CHIP_SIZE = 20 * SCALE
SPACE_SIZE = 5
N_CHIP = 4*8
N_COL = 4
N_ROW = 8
CHIP_MAX_VALUE = 15
N_LEVEL = 4

PLAYER_NAME_TEMPLATE = 'Player {}'
PLAYER_TOKEN_RADIUS = 5 * SCALE
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PLAYER_INIT_SPACE = 20 * SCALE

MARGIN_WIDTH = (BOARD_WIDTH - (N_COL * CHIP_SIZE + SPACE_SIZE * (N_COL - 1))) / 2
MARGIN_HEIGHT = (BOARD_HEIGHT - (N_ROW * CHIP_SIZE + SPACE_SIZE * (N_ROW - 1))) / 2

LEVEL_COLOR = [(255, 255, 255), (172, 218, 207), (43, 206, 175), (8, 170, 139), (0, 65, 105)]

CHIPS = []

DEFAULT_FONT_SIZE = 12 * SCALE

for value in range(CHIP_MAX_VALUE + 1):
    level = int(value / N_LEVEL) + 1
    CHIPS.append(Chip(level, value))
    CHIPS.append(Chip(level, value))

random.shuffle(CHIPS)
CHIPS.sort(key=lambda x: x.level)

POS_DICT = {i: loc_to_pos(*get_chip_loc(i)) for i in range(len(CHIPS))}
