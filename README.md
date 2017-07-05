# twitter_play

Streams data using a particular tag from the tweeter feed. Populates a database and creates a map of the locations of the users using Google's Geocoding and Maps APIs.

## Instructions on how to run:

1. run ```create_db.py``` that creates a SQLite database.

2. run ```run.py``` which starts the streaming and populates the DB. After the streaming is done terminate the process.

3. run ```app.py``` and head to your local browser. You should see the map appearing.


NOTE: You will need to generate your own ```keys.py``` that holds all the keys for the API calls.
