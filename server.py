# Using:
# https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
# https://www.geeksforgeeks.org/python-create-a-simple-assistant-using-wolfram-alpha-api/
#
import yaml
import wolframalpha
import socket
import os
from _thread import *
import time
import sys
from cryptography.fernet import Fernet
import hashlib
import pickle

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)
ServerSocket = socket.socket()
host = cfg["server"]["host"]
port = cfg["server"]["port"]
app_id = cfg["server"]["app_id"]
socketSize = cfg["server"]["socketSize"]
ThreadCount = 0

if len(sys.argv) > 1:
    for argument in sys.argv:
        if str(argument) == '-sip':
            pass
            host = sys.argv[sys.argv.index(argument) + 1]
        elif str(argument) == '-sp':
            pass
            port = sys.argv[sys.argv.index(argument) + 1]
        elif str(argument) == '-z':
            pass
            socketSize = sys.argv[sys.argv.index(argument) + 1]

try:
    ServerSocket.bind((host, port))
    print('[Server ' + str(time.time()) + '] -- Created socket at ' + host + ' on port ' + str(port))
except socket.error as e:
    print(str(e))

print('[Server ' + str(time.time()) + '] -- Listening for client connections')
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode('CONNECTED'))
    while True:
        data = connection.recv(socketSize)
        if not data:
            break

        (key, encryptedQuestion, hashy) = pickle.loads(data)
        f = Fernet(key)
        checkHashy = hashlib.md5(encryptedQuestion)
        checkHashy = checkHashy.hexdigest()
        encryptedQuestion = encryptedQuestion.decode("utf-8")
        if checkHashy == hashy.decode("utf-8"):
            notEncrypted = f.decrypt(encryptedQuestion.encode())
            question = notEncrypted.decode("utf-8")
            print('[Server ' + str(time.time()) + '] -- Plain Text: ' + question)

            client = wolframalpha.Client(app_id)
            if not question:
                break
            res = client.query(question)
            print('[Server ' + str(time.time()) + '] -- Sending question to WolframAlpha')
            answer = next(res.results).text
            print('[Server ' + str(time.time()) + '] -- Received answer from WolframAlpha: ' + answer)

            key_answer = Fernet.generate_key() # encrypt key
            f_answer = Fernet(key_answer)
            b_answer = bytes(answer, 'utf-8') #key
            encrypted_answer = f_answer.encrypt(b_answer) #encrypted b
            hashy_answer = hashlib.md5(encrypted_answer) #md5 checksum
            # print(hashy.hexdigest().encode('utf-8')) #print checksum
            sendlist_answer = [key_answer, encrypted_answer, hashy_answer.hexdigest().encode('utf-8')] #
            senddata_answer = pickle.dumps(sendlist_answer) #dumps sendlist
            connection.sendall(senddata_answer)

    connection.close()
    # print ('DISCONNECTED')

while True:
    Client, address = ServerSocket.accept()
    print('[Server ' + str(time.time()) + '] -- Accepted client connection from ' + address[0] + ' on port '+ str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    # print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
