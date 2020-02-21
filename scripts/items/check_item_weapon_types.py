"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Load the processed cache data for items, check equipable items for an
entry in the data/items/weapon-types.json file, and print a generic
entry for manual insertion.

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
import json
from pathlib import Path

import config


def main():
    # Load current items-cache-data.json file
    items_cache_data_file = Path(config.DATA_ITEMS_PATH / "items-cache-data.json")
    with open(items_cache_data_file) as f:
        items_cache_data = json.load(f)

    # Load current invalid-items.json file
    invalid_items_file_path = Path(config.DATA_ITEMS_PATH / "invalid-items.json")
    with open(invalid_items_file_path) as f:
        invalid_items = json.load(f)

    # Load current weapon-types.json file
    weapon_type_file_path = Path(config.DATA_ITEMS_PATH / "weapon-types.json")
    with open(weapon_type_file_path) as f:
        weapon_types = json.load(f)

    # Load current OSRS Wiki item dump
    processed_wikitextfile_path = Path(config.DATA_WIKI_PATH / "processed-wikitext-items.json")
    with open(processed_wikitextfile_path) as f:
        all_wikitext_processed = json.load(f)

    for item_id, item_data in items_cache_data.items():
        # Check if item is equipable, skip if not
        if not item_data["equipable"]:
            continue

        # If item is equipable, and in invalid_items, skip
        if item_id in invalid_items:
            continue

        # Check for OSRS Wiki page, skip if non-existant
        try:
            all_wikitext_processed[item_id]
        except KeyError:
            continue

        # Check for "2h" or "weapon" in wikitext
        try:
            weapon_types[item_id]
        except KeyError:
            if "2h" in all_wikitext_processed[item_id] or "weapon" in all_wikitext_processed[item_id]:
                print(f"  > No entry in weapon_types: {item_id}, {item_data['name']}")


if __name__ == "__main__":
    main()
