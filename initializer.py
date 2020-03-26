import random
from constants import *
from DSA import Chip


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
    row_idx = int(idx / N_COL)
    last_col_idx = N_COL - 1

    if row_idx % 2 == 0:
        # even rows: place chips from left to right
        col_idx = idx % N_COL
    else:
        # odd rows: place chips from right to left
        col_idx = last_col_idx - (idx % N_COL)

    return row_idx, col_idx


def loc_to_pos(row, col):
    x = MARGIN_WIDTH + col * (CHIP_SIZE + SPACE_SIZE)
    y = MARGIN_HEIGHT + row * (CHIP_SIZE + SPACE_SIZE)

    return [int(e) for e in (x, y)]


def init_chips_and_pos():
    CHIPS = []

    for value in range(CHIP_MAX_VALUE + 1):
        level = int(value / N_LEVEL) + 1
        CHIPS.append(Chip(level, value))
        CHIPS.append(Chip(level, value))

    random.shuffle(CHIPS)
    CHIPS.sort(key=lambda x: x.level)

    POS_DICT = {}
    for i in range(len(CHIPS)):
        chip_loc = get_chip_loc(i)
        pos = loc_to_pos(chip_loc[0], chip_loc[1])
        # pos[1] += i * SPACE_SIZE
        POS_DICT[i] = pos


    return CHIPS, POS_DICT


if __name__ == "__main__":
    init_chips_and_pos()
