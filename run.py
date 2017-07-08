import tweepy
from keys import *
from Listener import Streamer

auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(TWITTER_KEY,TWITTER_SECRET)
api = tweepy.API(auth)

streamer = Streamer()

stream = tweepy.Stream(auth=api.auth, 
	listener=streamer)

stream.filter(track=['python'])