from pprint import pprint
import sqlite3
from typing import (List, Dict)

bg_connection = sqlite3.connect("MY-SQL-DB-PATH")
bg_cursor = bg_connection.cursor()


def pull_game_ids():
    return bg_cursor.execute("SELECT game_id, bgg_object_id FROM game_list").fetchall()

def associate_game_traits(game_id: int, trait: Dict):
    info_type = str(trait["type"])
    info_name = str(trait["name"])
    print(f"Adding {info_name} to {game_id}")
    insert_function = f"INSERT INTO {info_type} ({info_type}_name, game_id) VALUES ('{info_name}', '{game_id}')"
    bg_cursor.execute(insert_function)
    bg_connection.commit()
