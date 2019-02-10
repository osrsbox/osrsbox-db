"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Copyright (c) 2019, PH01L

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""

import datetime
import dateparser
from typing import List


def clean_weight(value: str) -> float:
    """A helper method to convert the weight entry from a OSRS Wiki infobox to a float.

    :return weight: The weight on an item.
    """
    weight = str(value)
    weight = weight.strip()

    # Replace generic wiki text links
    weight = weight.replace("[", "")
    weight = weight.replace("]", "")

    # Remove "kg" from weight
    weight = weight.replace("kg", "")

    # Some items have Inventory/Equipped weights:
    # For example: "'''Inventory:''' 0.3{{kg}}<br> '''Equipped:''' -4.5"
    if "inventory" in weight.lower():
        weight = weight.replace("'''", "")
        weight = weight.replace("{", "")
        weight = weight.replace("}", "")
        # Split based on HTML break
        if "<br>" in weight:
            weight_list = weight.split("<br>")
        if "<br />" in weight:
            weight_list = weight.split("<br />")
        if "<br/>" in weight:
            weight_list = weight.split("<br/>")
        # Grab first list entry
        weight = weight_list[0]
        weight = weight.lower()
        weight = weight.replace("in inventory:", "")
        weight = weight.replace("inventory:", "")

    # Remove greater than, less than for approximate weights
    if ">" in weight:
        weight = weight.replace(">", "")
    if "<" in weight:
        weight = weight.replace("<", "")

    # Strip the string again...
    weight = weight.strip()

    # TEMPORARY MODIFIERS:
    weight = weight.replace("😎😎", "")  # WTF: https://oldschool.runescape.wiki/w/Unidentified_rare_fossil

    # If weight string is empty, set to None
    if weight == "":
        weight = 0

    # Cast to a float, and return
    weight = float(weight)
    return weight


def clean_quest(value: str) -> List:
    """A helper method to convert the quest entry from an OSRS Wiki infobox to a boolean.

    :return quest: A boolean to identify if an item is associated with a quest.
    """
    # Clean a quest value
    quest = value
    quest = quest.strip()

    quest = quest.replace("Growing Pains]] [[Fairy Tale II", "Growing Pains]] <br> [[Fairy Tale II")
    quest = quest.replace("[", "")
    quest = quest.replace("]", "")
    quest = quest.replace("{", "")
    quest = quest.replace("}", "")
    quest = quest.replace("*", "")
    quest = quest.replace("II|II", "II")
    quest = quest.replace("Tears of Guthix (quest)|", "")
    quest = quest.replace("(quest)", "")
    quest = quest.replace("(miniquest)", "")
    quest = quest.replace("miniquest", "")
    quest = quest.replace("Miniquest", "")
    quest = quest.replace("various", "Various")

    quest = quest.strip()

    # Generic test for not a quest item
    if quest.lower() == "no":
        return None
    if quest.lower() == "yes":
        # This returns none, as the db wants a quest name
        return None

    quest_list = list()
    # Start trying to split quests
    if ", <br>" in quest:
        quest_list = quest.split(", <br>")
    elif ",<br>" in quest:
        quest_list = quest.split(",<br>")
    elif ",<br/>" in quest:
        quest_list = quest.split(",<br/>")
    elif ", <br/>" in quest:
        quest_list = quest.split(", <br/>")
    elif ",<br />" in quest:
        quest_list = quest.split(",<br />")
    elif ", <br />" in quest:
        quest_list = quest.split(", <br />")
    elif "<br>" in quest:
        quest_list = quest.split("<br>")
    elif "<br >" in quest:
        quest_list = quest.split("<br >")
    elif "<br/>" in quest:
        quest_list = quest.split("<br/>")
    elif "<br />" in quest:
        quest_list = quest.split("<br />")
    elif "&" in quest:
        quest_list = quest.split("&")
    elif "\n" in quest:
        quest_list = quest.split("\n")
    if "," in quest:
        quest_list = quest.split(",")

    # Start creating the final list to return
    quest_list_fin = list()
    if quest_list:
        for quest_name in quest_list:
            quest_name = quest_name.strip()
            quest_name = quest_name.replace("<br>", "")
            quest_name = quest_name.replace("<br/>", "")
            quest_list_fin.append(quest_name)
    else:
        quest_list_fin.append(quest)

    return quest_list_fin


def clean_release_date(value: str) -> str:
    """A helper method to convert the release date entry from an OSRS Wiki infobox.

    The returned value will be a specifically formatted string: dd Month YYYY.
    For example, 25 June 2017 or 01 November 2014.

    :return release_date: A cleaned release date of an item.
    """
    release_date = value
    release_date = release_date.strip()
    release_date = release_date.replace("[", "")
    release_date = release_date.replace("]", "")
    try:
        release_date = datetime.datetime.strptime(release_date, "%d %B %Y")
        return release_date.strftime("%d %B %Y")
    except ValueError:
        pass

    try:
        release_date = dateparser.parse(release_date)
        release_date = release_date.strftime("%d %B %Y")
    except (ValueError, TypeError):
        return None

    return release_date


