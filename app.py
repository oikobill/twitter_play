from flask import Flask
from flask import render_template, jsonify, request
from google_maps_api import get_geocoordinates
import sqlite3
import pandas as pd
import numpy as np
import json
try:
    import _thread # multithreading in Python 2
except:
    import thread

app = Flask(__name__)

streamer = None

@app.route('/')
def index():
    #geo_data = get_geo_data(10)
    #print(geo_data)
    return render_template("index.html") # , map_data=json.dumps(geo_data))

@app.route('/', methods=['POST'])
def get_search_item():
    """ Get search term from the front end and spawn listener """
    search_term = request.form['search_item']

    # Here we need to make a new thread that we can work with

    return search_term

def start_streamer(search_term):
    """Starts the streamer, works in the background"""
    auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
    auth.set_access_token(TWITTER_KEY,TWITTER_SECRET)
    api = tweepy.API(auth)

    # makes streamer have global scope so that we can terminate it externally
    global streamer 

    streamer = Streamer()

    stream = tweepy.Stream(auth=api.auth, 
        listener=streamer)

    stream.filter(track=['python'])

# def get_geo_data(n=10):
#     conn = sqlite3.connect("tweets.db")
#     c = conn.cursor()
#     g = list(pd.read_sql_query("SELECT lat, lon, location from users;", conn).dropna().sample(n).values)
#     g.insert(0, ['Lat', 'Long', 'Name'])
#     g = [list(i) for i in g]
#     return g

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





