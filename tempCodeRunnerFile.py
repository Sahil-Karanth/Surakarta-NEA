# delete all tables

db.delete_table("Users")
db.delete_table("SavedGames")
db.delete_table("GameHistory")
db.delete_table("AIGameStats")

# create all tables

db.create_users_table()
db.create_saved_games_table()
db.create_game_history_table()
db.create_AI_game_stats_table()
