from tweepy import StreamListener
import sqlite3
import time
import numpy as np
import requests

from app.api.google_maps_api import get_geocoordinates
from app.api.get_new_user import get_new_user

class Streamer(StreamListener):
    """My Listener for looking at Twitter"""

    insert_command_tweets = "INSERT INTO tweets(ID, content, created_at, lang, user_id) VALUES(?, ?, ?, ?, ?);"
    insert_command_users = "INSERT INTO users(ID, favourites_count, followers_count, friends_count, location, lat, lon, name, screen_name, statuses_count, verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    insert_command_hashtags = "INSERT INTO hashtags(name) VALUES(?)"
    insert_command_taggings = "INSERT INTO taggings(tweet_id, hashtag_id, index_start, index_end) VALUES(?, ?, ?, ?)"
    insert_command_mentions = "INSERT INTO mentions(tweet_id, user_id) VALUES(?, ?)"

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

        # add taggings
        self.add_taggings(entities, ID)

        # add mentions
        self.add_mentions(entities, ID)

        print("Tweet detected")

        if self.check_db_size():
            """If specified DB size exceeded, stop the process"""
            return False

    def on_error(self, status_code):
        print("Exited with error code {}".format(status_code))
        # If rate has been exceeded then just sleep for 1 hr
        if status_code==88:
            time.sleep(3600)

    def flatten(self, lst):
            return [i[0] for i in lst]

    def add_mentions(self, entities, tweet_id):
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

        user_mentions = entities["user_mentions"]

        for u in user_mentions:
            user_id = u["id_str"]

            # check if user already exists in the database
            user_list = self.flatten(c.execute("SELECT ID from users;"))
            if user_id not in user_list:
                new_user_data = get_new_user(user_id)
                c.execute(self.insert_command_users, new_user_data)
                

            # insert into the mentions relation
            c.execute(self.insert_command_mentions, (tweet_id, user_id))

        conn.commit()
        conn.close()

    def add_taggings(self, entities, tweet_id):

        def process_hashtags(hashtag_dict):
            """Takes in a dictionary of hashtags and returns 
            (hashtag_name, start_index, end_index)
            """
            hashtag_name = "#"+hashtag_dict['text']
            start_index, end_index = hashtag_dict['indices']

            return hashtag_name, start_index, end_index
        
        hashtags_found = []

        for h in entities["hashtags"]:
            tup = process_hashtags(h)
            hashtags_found.append(tup)

        for hashtag, index_start, index_end in hashtags_found:
            hashtag_id = self.add_hashtags(hashtag)
            conn = sqlite3.connect('tweets.db')
            c = conn.cursor()
            c.execute(self.insert_command_taggings, (tweet_id, hashtag_id, index_start, index_end))
            conn.close()

    def add_hashtags(self, hashtag):
        """ Looks up a new hashtag on the table and creates one if it does not exist"""

        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

        hashtag_list = list(c.execute("SELECT name from hashtags"))

        if not hashtag in self.flatten(hashtag_list):
            c.execute(self.insert_command_hashtags, (hashtag,)) # throws error
            conn.commit()

        lst  = list(c.execute("SELECT ID FROM hashtags WHERE name=="+"'"+hashtag+"'"))[0][0]
        conn.close()
        return lst

    def check_db_size(self):
        """Returns True if number of users is more than 20,000"""
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

        lst = list(c.execute("SELECT COUNT(*) FROM users"))[0][0]>20000

        conn.close()
        return lst

    def add_db_tweets(self, data):
        """Given a row of data, adds it to the tweets DB"""
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()
        c.execute(self.insert_command_tweets, data)
        conn.commit()
        conn.close()

    def add_db_users(self, user):
        """Given a particular user, saves his info to a DB"""
        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

        ID = user.id_str
        favourites_count = user.favourites_count
        followers_count = user.followers_count
        friends_count = user.friends_count
        lang = user.lang
        location = user.location
        name = user.name
        screen_name = user.screen_name
        statuses_count = user.statuses_count
        verified = user.verified

        # make a Google API call to get the data for the lat and lon
        lat, lon = get_geocoordinates(location)

        data = (ID, favourites_count, followers_count, friends_count, location, lat, lon, name, screen_name, statuses_count, verified)

        # make sure the user is not already in the DB
        id_list = list(c.execute("SELECT ID from users"))

        if not ID in np.array(id_list).flatten():
            c.execute(self.insert_command_users, data)
            conn.commit()

        conn.close()
