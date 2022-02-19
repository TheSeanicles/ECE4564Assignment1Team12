import tweepy as tw
from cryptography.fernet import Fernet
import hashlib
import socket
import pickle
import yaml
import time

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
    print('[Client ' + str(time.time()) + '] -- New question found: ' + refinedtweetval2)

    key = Fernet.generate_key() # encrypt key
    f = Fernet(key)
    b = bytes(refinedtweetval2, 'utf-8') #key
    token = f.encrypt(b) #encrypted b
    hashy = hashlib.md5(token) #md5 checksum
    print(hashy.hexdigest().encode('utf-8')) #print checksum
    sendlist = [key, token, hashy.hexdigest().encode('utf-8')] #
    senddata = pickle.dumps(sendlist) #dumps sendlist

    print('Waiting for connection')
    Response = ClientSocket.recv(socketSize)
    Input = refinedtweetval2
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    ClientSocket.close()
