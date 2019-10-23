"""simple client"""

import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('127.0.0.1', 8887))


clientsocket.send(str.encode('hello'))