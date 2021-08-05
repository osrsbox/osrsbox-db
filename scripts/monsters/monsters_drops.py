"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to fetch OSRS Wiki drops for Monsters.

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
import json
from pathlib import Path
from fractions import Fraction
from collections import defaultdict

import requests

import config
from osrsbox import items_api
from scripts.wiki.wikitext_parser import WikitextTemplateParser


# Data structure for any monster with multiple drop tables
# Format: id: query_string
multi_drop_tables = dict()

ITEMS = [item for item in items_api.load() if not item.duplicate and not item.stacked]


def fetch():
    """Fetch monster drops using SMW queries.

    This is a request heavy method - querying about 1,000 endpoints
    to get monster drop data.
    """
    # Load the monster wikitext file of processed data
    with open(Path(config.DATA_MONSTERS_PATH / "monsters-wiki-page-text-processed.json")) as f:
        all_wikitext_processed = json.load(f)

    # Load the raw cache data that has been processed (this is ground truth)
    with open(Path(config.DATA_MONSTERS_PATH / "monsters-cache-data.json")) as f:
        all_monster_cache_data = json.load(f)

    for monster_id, monster_list in all_wikitext_processed.items():
        exists = all_monster_cache_data.get(monster_id, None)
        if not exists:
            continue
        if "dropversion" in monster_list[2].lower():
            name = all_monster_cache_data[monster_id]["name"]
            wikitext = monster_list[2]
            version = monster_list[1]
            wikitext_template = WikitextTemplateParser(wikitext)
            wikitext_template.extract_infobox("infobox monster")
            value = wikitext_template.extract_infobox_value(f"dropversion{version}")
            if not value:
                value = wikitext_template.extract_infobox_value(f"dropversion1")
            multi_drop_tables[monster_id] = f"[[Dropped from::{name}#{value}]]"

    api_url = "https://oldschool.runescape.wiki/api.php"

    # Specify what the SMW query should return
    selection = "|?Dropped item|?Drop Quantity|?Rarity|?Rolls|limit=500"

    # Set parameters to run a SMW query
    params = {
        "action": "ask",
        "format": "json",
        "query": None
    }

    # Data structures for storing conditions
    # Conditions are used to form the SMW query
    conditions_set = set()
    conditions_dict = defaultdict(list)

    # Loop raw monster cache data (ground truth)
    for monster_id, monster in all_monster_cache_data.items():
        if monster_id in multi_drop_tables:
            condition = multi_drop_tables[monster_id]
        else:
            condition = f"[[Dropped from::{monster['name']}]]"

        # Add to set of conditions to later query
        conditions_set.add(condition)

        # Add condition string for monster ID lookup
        conditions_dict[condition].append(monster_id)

    print(f">>> Fetching {len(conditions_set)} drop tables...")

    # Start fetching the data
    count = 0
    for condition in conditions_set:
        print(f"  > Processing {count}/{len(conditions_set)}: {condition}")

        params["query"] = f"{condition}{selection}"

        r = requests.get(api_url,
                         headers=config.custom_agent,
                         params=params)

        data = r.json()

        Path(config.DATA_MONSTERS_PATH / "monsters-drops-raw").mkdir(parents=True, exist_ok=True)

        for monster_id in conditions_dict[condition]:
            file_name = f"{monster_id}.json"
            file_path = Path(config.DATA_MONSTERS_PATH / "monsters-drops-raw" / file_name)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

        count += 1


def gem_drop_table(base_rarity: float) -> list:
    """Set Gem Drop Table items.

    Item drops are hard coded.
    Drop rates sourced from:
    https://osrs.wiki/w/Drop_table#Useful_herb_drop_table

    :param base_rarity: The rarity for the drop table.
    :return: List of items on the drop table.
    """

    # Populate drop table items
    items = [
        {
            "id": 1623,
            "name": "Uncut sapphire",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/4 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1621,
            "name": "Uncut emerald",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/8 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1619,
            "name": "Uncut ruby",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/16 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1452,
            "name": "Chaos talisman",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/42.67 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1462,
            "name": "Nature talisman",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/42.67 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1617,
            "name": "Uncut diamond",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/64 * base_rarity,
            "rolls": 1
        },
        {
            "id": 830,
            "name": "Rune javelin",
            "members": True,
            "quantity": "5",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "rolls": 1
        },
        {
            "id": 987,
            "name": "Loop half of key",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "rolls": 1
        },
        {
            "id": 985,
            "name": "Tooth half of key",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1247,
            "name": "Rune spear",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * 1/16 * base_rarity,
            "rolls": 1
        },
        {
            "id": 2366,
            "name": "Shield left half",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * 1/32 * base_rarity,
            "rolls": 1
        },
        {
            "id": 1249,
            "name": "Dragon spear",
            "members": True,
            "quantity": "1",
            "noted": False,
            "rarity": 1/128 * 1/42.67 * base_rarity,
            "rolls": 1
        }
    ]

    return(items)


