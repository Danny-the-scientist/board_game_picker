import sqlite3
from sql_tasks import pull_game_ids
from data_retrieve import _write_game_info

def main():
    games = pull_game_ids()
    for bgg, my_game in games:
        _write_game_info(bgg, my_game)

if __name__ == "__main__":
    main()