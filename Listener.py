from tweepy import StreamListener
import sqlite3
import time
import numpy as np
from google_maps_api import get_geocoordinates


class Streamer(StreamListener):
    """My Listener for looking at Twitter"""
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()

    insert_command_tweets = "INSERT INTO tweets(ID, text, created_at, lang, user_id) VALUES(?, ?, ?, ?, ?);"
    insert_command_users = "INSERT INTO users(ID, created_at, description, favourites_count, followers_count, friends_count, lang, location, lat, lon, name, screen_name, statuses_count, url, verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    def on_status(self, status):
        """Get all the information we need and throw into a DB"""
        ID = status.id_str
        contents = status.text
        coord = status.coordinates
        time = status.created_at
        lang = status.lang
        entities = status.entities
        user = status.user
        user_id = user.id_str
        source = status.source

        # add to tweets relation
        self.add_db_tweets((ID, contents, time, lang, user_id))

        # add to users relation
        self.add_db_users(user)

        print("Tweet detected")

        if self.check_db_size():
            """If specified DB size exceeded, stop the process"""
            return False

    def on_error(self, status_code):
        print("Exited with error code {}".format(status_code))
        # If rate has been exceeded then just sleep for 1 hr
        if status_code==88:
            time.sleep(3600)

    def check_db_size(self):
        """Returns True if number of users is more than 20,000"""
        return list(self.c.execute("SELECT COUNT(*) FROM users"))[0][0]>20000

    def add_db_tweets(self, data):
        """Given a row of data, adds it to the tweets DB"""
        self.c.execute(self.insert_command_tweets, data)
        self.conn.commit()

    def add_db_users(self, user):
        """Given a particular user, saves his info to a DB"""
        ID = user.id_str
        created_at = user.created_at
        description = user.description
        favourites_count = user.favourites_count
        followers_count = user.followers_count
        friends_count = user.friends_count
        lang = user.lang
        location = user.location
        name = user.name
        screen_name = user.screen_name
        statuses_count = user.statuses_count
        url = user.url
        verified = user.verified

        # make a Google API call to get the data for the lat and lon
        lat, lon = get_geocoordinates(location)

        data = (ID, created_at, description, favourites_count, followers_count, friends_count, lang, location,lat, lon, name, screen_name, statuses_count, url, verified)

        # make sure the user is not already in the DB
        id_list = list(self.c.execute("SELECT ID from users"))

        if not ID in np.array(id_list).flatten():
            self.c.execute(self.insert_command_users, data)
            self.conn.commit()