def clean_tradeable(value: str) -> bool:
    """A helper method to convert the tradeable entry from an OSRS Wiki infobox.

    :return tradeable: A cleaned tradeable property of an item.
    """
    tradeable = str(value)
    tradeable = tradeable.strip()

    tradeable = tradeable.replace("[", "")
    tradeable = tradeable.replace("]", "")

    if tradeable in ["True", "true", True, "Yes", "yes"]:
        tradeable = True
    elif tradeable in ["False", "false", False, "No", "no"]:
        tradeable = False
    else:
        tradeable = False

    return tradeable


def clean_examine(value, name):
    """docstring"""
    examine = value
    examine = examine.strip()
    examine = examine.replace("'''", "")
    examine = examine.replace("''", "")
    examine = examine.replace("{", "")
    examine = examine.replace("}", "")
    examine = examine.replace("[", "")
    examine = examine.replace("]", "")
    examine = examine.replace("*", "")
    examine = examine.replace("<nowiki>", "")
    examine = examine.replace("</nowiki>", "")
    # examine = examine.replace("sic", "")
    examine = examine.replace("à", "")  # TODO: Not working, only one item affected
    examine = examine.replace("(empty)", "Empty:")
    examine = examine.replace("(full)", "Full:")
    examine = examine.replace("(Player's Name)", "<players-name>")
    examine = examine.replace("<number of cabbages>", "x")
    examine = examine.replace("2!", "")
    examine = examine.replace("In POH", "POH")

    # Examine text fixes for some quest items
    examine = examine.replace("(Used in the Shield of Arrav quest)", "")
    examine = examine.replace("(Used in The Grand Tree quest)", "")
    examine = examine.replace("(Edgeville Dungeon entrance)", "")
    examine = examine.replace("(Used to open the muddy chest in the lava maze)", "")
    examine = examine.replace("(Used to open the sinister chest in Yanille dungeon)", "")
    examine = examine.replace("(Used in the Dragon Slayer quest)", "")
    examine = examine.replace("(Used in Heroes' Quest)", "")
    examine = examine.replace("(Provides access to the deeper parts of Taverley Dungeon)", "")
    examine = examine.replace("(Provides access to the Desert Mining Camp)", "")
    examine = examine.replace("(Unlocks the cell door in the Desert Mining Camp)", "")
    examine = examine.replace("(Access to the Desert Mining Camp's mine)", "")
    examine = examine.replace("(Used in the Tourist Trap quest)", "")
    examine = examine.replace("(Used in the Watchtower quest)", "")
    examine = examine.replace("(Used in the Zogre Flesh Eaters quest)", "")
    examine = examine.replace("(Used in the Creature of Fenkenstrain quest)", "")
    examine = examine.replace("(Opens chests found in the Mort'ton catacombs)", "")
    examine = examine.replace("(Used in the Fremennik Trials quest)", "")
    examine = examine.replace("(Allows access to the Crystal mine from the Haunted mine quest)", "")
    examine = examine.replace("(Used in the Horror from the Deep quest)", "")
    examine = examine.replace("(Used in the Darkness of Hallowvale quest)", "")
    examine = examine.replace("(Used in the Priest in Peril quest)", "")
    examine = examine.replace("(Allows access to the Water Ravine Dungeon from the Spirits of the Elid quest)", "")
    examine = examine.replace("(Used to enter the cavern near the Temple of Light)", "")
    examine = examine.replace("(Opens the locked coffins in the cave at Jiggig)", "")
    examine = examine.replace("(Used to open a chest upstairs in Slepe church)", "")
    examine = examine.replace("(Unlocks the gate to the roof of the Slayer Tower)", "")
    examine = examine.replace("(Used in the Misthalin Mystery quest)", "")
    examine = examine.replace("(Allows access to the goblin kitchen in the Observatory Dungeon)", "")
    examine = examine.replace("(Used to access the prison cell inside of the Mourner HQ)", "")
    examine = examine.replace("(Provides access to the elemental workshop)", "")
    examine = examine.replace("(Provides access to the Black Knights jail cell in Taverley Dungeon)", "")
    examine = examine.replace("(Used in the In Aid of the Myreque quest)", "")
    examine = examine.replace("(Used in the Troll Stronghold quest)", "")
    examine = examine.replace("(Used in the Smoke Dungeon in Desert Treasure)", "")
    examine = examine.replace("(Quick access into the Temple of Ikov)", "")
    examine = examine.replace("(Used to access the prison cell inside of the Mourner HQ)", "")
    examine = examine.replace("(Used in The Golem quest)", "")
    examine = examine.replace("(Used in the Smoke Dungeon in Desert Treasure)", "")
    examine = examine.replace("(Allows access to the Crystal mine from the Haunted mine quest)", "")
    examine = examine.replace("(Used in the Eadgar's Ruse quest)", "")
    examine = examine.replace("(Used in the Troll Stronghold quest)", "")
    examine = examine.replace("(Used in the Plague City quest)", "")
    examine = examine.replace("(used to access the Hill Titan's lair)", "")
    examine = examine.replace("(Used in the Ernest the Chicken quest)", "")
    examine = examine.replace("(Unlocks a door found in the Waterfall Dungeon)", "")
    examine = examine.replace("(Opens the cell found in the Gnome Village Dungeon)", "")
    examine = examine.replace("(Used in the Biohazard quest)", "")
    examine = examine.replace("(Used in the Pirate's Treasure quest)", "")
    examine = examine.replace("(Provides access to Rashiliyia's Tomb)", "")
    examine = examine.replace("(Used in The Digsite quest)", "")
    examine = examine.replace("(Used in the Demon Slayer quest)", "")
    examine = examine.replace("(Used in the Hazeel Cult quest)", "")
    examine = examine.replace("(Used in the Witch's House quest)", "")
    examine = examine.replace("(Used in the Prince Ali Rescue quest)", "")
    examine = examine.replace("(Used in The Lost Tribe quest)", "")
    examine = examine.replace("(Used in the Recruitment Drive quest)", "")
    examine = examine.replace("(Used to open a chest deep in the HAM cave)", "")
    examine = examine.replace("(Used to open the hatch in the elemental workshop)", "")
    examine = examine.replace("(Used in Olaf's Quest)", "")
    examine = examine.replace("(Used in the Ghost Ahoy quest)", "")
    examine = examine.replace("(Used in the Ghosts Ahoy quest)", "")

    # Special cirumstances for clue scrolls:
    if name == "Clue scroll (easy)":
        examine = """A set of instructions to be followed.; A clue!; A piece of the world map, but where?; It points to great treasure!"""
    if name == "Clue scroll (medium)":
        examine = """A set of instructions to be followed; A clue!; A piece of the world map,but where?; Perhaps someone at the observatory can teach me to navigate?; It points to great treasure!"""
    if name == "Clue scroll (hard)":
        examine = """Emote: A set of instructions to be followed.; Anagram: A clue!, Map: A place of the world map, but where?; Coordinates: Perhaps someone at the observatory can teach me to navigate?; Fairy ring: A clue suggested by <players-name>!"""
    if name == "Clue scroll (elite)":
        examine = "A clue!; Sherlock: A clue suggested by <players-name>!"

    if name in ["Hell cat",
                     "Hell-kitten",
                     "Lazy cat",
                     "Lazy hell cat",
                     "Overgrown hellcat",
                     "Pet cat",
                     "Pet kitten",
                     "Wily hellcat"]:
        examine = """Inventory: This kitten seems to like you. (Kitten), This cat definitely likes you. (Cat), This cat is so well fed it can hardly move. (Overgrown); Follower: A friendly little pet. (Kitten), A fully grown feline. (Cat), A friendly, not-so-little pet. (Overgrown)"""

    if name == "Clue scroll":
        examine = "A clue!; A clue suggested by <players-name>!"

    return examine


