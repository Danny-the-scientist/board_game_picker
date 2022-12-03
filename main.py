import sqlite3
from sql_tasks import pull_game_ids, pull_expansion_ids, update_search_table
from data_retrieve import write_game_info, pull_current_bgg

def main():
    bgg_game_ids = pull_current_bgg()
    for i in range(0, len(bgg_game_ids)):
        bgg_game_ids[i] = int(bgg_game_ids[i])

    current_game_ids = pull_game_ids()
    current_bgg_games = []
    for i in current_game_ids:
        current_bgg_games.append(i[1])

    current_expansion_ids = pull_expansion_ids()
    current_bgg_expansions = []
    for i in current_expansion_ids:
        current_bgg_expansions.append(i[1])

    current_all = (current_bgg_games + current_bgg_expansions)
    new_all_bgg = (set(bgg_game_ids) - set(current_all))

    current_games = len(current_bgg_games)
    current_expansions = len(current_bgg_expansions)

    for new_game in new_all_bgg:
        write_game_info(current_games, current_expansions, new_game)
    
    update_search_table()
    #online_games = pull_current_bgg()
    #for bgg, my_game in db_games:
     #   write_game_info(bgg, my_game)

if __name__ == "__main__":
    main()