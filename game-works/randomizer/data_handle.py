import sql_pull
import pandas

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
    
    if min_age != 0:
        fg.drop(fg[fg.age_min < min_age].index, inplace=True)
    
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
            fg.drop(fg[fg.category_name != cat].index, inplace=True)
    
    if picked_mechs:
        for mech in picked_mechs:
            fg.drop(fg[fg.mechanics_name != mech].index, inplace=True)
    
    if picked_design:
        for designer in picked_design:
            fg.drop(fg[fg.designer_name != designer].index, inplace=True)

    if picked_pubs:
        for pub in picked_pubs:
            fg.drop(fg[fg.publisher_name != pub].index, inplace=True)

    return fg
