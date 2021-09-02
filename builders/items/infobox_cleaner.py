"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Various methods to help clean OSRS Wiki wikitext entries.

Copyright (c) 2021, PH01L

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
from datetime import datetime

import dateparser


# Source: runelite/runelite-wiki-scraper
WEIGHT_REDUCTION_EXTRACTOR = re.compile(
    r"(?i)'''(?:In )?inventory:?''':? ([0-9.-]+) kg<br ?\/?> *'''Equipped:?''':? ([0-9.-]+)")

unequipable = [
    286,  # Orange goblin mail
    287,  # Blue goblin mail,
    288,  # Goblin mail
    740,  # Blue hat (Legends' Quest)
    713,  # Clue scroll
    818,  # Poisoned dart(p)
    1235,  # Poisoned dagger(p)
    2422,  # Blue partyhat (Draynor Bank Robbery) 
    2513,  # Dragon chainbody (My Arm's Big Adventure)
    4178,  # Abyssal whip (My Arm's Big Adventure)
    4180,  # Dragon platelegs (My Arm's Big Adventure)
    4181,  # Mouth grip
    4213,  # New crystal bow
    4235,  # New crystal shield
    5056,  # Dwarven battleaxe
    5057,  # Dwarven battleaxe
    5058,  # Dwarven battleaxe
    5059,  # Dwarven battleaxe
    5062,  # Left boot
    5063,  # Right boot
    5064,  # Exquisite boots
    5067,  # Exquisite clothes
    5684,  # Poison dagger(p+)
    5702,  # Poison dagger(p++)
    6788,  # Torn robe
    6789,  # Torn robe
    6818,  # Bow-sword
    6864,  # Marionette handle
    6893,  # Leather boots (Mage Training Arena)
    6894,  # Adamant kiteshield (Mage Training Arena)
    6895,  # Adamant med helm (Mage Training Arena)
    6897,  # Rune longsword (Mage Training Arena)
    6967,  # Dragon med helm (My Arm's Big Adventure)
    7804,  # Zaros mjolnir
    8871,  # Crate with zanik [TODO: no attack speed]
    8856,  # Defensive shield [TODO: no weapon type]
    9054,  # Red goblin mail
    9055,  # Black goblin mail
    9056,  # Yellow goblin mail
    9057,  # Green goblin mail
    9058,  # Purple goblin mail
    9059,  # Pink goblin mail
    9665,  # Torch
    9702,  # Stick
    9906,  # Ghost buster 500
    9907,  # Ghost buster 500
    9908,  # Ghost buster 500
    9909,  # Ghost buster 500
    9910,  # Ghost buster 500
    9911,  # Ghost buster 500
    9912,  # Ghost buster 500
    10840,  # A jester stick
    11165,  # Phoenix crossbow
    11167,  # Phoenix crossbow
    11700,  # Bronze arrow (Barbarian Assault)
    11701,  # Iron arrow (Barbarian Assault)
    11702,  # Steel arrow (Barbarian Assault)
    11703,  # Mithril arrow (Barbarian Assault)
    22664,  # Scythe of vitur (JMod item)
    22665,  # Armadyl godsword (JMod item)
    22666,  # Rubber chicken (JMod item)
    10556,  # Attacker icon
    22346,  # Attacker icon
    22347,  # Attacker icon
    22348,  # Attacker icon
    22349,  # Attacker icon
    22721,  # Attacker icon
    22722,  # Attacker icon
    22723,  # Attacker icon
    22729,  # Attacker icon
    22730,  # Attacker icon
    23460,  # Attacker icon
    23461,  # Attacker icon
    23462,  # Attacker icon
    23463,  # Attacker icon
    23464,  # Attacker icon
    23465,  # Attacker icon
    10558,  # Defender icon
    22340,  # Defender icon
    22341,  # Defender icon
    22342,  # Defender icon
    22343,  # Defender icon
    22344,  # Defender icon
    22345,  # Defender icon
    22725,  # Defender icon
    22726,  # Defender icon
    22727,  # Defender icon
    22728,  # Defender icon
    23466,  # Defender icon
    23467,  # Defender icon
    23468,  # Defender icon
    23469,  # Defender icon
    23470,  # Defender icon
    10557,  # Collector icon
    22312,  # Collector icon
    22313,  # Collector icon
    22314,  # Collector icon
    22315,  # Collector icon
    22337,  # Collector icon
    22338,  # Collector icon
    22339,  # Collector icon
    22724,  # Collector icon
    23471,  # Collector icon
    23472,  # Collector icon
    23473,  # Collector icon
    23474,  # Collector icon
    23475,  # Collector icon
    23476,  # Collector icon
    23477,  # Collector icon
    10559,  # Healer icon
    10567,  # Healer icon
    20802,  # Healer icon
    22308,  # Healer icon
    22309,  # Healer icon
    22310,  # Healer icon
    22311,  # Healer icon
    23478,  # Healer icon
    23479,  # Healer icon
    23480,  # Healer icon
    23481,  # Healer icon
    23482,  # Healer icon
    23483,  # Healer icon
    23484,  # Healer icon
    23485,  # Healer icon
    23486,  # Healer icon
    13538,  # Shayzien supply gloves (1)
    13539,  # Shayzien supply boots (1)
    13540,  # Shayzien supply helm (1)
    13541,  # Shayzien supply greaves (1)
    13542,  # Shayzien supply platebody (1)
    13543,  # Shayzien supply gloves (2)
    13544,  # Shayzien supply boots (2)
    13545,  # Shayzien supply helm (2)
    13546,  # Shayzien supply greaves (2)
    13547,  # Shayzien supply platebody (2)
    13548,  # Shayzien supply gloves (3)
    13549,  # Shayzien supply boots (3)
    13550,  # Shayzien supply helm (3)
    13551,  # Shayzien supply greaves (3)
    13552,  # Shayzien supply platebody (3)
    13553,  # Shayzien supply gloves (4)
    13554,  # Shayzien supply boots (4)
    13555,  # Shayzien supply helm (4)
    13556,  # Shayzien supply greaves (4)
    13557,  # Shayzien supply platebody (4)
    13558,  # Shayzien supply gloves (5)
    13559,  # Shayzien supply boots (5)
    13560,  # Shayzien supply helm (5)
    13561,  # Shayzien supply greaves (5)
    13562,  # Shayzien supply platebody (5)
    21428,  # Wilderness cape (Wilderness Wars)
    21429,  # Wilderness cape (Wilderness Wars)
    21430,  # Wilderness cape (Wilderness Wars)
    21431,  # Wilderness cape (Wilderness Wars)
    21432,  # Wilderness cape (Wilderness Wars)
    21433,  # Wilderness champion amulet
    21434,  # Wilderness cape (Wilderness Wars, Champion)
    21435,  # Wilderness cape (Wilderness Wars, Champion)
    21436,  # Wilderness cape (Wilderness Wars, Champion)
    21437,  # Wilderness cape (Wilderness Wars, Champion)
    21438,  # Wilderness cape (Wilderness Wars, Champion)
    22812,  # Dragon knife (animation item)
    22814,  # Dragon knife (animation item)
    25212,  # Blue icon
    25213,  # Blue icon
    25214,  # Blue icon
    25215,  # Blue icon
    25216,  # Blue icon
    25217,  # Blue icon
    25218,  # Blue icon
    25219,  # Blue icon
    25220,  # Blue icon
    25221,  # Blue icon
    25222,  # Blue icon
    25223,  # Blue icon
    25224,  # Blue icon
    25225,  # Blue icon
    25226,  # Blue icon
    25227,  # Blue icon
    25228,  # Red icon
    25229,  # Red icon
    25230,  # Red icon
    25231,  # Red icon
    25232,  # Red icon
    25233,  # Red icon
    25234,  # Red icon
    25235,  # Red icon
    25236,  # Red icon
    25237,  # Red icon
    25238,  # Red icon
    25239,  # Red icon
    25240,  # Red icon
    25241,  # Red icon
    25242,  # Red icon
    25243,  # Red icon
    25987,  # Tumeken's heka
    25989,  # Tumeken's heka (uncharged)
]


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


