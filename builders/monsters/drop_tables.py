"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Populate hard-coded drop tables for monsters.

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
            "drop_requirements": "superior-only"
        },
        "20736": {
            "id": 20736,
            "name": "Dust battlestaff",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": staff_drop_rate,
            "drop_requirements": "superior-only"
        },
        "21270": {
            "id": 21270,
            "name": "Eternal gem",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": other_drop_rate,
            "drop_requirements": "superior-only"
        },
        "20724": {
            "id": 20724,
            "name": "Imbued heart",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": other_drop_rate,
            "drop_requirements": "superior-only"
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
    # if not combat_level or not hitpoints or not slayer_level:
    if not combat_level or not slayer_level:
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
        larrans_key_drop_rate = 100 + ((3 / 10) * (80 - combat_level) * (80 - combat_level))
        larrans_key_drop_rate = f"1/{larrans_key_drop_rate}"
        larrans_key_drop_rate = eval(larrans_key_drop_rate)
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
            "drop_requirements": "krystilia-task-only"
        },
        "21257": {
            "id": 21257,
            "name": "Slayer's enchantment",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": slayers_enchantment_drop_rate,
            "drop_requirements": "krystilia-task-only"
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
            "drop_requirements": "catacombs-only"
        },
        "19679": {
            "id": 19679,
            "name": "Dark totem base",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": totem_drop_rate,
            "drop_requirements": "catacombs-only"
        },
        "19681": {
            "id": 19681,
            "name": "Dark totem middle",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": totem_drop_rate,
            "drop_requirements": "catacombs-only"
        },
        "19683": {
            "id": 19683,
            "name": "Dark totem top",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": totem_drop_rate,
            "drop_requirements": "catacombs-only"
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
    if "Rolls=3" in drop_table_template:
        drop_table_template.remove('Rolls=3')

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
        print("NO BASE RARITY FOR: drop_tables.herb")
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
        print("NO BASE RARITY FOR: drop_tables.usefulherb")
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
        print("NO BASE RARITY FOR: drop_tables.herb")
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


def fixedallotmentseed(wikitext: str) -> Dict:
    """Set allotment seed drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Fixed_allotment_seed_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "fixedallotmentseeddroptable2" in template.lower():
            drop_table_template = template
        if "dropsallotmenttable" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except (ValueError, IndexError):
        # print("NO BASE RARITY FOR: drop_tables.allotmentseed")
        base_rarity = 6/128

    # Populate drop table items
    items = {
        "5318": {
            "id": 5318,
            "name": "Potato seed",
            "members": True,
            "quantity": "4",
            "noted": False,
            "rarity": 1/2.74 * base_rarity,
            "drop_requirements": None
        },
        "5319": {
            "id": 5319,
            "name": "Onion seed",
            "members": True,
            "quantity": "4",
            "noted": False,
            "rarity": 1/3.653 * base_rarity,
            "drop_requirements": None
        },
        "5324": {
            "id": 5324,
            "name": "Cabbage seed",
            "members": True,
            "quantity": "4",
            "noted": False,
            "rarity": 1/5.479 * base_rarity,
            "drop_requirements": None
        },
        "5322": {
            "id": 5322,
            "name": "Tomato seed",
            "members": True,
            "quantity": "3",
            "noted": False,
            "rarity": 1/10.96 * base_rarity,
            "drop_requirements": None
        },
        "5320": {
            "id": 5320,
            "name": "Sweetcorn seed",
            "members": True,
            "quantity": "3",
            "noted": False,
            "rarity": 1/21.92 * base_rarity,
            "drop_requirements": None
        },
        "5323": {
            "id": 5323,
            "name": "Strawberry seed",
            "members": True,
            "quantity": "2",
            "noted": False,
            "rarity": 1/43.83 * base_rarity,
            "drop_requirements": None
        },
        "5321": {
            "id": 5321,
            "name": "Watermelon seed",
            "members": True,
            "quantity": "2",
            "noted": False,
            "rarity": 1/87.67 * base_rarity,
            "drop_requirements": None
        },
        "22879": {
            "id": 22879,
            "name": "Snape grass seed",
            "members": True,
            "quantity": "2",
            "noted": False,
            "rarity": 1/131.5 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def treeseed(wikitext: str) -> Dict:
    """Set tree seed drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Tree-herb_seed_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "treeherbseeddroptable2" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR: drop_tables.treeseed")
        exit(1)

    if "multiplier=2-3" in drop_table_template:
        quantity = "2-3"
        watermelon_quantity = "30-45"
    elif "multiplier=2" in drop_table_template:
        quantity = "2"
        watermelon_quantity = "30"
    else:
        quantity = "1"
        watermelon_quantity = "15"

    # Populate drop table items
    items = {
        "5295": {
            "id": 5295,
            "name": "Ranarr seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/8.333 * base_rarity,
            "drop_requirements": None
        },
        "5300": {
            "id": 5300,
            "name": "Snapdragon seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/8.929 * base_rarity,
            "drop_requirements": None
        },
        "5304": {
            "id": 5304,
            "name": "Torstol seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/11.36 * base_rarity,
            "drop_requirements": None
        },
        "5321": {
            "id": 5321,
            "name": "Watermelon seed",
            "members": True,
            "quantity": watermelon_quantity,
            "noted": False,
            "rarity": 1/12.5 * base_rarity,
            "drop_requirements": None
        },
        "5313": {
            "id": 5313,
            "name": "Willow seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/12.5 * base_rarity,
            "drop_requirements": None
        },
        "21488": {
            "id": 21488,
            "name": "Mahogany seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/13.89 * base_rarity,
            "drop_requirements": None
        },
        "5314": {
            "id": 5314,
            "name": "Maple seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/13.89 * base_rarity,
            "drop_requirements": None
        },
        "21486": {
            "id": 21486,
            "name": "Teak seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/13.89 * base_rarity,
            "drop_requirements": None
        },
        "5315": {
            "id": 5315,
            "name": "Yew seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/13.89 * base_rarity,
            "drop_requirements": None
        },
        "5288": {
            "id": 5288,
            "name": "Papaya tree seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/17.86 * base_rarity,
            "drop_requirements": None
        },
        "5316": {
            "id": 5316,
            "name": "Magic seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/20.83 * base_rarity,
            "drop_requirements": None
        },
        "5289": {
            "id": 5289,
            "name": "Palm tree seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/25 * base_rarity,
            "drop_requirements": None
        },
        "5317": {
            "id": 5317,
            "name": "Spirit seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/31.25 * base_rarity,
            "drop_requirements": None
        },
        "22877": {
            "id": 22877,
            "name": "Dragonfruit tree seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/41.67 * base_rarity,
            "drop_requirements": None
        },
        "22869": {
            "id": 22869,
            "name": "Celastrus seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/62.5 * base_rarity,
            "drop_requirements": None
        },
        "22871": {
            "id": 22871,
            "name": "Redwood tree seed",
            "members": True,
            "quantity": quantity,
            "noted": False,
            "rarity": 1/62.5 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def rareseed(wikitext: str) -> Dict:
    """Set rare seed drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Rare_seed_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "rareseeddroptable" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")
    drop_table_template = drop_table_template.replace("|Rolls=3", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR: drop_tables.rareseed")
        exit(1)

    # Populate drop table items
    items = {
        "5296": {
            "id": 5296,
            "name": "Toadflax seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/5.064 * base_rarity,
            "drop_requirements": None
        },
        "5297": {
            "id": 5297,
            "name": "Irit seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/7.438 * base_rarity,
            "drop_requirements": None
        },
        "5281": {
            "id": 5281,
            "name": "Belladonna seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/7.677 * base_rarity,
            "drop_requirements": None
        },
        "5298": {
            "id": 5298,
            "name": "Avantoe seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/10.82 * base_rarity,
            "drop_requirements": None
        },
        "5106": {
            "id": 5106,
            "name": "Poison ivy seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/10.82 * base_rarity,
            "drop_requirements": None
        },
        "5280": {
            "id": 5280,
            "name": "Cactus seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/11.33 * base_rarity,
            "drop_requirements": None
        },
        "5299": {
            "id": 5299,
            "name": "Kwuarm seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/15.87 * base_rarity,
            "drop_requirements": None
        },
        "22873": {
            "id": 22873,
            "name": "Potato cactus seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/15.87 * base_rarity,
            "drop_requirements": None
        },
        "5300": {
            "id": 5300,
            "name": "Snapdragon seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/23.8 * base_rarity,
            "drop_requirements": None
        },
        "5301": {
            "id": 5301,
            "name": "Cadantine seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/34 * base_rarity,
            "drop_requirements": None
        },
        "5302": {
            "id": 5302,
            "name": "Lantadyme seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/47.6 * base_rarity,
            "drop_requirements": None
        },
        "22879": {
            "id": 22879,
            "name": "Snape grass seed",
            "members": True,
            "quantity": "3",
            "noted": False,
            "rarity": 1/59.5 * base_rarity,
            "drop_requirements": None
        },
        "5303": {
            "id": 5303,
            "name": "Dwarf weed seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/79.33 * base_rarity,
            "drop_requirements": None
        },
        "5304": {
            "id": 5304,
            "name": "Torstol seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/119 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def variableallotmentseed(wikitext: str) -> Dict:
    """Set rare seed drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Rare_seed_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "rareseeddroptable" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR: drop_tables.rareseed")
        exit(1)

    # Populate drop table items
    items = {
        "5318": {
            "id": 5318,
            "name": "Potato seed",
            "members": True,
            "quantity": "1-4",
            "noted": False,
            "rarity": 1/2 * base_rarity,
            "drop_requirements": None
        },
        "5319": {
            "id": 5319,
            "name": "Onion seed",
            "members": True,
            "quantity": "1-3",
            "noted": False,
            "rarity": 1/4 * base_rarity,
            "drop_requirements": None
        },
        "5324": {
            "id": 5324,
            "name": "Cabbage seed",
            "members": True,
            "quantity": "1-3",
            "noted": False,
            "rarity": 1/8 * base_rarity,
            "drop_requirements": None
        },
        "5322": {
            "id": 5322,
            "name": "Tomato seed",
            "members": True,
            "quantity": "1-2",
            "noted": False,
            "rarity": 1/16 * base_rarity,
            "drop_requirements": None
        },
        "5320": {
            "id": 5320,
            "name": "Sweetcorn seed",
            "members": True,
            "quantity": "1-2",
            "noted": False,
            "rarity": 1/32 * base_rarity,
            "drop_requirements": None
        },
        "5323": {
            "id": 5323,
            "name": "Strawberry seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/64 * base_rarity,
            "drop_requirements": None
        },
        "5321": {
            "id": 5321,
            "name": "Watermelon seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "drop_requirements": None
        },
        "22879": {
            "id": 22879,
            "name": "Snape grass seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def commonseed(wikitext: str) -> Dict:
    """Set common seed drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Common_seed_drop_table

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "manyseeddroptable2" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR: drop_tables.commonseed")
        exit(1)

    # Populate drop table items
    items = {
        "5100": {
            "id": 5100,
            "name": "Limpwurt seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/7.65 * base_rarity,
            "drop_requirements": None
        },
        "5323": {
            "id": 5323,
            "name": "Strawberry seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/8 * base_rarity,
            "drop_requirements": None
        },
        "5292": {
            "id": 5292,
            "name": "Marrentill seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/8.384 * base_rarity,
            "drop_requirements": None
        },
        "5104": {
            "id": 5104,
            "name": "Jangerberry seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/11.39 * base_rarity,
            "drop_requirements": None
        },
        "5293": {
            "id": 5293,
            "name": "Tarromin seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/12.33 * base_rarity,
            "drop_requirements": None
        },
        "5311": {
            "id": 5311,
            "name": "Wildblood seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/12.63 * base_rarity,
            "drop_requirements": None
        },
        "5321": {
            "id": 5321,
            "name": "Watermelon seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/16.63 * base_rarity,
            "drop_requirements": None
        },
        "5294": {
            "id": 5294,
            "name": "Harralander seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/18.71 * base_rarity,
            "drop_requirements": None
        },
        "22879": {
            "id": 22879,
            "name": "Snape grass seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/26.2 * base_rarity,
            "drop_requirements": None
        },
        "5295": {
            "id": 5295,
            "name": "Ranarr seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/26.87 * base_rarity,
            "drop_requirements": None
        },
        "5105": {
            "id": 5105,
            "name": "Whiteberry seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/30.82 * base_rarity,
            "drop_requirements": None
        },
        "5282": {
            "id": 5282,
            "name": "Mushroom spore",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/36.14 * base_rarity,
            "drop_requirements": None
        },
        "5296": {
            "id": 5296,
            "name": "Toadflax seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/38.81 * base_rarity,
            "drop_requirements": None
        },
        "5281": {
            "id": 5281,
            "name": "Belladonna seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/58.22 * base_rarity,
            "drop_requirements": None
        },
        "5297": {
            "id": 5297,
            "name": "Irit seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/58.22 * base_rarity,
            "drop_requirements": None
        },
        "5106": {
            "id": 5106,
            "name": "Poison ivy seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/80.62 * base_rarity,
            "drop_requirements": None
        },
        "5298": {
            "id": 5298,
            "name": "Avantoe seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/87.33 * base_rarity,
            "drop_requirements": None
        },
        "5280": {
            "id": 5280,
            "name": "Cactus seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/87.33 * base_rarity,
            "drop_requirements": None
        },
        "5299": {
            "id": 5299,
            "name": "Kwuarm seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/116.4 * base_rarity,
            "drop_requirements": None
        },
        "22873": {
            "id": 22873,
            "name": "Potato cactus seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/131 * base_rarity,
            "drop_requirements": None
        },
        "5300": {
            "id": 5300,
            "name": "Snapdragon seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/209.6 * base_rarity,
            "drop_requirements": None
        },
        "5301": {
            "id": 5301,
            "name": "Cadantine seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/262 * base_rarity,
            "drop_requirements": None
        },
        "5302": {
            "id": 5302,
            "name": "Lantadyme seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/349.3 * base_rarity,
            "drop_requirements": None
        },
        "5303": {
            "id": 5303,
            "name": "Dwarf weed seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/524 * base_rarity,
            "drop_requirements": None
        },
        "5304": {
            "id": 5304,
            "name": "Torstol seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/1048 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def hopsseed(wikitext: str) -> Dict:
    """Set hops seed drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Template:HopsDropTable2

    :param wikitext: The monsters wikitext as a string.
    :return: Dictionary of items on the drop table.
    """
    drop_table_template = None
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    for template in templates:
        if "hopsdroptable2" in template.lower():
            drop_table_template = template

    drop_table_template = drop_table_template.replace("{", "")
    drop_table_template = drop_table_template.replace("}", "")

    try:
        base_rarity = float(Fraction(drop_table_template.split("|")[1]))
    except ValueError:
        print("NO BASE RARITY FOR: drop_tables.hopsseed")
        exit(1)

    # Populate drop table items
    items = {
        "5305": {
            "id": 5305,
            "name": "Barley seed",
            "members": True,
            "quantity": "4",
            "noted": False,
            "rarity": 1/3.228 * base_rarity,
            "drop_requirements": None
        },
        "5307": {
            "id": 5307,
            "name": "Hammerstone seed",
            "members": True,
            "quantity": "3",
            "noted": False,
            "rarity": 1/4.035 * base_rarity,
            "drop_requirements": None
        },
        "5308": {
            "id": 5308,
            "name": "Asgarnian seed",
            "members": True,
            "quantity": "3",
            "noted": False,
            "rarity": 1/6.647 * base_rarity,
            "drop_requirements": None
        },
        "5306": {
            "id": 5306,
            "name": "Jute seed",
            "members": True,
            "quantity": "2",
            "noted": False,
            "rarity": 1/6.647 * base_rarity,
            "drop_requirements": None
        },
        "5309": {
            "id": 5309,
            "name": "Yanillian seed",
            "members": True,
            "quantity": "2",
            "noted": False,
            "rarity": 1/10.272 * base_rarity,
            "drop_requirements": None
        },
        "5310": {
            "id": 5310,
            "name": "Krandorian seed",
            "members": True,
            "quantity": "2",
            "noted": False,
            "rarity": 113/4 * base_rarity,
            "drop_requirements": None
        },
        "5311": {
            "id": 5311,
            "name": "Wildblood seed",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/113 * base_rarity,
            "drop_requirements": None
        }
    }

    return(items)


def revenants(wikitext: str, combat_level: int, hitpoints: int) -> Dict:
    """Set revenant drop tables items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://oldschool.runescape.wiki/w/Template:Revenants/Drops
    https://twitter.com/JagexAsh/status/1051241566852050944/photo/1
    https://www.reddit.com/r/2007scape/comments/9nzkf5/using_mod_ashs_newly_release_rev_drop_formula/

    :param wikitext: The monsters wikitext as a string.
    :param combat_level: The monsters combat level.
    :param hitpoints: The monsters hitpoints level.
    :return: Dictionary of items on the drop table.
    """

    """
    {{#vardefine:A|{{#expr:floor(2200/floor(sqrt({{{combat|135}}})))}}}}
    {{#vardefine:B|{{#expr:15 + floor((({{{combat|135}}}+60)^2)/200)}}}}
    {{#vardefine:mediocreStandardChance|
    {{#expr:106*{{max|1|{{#var:A}}/({{min|{{#var:B}}|{{#var:A}}}}-1)}}}}}}
    """
    A = math.floor(2200/math.floor(math.sqrt(combat_level)))
    B = 15 + math.floor((combat_level + 60) ** 2 / 200)
    MSC = 106 * max(1, A) / (min(B, A) - 1)
    # print("A", A)
    # print("B", B)
    # print("MSC", MSC)

    # Determine Revenant ether quantity using combat level
    ether_quantity = 1 + math.floor(math.sqrt(combat_level) + 1 / 2)

    # Populate drop table items
    items = {
        "21820": {
            "id": 21820,
            "name": "Revenant ether",
            "members": True,
            "quantity": f"1-{ether_quantity}",
            "noted": False,
            "rarity": 1.0,
            "drop_requirements": None
        },
        "22557": {
            "id": 22557,
            "name": "Amulet of avarice",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 * 2.5),
            "drop_requirements": None
        },
        "22547": {
            "id": 22547,
            "name": "Craw's bow (u)",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 * 5),
            "drop_requirements": None
        },
        "22552": {
            "id": 22552,
            "name": "Thammaron's sceptre (u)",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 * 5),
            "drop_requirements": None
        },
        "22542": {
            "id": 22557,
            "name": "Viggora's chainmace (u)",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 * 5),
            "drop_requirements": None
        },
        "21807": {
            "id": 21807,
            "name": "Ancient emblem",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 6),
            "drop_requirements": None
        },
        "21810": {
            "id": 21810,
            "name": "Ancient totem",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 5),
            "drop_requirements": None
        },
        "21813": {
            "id": 21813,
            "name": "Ancient statuette",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 4),
            "drop_requirements": None
        },
        "21804": {
            "id": 21804,
            "name": "Ancient crystal",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 3),
            "drop_requirements": None
        },
        "22299": {
            "id": 22299,
            "name": "Ancient medallion",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 2),
            "drop_requirements": None
        },
        "22302": {
            "id": 22302,
            "name": "Ancient effigy",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 1),
            "drop_requirements": None
        },
        "22305": {
            "id": 22305,
            "name": "Ancient relic",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 1),
            "drop_requirements": None
        },
        "1391": {
            "id": 1391,
            "name": "Battlestaff",
            "members": True,
            "quantity": "3",
            "noted": True,
            "rarity": 1 / (MSC / 5),
            "drop_requirements": None
        },
        "21817": {
            "id": 21817,
            "name": "Bracelet of ethereum (uncharged)",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 15),
            "drop_requirements": None
        },
        "1163": {
            "id": 1163,
            "name": "Rune full helm",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "1127": {
            "id": 1127,
            "name": "Rune platebody",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "1079": {
            "id": 1079,
            "name": "Rune platelegs",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "1201": {
            "id": 1201,
            "name": "Rune kiteshield",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "1347": {
            "id": 1347,
            "name": "Rune warhammer",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "4087": {
            "id": 4087,
            "name": "Dragon platelegs",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 1),
            "drop_requirements": None
        },
        "4585": {
            "id": 4585,
            "name": "Dragon plateskirt",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 1),
            "drop_requirements": None
        },
        "1215": {
            "id": 1215,
            "name": "Dragon dagger",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 1),
            "drop_requirements": None
        },
        "1305": {
            "id": 1305,
            "name": "Dragon longsword",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 1),
            "drop_requirements": None
        },
        "1149": {
            "id": 1149,
            "name": "Dragon med helm",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (A * 40 / 13),
            "drop_requirements": None
        },
        "453": {
            "id": 453,
            "name": "Coal",
            "members": True,
            "quantity": "50-100",
            "noted": True,
            "rarity": 1 / (MSC / 6),
            "drop_requirements": None
        },
        "2361": {
            "id": 2361,
            "name": "Adamantite bar",
            "members": True,
            "quantity": "8-12",
            "noted": True,
            "rarity": 1 / (MSC / 6),
            "drop_requirements": None
        },
        "451": {
            "id": 451,
            "name": "Runite ore",
            "members": True,
            "quantity": "3-6",
            "noted": True,
            "rarity": 1 / (MSC / 6),
            "drop_requirements": None
        },
        "2363": {
            "id": 2363,
            "name": "Runite bar",
            "members": True,
            "quantity": "3-5",
            "noted": True,
            "rarity": 1 / (MSC / 6),
            "drop_requirements": None
        },
        "1747": {
            "id": 1747,
            "name": "Black dragonhide",
            "members": True,
            "quantity": "10-15",
            "noted": True,
            "rarity": 1 / (MSC / 6),
            "drop_requirements": None
        },
        "8782": {
            "id": 8782,
            "name": "Mahogany plank",
            "members": True,
            "quantity": "15-25",
            "noted": True,
            "rarity": 1 / (MSC / 5),
            "drop_requirements": None
        },
        "391": {
            "id": 391,
            "name": "Manta ray",
            "members": True,
            "quantity": "30-50",
            "noted": True,
            "rarity": 1 / (MSC / 3),
            "drop_requirements": None
        },
        "1515": {
            "id": 1515,
            "name": "Yew logs",
            "members": True,
            "quantity": "60-100",
            "noted": True,
            "rarity": 1 / (MSC / 3),
            "drop_requirements": None
        },
        "1513": {
            "id": 1513,
            "name": "Magic logs",
            "members": True,
            "quantity": "15-25",
            "noted": True,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "1631": {
            "id": 1631,
            "name": "Uncut dragonstone",
            "members": True,
            "quantity": "5-7",
            "noted": True,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "5316": {
            "id": 5316,
            "name": "Magic seed",
            "members": True,
            "quantity": "5-9",
            "noted": False,
            "rarity": 1 / (A * 40 / 4),
            "drop_requirements": None
        },
        "21802": {
            "id": 21802,
            "name": "Revenant cave teleport",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / (MSC / 7),
            "drop_requirements": None
        },
        "3024": {
            "id": 3024,
            "name": "Super restore(4)",
            "members": True,
            "quantity": "3-5",
            "noted": True,
            "rarity": 1 / (MSC / 4),
            "drop_requirements": None
        },
        "9193": {
            "id": 9193,
            "name": "Dragonstone bolt tips",
            "members": True,
            "quantity": "40-70",
            "noted": False,
            "rarity": 1 / (MSC / 4),
            "drop_requirements": None
        },
        "9194": {
            "id": 9194,
            "name": "Onyx bolt tips",
            "members": True,
            "quantity": "5-10",
            "noted": False,
            "rarity": 1 / (MSC / 4),
            "drop_requirements": None
        },
        "563": {
            "id": 563,
            "name": "Law rune",
            "members": True,
            "quantity": "80-120",
            "noted": False,
            "rarity": 1 / (MSC / 2),
            "drop_requirements": None
        },
        "560": {
            "id": 560,
            "name": "Death rune",
            "members": True,
            "quantity": "60-100",
            "noted": False,
            "rarity": 1 / (MSC / 3),
            "drop_requirements": None
        },
        "565": {
            "id": 565,
            "name": "Blood rune",
            "members": True,
            "quantity": "60-100",
            "noted": False,
            "rarity": 1 / (MSC / 3),
            "drop_requirements": None
        },
        "11941": {
            "id": 11941,
            "name": "Looting bag",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1 / 3,
            "drop_requirements": None
        }
    }

    return(items)
