import sql_pull
import pandas as pd
from typing import AnyStr

def get_unique_mech():
    mechs = sql_pull.get_mechanics_json()
    unique_mech = []
    for mech in mechs:
        if mech['mechanics_name'] not in unique_mech:
            unique_mech.append(mech['mechanics_name'])
    
    return unique_mech

def get_unique_cats():
    cats = sql_pull.get_categories_json()
    unique_cat = []
    for cat in cats:
        if cat['category_name'] not in unique_cat:
            unique_cat.append(cat['category_name'])
    
    return unique_cat

def get_unique_publisher():
    pubs = sql_pull.get_publishers_json()
    unique_pub = []
    for pub in pubs:
        if pub['publisher_name'] not in unique_pub:
            unique_pub.append(pub['publisher_name'])
    
    return unique_pub

def get_unique_designer():
    designers = sql_pull.get_designers_json()
    unique_des = []
    for des in designers:
        if des['designer_name'] not in unique_des:
            unique_des.append(des['designer_name'])
    
    return unique_des

def get_filtered_games(all_game_info_df,
group_size,
group_number,
min_play,
max_play,
reccomended_play,
reccomended_age,
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
picked_pubs):

    fg = all_game_info_df
    final_keep = sql_pull.get_game_id_list()

    if reccomended_play:
        if group_size:
            fg.drop(fg[fg.player_rec_min > group_number].index, inplace=True)
            fg.drop(fg[fg.player_rec_max < group_number].index, inplace=True)
        else:
            if min_play != 0:
                fg.drop(fg[fg.player_rec_min < min_play].index, inplace=True)
            if max_play != 0:
                fg.drop(fg[fg.player_rec_max > max_play].index, inplace=True)
    else:
        if group_size:
            fg.drop(fg[fg.player_min > group_number].index, inplace=True)
            fg.drop(fg[fg.player_max < group_number].index, inplace=True)
        if min_play != 0:
            fg.drop(fg[fg.player_min < min_play].index, inplace=True)
        if max_play != 0:
            fg.drop(fg[fg.player_max > max_play].index, inplace=True)
    
    if reccomended_age:
        if min_age != 0:
            fg.drop(fg[fg.rec_age_min < min_age].index, inplace=True)
            fg.dropna(subset=['rec_age_min'], inplace=True)
    else:
        if min_age != 0:
            fg.drop(fg[fg.pub_age_min < min_age].index, inplace=True)
            fg.dropna(subset=['pub_age_min'], inplace=True)           
    
    if min_time != 0:
        fg.drop(fg[fg.playtime_min < min_time].index, inplace=True)
    if max_time != 0:
        fg.drop(fg[fg.playtime_max > max_time].index, inplace=True)
    
    if bgg_rating_min != 0:
        fg.drop(fg[fg.bgg_rating < bgg_rating_min].index, inplace=True)
    if bgg_rating_max != 0:
        fg.drop(fg[fg.bgg_rating > bgg_rating_max].index, inplace=True)

    if bgg_complexity_min != 0:
        fg.drop(fg[fg.bgg_complexity < bgg_complexity_min].index, inplace=True)
    if bgg_complexity_max != 0:
        fg.drop(fg[fg.bgg_complexity > bgg_complexity_max].index, inplace=True)
    
    if picked_cats:
        for cat in picked_cats:
            cat_new = []
            new_select = fg.loc[fg['category_name'] == cat]
            for index, row in new_select.iterrows():
                cat_new.append(row['game_id'])
            final_keep = set(final_keep) & set(cat_new)
    
    if picked_mechs:
        for mech in picked_mechs:
            mech_new = []
            new_select = fg.loc[fg['mechanics_name'] == mech]
            for index, row in new_select.iterrows():
                mech_new.append(row['game_id'])
            final_keep = set(final_keep) & set(mech_new)
    
    if picked_design:
        for designer in picked_design:
            des_new = []
            new_select = fg.loc[fg['designer_name'] == designer]
            for index, row in new_select.iterrows():
                des_new.append(row['game_id'])
            final_keep = set(final_keep) & set(des_new)

    if picked_pubs:
        for pub in picked_pubs:
            pub_new = []
            new_select = fg.loc[fg['publisher_name'] == pub]
            for index, row in new_select.iterrows():
                pub_new.append(row['game_id'])
            final_keep = set(final_keep) & set(pub_new)

    if final_keep:
        new_fg = pd.DataFrame(columns=fg.columns)
        for game in final_keep:
            matched_game = fg.loc[fg.game_id == game]
            new_fg = new_fg.append(matched_game)
        return new_fg
    elif picked_cats or picked_design or picked_mechs or picked_pubs:
        fg_none = pd.DataFrame(columns=fg.columns)
        return fg_none
    else:
        return fg