def quantity_cleaner(quantity: str) -> str:
    """Convert the drop quantity text entry.

    :param quantity: The extracted raw wiki text.
    :return: A cleaned drop quantity property value.
    """
    if quantity is None:
        return None

    if quantity.lower() == "unknown":
        return None

    quantity = quantity.replace(" ", "")
    quantity = quantity.replace(u"\u2013", "-")
    quantity = re.sub(r" *\(noted\) *", '', quantity)

    # Change semi-colon seperated list of numbers to commas
    quantity = re.sub(r"[; ]", ',', quantity)

    # Check the extracted and processed value against the supplied regex
    # Potenital format: "1-10", "1", "2,4,5"
    pattern = re.compile(r"^[0-9]*([-,][0-9]*)?")
    if quantity and not pattern.match(quantity):
        print(f">>> Drop quantity regex failed: {quantity}")
        exit(1)

    return quantity


def rarity_cleaner(rarity: str):
    if rarity.lower() == "always":
        return "1/1"
    elif rarity.lower() == "common":
        return "1/8"
    elif rarity.lower() == "uncommon":
        return "1/32"
    elif rarity.lower() == "rare":
        return "1/128"
    elif rarity.replace(" ", "").lower() == "veryrare":
        return "1/512"


def item_id_lookup(name: str) -> int:
    if name == "Black mask":
        name = "Black mask (10)"

    for item in ITEMS:
        if item.wiki_name == name:
            return item.id, item.members

    for item in ITEMS:
        if item.name == name:
            return item.id, item.members

    print(f"  > COULD NOT FIND: {name}")
    return None, None


def process_one(data: dict) -> dict:
    results = data["query"]["results"]
    drops = []

    if not results:
        return drops

    for query_str, printouts in results.items():

        try:
            name = printouts["printouts"]["Dropped item"][0]["fulltext"]

            if "#" in name:
                name = name.replace("#", "")
        except (KeyError):
            name = None

        # Skip if drop has no name
        if not name:
            continue

        # RARITY
        try:
            rarity = printouts["printouts"]["Rarity"][0]

            # Convert string rarity to a string fraction
            if rarity.lower() in ["always", "common", "uncommon", "rare", "veryrare"]:
                rarity = rarity_cleaner(rarity)

            # Remove thousand seperators from fractions
            rarity = rarity.replace(",", "")

            # Split fraction for calculation
            numerator, denominator = rarity.split('/')

            # Convert to a float - the safe way 0_o
            rarity = float(Fraction(numerator) / Fraction(denominator))
        except (IndexError, KeyError, ValueError):
            rarity = float(Fraction(1) / Fraction(512))

        if "gem drop table" in name.lower():
            items = gem_drop_table(rarity)
            drops.extend(items)
            continue

        if "rare drop table" in name.lower():
            continue

        itemid, members = item_id_lookup(name)

        # Skip if not item ID
        if not itemid:
            continue

        # QUANTITY
        try:
            quantity = printouts["printouts"]["Drop Quantity"][0]
            quantity = quantity_cleaner(quantity)
        except (IndexError, KeyError, ValueError):
            quantity = None

        # NOTED
        try:
            noted = "noted" in printouts["printouts"]["Drop Quantity"][0].lower()
        except (IndexError, KeyError, ValueError):
            noted = False

        # ROLLS
        try:
            rolls = printouts["printouts"]["Rolls"][0]
            rolls = int(rolls)
        except (IndexError, KeyError, ValueError):
            rolls = 1

        drop = {
            "id": itemid,
            "name": name,
            "members": members,
            "quantity": quantity,
            "noted": noted,
            "rarity": rarity,
            "rolls": rolls
        }
        drops.append(drop)

    return drops


def process():
    print(">>> Processing monster drops...")

    fis = Path(config.DATA_MONSTERS_PATH / "monsters-drops-raw").glob("*.json")

    all_monster_drops = dict()

    file_name = "monsters-drops.json"
    file_path = Path(config.DATA_MONSTERS_PATH / file_name)

    for fi in fis:
        with open(fi) as f:
            raw_data = json.load(f)

            processed_data = process_one(raw_data)
            monster_id = int(fi.stem)
            all_monster_drops[monster_id] = processed_data

    with open(file_path, "w") as f:
        json.dump(all_monster_drops, f)


if __name__ == "__main__":
    # fetch()
    process()
