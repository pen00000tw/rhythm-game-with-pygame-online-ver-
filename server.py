import socket
from _thread import *
import sys

server = "192.168.1.104"
port = 5555
currentPlayer = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

catch = ['disconnect','disconnect']

def threaded_client(conn, player):
    global currentPlayer
    conn.send(str.encode('連接成功'))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            catch[player] = data
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = catch[0]
                else:
                    reply = catch[1]
                print("Received: ", data)
                print("Sending : ", reply)
            conn.send(str.encode(reply))
        except:
            break
    print("Lost connection")
    conn.close()
    currentPlayer -= 1

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1