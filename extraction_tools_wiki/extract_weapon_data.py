"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A Python script to extract all data from the Weapon/Types page on the OSRS
Wiki. The output is a structured JSON file with:
- `weapon_type`: axe, bow etc.
- `combat style`: chop, block, accurate, longrange etc.
- `attack type`: slash, crush
- `attack style`: accurate, aggessive etc.
- `experience`: strength, defence, ranged etc.
- `boosts`: any boosts a specific stance provides

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

import json
import collections
from pathlib import Path
from typing import Dict

import config
from osrsbox import items_api
from extraction_tools_wiki.wiki_page_text import WikiPageText

import wikitextparser


OSRS_WIKI_API_URL = "https://oldschool.runescape.wiki/api.php"

CATEGORIES = {
    "axes": "melee",
    "blunt_weapons": "melee",
    "bulwarks": "melee",
    "claws": "melee",
    "halberds": "melee",
    "pickaxes": "melee",
    "scythes": "melee",
    "slashing_swords": "melee",
    "spears": "melee",
    "spiked_weapons": "melee",
    "stabbing_swords": "melee",
    "two-handed_swords": "melee",
    "whips": "melee",
    "bows": "ranged weapons",
    "chinchompas": "ranged_weapons",
    "crossbows": "ranged_weapons",
    "thrown_weapons": "ranged_weapons",
    "staves": "magical_weapons",
    "bladed_staves": "magical_weapons",
    "trident-class_weapons": "magical_weapons",
    "banners": "other",
    "blasters": "other",
    "guns": "other",
    "polestaves": "other",
    "salamanders": "other",
    "unarmed": "other"
}


def clean_wiki_text(wiki_text_str: str):
    """Clean a single wikitext table entry.

    :param wiki_text_str: The parsed wikitext table entry.
    """
    wiki_text_str = wiki_text_str.replace("[[", "")
    wiki_text_str = wiki_text_str.replace("]]", "")
    wiki_text_str = wiki_text_str.lower()
    return wiki_text_str


def parse_weapon_types_page(wiki_text: str):
    """Parses the OSRS Wiki page for Weapon/Type to extract weapon stance data.

    :param wikitext: The fetched OSRS Wiki page text.
    """
    categories_weapon_stances = dict()
    categories_weapon_names = collections.defaultdict(list)
    categories_keys = list(CATEGORIES.keys())

    # Use wikitextparser library to read in wikitext
    parsed = wikitextparser.parse(wiki_text)

    # STAGE ONE: Extract the table data for each weapon type

    # Loop each of the tables in the parsed wikitext
    for n, table in enumerate(parsed.tables):
        # Set an index for determining the column number used for each type of data
        table_index = {
            "combat_style": None,
            "attack_type": None,
            "attack_style": None,
            "experience": None,
            "boosts": None
        }

        # Create a hard-coded dictionary of lists for each row in the table
        table_output = {
            "combat_style": list(),
            "attack_type": list(),
            "attack_style": list(),
            "experience": list(),
            "boosts": list()
        }

        # Use the wikitextparser library to read in table row by row
        table_data = table.data(span=False)
        for row in table_data:
            # Loop each entry in each row
            for i, entry in enumerate(row):
                # Clean the wiki text
                entry = clean_wiki_text(entry)

                # Determine which column has what data
                # This is only used for the table headers
                if entry == "combat style":
                    table_index["combat_style"] = i - 1
                    continue
                elif entry == "attack type":
                    table_index["attack_type"] = i - 1
                    continue
                elif entry == "attack style":
                    table_index["attack_style"] = i - 1
                    continue
                elif entry == "experience":
                    table_index["experience"] = i - 1
                    continue
                elif entry == "boosts":
                    table_index["boosts"] = i - 1
                    continue

                # On subsequent runs, check the iterator against the table index
                # When iterator matches a table index, append data to the table_output
                if i == table_index["combat_style"]:
                    table_output["combat_style"].append(entry)
                elif i == table_index["attack_type"]:
                    table_output["attack_type"].append(entry)
                elif i == table_index["attack_style"]:
                    table_output["attack_style"].append(entry)
                elif i == table_index["experience"]:
                    table_output["experience"].append(entry)
                elif i == table_index["boosts"]:
                    table_output["boosts"].append(entry)

        # The entrie table has been dumper
        classification = categories_keys[n]
        categories_weapon_stances[classification] = table_output

    # STAGE TWO: Extract the items to map to each weapon type

    # Split the lines in the fetched OSRS Wiki page, then loop each line
    lines = wiki_text.split("\n")
    for line in lines:
        if line.startswith("==="):  # 3 x === is a sub-heading for each weapon type
            current_weapon_type = line.lower()
            current_weapon_type = current_weapon_type.replace("===", "")
            current_weapon_type = current_weapon_type.replace(" ", "_")

        # We know the current weapon type
        # Now extract lines starting with "*[[" - these are all items
        if line.startswith("*[["):
            # Tidy the entry
            line = line.replace("*[[", "")
            line = line.replace("]]", "")
            # Unique cases require splitting the string...
            # Split <ref>All attack styles are aggressive.</ref>
            # Split |Undead chicken
            line = line.split("<ref>")[0]
            line = line.split("|")[0]
            # Append the item to a dict using weapon_type
            categories_weapon_names[current_weapon_type].append(line)

    return categories_weapon_stances, categories_weapon_names


