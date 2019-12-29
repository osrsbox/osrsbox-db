"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Populate hard-coded drop tables for monsters.

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
import math
import logging
from typing import Dict
from fractions import Fraction

import mwparserfromhell

logger = logging.getLogger(__name__)


def superior(slayer_level: int) -> Dict:
    """Set superior drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Superior_slayer_monster

    :param slayer_level: The monsters slayer level.
    :return: Dictionary of items on the drop table.
    """
    # Exit if required levels not provided
    if not slayer_level:
        print("Error: drop_tables.superior")
        print("You need these to determine drop rarity!")
        exit(1)

    # Determine drop rates
    staff_drop_rate = 3 / (8 * (200 - (slayer_level + 55)**2 / 125))
    other_drop_rate = 1 / (8 * (200 - (slayer_level + 55)**2 / 125))

    # Populate drop table items
    items = {
        "20730": {
            "id": 20730,
            "name": "Mist battlestaff",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": staff_drop_rate,
            "drop_requirements": "superior"
        },
        "20736": {
            "id": 20736,
            "name": "Dust battlestaff",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": staff_drop_rate,
            "drop_requirements": "superior"
        },
        "21270": {
            "id": 21270,
            "name": "Eternal gem",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": other_drop_rate,
            "drop_requirements": "superior"
        },
        "20724": {
            "id": 20724,
            "name": "Imbued heart",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": other_drop_rate,
            "drop_requirements": "superior"
        }
    }

    return(items)


def wildernessslayer(monster_name: str, combat_level: int, hitpoints: int, slayer_level: int) -> Dict:
    """Set wilderness slayer drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://twitter.com/jagexash/status/1152237123778555904
    https://osrs.wiki/w/Larran%27s_key
    https://osrs.wiki/w/Slayer%27s_enchantment

    :param monster_name: The monsters name.
    :param combat_level: The monsters combat level.
    :param hitpoints: The monsters hitpoints level.
    :param slayer_level: The monsters slayer level.
    :return: Dictionary of items on the drop table.
    """
    # Exit if required levels not provided
    if not combat_level or not hitpoints or not slayer_level:
        print("Error: drop_tables.wildernessslayer")
        print("You need these to determine drop rarity!")
        exit(1)

    # Determine slayer enchantment drop rate
    if monster_name == "Venenatis" or monster_name == "Vet'ion":
        slayers_enchantment_drop_rate = 1/30
    else:
        slayers_enchantment_drop_rate = 1 / (320 - math.floor(hitpoints * 0.8))

    # Determine Larran's key drop rate
    if combat_level <= 80:
        larrans_key_drop_rate = 100 + ((3 / 10) * (80 - combat_level) ** 2)
    elif combat_level > 80 and combat_level < 350:
        # Use linear interpolation to determine drop rate
        larrans_key_drop_rate = math.floor(((combat_level - 81) / (350 - 81)) * (50 - 99) + 99)
        if monster_name in ["Spiritual ranger", "Spiritual warrior", "Spiritual mage"]:
            # Only >= 2 slayer requirement (listed above) get 25% boost
            larrans_key_drop_rate = larrans_key_drop_rate * 1.25
        larrans_key_drop_rate = eval("1/" + str(larrans_key_drop_rate))
    elif combat_level >= 350:
        larrans_key_drop_rate = 1/50

    # Populate drop table items
    items = {
        "23490": {
            "id": 23490,
            "name": "Larran's key",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": larrans_key_drop_rate,
            "drop_requirements": "wilderness-slayer"
        },
        "21257": {
            "id": 21257,
            "name": "Slayer's enchantment",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": slayers_enchantment_drop_rate,
            "drop_requirements": "wilderness-slayer"
        }
    }

    return(items)


