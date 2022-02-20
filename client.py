import tweepy as tw
from cryptography.fernet import Fernet
import hashlib
import socket
import pickle
import yaml
import time
import sys

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

ClientSocket = socket.socket()
host = cfg["client"]["host"]
port = cfg["client"]["port"]
socketSize = cfg["client"]["socketSize"]

if len(sys.argv) > 1:
    for argument in sys.argv:
        if str(argument) == '-sp':
            pass
            port = sys.argv[sys.argv.index(argument) + 1]
        elif str(argument) == '-z':
            pass
            socketSize = sys.argv[sys.argv.index(argument) + 1]

try:
    ClientSocket.connect((host, port))
    print('[Client ' + str(time.time()) + '] -- Connecting to ' + host + ' on port ' + str(port))
    Response = ClientSocket.recv(socketSize)
except socket.error as e:
    print(str(e))

client = tw.Client(bearer_token=cfg["client"]["bearer_token"])

query = '#ECE4564T12 -is:retweet'

# Name and path of the file where you want the Tweets written to
file_name = 'tweets.txt'

print('[Client ' + str(time.time()) + '] -- Listening for tweets from Twitter API that contain questions')
for tweet in tw.Paginator(client.search_recent_tweets, query=query,tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000):
    tweetval = tweet.text
    refinedtweetval1 = tweetval.replace('#ECE4564T12 ', '')#these 3 remove the hashtag part and any leftover whitespaces
    refinedtweetval2 = refinedtweetval1.replace(' #ECE4564T12', '')
    print('[Client ' + str(time.time()) + '] -- New question found: ', end ='')
    print(refinedtweetval2)

    key = Fernet.generate_key()
    print('[Client ' + str(time.time()) + '] -- Generated Encryption Key: ', end ='')
    print(key)
    f = Fernet(key)
    b = bytes(refinedtweetval2, 'utf-8')
    token = f.encrypt(b)
    print('[Client ' + str(time.time()) + '] -- Cipher Text: ', end ='')
    print(token)
    hashy = hashlib.md5(token)
    sendlist = [key, token, hashy.hexdigest().encode('utf-8')]
    print('[Client ' + str(time.time()) + '] -- Question payload: ', end ='')
    print(sendlist)
    senddata = pickle.dumps(sendlist)
    print('[Client ' + str(time.time()) + '] -- Sending question: ', end ='')
    print(senddata)
    ClientSocket.send(senddata)

    Response = ClientSocket.recv(socketSize)
    print('[Client ' + str(time.time()) + '] -- Received data: ', end ='')
    print(Response)
    (key_response, encrypted_response, hashy_response) = pickle.loads(Response)
    print('[Client ' + str(time.time()) + '] -- Decrypt Key: ', end ='')
    print(key_response)
    f_response = Fernet(key_response)
    checkHashy = hashlib.md5(encrypted_response)
    checkHashy = checkHashy.hexdigest()
    encrypted_response = encrypted_response.decode("utf-8")
    if checkHashy == hashy_response.decode("utf-8"):
        notEncrypted = f_response.decrypt(encrypted_response.encode())
        answer = notEncrypted.decode("utf-8")
        print('[Client ' + str(time.time()) + '] -- Plain Text: ', end ='')
        print(answer)
    ClientSocket.close()
