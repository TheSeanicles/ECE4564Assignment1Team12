# Using:
# https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
#
import yaml
import socket
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)
ClientSocket = socket.socket()
host = cfg["client"]["host"]
port = cfg["client"]["port"]
socketSize = cfg["client"]["socketSize"]

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(socketSize)
while True:
    Input = input('Ask Question: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()