def talisman(wikitext: str) -> Dict:
    """Set superior drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Talisman_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "talismandroptable2" in template.lower():
            drop_table_template = template

    table_drop_rate = drop_table_template.split("|")[1]
    table_drop_rate = table_drop_rate.replace("}", "")
    table_drop_rate = float(Fraction(table_drop_rate))

    base_drop_rate = 10/70 * table_drop_rate

    cosmic_drop_rate = 4/70 * table_drop_rate

    chaos_nature_drop_rate = 3/70 * table_drop_rate

    # Populate drop table items
    items = {
        "1438": {
            "id": 1438,
            "name": "Air talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": base_drop_rate,
            "drop_requirements": None
        },
        "1446": {
            "id": 1446,
            "name": "Body talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": base_drop_rate,
            "drop_requirements": None
        },
        "1440": {
            "id": 1440,
            "name": "Earth talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": base_drop_rate,
            "drop_requirements": None
        },
        "1442": {
            "id": 1442,
            "name": "Fire talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": base_drop_rate,
            "drop_requirements": None
        },
        "1448": {
            "id": 1448,
            "name": "Mind talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": base_drop_rate,
            "drop_requirements": None
        },
        "1444": {
            "id": 1444,
            "name": "Water talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": base_drop_rate,
            "drop_requirements": None
        },
        "1454": {
            "id": 1454,
            "name": "Cosmic talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": cosmic_drop_rate,
            "drop_requirements": None
        },
        "1452": {
            "id": 1452,
            "name": "Chaos talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": chaos_nature_drop_rate,
            "drop_requirements": None
        },
        "1462": {
            "id": 1462,
            "name": "Nature talisman",
            "members": False,
            "quantity": "1",
            "noted": False,
            "rarity": chaos_nature_drop_rate,
            "drop_requirements": None
        }
    }

    return(items)


def catacombs(monster_name: str, hitpoints: int, wikitext: str) -> Dict:
    """Set catacombs drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Dark_totem

    :param monster_name: The monsters name.
    :param hitpoints: The monsters hitpoints level.
    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    # Exit if required levels not provided
    if not hitpoints:
        print("Error: drop_tables.catacombs")
        print("You need these to determine drop rarity!")
        exit(1)

    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "catacombsdroptable" in template.lower():
            drop_table_template = template

    # Determine if the monster is superior
    superior = False
    if "superior" in drop_table_template.lower():
        superior = True

    # Determine Ancient shard drop rate, and then quantity
    ancient_shard_drop_rate = 1 / (2/3 * (500 - hitpoints))

    if monster_name == "Skotizo":
        ancient_shard_quantity = "1-4"
    else:
        ancient_shard_quantity = "1"

    # Determine totem drop rate
    if superior:
        totem_drop_rate = 1
    else:
        totem_drop_rate = 1 / (500 - hitpoints)

    # Populate drop table items
    items = {
        "19677": {
            "id": 19677,
            "name": "Ancient shard",
            "members": True,
            "quantity": ancient_shard_quantity,
            "noted": False,
            "rarity": ancient_shard_drop_rate,
            "drop_requirements": "catacombs"
        },
        "19679": {
            "id": 19679,
            "name": "Dark totem base",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": totem_drop_rate,
            "drop_requirements": "catacombs"
        },
        "19681": {
            "id": 19681,
            "name": "Dark totem middle",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": totem_drop_rate,
            "drop_requirements": "catacombs"
        },
        "19683": {
            "id": 19683,
            "name": "Dark totem top",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": totem_drop_rate,
            "drop_requirements": "catacombs"
        }
    }

    return(items)


