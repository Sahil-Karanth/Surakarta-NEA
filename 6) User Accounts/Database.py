import sqlite3
import hashlib
import os
from datetime import datetime

class Database:

    """Class for interacting with the database. Used inside of the UI class."""

    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        
    def create_users_table(self):
        
        """Creates the Users table if it doesn't already exist."""

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER,
                username TEXT,
                password TEXT,
                account_creation_date DATE,
                piece_colour TEXT,
                PRIMARY KEY (user_id)
            );

            """

        )
        
        self.__conn.commit()

    def create_saved_games_table(self):

        """Creates the SavedGames table if it doesn't already exist."""

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS SavedGames (
                saved_game_id INTEGER,
                user_id INTEGER,
                date_saved DATE,
                game_state_string TEXT,
                opponent_name TEXT,
                player2_starts BOOLEAN,
                player1_num_pieces INTEGER,
                player2_num_pieces INTEGER,
                player1_colour TEXT,
                PRIMARY KEY (saved_game_id)
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            """

        )

        self.__conn.commit()

    def create_game_history_table(self):

        """Creates the GameHistory table if it doesn't already exist."""

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS GameHistory (
                historical_game_id INTEGER,
                user_id INTEGER,
                opponent TEXT,
                game_date DATE,
                winner TEXT,
                PRIMARY KEY (historical_game_id)
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );

            """

        )

        self.__conn.commit()

    def create_AI_game_stats_table(self):

        """Creates the AIGameStats table if it doesn't already exist."""

        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS AIGameStats (
                AI_game_stat_id INTEGER,
                user_id INTEGER,
                AI_difficulty TEXT,
                win_count INTEGER,
                loss_count INTEGER,
                PRIMARY KEY (AI_game_stat_id)
            );

            """

        )

        self.__conn.commit()

    def __get_new_primary_key(self, table_name, primary_key_name):
        
        """Returns the next available primary key for a table."""

        # get the current highest primary key value
        self.__cursor.execute(f"SELECT MAX({primary_key_name}) FROM {table_name};")
        old_key = self.__cursor.fetchone()[0]

        # the first key in the table will be 1
        if old_key == None:
            return 1

        # otherwise, increment the old key by 1
        else:
            return old_key + 1
        
    def __get_user_id_from_username(self, username):
        
        """Returns the user_id of a user given their username."""

        self.__cursor.execute("SELECT user_id FROM Users WHERE username = ?;", (username,))
        return self.__cursor.fetchone()[0]

    def check_if_username_exists(self, username):
        
        """Returns True if a username exists in the database, otherwise returns False."""

        self.__cursor.execute("SELECT username FROM Users WHERE username = ?;", (username,))
        return self.__cursor.fetchone() != None
    
    def add_user(self, username, password, preferred_piece_colour):
        
        """Adds a user to the database. The password is hashed and salted before being stored."""

        # hash and salt the password
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)
        hashed_password = salt.hex() + hashed_password.hex()

        # get the current date
        account_creation_date = datetime.now().strftime("%Y-%m-%d")

        user_id = self.__get_new_primary_key("Users", "user_id")

        # add the user to the Users table
        self.__cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?);", (user_id, username, hashed_password, account_creation_date, preferred_piece_colour))

        # add a record for each AI difficulty to the AIGameStats table for the new user
        AI_game_stat_id = self.__get_new_primary_key("AIGameStats", "AI_game_stat_id")
    
        for difficulty in ["Easy AI", "Medium AI", "Hard AI"]:
            self.__cursor.execute("INSERT INTO AIGameStats VALUES (?, ?, ?, ?, ?);", (AI_game_stat_id, user_id, difficulty, 0, 0))
            AI_game_stat_id += 1

        
        self.__conn.commit()

    def login(self, username, password):

        """Returns True if the username and password match a record in the database, otherwise returns False.
        The password is hashed and salted before being compared to the stored password."""

        # get the stored password and salt for the username
        stored_password = self.__cursor.execute("SELECT password FROM Users WHERE username = ?;", (username,)).fetchone()

        if stored_password == None:
            return False
        
        stored_password = stored_password[0]

        # split the stored password into the salt and the hashed password
        stored_salt = stored_password[:32]
        stored_password = stored_password[32:]

        # hash and salt the password passed as an argument
        hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode(), bytes.fromhex(stored_salt), 100000)
        hashed_password = hashed_password.hex()

        # compare the stored password and the hashed password
        return stored_password == hashed_password

    def get_preferred_piece_colour(self, username):
        
        """Returns the preferred piece colour of a user given their username."""

        self.__cursor.execute("SELECT piece_colour FROM Users WHERE username = ?;", (username,))
        return self.__cursor.fetchone()[0]
        
    def get_user_stats(self, username):
        
        """Returns a user's win_count and loss_count for each AI difficulty."""

        self.__cursor.execute(
                
                """
                
                SELECT AI_difficulty, win_count, loss_count FROM AIGameStats
                    INNER JOIN Users ON Users.user_id = AIGameStats.user_id
                WHERE Users.username = ?;

                """, (username,)
        )

        return self.__cursor.fetchall()
    
    def __increment_win_stat(self, username, ai_difficulty):
        
        """Increments the win_count for a user and AI difficulty."""

        self.__cursor.execute(
            f"""            

            UPDATE AIGameStats
            SET win_count = win_count + 1
            WHERE AI_difficulty = ? AND user_id = ?;

            """, (ai_difficulty, self.__get_user_id_from_username(username))
        )

        self.__conn.commit()

    def __increment_loss_stat(self, username, ai_difficulty):
            
            """Increments the loss_count for a user and AI difficulty."""
            
            self.__cursor.execute(
                """            
    
                UPDATE AIGameStats
                SET loss_count = loss_count + 1
                WHERE AI_difficulty = ? AND user_id = ?;
    
                """, (ai_difficulty, self.__get_user_id_from_username(username))
            )
    
            self.__conn.commit()
    
    def update_user_stats(self, username, human_won, ai_difficulty):
        
        """Updates a user's win_count and loss_count for a given AI difficulty depending on whether the user won or lost."""

        if human_won:
            self.__increment_win_stat(username, ai_difficulty)

        else:
            self.__increment_loss_stat(username, ai_difficulty)

    def delete_table(self, table_name):
        
        """Deletes a table from the database."""

        self.__cursor.execute(f"DROP TABLE {table_name};")
        self.__conn.commit()

    def save_game_state(self, username, game_state_string, opponent_name, player2_starts, player1_num_pieces, player2_num_pieces, player1_colour):

        """Saves a match to the database (SavedGames table)."""
        
        # get the current date
        date_today = datetime.now().strftime("%Y-%m-%d")

        # get the next available primary key for the SavedGames table
        saved_game_id = self.__get_new_primary_key("SavedGames", "saved_game_id")

        # get the user_id of the user
        user_id = self.__get_user_id_from_username(username)

        # add the game state to the SavedGames table
        self.__cursor.execute("INSERT INTO SavedGames VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (saved_game_id, user_id, date_today, game_state_string, opponent_name, player2_starts, player1_num_pieces, player2_num_pieces, player1_colour))
        self.__conn.commit()

    def load_saved_games(self, username):
        
        """Returns a list of saved games for a user."""

        self.__cursor.execute(
            """

            SELECT saved_game_id, date_saved, opponent_name FROM SavedGames
                INNER JOIN Users ON Users.user_id = SavedGames.user_id
            WHERE username = ?;

            """, (username,)
        )

        return self.__cursor.fetchall()
    
    def load_game_state(self, saved_game_id):

        """Returns the data stored for a saved game given its saved_game_id."""

        self.__cursor.execute("SELECT game_state_string, opponent_name, player2_starts, player1_num_pieces, player2_num_pieces, player1_colour FROM SavedGames WHERE saved_game_id = ?;", (saved_game_id,))
        return self.__cursor.fetchone()
    
    def delete_saved_game(self, saved_game_id):
        
        """Deletes a saved game from the database given its saved_game_id."""

        self.__cursor.execute(
            """

            DELETE FROM SavedGames
            WHERE saved_game_id = ?;

            """, (saved_game_id,)

        )

        self.__conn.commit()

    def add_game_to_history(self, username, player2name, winner_name):
        
        """Adds a game to the GameHistory table."""

        # get the current date
        game_date = datetime.now().strftime("%Y-%m-%d")

        # get the next available primary key for the GameHistory table
        historical_game_id = self.__get_new_primary_key("GameHistory", "historical_game_id")

        # get the user_id of the user
        user_id = self.__get_user_id_from_username(username)

        # add the game to the GameHistory table
        self.__cursor.execute("INSERT INTO GameHistory VALUES (?, ?, ?, ?, ?);", (historical_game_id, user_id, player2name, game_date, winner_name))
        self.__conn.commit()

    def get_game_history(self, username):

        """Returns a list of games from the GameHistory table for a user given their username."""

        self.__cursor.execute(
            """

            SELECT historical_game_id, game_date, opponent, winner FROM GameHistory
                INNER JOIN Users ON Users.user_id = GameHistory.user_id
            WHERE username = ?;

            """, (username,)
        )

        return self.__cursor.fetchall()

        # self.__cursor.execute("SELECT historical_game_id, game_date, opponent, winner FROM GameHistory WHERE username = ?;", (username,))
        # return self.__cursor.fetchall()

    def update_preferred_piece_colour(self, username, new_colour):
        
        """Updates a user's preferred piece colour in the Users table."""

        self.__cursor.execute(
            """

            UPDATE Users
            SET piece_colour = ?
            WHERE username = ?;

            """, (new_colour, username)
        )

        self.__conn.commit()
    


# db = Database("database.db")

# db.save_game_state("f", "$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$green$.$.$.$.$.$.$.$.$orange$.$.$", "testopp1", False, 1, 1)

# db.delete_table("Users")
# db.delete_table("GameHistory")
# db.delete_table("AIGameStats")
# db.delete_table("SavedGames")

# db.create_users_table()
# db.create_game_history_table()
# db.create_AI_game_stats_table()
# db.create_saved_games_table()