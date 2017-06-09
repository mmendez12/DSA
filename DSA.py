import numpy as np


class Player:
    
    def __init__(self, name):
        self.name = name
        self.bag = []
        self.stock = []
        self.position = -1
        self.direction = 1
        self.on_board = True

    def transfer_bag(self):
        self.stock.extend(self.bag)
        self.bag = []
    
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
        self.bag.append(board.road[self.position])
        board.road[self.position] = make_empty_chip()
    
    def show_bag(self):
        print('idx: level')
        for i, chip in enumerate(self.bag):
            print('{}: {}'.format(i, chip.level))
    
    @property
    def is_onboard(self):
        return self.position >= 0
    
    @property
    def is_back(self):
        return (not self.is_onboard) and (self.direction == -1)
    
    def __repr__(self):
        return "Player(name={}, bag={}, stock={}, position={})".format(self.name, self.bag, self.stock, self.position)

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
        return "Chip(level={}), value={})".format(self.level, self.value)


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


def make_empty_chip():
    return Chip(level=0, value=0)


def roll_dice():
    return np.random.randint(low=1, high=4, size=2).sum()


if __name__ == '__main__':

    class Game:

        def __init__(self, submarine, board, players):

            self.board = board
            self.players = players
            self.players_in_submarine = []
            self.submarine = submarine


            n_round = 3

            for cur_round in range(n_round):
                print('Round {}'.format(cur_round))

                while (self.submarine.air > 0) or (any(player.on_board for player in self.players)):

                    for player in self.players:
                        print('{} turn'.format(player.name))

                        if player.is_back:
                            continue

                        #reduce_air
                        self.submarine.reduce_air(player)

                        if (player.direction == 1) and player.on_board:
                            if input("Going back? (y/n)").lower() == 'y':
                                player.direction = -1

                        #roll dice
                        dice_roll = roll_dice()
                        player.move(dice_roll, self.board)

                        cur_chip = self.board.road[player.position]

                        if not cur_chip.is_empty:
                            if input('Take level {} chip? (y/n)'.format(cur_chip.level)).lower() == 'y':
                                player.take_chip(board)
                        elif (cur_chip.is_empty) and (player.bag):
                            player.show_bag()
                            while True:
                                chip_idx = input('Drop chip?\nType a number or n')
                                if chip_idx == 'n':
                                    break
                                elif not chip_idx.isdigit():
                                    print('Input is not a digit')
                                    continue
                                elif chip_idx not in [range(len(player.bag))]:
                                    print('Input not in index')
                                    continue
                                else:
                                    self.board.road[player.position] = player.bag.pop(chip_idx)
                                    break

    # for i in zip(*[list(range(board.road_len)), board.tile_status, [c.level for c in board.road]]):
    #     print (i)

    # Game(submarine=Submarine(), board=board, players=players)