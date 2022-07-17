"""Original coding by Daniel (Danny) C
Git: danny-the-scientist"""

import streamlit as st
import pandas as pd
import sql_pull
import data_handle
import random

cats = data_handle.get_unique_cats()
mechs = data_handle.get_unique_mech()
pubs = data_handle.get_unique_publisher()
designers = data_handle.get_unique_designer()
game_names = sql_pull.get_game_names_list()
all_game_info = pd.DataFrame(sql_pull.get_all_games_json())

game_names_df = pd.DataFrame({"Game Name": game_names})
all_game_info_df = pd.DataFrame(all_game_info)

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)



st.title('Board Game Picker')
st.write("Welcome to the board game picking app by Daniel (Danny) C! This will help you narrow down what game(s) to play based on your group's preferences for everything from complexity a favorite designer, or roll the dice for a random pick!")
st.write("Use the sliders to the left for numerical filtering and pick any number of options from game categories, mechanics, designers, and publishers below!")
st.write("You'll see a random selection of 15 matching games, but can also view the full match list if you prefer, as well as all available games.")
st.subheader("Enjoy, and happy gaming!")


group_number = 0
min_play = 0
max_play = 0
group_size = st.sidebar.checkbox('Specify the number of players present?')
reccomended_play = st.sidebar.checkbox('Use BGG recommended player numbers?')
if group_size:
    group_number = st.sidebar.number_input('Select your group size',1,50)
else:
    min_play = st.sidebar.slider('Min number of players', 0, 10, 0)
    max_play = st.sidebar.slider('Max number of players', 0, 40, 0)

min_age = st.sidebar.slider('Minimum Recommended Age', 0, 18, 0)
min_time = st.sidebar.slider('Minimum Time (Minutes)', 0, 600, 0)
max_time = st.sidebar.slider('Maximum Time (Minutes)', 0, 600, 0)
bgg_rating_min = st.sidebar.slider('BoardGameGeek Avg Rating Min',0.0, 10.0, 0.0)
bgg_rating_max = st.sidebar.slider('BoardGameGeek Avg Rating Max',0.0, 10.0, 0.0)
bgg_complexity_min = st.sidebar.slider('BoardGameGeek Complexity Min', 0.0, 5.0, 0.0)
bgg_complexity_max = st.sidebar.slider('BoardGameGeek Complexity Max', 0.0, 5.0, 0.0)

st.write('#')
st.write('#')

st.header('Take a "Chance!"')
if st.button('Random Game'):
    game_number = random.randrange(0, len(game_names))
    st.subheader('Your game is...')
    st.write('###')
    st.subheader(f"{game_names[game_number]}!! Enjoy!")
st.write('#')
if st.button("Danny's Favorite!"):
    st.subheader('Your game is...')
    st.write('###')
    st.subheader("Cosmic Encounter!! Enjoy!")


st.write('#')
st.header('Search for a game:')
search_input = st.text_input('Type part of a game name and press enter')
if search_input:
    search_result = sql_pull.get_search_game(search_input)
    result_df = pd.DataFrame(search_result)
    result_final = result_df.rename(columns={col: "Game Name" for col in result_df})
    st.table(result_final)

st.header('Categories')
picked_cats = st.multiselect('', cats)

st.header('Mechanics')
picked_mechs = st.multiselect('', mechs)

st.header('Designers')
picked_design = st.multiselect('',designers)

st.header('Publishers')
picked_pubs = st.multiselect('', pubs)

filtered_games = data_handle.get_filtered_games(all_game_info_df,
group_size,
group_number,
min_play,
max_play,
reccomended_play,
min_age,
min_time,
max_time,
bgg_rating_min,
bgg_rating_max,
bgg_complexity_min,
bgg_complexity_max,
picked_cats,
picked_mechs,
picked_design,
picked_pubs)
final_games = []
filtered_names = pd.DataFrame({"Game Name": filtered_games.name.unique()})
number_filtered = filtered_names.shape[0]


st.write('#')

if number_filtered >= 15:
    st.header('A Random 15:')
    st.table(filtered_names.sample(n = 15))
elif number_filtered > 0:
    st.header(f"Your {number_filtered} result(s):")
    st.table(filtered_names)
else:
    st.header("No matches found :(")


st.write('#')
view_matches = st.checkbox('View all matches')
if view_matches:
    st.header('All matching games:')
    st.table(filtered_names)


st.write('#')
view_full = st.checkbox('View full game list')
if view_full:
    st.header('All games:')
    st.table(game_names_df)