def fetch_index(weapon_type_list, key, index):
    """A simple function to extract an entry from a parsed wiki table.

    :param weapon_type_list: The list of weapon stance data
    :param key: The key, the column to extract
    :param index: The currently processed table index
    :return: The extracted table index entry
    """
    try:
        return weapon_type_list[key][index]
    except IndexError:
        return None


def process_weapon_stances(weapon_stances: Dict):
    weapon_stances_dict = dict()

    for weapon_type, entries in weapon_stances.items():
        combat_style_count = len(entries["combat_style"])

        stances = list()
        current_index = 0

        while current_index < combat_style_count:
            stance = {"combat_style": fetch_index(entries, "combat_style", current_index),
                      "attack_type": fetch_index(entries, "attack_type", current_index),
                      "attack_style": fetch_index(entries, "attack_style", current_index),
                      "experience": fetch_index(entries, "experience", current_index),
                      "boosts": fetch_index(entries, "boosts", current_index)}

            stances.append(stance)
            current_index += 1

        weapon_stances_dict[weapon_type] = stances

    weapon_stances_file = Path(config.DATA_PATH / "weapon-stances.json")
    with open(weapon_stances_file, mode='w') as f:
        json.dump(weapon_stances_dict, f, indent=4)


def process_weapon_types(weapon_types: Dict):
    """Extract weapon types, correlate to weapons in items_api

    :param weapon_types: A dictionary of weapon types.
    """
    # Load all normalized names
    normalized_names = dict()
    normalized_names_path = Path(config.ITEMS_BUILDER_PATH / "normalized_names.txt")
    with open(normalized_names_path) as f:
        for line in f:
            line = line.strip()
            if "#" in line or line.startswith("TODO"):
                continue
            line = line.split("|")
            normalized_names[line[0]] = [line[1], line[2], line[3]]

    extracted_weapon_types = dict()
    for weapon_type in weapon_types:
        for weapon_name in weapon_types[weapon_type]:
            extracted_weapon_types[weapon_name] = weapon_type

    weapon_type_dict = dict()

    # Load the osrsbox items API
    all_db_items = items_api.load()
    for item in all_db_items:
        if item.equipable_by_player:
            if item.equipment.slot in ["2h", "weapon"]:
                try:
                    item_name = normalized_names[str(item.id)][1]
                except KeyError:
                    item_name = item.name
                try:
                    weapon_type = extracted_weapon_types[item_name]
                    weapon_type_dict[item.id] = {"name": item.name, "weapon_type": weapon_type}
                except KeyError:
                    weapon_type_dict[item.id] = {"name": item.name, "weapon_type": None}

    weapon_types_file = Path(config.DATA_PATH / "weapon-types.json")
    with open(weapon_types_file, mode='w') as f:
        json.dump(weapon_type_dict, f, indent=4)


def main():
    # Page title to extract data from
    page_title = "Weapon/Types"

    # Specify the custom user agent for the request
    user_agent = "some-agent"
    user_email = "name@domain.com"

    # Create object to extract page wiki text
    wiki_page_text = WikiPageText(OSRS_WIKI_API_URL,
                                  page_title,
                                  user_agent,
                                  user_email)

    # Extract the actual wikitext
    wiki_page_text.extract_page_wiki_text()
    wiki_text = wiki_page_text.wiki_text

    # Extract the weapon types, stance information etc. from the page data
    weapon_stances, weapon_types = parse_weapon_types_page(wiki_text)

    process_weapon_stances(weapon_stances)
    process_weapon_types(weapon_types)


if __name__ == "__main__":
    # Run main() function
    main()
