# Using:
# https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
# https://www.geeksforgeeks.org/python-create-a-simple-assistant-using-wolfram-alpha-api/
#
import yaml
import wolframalpha
import socket
import os
from _thread import *

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

ServerSocket = socket.socket()
host = cfg["server"]["host"]
port = cfg["server"]["port"]
app_id = cfg["server"]["app_id"]
socketSize = cfg["server"]["socketSize"]
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('CONNECTED'))
    while True:
        data = connection.recv(socketSize)
        if not data:
            break
        question = data.decode('utf-8')
        client = wolframalpha.Client(app_id)
        if not question:
            break
        res = client.query(question)
        reply = 'Answer: ' + next(res.results).text
        connection.sendall(str.encode(reply))
    connection.close()
    print ('DISCONNECTED')

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
