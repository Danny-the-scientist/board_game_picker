import sqlite3
from typing import (List, Dict)

BG_CONNECTION = sqlite3.connect("C:\Databases\Playground.db")
BG_CURSOR = BG_CONNECTION.cursor()


def pull_game_ids():
    return BG_CURSOR.execute("SELECT game_id, bgg_object_id FROM game_list").fetchall()

def pull_expansion_ids():
    return BG_CURSOR.execute("SELECT expansion_id, bgg_object_id FROM expansions").fetchall()

def write_game_polls(poll:list):
    reading = poll[0]['level']
    age_rec = poll[1]['age']
    low_play_rec = poll[2]['low_players']
    high_play_rec = poll[2]['high_players']
    my_id = poll[3]

    insert_function = f"UPDATE game_list SET rec_age_min = '{age_rec}', player_rec_min = '{low_play_rec}', player_rec_max = '{high_play_rec}', language_requirement = '{reading}' WHERE game_id = '{my_id}'"
    BG_CURSOR.execute(insert_function)
    BG_CONNECTION.commit()

def write_expansion_polls(poll:list):
    reading = poll[0]['level']
    age_rec = poll[1]['age']
    low_play_rec = poll[2]['low_players']
    high_play_rec = poll[2]['high_players']
    my_id = poll[3]

    insert_function = f"UPDATE expansions SET rec_age_min = '{age_rec}', player_rec_min = '{low_play_rec}', player_rec_max = '{high_play_rec}', language_requirement = '{reading}' WHERE expansion_id = '{my_id}'"
    BG_CURSOR.execute(insert_function)
    BG_CONNECTION.commit()

def write_base_info(game_info: Dict):
    my_id = game_info["my_id"]
    bgg_id = game_info["bgg_id"]
    year = game_info["year"]
    age = game_info["pub_age"]
    bgg_rating = game_info["bgg_rating"] 
    complexity = game_info["bgg_complexity"]
    playtime_min = game_info["playtime_min"] 
    playtime_max = game_info["playtime_max"] 
    player_min = game_info["player_min"] 
    player_max = game_info["player_max"]
    name = game_info["name"]
    own = game_info["own"]

    insert_function = f"INSERT INTO game_list (game_id, bgg_object_id, name, year_released, pub_age_min, bgg_rating, bgg_complexity, playtime_min, playtime_max, player_min, player_max, own) VALUES ('{my_id}','{bgg_id}','{name}','{year}','{age}', '{bgg_rating}','{complexity}','{playtime_min}','{playtime_max}','{player_min}','{player_max}','{own}')"
    BG_CURSOR.execute(insert_function)
    BG_CONNECTION.commit()

def write_expansion_info(game_info: Dict):
    my_id = game_info["my_id"]
    expands = game_info["expansion_to"]
    bgg_id = game_info["bgg_id"]
    year = game_info["year"]
    age = game_info["pub_age"]
    bgg_rating = game_info["bgg_rating"] 
    complexity = game_info["bgg_complexity"]
    playtime_min = game_info["playtime_min"] 
    playtime_max = game_info["playtime_max"] 
    player_min = game_info["player_min"] 
    player_max = game_info["player_max"]
    name = game_info["name"]
    own = game_info["own"]
    insert_function = f"INSERT INTO expansions (expansion_id, game_id, bgg_object_id, expansion_name, year_released, pub_age_min, bgg_rating, bgg_complexity, playtime_min, playtime_max, player_min, player_max, own) VALUES ('{my_id}','{expands}','{bgg_id}','{name}','{year}','{age}','{bgg_rating}','{complexity}','{playtime_min}','{playtime_max}','{player_min}','{player_max}','{own}')"
    BG_CURSOR.execute(insert_function)
    BG_CONNECTION.commit()
  

def associate_game_traits(game_id: int, trait: Dict):
    info_type = str(trait["type"])
    info_name = str(trait["name"])
    print(f"Adding {info_name} to {game_id}")
    insert_function = f"INSERT INTO {info_type} ({info_type}_name, game_id) VALUES ('{info_name}', '{game_id}')"
    BG_CURSOR.execute(insert_function)
    BG_CONNECTION.commit()

def update_search_table():
    drop_state = "DROP TABLE name_list"
    BG_CURSOR.execute(drop_state)
    BG_CONNECTION.commit()
    make_state = "CREATE VIRTUAL TABLE name_list USING fts5(game_name)"
    BG_CURSOR.execute(make_state)
    BG_CONNECTION.commit()
    populate_search = "insert into name_list (game_name) select distinct name from game_list"
    BG_CURSOR.execute(populate_search)
    BG_CONNECTION.commit()