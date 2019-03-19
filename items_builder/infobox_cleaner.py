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

import re
import datetime
from typing import List

import dateparser


def clean_weight(value: str) -> float:
    """A helper method to convert the weight entry from a OSRS Wiki infobox to a float.

    :param value: The extracted raw wiki text.
    :return weight: The weight of an item.
    """
    weight = str(value)
    weight = weight.strip()

    # Replace generic wiki text links
    weight = weight.replace("[", "")
    weight = weight.replace("]", "")

    # Remove "kg" from weight
    weight = weight.replace("kg", "")

    weight = weight.replace(",", ".")

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

    :param value: The extracted raw wiki text.
    :return quest: A boolean to identify if an item is associated with a quest.
    """
    # Clean a quest value
    quest = value
    quest = quest.strip()

    # Generic test for not a quest item
    if quest.lower() == "no" or quest.lower() == "":
        quest = False
    elif quest.lower() == "yes":
        quest = True
    elif "[[" in quest:
        quest = True
    else:
        # Only two items get here (Rune mysteries related items)
        quest = True

    return quest


def clean_release_date(value: str) -> str:
    """A helper method to convert the release date entry from an OSRS Wiki infobox.

    The returned value will be a specifically formatted string: dd Month YYYY.
    For example, 25 June 2017 or 01 November 2014.

    :param value: The extracted raw wiki text.
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

    :param value: The extracted raw wiki text.
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


def clean_examine(value: str, name: str) -> str:
    """A helper method to convert the examine text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :param name: The name of the item being processed.
    :return tradeable: A cleaned tradeable property of an item.
    """
    examine = str(value)
    examine = examine.strip()

    examine = examine.replace("[", "")
    examine = examine.replace("]", "")

    # Generic fix for clue scroll related items
    clue_scrolls = ["Clue scroll (easy)",
                    "Clue scroll (medium)",
                    "Clue scroll (hard)",
                    "Clue scroll (elite)"]
    if name in clue_scrolls:
        examine = "A clue!"
        return examine
    if name == "Key (medium)":
        examine = "A key to unlock a treasure chest."
        return examine

    # Fix for quest related examine texts (mostly for keys)
    examine = re.sub(r' \([^()]*\)', '', examine)

    # Remove nowiki tags
    examine = examine.replace("<nowiki>", "")
    examine = examine.replace("</nowiki>", "")

    # Remove linked tags
    examine = examine.replace("{{*}}", "")

    # Remove triple/double quotes
    examine = examine.replace("'''", "")
    examine = examine.replace("''", "")

    # Remove stars (used for lists in wiki)
    examine = examine.replace("*", "")

    # Remove breaks
    examine = examine.replace("<br />", " ")
    examine = examine.replace("<br/>", " ")
    examine = examine.replace("<br>", " ")

    # Remove any line breaks for spaces
    examine = examine.replace("\n", " ")

    # Remove double spaces for single spaces
    examine = examine.replace("  ", " ")

    examine = examine.strip()

    return examine


def clean_store_price(value: str) -> str:
    """"A helper method to convert the store price entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
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

    :param value: The extracted raw wiki text.
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
