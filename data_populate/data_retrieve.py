from xml.dom.minidom import Element
from xml.etree import ElementTree
import requests
import time
from sql_tasks import associate_game_traits, write_base_info, write_expansion_info, write_game_polls, write_expansion_polls

API_BASE = "https://boardgamegeek.com/xmlapi/"
NEW_GAME_ID = 1
NEW_EXPANSION_ID = 1

def pull_current_bgg():
    my_api = requests.get(f"{API_BASE}/collection/DannyCGaming?own=1")
    collection_root = ElementTree.fromstring(my_api.content)
    item_tag = collection_root.findall('./item')
    current_games = []
    for item in item_tag:
        obj_tag = item.get('objectid')
        current_games.append(obj_tag)
    return current_games

def _get_poll_values(root: Element, my_id: int):
    poll_tag = root.findall('./boardgame/poll')
    for poll in poll_tag:
        if poll.get('name') == 'language_dependence':
            results_tag = poll.findall('./results/result')
            results_language = {"level":[], "votes":[]}
            max_votes = 0
            for results in results_tag:
                if int(results.get('numvotes')) > max_votes:
                    results_language['level'] = results.get('value')
                    results_language['votes'] = results.get('numvotes')
                    max_votes = int(results.get('numvotes'))
                elif max_votes == 0: 
                    results_language['level'] = None

        elif poll.get('name') == 'suggested_playerage':
            results_tag = poll.findall('./results/result')
            results_age = {"age":[], "votes":[]}
            max_votes = 0
            for results in results_tag:
                if int(results.get('numvotes')) > max_votes:
                    results_age['age'] = results.get('value')
                    results_age['votes'] = results.get('numvotes')
                    max_votes = int(results.get('numvotes'))
                elif max_votes == 0:
                    results_age['age'] = None
                    
        elif poll.get('name') == 'suggested_numplayers':
            final_values = {"low_players":[], "high_players":[]}
            if poll.get('totalvotes') != "0":
                results_tag = poll.findall('./results')
                results_players = {"number":[], "votes_best":[], "votes_rec":[], "votes_not_rec":[]}
                low_num = True
                high_num = True
                for results in results_tag:
                    results_players["number"].append(results.get('numplayers'))
                    vote_result = results.findall('./result')
                    for vote_info in vote_result:
                            if vote_info.get('value') == 'Best':
                                results_players['votes_best'].append(vote_info.get('numvotes'))
                            if vote_info.get('value') == 'Recommended':
                                results_players['votes_rec'].append(vote_info.get('numvotes'))
                            if vote_info.get('value') == 'Not Recommended':
                                results_players['votes_not_rec'].append(vote_info.get('numvotes'))
                to_test = 0
                for i in results_players['number']:
                    while low_num:
                        if (int(results_players['votes_best'][to_test]) + int(results_players['votes_rec'][to_test])) > int(results_players['votes_not_rec'][to_test]):
                            final_values['low_players'] = (results_players['number'][to_test])
                            low_num = False
                        else:
                            to_test += 1
                            if to_test == len(results_players['number']):
                                final_values['low_players'] = None 
                    to_test += 1
                    while high_num:
                        if (int(results_players['votes_best'][to_test]) + int(results_players['votes_rec'][to_test])) > int(results_players['votes_not_rec'][to_test]):
                            if to_test == len(results_players['number']):
                                final_values['high_players'].append(results_players['number'][to_test])
                                high_num = False
                            final_values['high_players'].append(results_players['number'][to_test])
                            to_test += 1
                            if to_test == len(results_players['number']):
                                high_num = False
                        else:
                            to_test += 1
                            if to_test == len(results_players['number']):
                                final_values['high_players'].append(None)
                                high_num = False

                if len(final_values['high_players']) > 1:
                    final_values['high_players'] = final_values['high_players'][-2]
            else:
                final_values['low_players'] = None
                final_values['high_players'] = None
            if "+" in str(final_values['high_players']):
                final_values['high_players'] = final_values['high_players'][0].replace("+",'')
    return [results_language, results_age, final_values, my_id]

