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

import dateparser


def clean_wikitext(value: str) -> str:
    """Generic infobox property cleaner.

    This helper method is a generic cleaner for all infobox template properties.
    The value is string cast, stipped of new line characters, then any square
    brackets (wikitext links) are stripped, then anything in trailing brackets,
    then any HTML line breaks are removed.

    :param value: Template value extracted in raw wikitext format.
    :return value: Template value with square brackets stripped.
    """
    value = str(value)
    value = value.strip()
    value = re.sub(r'[\[\]]+', '', value)  # Removes all "[" and "]"
    value = re.sub(r' \([^()]*\)', '', value)  # Removes " (anything)"
    value = re.sub(r'<!--(.*?)-->', '', value)  # Removes "<!--anything-->"
    value = re.sub(r'<br(.*)', '', value)  # Removes "<br"
    return value


def clean_boolean(value: str) -> bool:
    """Convert an infobox property to a boolean.

    :param value: Template value extracted in raw wikitext format.
    :return value: Template value converted into a boolean.
    """
    if value is None:
        return None
    value = clean_wikitext(value)

    if value in ["True", "true", True, "Yes", "yes"]:
        value = True
    elif value in ["False", "false", False, "No", "no"]:
        value = False
    else:
        # If unable to determine boolean, set to False
        value = False

    return value


def clean_integer(value: str) -> bool:
    """Convert an infobox property to a boolean.

    :param value: Template value extracted in raw wikitext format.
    :return value: Template value converted into a boolean.
    """
    if value is None:
        return None
    value = clean_wikitext(value)
    if value == "":
        return 0

    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            # If unable to cast value, set to 0
            value = 0

    return value


def clean_stats_value(value: str) -> int:
    """Clean a item/monster stats bonuses value extracted from a wiki template.

    :param value: Template value extracted in raw wikitext format.
    :return value: Template value converted into an integer.
    """
    if value is None:
        return None
    value = clean_wikitext(value)
    if value == "":
        return 0

    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        if value[0] == "-":
            if value[1:].isdigit():
                value = int(value)
        elif value[0] == "+":
            if value[1:].isdigit():
                value = int(value)
        else:
            if value.isdigit():
                value = int(value)
    else:
        # If unable to process, set to 0
        value = 0

    return value


def clean_weight(value: str, item_id: int) -> float:
    """Convert the weight entry from a OSRS Wiki infobox to a float.

    :param value: Template value extracted in raw wikitext format.
    :param item_id: The item ID number.
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

    # If weight string is empty, set to None
    if weight == "":
        weight = 0

    # Handle special weight reducing equipment. When worn, weight reducing items
    # have a specific item ID number that changes
    item_id = int(item_id)
    # Boots of lightness
    if item_id == 89:
        weight = -4.5
    # Penance gloves
    elif item_id == 10554:
        weight = -4.5
    # Max cape
    elif item_id == 13342:
        weight = -4.0
    # Spotted cape
    elif item_id == 10073:
        weight = -2.2
    # Spottier cape
    elif item_id == 10074:
        weight = -4.5
    # Agility cape (t)
    elif item_id == 13341:
        weight = -4.0
    # Agility cape
    elif item_id == 13340:
        weight = -4.0
    # Graceful
    elif item_id in [11851, 13580, 13592, 13604, 13616, 13628, 13668, 21063]:  # hood
        weight = -3
    elif item_id in [11853, 13582, 13594, 13606, 13618, 13630, 13670, 21066]:  # cape
        weight = -4
    elif item_id in [11855, 13584, 13596, 13608, 13620, 13632, 13672, 21069]:  # top
        weight = -5
    elif item_id in [11857, 13586, 13598, 13610, 13622, 13634, 13674, 21072]:  # legs
        weight = -6
    elif item_id in [11859, 13588, 13600, 13612, 13624, 13636, 13676, 21075]:  # gloves
        weight = -3
    elif item_id in [11861, 13590, 13602, 13614, 13626, 13638, 13678, 21078]:  # boots
        weight = -4

    # Cast to a float, and return
    weight = float(weight)
    return weight


def clean_quest(value: str) -> bool:
    """Convert the quest entry from an OSRS Wiki infobox to a boolean.

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

    if release_date is None or release_date == "":
        return None

    try:
        release_date = datetime.datetime.strptime(release_date, "%d %B %Y")
        return release_date.date().isoformat()
    except ValueError:
        pass

    try:
        release_date = dateparser.parse(release_date)
        release_date = release_date.date().isoformat()
    except (ValueError, TypeError):
        return None

    return release_date


def clean_examine(value: str, name: str) -> str:
    """Convert the examine text entry from an OSRS Wiki infobox.

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

    # Remove sic
    examine = examine.replace("{{sic}}", "")

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
