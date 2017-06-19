import numpy as np
import copy

class Player:
    
    def __init__(self, name):
        self.name = name
        self.bag = []
        self.stock = []
        self.position = -1
        self.direction = 1
        # self.on_board = True

    def transfer_bag(self):
        self.stock.extend(self.bag)
        self.bag = []

    @property
    def total_score(self):
        return sum(chip.value for chip in self.bag)
    
    def move(self, dice_roll, board):
        n_chip = len(self.bag)
        n_step = max(0, dice_roll - n_chip)
        
        board.tile_status[self.position] = 0

        while n_step > 0:
            next_step = self.position + self.direction

            if next_step > board.last_free_tile:
                break

            if not board.is_occupied(next_step):
                n_step -= 1

            self.position = next_step

        self.position = min(self.position, len(board.road))
        board.tile_status[self.position] = 1
        
    def take_chip(self, board):
        current_chip = board.road[self.position]
        self.bag.append(current_chip)

        new_chip = copy.copy(current_chip)
        new_chip.level = 0
        new_chip.value = 0
        new_chip.color = (255, 255, 255)

        board.road[self.position] = new_chip
    
    def go_back(self):
        self.direction = -1

    # def
    
    @property
    def is_onboard(self):
        return self.position >= 0
    
    @property
    def is_back(self):
        return (self.position < 0) and (self.direction == -1)

    @property
    def is_start(self):
        return (not self.is_onboard) and (self.direction == 1)
    
    def __repr__(self):
        return "Player(name={}, bag={}, stock={}, position={})".format(
            self.name, self.bag, self.stock, self.position)

    def __str__(self):
        s = "Player: {} - bag: {} - 1: {} - 2: {} - 3: {} - 4: {}"
        levels = [chip.level for chip in self.bag]
        counts = [levels.count(i) for i in range(1, 5)]

        return s.format(self.name, len(self.bag), *counts)


class Submarine:
    
    def __init__(self):
        self.air = 25
            
    def reduce_air(self, player):
        n_chip = len(player.bag)
        self.air = max(0, self.air - n_chip)
        return self.air
    
    def __repr__(self):
        return "Submarine(air={})".format(self.air)


class Chip:
    
    def __init__(self, level, value):
        self.level = level
        self.value = value
        
    @property
    def is_empty(self):
        return self.level == 0
        
    def __repr__(self):
        return "Chip(level={}, value={})".format(self.level, self.value)


class Board:
    
    def __init__(self, chips):
        self.tile_status = [0] * len(chips)
        self.road = chips

    def is_occupied(self, idx):
        return self.tile_status[idx] == 1

    @property
    def last_free_tile(self):
        return ''.join(map(str, self.tile_status)).rfind('0')

    def __repr__(self):
        return ", ".join([chip.level for chip in self.road])


def roll_dice():
    return np.random.randint(low=1, high=4, size=2).sum()


if __name__ == '__main__':
    pass