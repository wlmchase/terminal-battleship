### IMPORTS ###
import time
from network import Network
import re

### GLOBAL VARIABLES ###
# client side boolean if player placed ships
placed_ships = False
# List of ship positions - sent to server to verify if sunk
ship_positions = []
# player's grid, fill with water
myGrid = [["~" for x in range(11)] for y in range(11)]
# enemy's grid, fill with water
enemyGrid = [["~" for z in range(11)] for t in range(11)]

"""
COMP4911 - Computer Networks
Final Project - Terminal based Battleship

:date 21 April 2022
:author (Wallace) Mackenzie Chase

This is the client side of the networked game
It requires the Networks class to connect to the server
"""

# If player wins
def print_won():
    print("Nicely done! You WIN!")


# If player loses
def print_lost():
    print("Better luck next time. You Lost")


# Gets the row and column of the coordinate
def get_row_and_col(coordinate):
    row_list = re.findall("\d", coordinate)  # Gets numerics
    column_list = re.findall("[aA-jJ]", coordinate)  # Get alphas

    # Converts row string to integer
    s = [str(integer) for integer in row_list]
    a_string = "".join(s)
    row: int = int(a_string)

    # Converts col string to integer
    s = [str(integer) for integer in column_list]
    a_string = "".join(s)
    col: int = ord(a_string.lower()) - 97

    return row, col


# Verifies valid coordinate
def check_valid_coordinate(coordinate):
    coordinate.replace(" ", "")
    if len(coordinate) != 2:
        return False

    row_list = re.findall("\d", coordinate)  # Gets all numerics
    if len(row_list) != 1:
        return False
    column_list = re.findall("[aA-jJ]", coordinate)  # gets all alphas in correct range
    if len(column_list) != 1:
        return False

    # Convert row string to integer
    s = [str(integer) for integer in row_list]
    a_string = "".join(s)
    row = int(a_string)

    # Convert col string to integer
    s = [str(integer) for integer in column_list]
    a_string = "".join(s)
    col = ord(a_string.lower()) - 97

    # Check row and col are in bounds of grid
    if row < 0 or row > 10 or col < 0 or col > 10:
        return False
    else:
        if enemyGrid[row][col] != "~":
            print("You have already shot this coordinate!")
            return False
        else:
            return True


# PLayer is making a move
def make_move(player, game):
    print("It's now your turn!")
    print("_____________")
    print("\n Enemy Grid\n")
    print_grid(enemyGrid)
    coordinate = input("Please enter the coordinate of where you would like to shoot: ")
    if not check_valid_coordinate(coordinate):
        print("Invalid coordinate, try again")
        make_move(player, game)
    else:
        return get_row_and_col(coordinate)


# Player waits their turn
def wait_turn():
    print("_____________")
    print("\n My Grid\n")
    print_grid(myGrid)
    print("Other player is making a move")
    time.sleep(10)


# Verifies valid ship direction
def check_valid_direction(direction):
    direction.replace(" ", "")
    if len(direction) != 1:
        return False
    else:
        if re.match("h|H|v|V", direction) is None:
            return False
        else:
            return True


# Gets the direction of a player's ship placement
def get_direction():
    direction = input("Which direction do you want your ship? (v for Vertical , h for Horizontal): ")
    if check_valid_direction(direction) == False:
        print("Invalid direction, try again")
        direction = get_direction()
        return direction
    else:
        return direction


# Verifies a player's desired ship placement is valid
def check_valid_ship_placement(ship_size, row, col, direction):
    if ship_size == 0:
        return True
    else:
        if direction.lower() == "v":
            if row + ship_size > 10:  # out of bounds
                return False
        elif direction.lower() == "h":
            if col + ship_size > 10:  # out of bounds
                return False

        if myGrid[row][col] == "O":  # Ship is already there
            return False

        if direction.lower() == "v":
            check_valid_ship_placement(ship_size - 1, row + 1, col, direction)
        else:
            check_valid_ship_placement(ship_size - 1, row, col + 1, direction)


