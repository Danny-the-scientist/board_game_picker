from xml.dom.minidom import Element
from xml.etree import ElementTree
import requests
import time
from sql_tasks import associate_game_traits

api_base = "https://boardgamegeek.com/xmlapi/"

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


def _write_game_info(my_id, bgg_id):
    game_api = requests.get(f"{api_base}boardgame/{bgg_id}")
    time.sleep(2)
    game_root = ElementTree.fromstring(game_api.content)
    _get_mech_tags(game_root, my_id)
    _get_pub_tags(game_root, my_id)
    _get_cat_tags(game_root, my_id)
    _get_des_tags(game_root, my_id)