def clean_store_price(value: str) -> str:
    """"A helper method to convert the store price entry from an OSRS Wiki infobox.

    :return store_price: A cleaned store price property of an item.
    """
    store_price = value
    store_price = store_price.strip()

    # Generic test for no store price value
    if (store_price.lower() == "no" or
            "not sold" in store_price.lower() or
            store_price == "" or
            store_price == "N/A"):
        return None

    # Remove thousand separator
    store_price = store_price.replace(",", "")

    # Try cast the value, if successful, return it
    try:
        return int(store_price)
    except ValueError:
        return None

    return store_price


def clean_seller(value: str) -> str:
    """A helper method to convert the seller entry from an OSRS Wiki infobox.

    :return seller: A cleaned seller property of an item.
    """
    seller = value
    seller = seller.strip()

    # Generic test for no store price value
    if (seller.lower() == "no" or
            "not sold" in seller.lower() or
            seller == "" or
            seller == "N/A"):
        return None

    seller = seller.replace("{{l/c}}", "")
    seller = seller.replace("{{l/o}}", "")

    # TODO: Still fixing this

    # if seller == "" or seller.lower() == "no" or seller:
    #     return None
    #

    # seller = seller.replace("{", "")
    # seller = seller.replace("}", "")
    # seller = seller.replace("[", "")
    # seller = seller.replace("]", "")
    #
    # seller = seller.replace(" - Mystic Robes", "")
    # seller = seller.replace("41,600", "")
    #
    # seller_list = list()
    # if "!" in seller:
    #     seller_list.append(seller.split("!")[0])
    # elif " and " in seller:
    #     seller_list = seller.split(" and ")
    # elif " or " in seller:
    #     seller_list = seller.split(" or ")
    #
    # seller_list_fin = list()
    # if seller_list:
    #     for seller_name in seller_list:
    #         seller_name = seller_name.strip()
    #         seller_list_fin.append(seller_name)
    # else:
    #     seller_list_fin.append(seller)

    return seller
