"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Various methods to help clean OSRS Wiki wikitext entries.

Copyright (c) 2020, PH01L

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


# GENERIC CLEANERS...

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


def clean_float(value: str) -> float:
    """Convert an infobox property to a float.

    :param value: Template value extracted in raw wikitext format.
    :return value: Template value converted into a float.
    """
    if value is None:
        return None
    value = clean_wikitext(value)
    if value == "":
        return None

    if isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            # If unable to cast value, set to 0
            value = 0.0

    return value


def clean_integer(value: str) -> int:
    """Convert an infobox property to a integer.

    :param value: Template value extracted in raw wikitext format.
    :return value: Template value converted into a integer.
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


# ITEM CLEANERS...


def clean_weight(value: str, item_id: int) -> float:
    """Convert the weight entry from a OSRS Wiki infobox to a float.

    :param value: Template value extracted in raw wikitext format.
    :param item_id: The item ID number.
    :return weight: The weight of an item.
    """
    item_id = int(item_id)

    weight = str(value)
    weight = weight.strip()

    # Handle weight reducing items... (item ID changes when equipped)
    # Generic weight reducing items (not graceful)
    if item_id == 89:
        return -4.5  # Boots of lightness
    elif item_id == 10554:
        return -4.5  # Penance gloves
    elif item_id == 13342:
        return -4.0  # Max cape
    elif item_id == 10073:
        return -2.2  # Spotted cape
    elif item_id == 10074:
        return -4.5  # Spottier cape
    elif item_id == 13341:
        return -4.0  # Agility cape (t)
    elif item_id == 13340:
        return -4.0  # Agility cape
    # Graceful items
    elif item_id in [11851, 13580, 13592, 13604, 13616, 13628, 13668, 21063]:
        return -3  # Graceful hood
    elif item_id in [11853, 13582, 13594, 13606, 13618, 13630, 13670, 21066]:
        return -4  # Graceful cape
    elif item_id in [11855, 13584, 13596, 13608, 13620, 13632, 13672, 21069]:
        return -5  # Graceful top
    elif item_id in [11857, 13586, 13598, 13610, 13622, 13634, 13674, 21072]:
        return -6  # Graceful legs
    elif item_id in [11859, 13588, 13600, 13612, 13624, 13636, 13676, 21075]:
        return -3  # Graceful gloves
    elif item_id in [11861, 13590, 13602, 13614, 13626, 13638, 13678, 21078]:
        return -4  # Graceful boots

    # The weight property is usally quite clean...
    # Try float cast the value, and return
    try:
        return float(weight)
    except ValueError:
        pass

    # Some items have Inventory/Equipped weights:
    # For example: "'''Inventory:''' 0.3{{kg}}<br> '''Equipped:''' -4.5"
    # There are multiple HTML break tags: <br> <br /> <br/>
    break_tags = ["<br>", "<br />", "<br/>"]
    if "inventory" in weight.lower():
        weight = weight.replace("'''", "")
        for break_tag in break_tags:
            if break_tag in weight:
                weight_list = weight.split(break_tag)
                # Grab first list entry, convert to lower case and replace string
                weight = weight_list[0]
                weight = weight.lower()
                weight = weight.replace("in inventory:", "")
                weight = weight.replace("inventory:", "")
                weight = weight.replace("kg", "")
                try:
                    return float(weight)
                except ValueError:
                    print("ERROR: clean_weight: Cleaning inventory weight failed.")
                    print(value, weight)
                    exit()

    # Some items have Without/With weights:
    # For example: "'''Without falcon:''' 0.907 kg<br/> '''With falcon:''' 1.814 kg"
    # There are multiple HTML break tags: <br> <br /> <br/>
    break_tags = ["<br>", "<br />", "<br/>"]
    if "without" in weight.lower():
        weight = weight.replace("'''", "")
        for break_tag in break_tags:
            if break_tag in weight:
                weight_list = weight.split(break_tag)
                # Grab first list entry, convert to lower case and replace string
                weight = weight_list[0]
                weight = weight.lower()
                weight = weight.replace("without falcon:", "")
                weight = weight.replace("kg", "")
                try:
                    return float(weight)
                except ValueError:
                    print("ERROR: clean_weight: Cleaning falcon weight failed.")
                    print(value, weight)
                    exit()

    # Do a generic check for an empty string
    # If found, set weight to 0
    if weight == "":
        return 0

    print("ERROR: clean_weight: Cleaning weight property failed.")
    print(value, weight)
    exit()


def clean_quest(value: str, item_id: int) -> bool:
    """Convert the quest entry from an OSRS Wiki infobox to a boolean.

    :param value: The extracted raw wiki text.
    :param item_id: The item ID number.
    :return quest: A boolean to identify if an item is associated with a quest.
    """
    item_id = int(item_id)

    # Clean a quest value
    quest = str(value)
    quest = quest.strip()
    quest = quest.lower()

    # Specific item ID checks
    if item_id in [19730, 19731]:
        return False  # Bloodhound

    # Check quest entry and categorize based on string content
    if quest in ["", "no", "none"]:
        return False
    elif quest in ["yes", "rune mysteries"]:
        return True
    elif "[[" in quest:
        return True
    else:
        print("ERROR: clean_quest: Cleaning quest failed.")
        print(value, quest)
        exit()


def clean_release_date(value: str) -> str:
    """A helper method to convert the release date entry from an OSRS Wiki infobox.

    The returned value will be a specifically formatted string: dd Month YYYY.
    For example, 25 June 2017 or 01 November 2014.

    :param value: The extracted raw wiki text.
    :return release_date: A cleaned release date of an item.
    """
    release_date = str(value)
    release_date = release_date.strip()
    release_date = release_date.replace("[", "")
    release_date = release_date.replace("]", "")

    if release_date == "":
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
        print("ERROR: clean_release_date: Cleaning release date failed.")
        print(value, release_date)
        exit()


def clean_tradeable(value: str, item_id: int) -> bool:
    """Convert the tradeable entry from an OSRS Wiki infobox to a boolean.

    :param value: The extracted raw wiki text.
    :param item_id: The item ID number.
    :return quest: A boolean to identify if an item is tradeable.
    """
    item_id = int(item_id)

    # Clean a quest value
    tradeable = str(value)
    tradeable = tradeable.strip()
    tradeable = tradeable.lower()

    if tradeable in ["", "no", "none"]:
        return False
    elif tradeable in ["yes"]:
        return True
    else:
        print("ERROR: clean_tradeable: Cleaning tradeable property failed.")
        print(value, tradeable)
        exit()


def clean_examine(value: str, name: str) -> str:
    """Convert the examine text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :param name: The name of the item being processed.
    :return tradeable: A cleaned tradeable property of an item.
    """
    examine = str(value)
    examine = examine.strip()

    # Apart from "Clue scroll (master)" and "Clue scroll (beginner)"
    # clues have variable examine text
    clue_scrolls = ["Clue scroll (easy)",
                    "Clue scroll (medium)",
                    "Clue scroll (hard)",
                    "Clue scroll (elite)"]
    if name in clue_scrolls:
        return "A clue!"

    # Medium clue keys are also variable (but not other key variants)
    # Set to first value available
    if name == "Key (medium)":
        return "A key to unlock a treasure chest."

    # Ghrim's book
    # Example: ''Managing Thine Kingdom for Noobes'' by A. Ghrim.
    if name == "Ghrim's book":
        examine = examine.replace("''", "")
        return examine

    # Pet smoke devil
    # Example: <nowiki>*cough*</nowiki>
    if name == "Pet smoke devil":
        return "*cough*"

    # Fix for quest related examine texts (mostly for keys)
    examine = re.sub(r' \([^()]*\)', '', examine)

    # Remove sic
    examine = examine.replace("{{sic}}", "")

    return examine


# MONSTER CLEANERS...


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

    # Quick fix for an equals sign in stats value
    if "=" in value:
        value = value.replace("=", "")

    if isinstance(value, int):
        return value
    elif isinstance(value, str):
        if value[0] == "-" and value[1:].isdigit():
            value = int(value)
        elif value[0] == "+" and value[1:].isdigit():
            value = int(value)
        elif value.isdigit():
            value = int(value)
        else:
            print("clean_stats_value: Cannot int cast stat value")
            exit()
    else:
        # If unable to process, set to 0
        value = 0

    return value


def clean_drop_quantity(value: str) -> str:
    """Convert the drop quantity text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned drop quantity property value.
    """
    if value is None:
        return None
    value = clean_wikitext(value)
    if value == "":
        return None

    # Replace spaces, then remove "(noted)"
    value = value.replace(" ", "")
    value = re.sub(r" *\(noted\) *", '', value)

    # Change semi-colon seperated list of numbers to commas
    value = re.sub(r"[; ]", ',', value)

    # Check the extracted and processed value against the supplied regex
    # Potenital format: "1-10", "1", "2,4,5"
    pattern = re.compile(r"^[0-9]*([-,][0-9]*)?")
    if value and not pattern.match(value):
        print(f"Drop quantity regex failed: {value}")
        exit()

    return value


def clean_drop_rarity(value: str, base_value: str = None) -> float:
    """Convert the drop rartiy text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :param base_value: Used for special drop rartiy rates.
    :return: A cleaned drop rarity property value.
    """
    # Temp fix for 0 division: 484 Bloodveld
    if value == "0/0":
        return float(1/128)

    if value is None:
        return None
    if "#expr" not in value:
        value = clean_wikitext(value)
    if value == "":
        return None

    # Clean the original value
    # Remove: brackets, curly braces, spaces, tidle, plus
    # Remove (if expr): curly braces, spaces
    if "#expr" not in value:
        value = re.sub(r"[\(\){}, ~\+]", '', value)
    else:
        value = re.sub(r"[{} ]", '', value)
    # Quick fix, remove <small></small>
    if "<small>" in value:
        value = re.sub(r"<.*?>", '', value)
    # Remove "Rarity|" from value
    value = value.replace("Rarity|", "")

    # Convert raw value into fraction
    if not value:
        value = None
    elif value.lower() in ["unknown", "varies", "unsure", "random"]:
        value = None
    elif value.lower() == "always":
        value = "1/1"
    elif value.lower() == "common":
        value = "1/8"
    elif value.lower() == "uncommon":
        value = "1/32"
    elif value.lower() == "rare":
        value = "1/128"
    elif value.lower() == "veryrare":
        value = "1/512"
    elif "brimstone" in value.lower():
        # Rarity={{Brimstone rarity|96|bonus=yes}}
        value = value.split("|")
        level = int(value[1])
        try:
            bonus = value[2]
        except IndexError:
            bonus = "no"
        if int(level) < 100:
            value = 0.2 * (level - 100) ** 2 + 100
        else:
            value = -0.2 * level + 120
        if "yes" in bonus:
            value = value * 0.8
        value = f"1/{value}"
    elif "var:herbbase" in value:
        # 1/#expr:1/(40*#var:herbbase) round 1
        numerator = value.split("/")[0]
        denominator = value.split("#expr:")[1]
        denominator = re.sub("round[1 ]", "", denominator)
        denominator = denominator.replace("#var:herbbase", str(base_value))
        denominator = eval(denominator)
        denominator = round(denominator, 1)
        value = str(numerator) + "/" + str(denominator)
    elif "var:seedbase" in value:
        # 1/#expr:1/(40*#var:seedbase) round 1
        numerator = value.split("/")[0]
        denominator = value.split("#expr:")[1]
        denominator = re.sub("round[1 ]", "", denominator)
        denominator = denominator.replace("#var:seedbase", str(base_value))
        denominator = eval(denominator)
        denominator = round(denominator, 1)
        value = str(numerator) + "/" + str(denominator)
    elif "var:uht" in value:
        # 1/#expr:1/(5*#var:uht)round 2
        numerator = value.split("/")[0]
        denominator = value.split("#expr:")[1]
        denominator = re.sub("round[2 ]", "", denominator)
        denominator = denominator.replace("#var:uht", str(base_value))
        denominator = eval(denominator)
        denominator = round(denominator, 1)
        value = str(numerator) + "/" + str(denominator)
    elif "var:bolttipbase" in value:
        # 1/#expr:1/(10*#var:bolttipbase)round1
        numerator = value.split("/")[0]
        denominator = value.split("#expr:")[1]
        denominator = re.sub("round[1 ]", "", denominator)
        denominator = denominator.replace("#var:bolttipbase", str(base_value))
        denominator = eval(denominator)
        denominator = round(denominator, 1)
        value = str(numerator) + "/" + str(denominator)
    elif "#expr:" in value:
        # 1/#expr:1/(1800 / 3500) round 1
        numerator = value.split("/")[0]
        denominator = value.split("#expr:")[1]
        denominator = re.sub("round[1 ]", "", denominator)
        denominator = eval(denominator)
        denominator = round(denominator, 1)
        value = str(numerator) + "/" + str(denominator)
    elif ":" in value:
        value = value.split(":")[0]
    else:
        value = value

    # Check the extracted and processed value against the supplied regex
    # Potential format: "1/1", "1/2.3", "3.5/4", "9.5/5.6"
    pattern = re.compile(r"^[0-9]*(\.[0-9]*)?\/([0-9]*)(\.[0-9]*)?")
    if value and not pattern.match(value):
        print(f"Drop rarity regex failed: {value}")
        # quit()
        value = "0"

    if value is not None:
        value = float(eval(value))

    return value


def clean_drop_requirements(value: str) -> str:
    """Convert the drop requirements text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned drop requirements property value.
    """
    if value is None:
        return None
    value = clean_wikitext(value)
    if value == "":
        return None

    # Parse the drop requirements and try to classify
    if not value:
        value = None
    elif "[[Wilderness" in value:
        value = "wilderness-only"
    elif "[[Konar quo Maten]]" in value:
        value = "konar-task-only"
    elif ("[[Catacombs of Kourend]]" in value or
          "name=catacomb" in value or
          'name="catacomb"' in value):
        value = "catacombs-only"
    elif "[[Krystilia]]" in value:
        value = "wilderness-slayer"
    elif "[[Treasure Trails" in value:
        value = "treasure-trails-only"
    elif "[[Iorwerth Dungeon]]" in value:
        value = "iorwerth-dungeon-only"
    elif "Forthos Dungeon" in value:
        value = "forthos-dungeon-only"
    elif ("[[Revenant Caves]]" in value or
            'name="revcaves"' in value):
        value = "revenants-only"
    else:
        value = None

    return value


def clean_monster_examine(value: str) -> bool:
    """Convert the an examine text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned examine property value.
    """
    if value is None:
        return ""
    value = clean_wikitext(value)
    if value == "":
        return ""

    # Quick fix for multiline examine texts
    value = value.split("\n")[0]

    # Clean the original value
    # Remove: brackets, curly braces, spaces, tidle, plus
    value = re.sub(r'[{}\*"]', '', value)

    # Fix three periods style
    value = value.replace("…", "...")

    # Remove versioned examine text markers
    value = re.sub(r"'{2,}[^']+[']*", '', value)

    # Finally, strip any remaining whitespace
    value = value.strip()

    return value


def clean_attack_type(value: str) -> List:
    """Convert the attack type text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned attack type property value.
    """
    attack_type_list = list()

    if value is None or value == "":
        return attack_type_list

    value = value.lower()

    # Check for specific melee attack types
    if "slash" in value:
        attack_type_list.append("slash")
    if "crush" in value:
        attack_type_list.append("crush")
    if "stab" in value:
        attack_type_list.append("stab")

    # Check for generic melee attack type
    # Do not add if specific melee attack type found
    if "melee" in value:
        if ("slash" not in value and "crush" not in value and "stab" not in value):
            attack_type_list.append("melee")

    if "typeless" in value:
        attack_type_list.append("typeless")

    if "dragonfire" in value:
        attack_type_list.append("dragonfire")

    if "range" in value:
        attack_type_list.append("ranged")

    if "magic" in value and "dragonfire" not in value:
        attack_type_list.append("magic")

    if "curse" in value:
        attack_type_list.append("curse")

    return attack_type_list


def clean_attributes(value: str) -> str:
    """Convert the attributes text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned attribute property value.
    """
    attributes_list = list()

    if value is None or value == "":
        return None

    value = value.lower()

    # Check for specific melee attack types
    if "demon" in value:
        attributes_list.append("demon")
    if "dragon" in value:
        attributes_list.append("dragon")
    if "fiery" in value:
        attributes_list.append("fiery")
    if "kalphite" in value:
        attributes_list.append("kalphite")
    if "leafy" in value:
        attributes_list.append("leafy")
    if "penance" in value:
        attributes_list.append("penance")
    if "shade" in value:
        attributes_list.append("shade")
    if "undead" in value:
        attributes_list.append("undead")
    if "vampyre" in value:
        attributes_list.append("vampyre")
    if "xerician" in value:
        attributes_list.append("xerician")

    if not attributes_list:
        return None

    return attributes_list


def clean_category(value: str) -> str:
    """Convert the category text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned categories property value.
    """
    category_list = list()

    if value is None or value == "" or value.lower() == "no":
        return category_list

    value = clean_wikitext(value)

    value = value.lower()

    value = value.replace("wolves", "wolf")
    value = value.replace("zombies", "zombie")
    value = value.replace("shades", "shade")
    value = value.replace("dogs", "dog")
    value = value.replace("chaos druids", "chaos druid")
    value = value.replace("birds", "bird")
    value = value.replace("knights", "knight")
    value = value.replace("pirates", "pirate")
    value = value.replace("skeletons", "skeleton")
    value = value.replace("lizard", "lizards")
    value = value.replace("lizardsmen", "lizardmen")

    if "|" in value:
        value = value.split("|")[1]

    value_list = None
    if "," in value:
        value_list = list()
        for v in value.split(","):
            v = v.strip()
            value_list.append(v)

    if value_list:
        for value in value_list:
            category_list.append(value)
    else:
        category_list.append(value)

    return category_list


def clean_slayer_xp(value: str) -> float:
    """Convert the slayer xp text entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return: A cleaned slayer_xp property value.
    """
    if value is None:
        return None
    value = clean_wikitext(value)
    if value == "":
        return None
    if "not" in value.lower():
        return None
    if "no" in value.lower():
        return None
    if "n/a" in value.lower():
        return None
    if "yes" in value.lower():
        return None
    if value == "None":
        return None
    if "-" in value.lower():
        value = value.split("-")[0]

    if isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    elif isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            print("Error converting slayer_xp value. exitting.")
            exit()

    return value