# Adds a ship placement to ship_positions and myGrid
def add_ship_to_fleet(ship_size, row, col, direction):
    starting_row = row
    starting_col = col
    if direction.lower() == "v":
        end_row = row + ship_size
        end_col = col + 1
    else:
        end_row = row + 1
        end_col = col + ship_size

    global ship_positions
    ship_positions.append([starting_row, end_row, starting_col, end_col])

    for i in range(ship_size):
        myGrid[row][col] = "O"
        if direction.lower() == "v":
            row += 1
        else:
            col += 1


# Prompt player to place Carrier
def place_carrier():
    print("Let's start with the Carrier (5)")
    coordinate = input("What coordinate do you want to place your Carrier? (for example 0A): ")
    if not check_valid_coordinate(coordinate):
        print("Invalid coordinate, try again")
        place_carrier()
    else:
        direction = get_direction()
        row, col = get_row_and_col(coordinate)
        if check_valid_ship_placement(5, row, col, direction) == False:
            print("here")
            place_carrier()
        else:
            add_ship_to_fleet(5, row, col, direction)
    print_grid(myGrid)
    print("Placed Carrier successfully")


# Prompt player to place Battleship
def place_battleship():
    print("Next the Battleship (4)")
    coordinate = input("What coordinate do you want to place your Battleship? (for example 0A): ")
    if not check_valid_coordinate(coordinate):
        print("Invalid coordinate, try again")
        place_battleship()
    else:
        direction = get_direction()
        row, col = get_row_and_col(coordinate)
        if check_valid_ship_placement(4, row, col, direction) == False:
            place_battleship()
        else:
            add_ship_to_fleet(4, row, col, direction)
    print_grid(myGrid)
    print("Placed Battleship successfully")


# Prompt player to place Submarine
def place_submarine():
    print("Next the Submarine (3)")
    coordinate = input("What coordinate do you want to place your Submarine? (for example 0A): ")
    if not check_valid_coordinate(coordinate):
        print("Invalid coordinate, try again")
        place_submarine()
    else:
        direction = get_direction()
        row, col = get_row_and_col(coordinate)
        if check_valid_ship_placement(3, row, col, direction) == False:
            place_submarine()
        else:
            add_ship_to_fleet(3, row, col, direction)
    print_grid(myGrid)
    print("Placed Submarine successfully")


# Prompt player to place Cruiser
def place_cruiser():
    print("Next the Cruiser (3)")
    coordinate = input("What coordinate do you want to place your Cruiser? (for example 0A): ")
    if not check_valid_coordinate(coordinate):
        print("Invalid coordinate, try again")
        place_cruiser()
    else:
        direction = get_direction()
        row, col = get_row_and_col(coordinate)
        if check_valid_ship_placement(3, row, col, direction) == False:
            place_cruiser()
        else:
            add_ship_to_fleet(3, row, col, direction)
    print_grid(myGrid)
    print("Placed Cruiser successfully")


# Prompt player to place Destroyer
def place_destroyer():
    print("Finally the Destroyer (2)")
    coordinate = input("What coordinate do you want to place your Destroyer? (for example 0A): ")
    if not check_valid_coordinate(coordinate, enemyGrid):
        print("Invalid coordinate, try again")
        place_destroyer()
    else:
        direction = get_direction()
        row, col = get_row_and_col(coordinate)
        if check_valid_ship_placement(2, row, col, direction) == False:
            place_destroyer()
        else:
            add_ship_to_fleet(2, row, col, direction)
    print_grid(myGrid)
    print("Placed Destroyer successfully")


# When in setup phase, player places ships
def place_ships():
    print("_____________")
    print("\n Your Grid\n")
    print_grid(myGrid)

    print("This is your grid")
    print("Where do you want to place your battleships?")
    place_carrier()
    place_battleship()
    place_cruiser()
    place_submarine()
    place_destroyer()
    print("Placed ships successfully")
    global placed_ships
    placed_ships = True


# update player grid after shot
def update_grid():
    print("_____________")
    print("\n My Grid\n")
    print_grid(myGrid)


""" 
    Main loop of the game
    Looks for a game connecting to the server through the Network Class
    
    Checks if game is connected - both players are connected
    Checks if game is over - won or lost
    Checks if game is in setup phase - players need to place their ships
    Checks if it it player's turn - make a shot or wait
"""


