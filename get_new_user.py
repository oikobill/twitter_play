# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
import oauth2
from urllib.parse import parse_qs
from keys import *
import json
from google_maps_api import get_geocoordinates

# Authentication stuff
def oauth_req(url, key, secret, http_method="GET", post_body=b"", http_headers=None):
    consumer = oauth2.Consumer(key=APP_KEY, secret=APP_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def get_new_user(user_id):
    user = oauth_req("https://api.twitter.com/1.1/users/show.json?user_id="+user_id, TWITTER_KEY, TWITTER_SECRET)
    user = json.loads(user.decode("utf-8"))
    ID = user['id_str']
    favourites_count = user['favourites_count']
    followers_count = user['followers_count']
    friends_count = user['friends_count']
    lang = user['lang']
    location = user['location']
    name = user['name']
    screen_name = user['screen_name']
    statuses_count = user['statuses_count']
    verified = user['verified']

    # hit Google Maps APIs
    lat, lon = get_geocoordinates(location)

    return (ID, favourites_count, followers_count, friends_count, location, lat, lon, name, screen_name, statuses_count, verified)