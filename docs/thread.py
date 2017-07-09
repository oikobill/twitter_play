import threading
import time
import tweepy
from Listener import Streamer
from keys import *
from create_db import create_db

stop = False
start_time = time.time()
stream = None



def start_streamer(search_term):
    """Starts the streamer, works in the background"""
    create_db()

    auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(TWITTER_KEY,TWITTER_SECRET)
    api = tweepy.API(auth)

    global stream

    # makes streamer have global scope so that we can terminate it externally
    streamer = Streamer()

    stream = tweepy.Stream(auth=api.auth, 
        listener=streamer)

    stream.filter(track=[search_term])

def fml():
    # Create new threads
    d = threading.Thread(target=start_streamer, args=("the",))
    d.start()


    for i in range(100):

        print("STEP 1")

        if time.time()-start_time>20:
            stream.disconnect()
            d.exit()
            break

        time.sleep(0.5)

    print ("Exited!")
