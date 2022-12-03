import sqlite3
import streamlit as st

BG_CONNECTION = sqlite3.connect("YOUR DATABASE PATH HERE", check_same_thread=False)
BG_CONNECTION.row_factory = sqlite3.Row
BG_CURSOR = BG_CONNECTION.cursor()

@st.cache(allow_output_mutation=True)
def get_all_games_json():
    
    BG_CURSOR.execute("""SELECT * FROM game_list, mechanics, category, designer, publisher
    WHERE game_list.game_id = mechanics.game_id
    AND game_list.game_id = category.game_id
    AND game_list.game_id = designer.game_id
    AND game_list.game_id = publisher.game_id""")
    full_games = [dict((BG_CURSOR.description[i][0], value) for i, value in enumerate(row)) for row in BG_CURSOR.fetchall()]
    BG_CONNECTION.close()
    return full_games


def get_mechanics_json():
    
    BG_CURSOR.execute("SELECT * from mechanics")
    mech = [dict((BG_CURSOR.description[i][0], value) for i, value in enumerate(row)) for row in BG_CURSOR.fetchall()]
    BG_CONNECTION.close()
    return mech


def get_categories_json():

    BG_CURSOR.execute("SELECT * from category")
    
    cats = [dict((BG_CURSOR.description[i][0], value) for i, value in enumerate(row)) for row in BG_CURSOR.fetchall()]
    BG_CONNECTION.close()
    return cats


def get_designers_json():

    BG_CURSOR.execute("SELECT * from designer")
    
    design = [dict((BG_CURSOR.description[i][0], value) for i, value in enumerate(row)) for row in BG_CURSOR.fetchall()]
    BG_CONNECTION.close()
    return design


def get_publishers_json():

    BG_CURSOR.execute("SELECT * from publisher")
    
    pub = [dict((BG_CURSOR.description[i][0], value) for i, value in enumerate(row)) for row in BG_CURSOR.fetchall()]
    BG_CONNECTION.close()
    return pub

@st.cache(allow_output_mutation=True)
def get_game_names_list():

    query = f"SELECT DISTINCT name from game_list ORDER BY name"

    game_list = []
    games = BG_CURSOR.execute(query).fetchall()
    for game in games:
        game_list.append(game[0])
    return game_list


def get_game_id_list():

    query = f"SELECT game_id from game_list"

    game_id_list = []
    game_ids = BG_CURSOR.execute(query).fetchall()
    for game in game_ids:
        game_id_list.append(game[0])
    return game_id_list

def get_search_game(user_str:str):

    query = f"select * from name_list where game_name LIKE '%{user_str}%'"
    result = BG_CURSOR.execute(query).fetchall()
    return result
