
# coding: utf-8

# In[433]:

import numpy as np
import random


# In[491]:

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
        
        while n_step:
            self.position += self.direction
            
            if not board.is_occupied(self.position): 
                n_step -= 1

        self.position = min(self.position, board.road_len)
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
        return f"Player(name={self.name}, bag={self.bag}, stock={self.stock}, position={self.position})"


# In[492]:

class Submarine:
    
    def __init__(self):
        self.air = 25
            
    def reduce_air(self, player):
        n_chip = len(player.bag)
        self.air = max(0, self.air - n_chip)
        return self.air
    
    def __repr__(self):
        return f"Submarine(air={self.air})"


# In[510]:

class Chip:
    
    def __init__(self, level, value):
        self.level = level
        self.value = value
        
    @property
    def is_empty(self):
        return self.level == 0
        
    def __repr__(self):
        return f"Chip(level={self.level}), value={self.value})"


# In[511]:

class Board:
    
    def __init__(self, chip_dict):
        self.road_len = sum(len(l) for l in chip_dict.values()) 
        self.tile_status = [0] * self.road_len
        self.road = []
        
        
        for level in range(1, 5):
            chips = chip_dict[level][:]
            random.shuffle(chips)
            
            self.road.extend(chips)
            
    def is_occupied(self, idx):
        return self.tile_status[idx] == 1

    def __repr__(self):
        return ", ".join([chip.level for chip in self.road])


# In[512]:

# class Deck:
    
#     def __init__


# In[513]:

CHIPS = {}
# CHIP_VALUES = [(i+1, j+4*i) for i in range(4) for j in range(4)]

# for level, value in CHIP_VALUES:
#     CHIPS.append(Chip(level, value))
#     CHIPS.append(Chip(level, value))

for level in range(4):
    chips = []
    for value in range(4):
        value = value + 4 * level
        chip = Chip(level + 1, value)
        chips.append(chip)
        chips.append(chip)
    
    CHIPS[level + 1] = chips


# In[514]:

def make_empty_chip():
    return Chip(level=0, value=0)


# In[515]:

def roll_dice():
    return np.random.randint(low=1, high=4, size=2).sum()


# In[516]:

board = Board(CHIPS)


# In[517]:

# def finish_roundb


# In[518]:

players = [Player('Player {}'.format(i)) for i in range(1, 5)]


# In[519]:

players[0].is_back


# In[522]:

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
                            chip_idx = input('Drop chip?\n{}\Type a number or n'.format(bag_str))
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


# In[504]:

# def plot_gameboard(board, players):
#     for player in players:
#         print(player)


# In[505]:

# import numpy as np


# In[509]:

for i in zip(*[list(range(board.road_len)), board.tile_status, [c.level for c in board.road]]):
    print (i)


# In[507]:

# plot_gameboard(board, players)


# In[508]:

Game(submarine=Submarine(), board=board, players=players)


# In[338]:

t = input()


# In[ ]:

t


# In[346]:

t = 1
if t:
    print('hello')


# In[358]:

'1'.isdigit()


# In[359]:

l = []


# In[ ]:

l.pop()

