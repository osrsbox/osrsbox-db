"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to update JSON files.

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

import config
from osrsbox import items_api
from osrsbox import monsters_api
from osrsbox import prayers_api


def generate_items_complete():
    """Generate the `docs/items-complete.json` file."""
    # Read in the item database content
    path_to_items_json = Path(config.DOCS_PATH / "items-json")
    all_db_items = items_api.all_items.AllItems(path_to_items_json)

    items = {}

    for item in all_db_items:
        json_out = item.construct_json()
        items[item.id] = json_out

    # Save all items to docs/items_complete.json
    out_fi = Path(config.DOCS_PATH / "items-complete.json")
    with open(out_fi, "w") as f:
        json.dump(items, f)

    # Save all items to osrsbox/docs/items_complete.json
    out_fi = Path(config.PACKAGE_PATH / "docs" / "items-complete.json")
    with open(out_fi, "w") as f:
        json.dump(items, f)


def generate_item_slot_files():
    """Generate the `docs/items-slot/` JSON files."""
    # Read in the item database content
    all_db_items = items_api.load()

    items = collections.defaultdict(list)

    # Fetch every equipable item with an item slot value
    for item in all_db_items:
        if item.equipable_by_player:
            items[item.equipment.slot].append(item)

    # Process each item found, and add to an individual file for each equipment slot
    for slot in items:
        json_out = {}
        for item in items[slot]:
            json_out_temp = item.construct_json()
            json_out[item.id] = json_out_temp
        out_fi = Path(config.DOCS_PATH / "items-json-slot" / f"items-{slot}.json")
        with open(out_fi, "w") as f:
            json.dump(json_out, f)


def generate_monsters_complete():
    """Generate the `docs/monsters-complete.json` file."""
    # Read in the monster database content
    path_to_monsters_json = Path(config.DOCS_PATH / "monsters-json")
    all_db_monsters = monsters_api.all_monsters.AllMonsters(path_to_monsters_json)

    monsters = {}

    for monster in all_db_monsters:
        json_out = monster.construct_json()
        monsters[monster.id] = json_out

    # Save all monsters to docs/monsters-complete.json
    out_fi = Path(config.DOCS_PATH / "monsters-complete.json")
    with open(out_fi, "w") as f:
        json.dump(monsters, f)

    # Save all monsters to osrsbox/docs/monsters-complete.json
    out_fi = Path(config.PACKAGE_PATH / "docs" / "monsters-complete.json")
    with open(out_fi, "w") as f:
        json.dump(monsters, f)


def generate_prayers_complete():
    """Generate the `docs/prayers-complete.json` file."""
    # Read in the item database content
    path_to_prayers_json = Path(config.DOCS_PATH / "prayers-json")
    all_db_prayers = prayers_api.all_prayers.AllPrayers(path_to_prayers_json)

    prayers = {}

    for prayer in all_db_prayers:
        json_out = prayer.construct_json()
        prayers[prayer.id] = json_out

    # Save all prayers to docs/prayers-complete.json
    out_fi = Path(config.DOCS_PATH / "prayers-complete.json")
    with open(out_fi, "w") as f:
        json.dump(prayers, f)

    # Save all prayers to osrsbox/docs/prayers-complete.json
    out_fi = Path(config.PACKAGE_PATH / "docs" / "prayers-complete.json")
    with open(out_fi, "w") as f:
        json.dump(prayers, f)


def generate_items_search_file():
    """Generate the `docs/items-search.json` file."""
    # Read in the item database content
    path_to_items_json = Path(config.DOCS_PATH / "items-json")
    all_db_items = items_api.all_items.AllItems(path_to_items_json)

    items_search = {}

    for item in all_db_items:
        # Make a temporary dictionary for each item
        temp_dict = dict()

        # Add id, name, type and duplicate status
        temp_dict["id"] = item.id
        temp_dict["name"] = item.name
        temp_dict["type"] = None
        if item.noted:
            temp_dict["type"] = "noted"
        elif item.placeholder:
            temp_dict["type"] = "placeholder"
        else:
            temp_dict["type"] = "normal"
        temp_dict["duplicate"] = item.duplicate

        # Add temp_dict to all items
        items_search[item.id] = temp_dict

    # Save search file to docs/items_complete.json
    out_fi = Path(config.DOCS_PATH / "items-search.json")
    with open(out_fi, "w") as f:
        json.dump(items_search, f, indent=4)


def main():
    """The main function for generating the static JSON files."""
    print("Generating items-complete.json file...")
    generate_items_complete()
    print("Generating items-json-slot JSON files...")
    generate_item_slot_files()
    print("Generating monsters-complete.json file...")
    generate_monsters_complete()
    print("Generating prayers-complete.json file...")
    generate_prayers_complete()
    print("Generating items-search.json file...")
    generate_items_search_file()


if __name__ == '__main__':
    main()
