"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Simple script to generate the equipment slot-based JSON files from the
osrsbox-db items database. Ingests the items_complete.json file, so make
sure that file is updated first.

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


def main():
    """The main function for generating the `docs/items-slot/` JSON files."""
    # Read in the item database content
    all_db_items = items_api.load()

    items = collections.defaultdict(list)

    for item in all_db_items:
        json_out = item.construct_json()
        items[item.id] = json_out

    # Fetch every equipable item with an item slot value
    for item in all_db_items:
        if item.equipable:
            if item.item_equipment.slot is not None:
                items[item.item_equipment.slot].append(item)

    # Process each item found, and add to an individual file for each equipment slot
    for slot in items:
        json_out = {}
        for item in items[slot]:
            json_out_temp = item.construct_json()
            json_out[item.id] = json_out_temp
        out_fi = Path(config.DOCS_PATH / "items-json-slot" / f"items-{slot}.json")
        with open(out_fi, "w") as f:
            json.dump(json_out, f)


if __name__ == "__main__":
    print("Generating items-json-slot JSON files...")
    main()