def _get_mech_tags(root: Element, my_id: int):
    mech_tag = root.findall('./boardgame/boardgamemechanic')
    for mechanic in mech_tag:
        each = mechanic.text
        if "'" in each:
            each = each.replace("'","''")
        trait = {'type':'mechanics', 'name':each}
        associate_game_traits(my_id, trait)

def _get_pub_tags(root: Element, my_id: int):
    pub_tag = root.findall('./boardgame/boardgamepublisher')
    for publisher in pub_tag:
        each = publisher.text
        if "'" in each:
            each = each.replace("'","''")
        trait = {'type':'publisher', 'name':each}
        associate_game_traits(my_id, trait)


def _get_cat_tags(root: Element, my_id: int):
    cat_tag = root.findall('./boardgame/boardgamecategory')
    for category in cat_tag:
        each = category.text
        if "'" in each:
            each = each.replace("'","''")
        trait = {'type':'category', 'name':each}
        associate_game_traits(my_id, trait)


def _get_des_tags(root: Element, my_id: int):
    des_tag = root.findall('./boardgame/boardgamedesigner')
    for designer in des_tag:
        each = designer.text
        if "'" in each:
            each = each.replace("'","''")
        trait = {'type':'designer', 'name':each}
        associate_game_traits(my_id, trait)

def _get_base_info(root:Element, bgg_id:int, my_game_id:int, my_expansion_id:int):
    pulled_game = root.find('./boardgame')
    game_info = {"my_id":int,"bgg_id":bgg_id, "name":"", "year":int,"bgg_rating":float,"pub_age":int, "bgg_complexity":float, "playtime_min":int,"playtime_max":int,"player_min":int,"player_max":int,"expansion_to":int,"own":1}
    game_info["year"] = pulled_game.find('./yearpublished').text
    game_info["bgg_rating"] = pulled_game.find('./statistics/ratings/average').text
    game_info["bgg_complexity"] = pulled_game.find('./statistics/ratings/averageweight').text
    game_info["playtime_min"] = pulled_game.find('./minplaytime').text
    game_info["playtime_max"] = pulled_game.find('./maxplaytime').text
    game_info["player_min"] = pulled_game.find('./minplayers').text
    game_info["player_max"] = pulled_game.find('./maxplayers').text
    game_info["pub_age"] = pulled_game.find('./age').text
    for names in pulled_game.findall('./name'):
        if names.get('primary') == 'true':
            game_info["name"] = names.text
            game_info["name"] = game_info["name"].replace("'","''")
    
    expansion_game = False
    if pulled_game.findall('./boardgameexpansion'):
        for expansion_test in pulled_game.findall('./boardgameexpansion'):
            if expansion_test.get('inbound') == 'true':
                expansion_game = True
                game_info["expansion_to"] = expansion_test.get('objectid')

    
    if not expansion_game:
        global NEW_GAME_ID
        my_game_id += NEW_GAME_ID
        NEW_GAME_ID += 1
        game_info["my_id"] = my_game_id
        write_base_info(game_info)
        poll = _get_poll_values(root, my_game_id)
        _get_mech_tags(root, my_game_id)
        _get_pub_tags(root, my_game_id)
        _get_cat_tags(root, my_game_id)
        _get_des_tags(root, my_game_id)
        write_game_polls(poll)
    else:
        global NEW_EXPANSION_ID
        my_expansion_id += NEW_EXPANSION_ID
        NEW_EXPANSION_ID += 1
        game_info["my_id"] = my_expansion_id
        write_expansion_info(game_info)
        poll = _get_poll_values(root, my_expansion_id)
        write_expansion_polls(poll)


def write_game_info(my_game_id, my_expansion_id, bgg_id):
    game_api = requests.get(f"{API_BASE}boardgame/{bgg_id}?stats=1")
    time.sleep(2)
    game_root = ElementTree.fromstring(game_api.content)
    print(f"Writing for {bgg_id}")
    _get_base_info(game_root, bgg_id, my_game_id, my_expansion_id)
    # _get_mech_tags(game_root, my_id)
    # _get_pub_tags(game_root, my_id)
    # _get_cat_tags(game_root, my_id)
    # _get_des_tags(game_root, my_id)