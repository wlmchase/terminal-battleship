### IMPORTS ###
import socket
try:
    import cPickle as pickle
except:
    import pickle

HEADER_SIZE = 10 # header size for packet buffer

"""
COMP4911 - Computer Networks
Final Project - Terminal based Battleship

:date 21 April 2022
:author (Wallace) Mackenzie Chase

This is the network class used by the client to communicate with the server.
"""


class Network:

    # initialize the network
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.ip = (self.server, self.port)
        self.player = self.connect()

    # Get the player
    def get_player(self):
        return self.player

    # Get if the game is connected
    def connect(self):
        try:
            self.client.connect(self.ip)
            return self.client.recv(2048 * 2).decode()
        except:
            pass

    # Send data to the server and get a response
    def send_data(self, data):
        data_to_send = pickle.dumps(data) # serialized data
        data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8") # data size
        try:
            self.client.send(data_size + data_to_send) # send it to the server

            package = self.receive_data() # receive a response (updated instance of the game)
            return package

        except socket.error as e:
            print(e)

    # Receive data from the server
    def receive_data(self):
        full_message = b'' # receive as bytes
        new_message = True
        while True:
            message = self.client.recv(16) # receive in chunks of 16 bytes
            if new_message:
                message_length = int(message[:HEADER_SIZE])
                new_message = False

            full_message += message

            if len(full_message) - HEADER_SIZE == message_length:
                data = pickle.loads(full_message[HEADER_SIZE:])
                break

        return data
