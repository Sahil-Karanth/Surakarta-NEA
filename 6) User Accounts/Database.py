import sqlite3
import hashlib
import os
import binascii
from datetime import datetime

class Database:

    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        

    def create_users_table(self):
        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT,
                account_creation_date DATE,
                preferred_piece_colour TEXT,
                saved_game TEXT,
                PRIMARY KEY (username)
            );

            """

        )
        
        self.__conn.commit()


    def create_game_history_table(self):

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS game_history (
                game_id INTEGER,
                username TEXT ,
                game_date DATE,
                game_result TEXT,
                ai_difficulty TEXT,
                PRIMARY KEY (game_id)
                FOREIGN KEY (username) REFERENCES users(username)
            );

            """

        )

        self.__conn.commit()


    def create_AI_game_stats_table(self):

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS AI_game_stats (
                AI_difficulty TEXT,
                username TEXT,
                wins INTEGER,
                losses INTEGER,
                PRIMARY KEY (AI_difficulty, username)
                FOREIGN KEY (username) REFERENCES users(username)
            );

            """

        )

        self.__conn.commit()


    def create_friends_table(self):

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS friends (
                username TEXT,
                friend_username TEXT,
                status TEXT,
                PRIMARY KEY (username, friend_username)
                FOREIGN KEY (username) REFERENCES users(username)
                FOREIGN KEY (friend_username) REFERENCES users(username)
            );

            """

        )

        self.__conn.commit()

    def check_if_username_exists(self, username):
        self.__cursor.execute("SELECT username FROM users WHERE username = ?;", (username,))
        return self.__cursor.fetchone() != None
    
    def add_user(self, username, password, preferred_piece_colour):

        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)

        hashed_password = salt.hex() + hashed_password.hex()

        account_creation_date = datetime.now().strftime("%Y-%m-%d")

        saved_game = ""

        self.__cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);", (username, hashed_password, account_creation_date, preferred_piece_colour, saved_game))
        self.__conn.commit()

    def login(self, username, password):

        stored_password = self.__cursor.execute("SELECT password FROM users WHERE username = ?;", (username,)).fetchone()

        if stored_password == None:
            return False
        
        stored_password = stored_password[0]

        stored_salt = stored_password[:32]
        stored_password = stored_password[32:]

        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode(), bytes.fromhex(stored_salt), 100000)
        hashed_password = hashed_password.hex()

        return stored_password == hashed_password

    def get_preferred_piece_colour(self, username):
        self.__cursor.execute("SELECT preferred_piece_colour FROM users WHERE username = ?;", (username,))
        return self.__cursor.fetchone()[0]
        


    def delete_table(self, table_name):
        self.__cursor.execute(f"DROP TABLE {table_name};")
        self.__conn.commit()

    


db = Database("database.db")


# print(db.login("test2", "amazing_pwd&"))

# db.add_user("valid_user", "password", "white")

# db.create_users_table()
# db.create_game_history_table()
# db.create_AI_game_stats_table()
# db.create_friends_table()

# db.delete_table("users")
# db.delete_table("game_history")
# db.delete_table("AI_game_stats")
# db.delete_table("friends")
