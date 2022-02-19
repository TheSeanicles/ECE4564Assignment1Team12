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

    key = Fernet.generate_key()
    f = Fernet(key)
    b = bytes(refinedtweetval2, 'utf-8')
    token = f.encrypt(b)
    hashy = hashlib.md5(token)
    print(hashy.hexdigest().encode('utf-8')) #b'473f3046b669911ef4d936e03b02e16a'
    sendlist = [key, token, hashy.hexdigest().encode('utf-8')]
    senddata = pickle.dumps(sendlist)

    print(key) #b'pS8RfDNRH2LF8L-fkM_kz3z-oX2iNxlrsRjoeIDi7vE='
    print(f) #<cryptography.fernet.Fernet object at 0x7f1e1ea34588>
    print(b) #b'what is a test?'
    print(token) #b'gAAAAABiEXepDJEnLe80cNqX0-XdPi1_jupNw3U4HgqP_DjkayeNfptUQyU7IjeXFqPMzlx2ty7hl_xZCPE2TEFD-BBJrRJoCw=='
    print(sendlist) #[b'pS8RfDNRH2LF8L-fkM_kz3z-oX2iNxlrsRjoeIDi7vE=', b'gAAAAABiEXepDJEnLe80cNqX0-XdPi1_jupNw3U4HgqP_DjkayeNfptUQyU7IjeXFqPMzlx2ty7hl_xZCPE2TEFD-BBJrRJoCw==', b'473f3046b669911ef4d936e03b02e16a']
    print(senddata) #b'\x80\x03]q\x00(C,pS8RfDNRH2LF8L-fkM_kz3z-oX2iNxlrsRjoeIDi7vE=q\x01CdgAAAAABiEXepDJEnLe80cNqX0-XdPi1_jupNw3U4HgqP_DjkayeNfptUQyU7IjeXFqPMzlx2ty7hl_xZCPE2TEFD-BBJrRJoCw==q\x02C 473f3046b669911ef4d936e03b02e16aq\x03e.'

    print('Waiting for connection')
    Response = ClientSocket.recv(socketSize)
    Input = refinedtweetval2
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))
    ClientSocket.close()
