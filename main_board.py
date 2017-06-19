import sys
import random
from collections import defaultdict

from DSA import Board, Chip, Submarine, Player, roll_dice
import pygame as pg

from constants import *
from graphics import *

ACTIONS = ['(b): go back', '(r): roll dice', '(t): take chip', '(d): drop chip', '(c): continue']

WHITE = (255, 255, 255)
GREY = (200, 200, 200)

INIT_ACTION_POS_Y = 100
ACTION_SPACE = 5

ACTION_COLORS_DICT = {False: GREY, True: WHITE}

class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.players_in_submarine = []
        self.submarine = Submarine()
        self.current_player_idx = 0
        self.round = 1
        self.dice_rolled = False
        self.just_took = False
        self.is_dropping = False
        self.just_dropped = False
        self.start = True
        self.end = False

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.dice_rolled = False
        self.just_took = False
        self.just_dropped = False

    def start_next_round(self):
        for player in self.players:
            player.transfer_bag()
            player.direction = 1
            player.position = -1

        no_empty_road = [chip for chip in self.board.road if not chip.is_empty]
        for i, chip in enumerate(no_empty_road):
            chip.rect.topleft = POS_DICT[i]

        self.board.road = no_empty_road
        self.round += 1

    def winner(self):

        self.players.sort(lambda p: p.total_score)
        max_score = self.players[-1]
        best_players = [p for p in self.players if p.total_score == max_score]

        if len(best_players) == 1:
            player_orders = self.players
        # else:
        #     for player in player_orders:
                # max_level


    @property
    def current_player(self):
        return self.players[self.current_player_idx]

    @property
    def current_chip(self):
        return self.board.road[self.current_player.position]

    @property
    def can_roll(self):
        return not self.dice_rolled

    @property
    def can_take(self):
        return self.dice_rolled and \
               not self.current_chip.is_empty and \
               not self.just_dropped

    @property
    def can_drop(self):
        return self.dice_rolled and \
               self.current_chip.is_empty and \
               bool(self.current_player.bag) and \
               not self.just_took

    @property
    def can_go_back(self):
        return self.can_roll and (self.current_player.direction == 1) and (self.current_player.position > 0)

    @property
    def can_continue(self):
        return self.dice_rolled



def screen_controls(surface, game):

    if game.end:
        # game.players.sort(key=lambda p: sum(), reverse=True)

    player_font = pg.font.SysFont('Sans Serif', DEFAULT_FONT_SIZE)
    label = player_font.render(str(game.current_player), 1, game.current_player.color)
    label_rect = label.get_rect()
    label_rect.topright = (BOARD_WIDTH, 0)
    surface.blit(label, label_rect.topleft)

    round_font = pg.font.SysFont('Sans Serif', DEFAULT_FONT_SIZE)
    round_label = round_font.render('Round {}'.format(game.round), 1, WHITE)
    round_rect = round_label.get_rect()
    round_rect.bottomleft = (0, BOARD_HEIGHT)
    surface.blit(round_label, round_rect.topleft)

    actions = [game.can_go_back, game.can_roll, game.can_take, game.can_drop, game.can_continue]

    for i, (action, b) in enumerate(zip(ACTIONS, actions)):
        try:
            action_font = pg.font.SysFont('Sans Serif', DEFAULT_FONT_SIZE)
            action_label = action_font.render(action, 1, ACTION_COLORS_DICT[b])
            surface.blit(action_label, (0, INIT_ACTION_POS_Y + (DEFAULT_FONT_SIZE + ACTION_SPACE)*i))
        except:
            print(i, action, b)

    if game.is_dropping:
        dropping_font = pg.font.SysFont('Sans Serif', DEFAULT_FONT_SIZE)
        dropping_label = dropping_font.render('Select level of chip to drop', 1, WHITE)
        dropping_rect = dropping_label.get_rect()
        dropping_rect.midtop = (BOARD_WIDTH/2, game.board.road[-1].rect.bottom + SPACE_SIZE)
        surface.blit(dropping_label, dropping_rect)



def main():

    # init variables
    fpsClock = pg.time.Clock()

    tiles = [ChipGraphix(chip, POS_DICT[i], LEVEL_COLOR[chip.level]) for i, chip in enumerate(CHIPS)]
    players = [PlayerGraphix(color, PLAYER_NAME_TEMPLATE.format(i), i) for i, color in enumerate([RED, GREEN, BLUE])]
    board = Board(tiles)

    game = Game(board, players)

    # init graphics
    pg.init()
    pg.display.set_caption('DSA!')
    BOARD_SURF = pg.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

    # main loop
    while True:
        BOARD_SURF.fill((0, 0, 0))
        screen_controls(BOARD_SURF, game)

        for e in board.road + players:
            e.draw(BOARD_SURF)

        if all(player.is_back for player in game.players) or game.submarine.air < 0:
            game.start_next_round()

        if game.round > 3:
            game.end = True

        if game.current_player.is_back:
            game.next_player()

        for event in pg.event.get():
            # quit pg
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # roll dice
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_r) and game.can_roll:
                    dice_roll = roll_dice()
                    print(dice_roll)
                    game.current_player.move(dice_roll, board)
                    if game.current_player.is_back:
                        game.current_player.move_to_submarine()
                    else:
                        x, y = tiles[game.current_player.position].rect.center
                        game.current_player.x, game.current_player.y = (x, y)
                    game.dice_rolled = True

                elif (event.key == pg.K_c) and game.can_continue:
                    game.next_player()

                elif (event.key == pg.K_b) and game.can_go_back:
                    game.current_player.go_back()

                elif (event.key == pg.K_t) and game.can_take:
                    game.current_player.take_chip(game.board)
                    game.just_took = True
                    pass

                elif (event.key == pg.K_d) and game.can_drop:
                    game.is_dropping = True

                elif (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4]) and game.is_dropping:
                    level_selected = [pg.K_1, pg.K_2, pg.K_3, pg.K_4].index(event.key) + 1
                    levels = [chip.level for chip in game.current_player.bag]

                    if not level_selected in levels:
                        break
                    else:
                        chip_index = levels.index(level_selected)
                        chip = game.current_player.bag.pop(chip_index)
                        chip.rect = game.current_chip.rect
                        game.board.road[game.current_player.position] = chip
                        game.is_dropping = False
                        game.just_dropped = True


        pg.display.update()

        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