def caller(value: str, prop: str):
    """Calls specific function based on property name.

    Since there is a dict loop method to reduce code duplication,
    there needs to be a way to call the function that matches the
    property. This helps call the function and return the cleaned
    values.

    :param value: Template value extracted in raw wikitext format.
    :param prop: The template property being processed.
    :return value: Cleaned template value.
    """
    value = globals()[prop](value)
    return value


def weight(value: str, item_id: int) -> float:
    """Convert the weight entry from a OSRS Wiki infobox to a float.

    :param value: Template value extracted in raw wikitext format.
    :param item_id: The item ID number.
    :return weight: The weight of an item.
    """
    if value is None or value == "":
        return None

    item_id = int(item_id)

    # Handle weight reducing items as ID changes when equipped
    if item_id in [10073]:
        # Spotted cape
        return -2.2
    elif item_id in [89, 10554, 10074]:
        # Boots of lightness, Penance gloves, Spottier cape
        return -4.5
    elif item_id in [13342, 13340, 13341]:
        # Max cape, Agility cape, Agility cape (t)
        return -4.0
    elif item_id in [11851, 13580, 13592, 13604, 13616, 13628, 13668, 21063]:
        # Graceful hood variants
        return -3.0
    elif item_id in [11853, 13582, 13594, 13606, 13618, 13630, 13670, 21066]:
        # Graceful cape variants
        return -4.0
    elif item_id in [11855, 13584, 13596, 13608, 13620, 13632, 13672, 21069]:
        # Graceful top variants
        return -5.0
    elif item_id in [11857, 13586, 13598, 13610, 13622, 13634, 13674, 21072]:
        # Graceful legs variants
        return -6.0
    elif item_id in [11859, 13588, 13600, 13612, 13624, 13636, 13676, 21075]:
        # Graceful gloves variants
        return -3.0
    elif item_id in [11861, 13590, 13602, 13614, 13626, 13638, 13678, 21078]:
        # Graceful boots variants
        return -4.0

    if value.endswith("kg"):
        value = value[:-2].strip()
    else:
        value = str(value).strip()

    # The weight property is usally quite clean...
    # Try float cast the value, and return
    try:
        return float(value)
    except ValueError:
        pass

    # Handle when there is inventory/equipable weights
    # Source: runelite/runelite-wiki-scraper
    reducer = WEIGHT_REDUCTION_EXTRACTOR.match(value)
    if reducer:
        # Get inventory weight (as worn wieght handled above)
        # Group 1 is inventory, 2 is equipped
        value = reducer.group(1)
        value = float(value)
        return value

    return None


