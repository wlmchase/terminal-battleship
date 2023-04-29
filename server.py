### IMPORTS ###
try:
    import cPickle as pickle
except:
    import pickle
import socket
from _thread import *
from game import Game


"""
COMP4911 - Computer Networks
Final Project - Terminal based Battleship

:date 21 April 2022
:author (Wallace) Mackenzie Chase

This is the server of the networked game
It requires the game class to create and maintain games
"""

# set to local host but can be changed to actual host
server = "127.0.0.1"
port = 5555

# create a socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.bind((server, port))
except socket.error as e:
    str(e)

socket.listen(2)
print("Server ready, waiting for connection")

games = {}
clientID = 0
HEADER_SIZE = 10 # header size for packet buffer

# receives data from a client
def receive_data(client):
    full_message = b'' # message in bytes
    new_message = True
    while True:
        message = client.recv(16) # receive 16 bytes
        if new_message:
            message_length = int(message[:HEADER_SIZE])
            new_message = False

        full_message += message

        if len(full_message) - HEADER_SIZE == message_length:
            data = pickle.loads(full_message[HEADER_SIZE:]) # unpack message
            break

    return data

# send data to the client
def send_data(client, data):
    data_to_send = pickle.dumps(data) # serialize data
    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8") # get data size
    try:
        client.send(data_size + data_to_send)
    except socket.error as e:
        print(e)

# create a thread, a new game which 2 players can join
def threadGame(client, player, gameID):
    global clientID
    client.send(str.encode(str(player))) # send client their player number

    while True:
        try:
            data = receive_data(client)
            print(data)

            if gameID in games: # game is still alive
                game = games[gameID]

                if not data:
                    break
                else:
                    if data == "reset": # reset the game
                        game.reset()
                    elif data != "get":
                        if type(data) == list: # expecting ship_positions and player grids
                            if game.player_placed_ships(player) == False: # players are in setup phase
                                game.set_ship_positions(player, data) # set ship_placements
                            else:
                                game.set_grid(player, data) # set player grids
                        elif type(data) == tuple: # expecting coordinates for shots
                            game.play(player, data)

                    send_data(client, game) # send client updated instance of the game

            else: # game is not alive
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameID]
        print("Closing game", gameID)
    except:
        pass
    clientID -= 1
    client.close()


# Entry point of the server
while True:
    client, ip = socket.accept() # Get client and ip
    print("Connected: ", ip)

    clientID += 1
    player = 0 # Player 1
    gameID = (clientID - 1) // 2
    if clientID % 2 == 1: # Need another player to start a game
        games[gameID] = Game(gameID)
        print("Starting new game")
    else:
        games[gameID].is_ready = True # game is ready
        games[gameID].toss_coin() # Toss coin for which player will start
        games[gameID].in_setup_phase() # game is now in setup phase
        player = 1 # Player 2

    start_new_thread(threadGame, (client, player, gameID)) # starts a game thread with 2 players
