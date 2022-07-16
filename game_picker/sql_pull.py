import sqlite3
import streamlit as st

@st.cache(allow_output_mutation=True)
def get_all_games_json():
    bg_connection = sqlite3.connect("YOUR-DB-PATH-HERE", check_same_thread=False)
    bg_connection.row_factory = sqlite3.Row
    bg_cursor = bg_connection.cursor()
    
    bg_cursor.execute("""SELECT * FROM game_list, mechanics, category,designer, publisher
    WHERE game_list.game_id = mechanics.game_id
    AND game_list.game_id = category.game_id
    AND game_list.game_id = designer.game_id
    AND game_list.game_id = publisher.game_id""")
    full_games = [dict((bg_cursor.description[i][0], value) for i, value in enumerate(row)) for row in bg_cursor.fetchall()]
    bg_connection.close()
    return full_games


def get_mechanics_json():
    bg_connection = sqlite3.connect("C:\Databases\Playground.db", check_same_thread=False)
    bg_connection.row_factory = sqlite3.Row
    bg_cursor = bg_connection.cursor()
    
    bg_cursor.execute("SELECT * from mechanics")
    mech = [dict((bg_cursor.description[i][0], value) for i, value in enumerate(row)) for row in bg_cursor.fetchall()]
    bg_connection.close()
    return mech

def get_categories_json():
    bg_connection = sqlite3.connect("C:\Databases\Playground.db", check_same_thread=False)
    bg_connection.row_factory = sqlite3.Row
    bg_cursor = bg_connection.cursor()
    bg_cursor.execute("SELECT * from category")
    
    cats = [dict((bg_cursor.description[i][0], value) for i, value in enumerate(row)) for row in bg_cursor.fetchall()]
    bg_connection.close()
    return cats

def get_designers_json():
    bg_connection = sqlite3.connect("C:\Databases\Playground.db", check_same_thread=False)
    bg_connection.row_factory = sqlite3.Row
    bg_cursor = bg_connection.cursor()
    bg_cursor.execute("SELECT * from designer")
    
    design = [dict((bg_cursor.description[i][0], value) for i, value in enumerate(row)) for row in bg_cursor.fetchall()]
    bg_connection.close()
    return design

def get_publishers_json():
    bg_connection = sqlite3.connect("C:\Databases\Playground.db", check_same_thread=False)
    bg_connection.row_factory = sqlite3.Row
    bg_cursor = bg_connection.cursor()
    bg_cursor.execute("SELECT * from publisher")
    
    pub = [dict((bg_cursor.description[i][0], value) for i, value in enumerate(row)) for row in bg_cursor.fetchall()]
    bg_connection.close()
    return pub


def get_game_names_list():
    bg_connection = sqlite3.connect("C:\Databases\Playground.db", check_same_thread=False)
    bg_connection.row_factory = sqlite3.Row
    bg_cursor = bg_connection.cursor()
    query = f"SELECT DISTINCT name from game_list ORDER BY name"

    game_list = []
    games = bg_cursor.execute(query).fetchall()
    for game in games:
        game_list.append(game[0])
    return game_list
