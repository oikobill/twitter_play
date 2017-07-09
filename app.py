from flask import Flask
from flask import render_template, jsonify, request
from google_maps_api import get_geocoordinates
import sqlite3
import pandas as pd
import numpy as np
import json
import threading
from start_streamer import start_streamer
from create_db import create_db

app = Flask(__name__)

stream = None
thread = None

@app.route('/')
def index():
    #geo_data = get_geo_data(10)
    #print(geo_data)

    return render_template("index.html") # , map_data=json.dumps(geo_data))

@app.route('/', methods=['POST'])
def get_search_item():
    """ Get search term from the front end and spawn listener """
    search_term = request.form['search_item']

    global thread

    # stop streamer if exists
    if stream:
        stream.disconnect()

    # start streaming on a new thread
    thread = threading.Thread(target=start_streamer, args=(search_term,))
    thread.start()

    return search_term

# def get_geo_data(n=10):
#     conn = sqlite3.connect("tweets.db")
#     c = conn.cursor()
#     g = list(pd.read_sql_query("SELECT lat, lon, location from users;", conn).dropna().sample(n).values)
#     g.insert(0, ['Lat', 'Long', 'Name'])
#     g = [list(i) for i in g]
#     return g

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





