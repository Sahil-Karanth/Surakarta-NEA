import sqlite3


class Database:

    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name)
        self.__cursor = self.__conn.cursor()
        

    def create_user_table(self):
        self.__cursor.execute(

            """

            CREATE TABLE IF NOT EXISTS users (
                username TEXT,
                password TEXT,
                global_rank INTEGER,
                account_creation_date TEXT,
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
    
    def add_user(self, username, password, global_rank, account_creation_date, preferred_piece_colour, saved_game):
        self.__cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);", (username, password, global_rank, account_creation_date, preferred_piece_colour, saved_game))
        self.__conn.commit()

    def delete_table(self, table_name):
        self.__cursor.execute(f"DROP TABLE {table_name};")
        self.__conn.commit()

    


db = Database("database.db")

db.add_user("test3", "test", 0, "2021,0101", "white", "test")



# db.create_user_table()
# db.create_game_history_table()
# db.create_AI_game_stats_table()
# db.create_friends_table()

# db.delete_table("game_history")