def main():
    print("Trying to connect to a game...")
    run = True

    n = Network()
    player = int(n.get_player())
    print("You are player", player)
    print("Looking for opponent...")
    time.sleep(3)

    # Run until game is over or player quits/disconnects
    while run:

        try:
            # Gets the game
            game = n.send_data("get")
        except:
            run = False
            print("Couldn't get game")
            break

        # wait to be paired with another player
        if not game.connected():
            time.sleep(2)
            continue
        else:
            global myGrid
            global enemyGrid
            # Game is over
            if game.is_over():
                if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):  # Player Won
                    run = False
                    enemyGrid = game.get_enemy_grid(player)
                    print_grid(enemyGrid)
                    print_won()
                    time.sleep(5)
                    continue
                else:  # Player Lost
                    run = False
                    myGrid = game.get_my_grid(player)
                    print_grid(myGrid)
                    print_lost()
                    time.sleep(5)
                    continue
            # Game is in setup phase - players are placing their ships
            if game.is_in_setup_phase():
                if placed_ships:  # if player has placed their ships but enemy hasn't, wait
                    print("Waiting for other player to finish placing ships")
                    time.sleep(10)
                else:
                    place_ships()
                    n.send_data(ship_positions)
                    n.send_data(myGrid)
            # Game is in session
            else:
                myGrid = game.get_my_grid(player)
                enemyGrid = game.get_enemy_grid(player)
                if game.get_turn() == player:  # Player's turn
                    update_grid()
                    coordinate = make_move(player, game)
                    n.send_data(coordinate)
                else:  # wait for enemy to make a move
                    wait_turn()


# prints the menu screen
# goes to main() upon pressing Enter
def menu_screen():
    print("                                     |__\n"
          "                                     |\\/\n"
          "                                     ---\n"
          "                                     / | [\n"
          "                              !      | |||\n"
          "                            _/|     _/|-++'\n"
          "                        +  +--|    |--|--|_ |-\n"
          "                     { /|__|  |/\\__|  |--- |||__/\n"
          "                    +---------------___[}-_===_.'____                 /\\\n"
          "                ____`-' ||___-{]_| _[}-  |     |_[___\\==--            \\/   _\n"
          " __..._____--==/___]_|__|_____________________________[___\\==--____,------' .7\n"
          "|                                                                     BB-61/\n"
          " \\_________________________________________________________________________|\n"
          "  Matthew Bace\n")

    print("          _           _   _   _           _     _       \n"
          "         | |         | | | | | |         | |   (_)      \n"
          "         | |__   __ _| |_| |_| | ___  ___| |__  _ _ __  \n"
          "         | '_ \\ / _` | __| __| |/ _ \\/ __| '_ \\| | '_ \\ \n"
          "         | |_) | (_| | |_| |_| |  __/\\__ \\ | | | | |_) |\n"
          "         |_.__/ \\__,_|\\__|\\__|_|\\___||___/_| |_|_| .__/ \n"
          "                                               | |    \n"
          "                                               |_|   \n")

    print("The aim of the game is to sink the other player's ships before they sink yours.\n"
          "You will have 5 ships to place: CARRIER(5), BATTLESHIP(4), CRUISER(3), SUBMARINE(3), and DESTROYER(2).\n"
          "Ships can only be place horizontally or vertically. Ships cannot overlap each other.\n")
    input("Press Enter to continue...")
    main()


# prints the player's grid or enemy grid with added space for neat look
def print_grid(grid):
    print("_____________\n")
    print("     A     B     C     D     E     F     G     H     I     J   ")
    print("   ___________________________________________________________ ")
    print("  |     |     |     |     |     |     |     |     |     |     |")
    print_ships(grid)
    print_legend()


# prints the contents of the grids
def print_ships(grid):
    for x in range(0, 10):
        print(x, end="")
        for y in range(0, 10):
            print(" |  ", end="")
            print(grid[x][y], end="")
            print(" ", end="")

        print(" |")
        print("  |_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|", end="")
        if x != 9:
            print("\n  |     |     |     |     |     |     |     |     |     |     |")
        else:
            print("   ")
            print("     A     B     C     D     E     F     G     H     I     J   ")
            print("   ")


# prints the legend of symbols
def print_legend():
    print("'~' is water.\n"
          "'O' are your ships.\n"
          "'@' are misses.\n"
          "'X' are hits.\n")


# entry point for the client
while True:
    menu_screen()
