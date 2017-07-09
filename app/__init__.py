from flask import Flask
from flask import render_template, jsonify, request
import sqlite3
import pandas as pd
import numpy as np
import json
import threading
from datetime import datetime, timedelta

from app.start_streamer import start_streamer
from app.api.google_maps_api import get_geocoordinates
 

app = Flask(__name__)

# Configurations
app.config.from_object('config')

stream = None
thread = None

@app.route('/')
def index():
    #geo_data = get_geo_data(10)
    #print(geo_data)

    return render_template("index.html") # , map_data=json.dumps(geo_data))

@app.route('/search_term/<search_term>')
def get_search_item(search_term):
    """ Get search term from the front end and spawn listener """
    try:
        global thread

        # stop streamer if exists
        if stream:
            stream.disconnect()

        # start streaming on a new thread
        thread = threading.Thread(target=start_streamer, args=(search_term,))
        thread.start()

        json_response = {"status":"success"}

    except:
        json_response = {"status":"failure"}

    return json.dumps(json_response)


@app.route('/time_plot/<time_window>')
def time_plot(time_window):
    """Retrieves the count for the number of tweets acquired in the past <time_window> seconds"""
    try:
        time_window = int(time_window)

        # make a connection and look up DB
        conn = sqlite3.connect("tweets.db")
        c = conn.cursor()

        t = datetime.now() - timedelta(seconds=time_window)
        part1 = """
        select COUNT(*)
        FROM tweets
        WHERE created_at > DATE('
        """
        t = t.strftime('%Y-%m-%d %H:%M:%S')   
        part2 = """'); """
        query = part1 + t + part2

        count = list(c.execute(query))[0][0]

        json_response = {"status":"success", "data":count}
    except:
        json_response = {"status":"failure"}

    return json.dumps(json_response)

# def get_geo_data(n=10):
#     conn = sqlite3.connect("tweets.db")
#     c = conn.cursor()
#     g = list(pd.read_sql_query("SELECT lat, lon, location from users;", conn).dropna().sample(n).values)
#     g.insert(0, ['Lat', 'Long', 'Name'])
#     g = [list(i) for i in g]
#     return g





