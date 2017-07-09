import sqlite3
import os

def create_db():
	# create db file
	os.remove("tweets.db")

	conn = sqlite3.connect('tweets.db')
	c = conn.cursor()

	# Reset database, drop all tables if they exist
	drop_table_tweets = """DROP TABLE IF EXISTS tweets"""
	drop_table_users = """DROP TABLE IF EXISTS users"""
	drop_table_hashtags = """DROP TABLE IF EXISTS hashtags"""
	drop_table_mentions = """DROP TABLE IF EXISTS mentions"""
	drop_table_taggings = """DROP TABLE IF EXISTS taggings"""

	c.execute(drop_table_tweets)
	c.execute(drop_table_users)
	c.execute(drop_table_hashtags)
	c.execute(drop_table_mentions)
	c.execute(drop_table_taggings)

	# Create all the tables with the appropriate schema

	create_table_users = 	""" 
				CREATE TABLE IF NOT EXISTS users(
				ID varchar PRIMARY KEY,
				name varchar NOT NULL,
				screen_name varchar NOT NULL,
				favourites_count int NOT NULL,
				followers_count int NOT NULL,
				friends_count int NOT NULL,
				location varchar,
				lat float, 
				lon float,			
				statuses_count NOT NULL,
				verified bool DEFAULT FALSE
				)
				"""

	create_table_tweets = """ 
				CREATE TABLE IF NOT EXISTS tweets(
				ID varchar PRIMARY KEY,
				content varchar NOT NULL,
				created_at timestamp NOT NULL,
				lang varchar NOT NULL,
				user_id varchar NOT NULL,
				FOREIGN KEY(user_id) REFERENCES users(ID) ON DELETE CASCADE
				)
				"""
	create_table_hashtags = """ 
				CREATE TABLE IF NOT EXISTS hashtags(
				ID INTEGER PRIMARY KEY autoincrement,
				name varchar NOT NULL
				)
				"""

	create_table_taggings = """ 
				CREATE TABLE IF NOT EXISTS taggings(
				ID INTEGER PRIMARY KEY autoincrement,
				tweet_id varchar NOT NULL,
				hashtag_id int NOT NULL,
				index_start int NOT NULL,
				index_end int NOT NULL,
				FOREIGN KEY(hashtag_id) REFERENCES hashtags(ID) ON DELETE CASCADE,
				FOREIGN KEY(tweet_id) REFERENCES tweets(ID) ON DELETE CASCADE
				)
				"""

	create_table_mentions = """ 
				CREATE TABLE IF NOT EXISTS mentions(
				ID INTEGER PRIMARY KEY autoincrement,
				tweet_id varchar NOT NULL,
				user_id varchar NOT NULL,
				FOREIGN KEY(user_id) REFERENCES users(ID) ON DELETE CASCADE,
				FOREIGN KEY(tweet_id) REFERENCES tweets(ID) ON DELETE CASCADE
				)
				"""

	c.execute(create_table_tweets)
	c.execute(create_table_users)
	c.execute(create_table_hashtags)
	c.execute(create_table_taggings)
	c.execute(create_table_mentions)

	conn.commit()
	conn.close()

create_db()