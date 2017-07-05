from flask import Flask
from flask import render_template, jsonify
from google_maps_api import get_geocoordinates
import sqlite3
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def index():
    geo_data = get_geo_data(10)
    print(geo_data)
    return render_template("index.html", map_data=json.dumps(geo_data))

def get_geo_data(n=10):
    conn = sqlite3.connect("tweets.db")
    c = conn.cursor()
    g = list(pd.read_sql_query("SELECT lat, lon, location from users;", conn).dropna().sample(n).values)
    g.insert(0, ['Lat', 'Long', 'Name'])
    g = [list(i) for i in g]
    return g

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



