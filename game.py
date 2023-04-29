### IMPORTS ###
import random
from copy import deepcopy

"""
COMP4911 - Computer Networks
Final Project - Terminal based Battleship

:date 21 April 2022
:author (Wallace) Mackenzie Chase

This is the Game class which contains all the functionality needed to operate a game
"""


class Game:

    # initialize
    def __init__(self, id):
        self.id = id  # game ID
        self.player_turn = 0
        self.is_ready = False
        self.is_setup_phase = False
        self.p1_ready = False
        self.p2_ready = False
        self.p1_placed_ships = False
        self.p2_placed_ships = False
        self.p1_grid = [[]]
        self.p2_grid = [[]]

        # the grid shown so p2 so they don't see the enemy's ships
        self.p1_hidden_grid = [["~" for x in range(11)] for y in range(11)]
        # the grid shown so p1 so they don't see the enemy's ships
        self.p2_hidden_grid = [["~" for x in range(11)] for y in range(11)]

        self.p1_ship_positions = [[]]
        self.p2_ship_positions = [[]]
        self.p1_ship_sunk_count = 0
        self.p2_ship_sunk_count = 0

    # resets a game if needed
    def reset(self):
        self.id = id  # game ID
        self.player_turn = 0
        self.is_ready = False
        self.is_setup_phase = False
        self.p1_ready = False
        self.p2_ready = False
        self.p1_placed_ships = False
        self.p2_placed_ships = False
        self.p1_grid = [[]]
        self.p2_grid = [[]]

        # the grid shown so p2 so they don't see the enemy's ships
        self.p1_hidden_grid = [["~" for x in range(11)] for y in range(11)]
        # the grid shown so p1 so they don't see the enemy's ships
        self.p2_hidden_grid = [["~" for x in range(11)] for y in range(11)]

        self.p1_ship_positions = [[]]
        self.p2_ship_positions = [[]]
        self.p1_ship_sunk_count = 0
        self.p2_ship_sunk_count = 0

    # Checks if a game is over
    def is_over(self):
        if self.p1_ship_sunk_count == 5 or self.p2_ship_sunk_count == 5:
            return True
        else:
            return False

    # Updates the sunken ship count
    def update_ship_sunk(self, player):
        if player == 0:
            self.p1_ship_sunk_count += 1
        else:
            self.p2_ship_sunk_count += 1

    # Makes a play
    def play(self, player, coordinate):
        row, col = coordinate
        if self.check_hit(player, row, col):
            print("Ship hit")
            if self.check_sunk(player, row, col):
                print("Ship sunk")
                self.update_ship_sunk(player)
        self.player_turn = not self.player_turn  # changes player turn

    # Checks if a move is a hit or miss
    def check_hit(self, player, row, col):
        if player == 0:
            if self.p2_grid[row][col] == "O":  # Hit
                self.p2_grid[row][col] = "X"
                self.p2_hidden_grid[row][col] = "X"
                return True
            else:  # Miss
                self.p2_grid[row][col] = "@"
                self.p2_hidden_grid[row][col] = "@"
                return False
        else:
            if self.p1_grid[row][col] == "O":  # Hit
                self.p1_grid[row][col] = "X"
                self.p1_hidden_grid[row][col] = "X"
                return True
            else:  # Miss
                self.p1_grid[row][col] = "@"
                self.p1_hidden_grid[row][col] = "@"
                return False

    # Checks if a ship has sunk
    def check_sunk(self, player, row, col):
        sunk = True
        if player == 0:
            for i in range(len(self.p2_ship_positions)):
                start_row = self.p2_ship_positions[i][0]
                end_row = self.p2_ship_positions[i][1]
                start_col = self.p2_ship_positions[i][2]
                end_col = self.p2_ship_positions[i][3]
                if start_row <= row <= end_row and start_col <= col <= end_col:
                    print("found ship")
                    for r in range(start_row, end_row):
                        for c in range(start_col, end_col):
                            if self.p2_grid[r][c] != "X":  # Not sunk
                                sunk = False
                    return sunk
        else:
            for i in range(len(self.p1_ship_positions)):
                start_row = self.p1_ship_positions[i][0]
                end_row = self.p1_ship_positions[i][1]
                start_col = self.p1_ship_positions[i][2]
                end_col = self.p1_ship_positions[i][3]
                if start_row <= row <= end_row and start_col <= col <= end_col:
                    print("found ship")
                    for r in range(start_row, end_row):
                        for c in range(start_col, end_col):
                            if self.p1_grid[r][c] != "X":  # Not sunk
                                sunk = False
                    return sunk

    # The game is in setup phase
    def in_setup_phase(self):
        self.is_setup_phase = True

    # Boolean if the game is in setup phase
    # Checks if both players are ready first
    def is_in_setup_phase(self):
        self.both_ready()
        return self.is_setup_phase

    # Game is ready
    def is_ready(self):
        self.is_ready = True

    # Boolean if game is ready
    def connected(self):
        return self.is_ready

    # Boolean if both players are done placing ships
    def both_ready(self):
        if (self.p1_ready == True) and (self.p2_ready == True):
            self.is_setup_phase = False

    # Gets the player turn
    def get_turn(self):
        if self.player_turn == 0:
            return 0
        else:
            return 1

    # Gets the winner
    def winner(self):
        winner = -1
        if self.p1_ship_sunk_count == 5:
            winner = 0
        if self.p2_ship_sunk_count == 5:
            winner = 1

        return winner

    # Tosses a coin to see who starts shooting first
    def toss_coin(self):
        coin = random.random()
        if coin < 0.5:
            self.player_turn = 0
        else:
            self.player_turn = 1

    # Set the player's grids
    def set_grid(self, player, grid):
        if player == 0:
            self.p1_grid = deepcopy(grid)
            self.p1_ready = True
        else:
            self.p2_grid = deepcopy(grid)
            self.p2_ready = True

    # Gets the enemy grid
    def get_enemy_grid(self, player):
        if player == 0:
            return self.p2_hidden_grid
        else:
            return self.p1_hidden_grid

    # Gets the player's grid
    def get_my_grid(self, player):
        if player == 0:
            return self.p1_grid
        else:
            return self.p2_grid

    # Gets if the player has placed their ships - used for the server to differentiate between getting ship placements
    # and player grids
    def player_placed_ships(self, player):
        if player == 0:
            return self.p1_placed_ships
        else:
            return self.p2_placed_ships

    # Sets the ship positions
    def set_ship_positions(self, player, data):
        if player == 0:
            self.p1_ship_positions = deepcopy(data)
            self.p1_placed_ships = True
        else:
            self.p2_ship_positions = deepcopy(data)
            self.p2_placed_ships = True
