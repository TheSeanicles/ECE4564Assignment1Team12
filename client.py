import tweepy as tw
from cryptography.fernet import Fernet
import hashlib
import socket
import pickle
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

HOST = cfg["client"]["host"]
PORT = cfg["client"]["port"]

client = tw.Client(bearer_token=cfg["client"]["bearer_token"])

query = '#ECE4564T12 -is:retweet'

# Name and path of the file where you want the Tweets written to
file_name = 'tweets.txt'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for tweet in tw.Paginator(client.search_recent_tweets, query=query,tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000):
    tweetval = tweet.text
    refinedtweetval1 = tweetval.replace('#ECE4564T12 ', '')#these 3 remove the hashtag part and any leftover whitespaces
    refinedtweetval2 = refinedtweetval1.replace(' #ECE4564T12', '')
    key = Fernet.generate_key()
    f = Fernet(key)
    b = bytes(refinedtweetval2, 'utf-8')
    token = f.encrypt(b)
    hashy = hashlib.md5(token)
    print(hashy.hexdigest().encode('utf-8'))
    sendlist = [key, token, hashy.hexdigest().encode('utf-8')]
    senddata = pickle.dumps(sendlist)
    s.connect((HOST, PORT))
    s.send(senddata)
    s.close()