def herb(members: bool, wikitext: str) -> Dict:
    """Set herb drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Template:HerbDropTable2/doc

    :param members: If the monster is members.
    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    # Exit if required levels not provided
    if members is None:
        print("Error: drop_tables.herb")
        print("You need these to determine drop rarity!")
        exit(1)

    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "herbdroptable2" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")
    drop_table_template = drop_table_template.split("|")

    try:
        quantity = drop_table_template[2]
        if quantity == "f2p=yes":
            quantity = "1"
    except IndexError:
        quantity = "1"

    try:
        base_rarity = eval(drop_table_template[1])
    except ValueError:
        print("Error: drop_tables.herb")
        print("There is no base rarity able to be extracted.")
        exit(1)

    # Populate drop table items
    items = {
        "199": {
            "id": 199,
            "name": "Grimy guam leaf",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/4 * base_rarity,
            "drop_requirements": None
        },
        "201": {
            "id": 201,
            "name": "Grimy marrentill",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/5.333 * base_rarity,
            "drop_requirements": None
        },
        "203": {
            "id": 203,
            "name": "Grimy tarromin",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/7.111 * base_rarity,
            "drop_requirements": None
        },
        "205": {
            "id": 205,
            "name": "Grimy harralander",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/9.143 * base_rarity,
            "drop_requirements": None
        },
        "207": {
            "id": 207,
            "name": "Grimy ranarr weed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/11.64 * base_rarity,
            "drop_requirements": None
        },
        "209": {
            "id": 209,
            "name": "Grimy irit leaf",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/16 * base_rarity,
            "drop_requirements": None
        },
        "211": {
            "id": 211,
            "name": "Grimy avantoe",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/21.33 * base_rarity,
            "drop_requirements": None
        },
        "213": {
            "id": 213,
            "name": "Grimy kwuarm",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/25.6 * base_rarity,
            "drop_requirements": None
        },
        "215": {
            "id": 215,
            "name": "Grimy cadantine",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/32 * base_rarity,
            "drop_requirements": None
        },
        "2485": {
            "id": 2485,
            "name": "Grimy lantadyme",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/42.67 * base_rarity,
            "drop_requirements": None
        },
        "217": {
            "id": 217,
            "name": "Grimy dwarf weed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/42.67 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def usefulherb(wikitext: str) -> Dict:
    """Set useful herb drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Useful_herb_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "usefulherbdroptable2" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        quantity = drop_table_template.split("|")[2]
    except IndexError:
        quantity = "1"

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR HERBDROPTABLE")
        exit(1)

    # Populate drop table items
    items = {
        "211": {
            "id": 211,
            "name": "Grimy avantoe",
            "members": True,
            "quantity": quantity,
            "noted": True,
            "rarity": 1/3.2 * base_rarity,
            "drop_requirements": None
        },
        "3051": {
            "id": 3051,
            "name": "Grimy snapdragon",
            "members": True,
            "quantity": quantity,
            "noted": True,
            "rarity": 1/4 * base_rarity,
            "drop_requirements": None
        },
        "207": {
            "id": 207,
            "name": "Grimy ranarr weed",
            "members": True,
            "quantity": quantity,
            "noted": True,
            "rarity": 1/4 * base_rarity,
            "drop_requirements": None
        },
        "219": {
            "id": 219,
            "name": "Grimy torstol",
            "members": True,
            "quantity": quantity,
            "noted": True,
            "rarity": 1/5.333 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def gem(wikitext: str) -> Dict:
    """Set gem drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Useful_herb_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "usefulherbdroptable2" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR HERBDROPTABLE")
        exit(1)

    # Populate drop table items
    items = {
        "1623": {
            "id": 1623,
            "name": "Uncut sapphire",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/4 * base_rarity,
            "drop_requirements": None
        },
        "1621": {
            "id": 1621,
            "name": "Uncut emerald",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/8 * base_rarity,
            "drop_requirements": None
        },
        "1619": {
            "id": 1619,
            "name": "Uncut ruby",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/16 * base_rarity,
            "drop_requirements": None
        },
        "1452": {
            "id": 1452,
            "name": "Chaos talisman",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/42.67 * base_rarity,
            "drop_requirements": None
        },
        "1462": {
            "id": 1462,
            "name": "Nature talisman",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/42.67 * base_rarity,
            "drop_requirements": None
        },
        "1617": {
            "id": 1617,
            "name": "Uncut diamond",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/64 * base_rarity,
            "drop_requirements": None
        },
        "830": {
            "id": 830,
            "name": "Rune javelin",
            "members": True,
            "quantity": "5",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "drop_requirements": None
        },
        "987": {
            "id": 987,
            "name": "Loop half of key",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "drop_requirements": None
        },
        "985": {
            "id": 985,
            "name": "Tooth half of key",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "drop_requirements": None
        },
        "1247": {
            "id": 1247,
            "name": "Rune spear",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * 1/16 * base_rarity,
            "drop_requirements": None
        },
        "2366": {
            "id": 2366,
            "name": "Shield left half",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * 1/32 * base_rarity,
            "drop_requirements": None
        },
        "1249": {
            "id": 1249,
            "name": "Dragon spear",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * 1/42.67 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)
