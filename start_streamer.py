import tweepy
from keys import *
from Listener import Streamer

# function that starts a streamer for a particular thread
def start_streamer(search_term):
    """Starts the streamer, works in the background"""

    # authentication stuff
    auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(TWITTER_KEY,TWITTER_SECRET)
    api = tweepy.API(auth)

    global stream

    # makes streamer have global scope so that we can terminate it externally
    streamer = Streamer()

    stream = tweepy.Stream(auth=api.auth, 
        listener=streamer)

    stream.filter(track=[search_term])