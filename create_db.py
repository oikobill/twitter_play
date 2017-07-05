import sqlite3

conn = sqlite3.connect('tweets.db')
c = conn.cursor()

# Reset database, drop all tables if they exist

drop_table_tweets = """DROP TABLE IF EXISTS tweets"""
drop_table_users = """DROP TABLE IF EXISTS users"""
drop_table_entities = """DROP TABLE IF EXISTS entities"""

c.execute(drop_table_tweets)
c.execute(drop_table_users)
c.execute(drop_table_entities)

# Create all the tables with the appropriate schema

create_table_tweets = """ CREATE TABLE tweets(
			ID varchar PRIMARY KEY,
			text varchar,
			created_at timestamp,
			lang varchar,
			user_id varchar,
			FOREIGN KEY(user_id) REFERENCES users(ID)
			)
			"""
create_table_users = 	""" 
			CREATE TABLE users(
			ID varchar PRIMARY KEY,
			created_at timestamp,
			description varchar,
			favourites_count int,
			followers_count int,
			friends_count int,
			lang varchar,
			location varchar,
			lat float,
			lon float,
			name varchar,
			screen_name varchar,
			statuses_count int,
			url varchar,
			verified bool
			)
			"""
c.execute(create_table_tweets)
c.execute(create_table_users)

conn.commit()
conn.close()
