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
                PRIMARY KEY (username)
            );

            """

        )
        
        self.__conn.commit()


    def create_saved_games_table(self):

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS saved_games (
                username TEXT,
                game_state_string TEXT,
                opponent_name TEXT,
                player2_starts BOOLEAN,
                PRIMARY KEY (username)
                FOREIGN KEY (username) REFERENCES users(username)
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

        self.__cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (username, hashed_password, account_creation_date, preferred_piece_colour))

        for difficulty in ["Easy AI", "Medium AI", "Hard AI"]:
            self.__cursor.execute("INSERT INTO AI_game_stats VALUES (?, ?, ?, ?);", (difficulty, username, 0, 0))
        
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
        
    def get_user_stats(self, username):
        self.__cursor.execute("SELECT ai_difficulty, wins, losses FROM AI_game_stats WHERE username = ?;", (username,))
        return self.__cursor.fetchall()
    
    def __increment_win_stat(self, username, ai_difficulty):
        self.__cursor.execute("UPDATE AI_game_stats SET wins = wins + 1 WHERE username = ? AND ai_difficulty = ?;", (username, ai_difficulty))
        self.__conn.commit()

    def __increment_loss_stat(self, username, ai_difficulty):
        self.__cursor.execute("UPDATE AI_game_stats SET losses = losses + 1 WHERE username = ? AND ai_difficulty = ?;", (username, ai_difficulty))
        self.__conn.commit()
    
    def update_user_stats(self, username, human_won, ai_difficulty):

        if human_won:
            self.__increment_win_stat(username, ai_difficulty)

        else:
            self.__increment_loss_stat(username, ai_difficulty)

        

        self.__conn.commit()

    def delete_table(self, table_name):
        self.__cursor.execute(f"DROP TABLE {table_name};")
        self.__conn.commit()

    def game_already_saved(self, username):

        self.__cursor.execute("SELECT username FROM saved_games WHERE username = ?;", (username,))
        return self.__cursor.fetchone() != None

    def save_game_state(self, username, game_state_string, opponent_name, player2_starts):

        if self.game_already_saved(username):
            self.__cursor.execute("DELETE FROM saved_games WHERE username = ?;", (username,))
        

        self.__cursor.execute("INSERT INTO saved_games VALUES (?, ?, ?, ?);", (username, game_state_string, opponent_name, player2_starts))
        self.__conn.commit()

    def load_game_state(self, username):

        self.__cursor.execute("SELECT game_state_string, opponent_name, player2_starts FROM saved_games WHERE username = ?;", (username,))
        return self.__cursor.fetchone()
    
    def delete_saved_game(self, username):
        self.__cursor.execute("DELETE FROM saved_games WHERE username = ?;", (username,))
        self.__conn.commit()


db = Database("database.db")



# print(db.login("test2", "amazing_pwd&"))

# db.add_user("valid_user", "password", "white")

# db.create_users_table()
# db.create_game_history_table()
# db.create_AI_game_stats_table()
# db.create_friends_table()
# db.create_saved_games_table()

# db.delete_table("users")
# db.delete_table("game_history")
# db.delete_table("AI_game_stats")
# db.delete_table("friends")
# db.delete_table("saved_games")