def quest(value: str) -> bool:
    """Convert the quest entry from an OSRS Wiki infobox to a boolean.

    :param value: The extracted raw wiki text.
    :return quest: A boolean to identify if an item is associated with a quest.
    """
    if value is None:
        return False

    quest = str(value).strip().lower()
    if quest in ["yes"]:
        return True
    elif "[[" in quest:
        return True
    else:
        return False


def release_date(value: str) -> str:
    """Convert the release date entry to ISO 8601 date format.

    :param value: The extracted raw wiki text.
    :return release_date: A cleaned release date of an item.
    """
    release_date = clean_wikitext(value)

    if release_date == "":
        return None

    try:
        release_date = datetime.strptime(release_date, "%d %B %Y")
        return release_date.date().isoformat()
    except ValueError:
        pass

    try:
        release_date = dateparser.parse(release_date)
        release_date = release_date.date().isoformat()
    except (ValueError, TypeError, AttributeError):
        return None


def tradeable(value: str) -> bool:
    """Convert the tradeable entry from an OSRS Wiki infobox to a boolean.

    :param value: The extracted raw wiki text.
    :return quest: A boolean to identify if an item is tradeable.
    """
    # Clean a quest value
    tradeable = str(value).strip().lower()

    if tradeable in ["yes"]:
        return True
    else:
        return False


def examine(value: str, name: str) -> str:
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


def stats(value: str) -> int:
    """Convert a item stat value to an integer.

    :param value: Template value extracted from raw wikitext.
    :return value: A cleaned stat value as an int.
    """
    try:
        return int(value)
    except ValueError:
        return 0


def slot(value: str) -> str:
    """Convert a slot value to a cleaned string.

    :param value: Template value extracted from raw wikitext.
    :return value: A cleaned slot value as an str.
    """
    if "\n" in value:  # TODO: Remove when comment fixed in fish sack barrel
        value = value.split("\n")[0]

    try:
        return value.lower()
    except ValueError:
        return ""


def speed(value: str) -> int:
    """Convert a item weapon speed value to an integer.

    :param value: Template value extracted from raw wikitext.
    :return value: A cleaned speed value as an int.
    """
    try:
        return int(value)
    except ValueError:
        return None


def weapon_type(value: str) -> str:
    """Convert a item weapon type value to a clean string.

    :param value: Template value extracted from raw wikitext.
    :return value: A cleaned weapon type value.
    """
    if not value:
        return None

    value = value.replace("{", "").replace("}", "")
    value = value.replace(" ", "_")
    value = value.lower()

    try:
        value = value.split("|")[1]
    except IndexError:
        return None

    return value
