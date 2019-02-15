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

import os
import json
import collections

from osrsbox.items_api import all_items

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i",
                    "--input",
                    required=True,
                    help="The single JSON file (items_complete.json)")
    args = vars(ap.parse_args())

    print(">>> Reading in items-json directory of JSON files...")
    ai = all_items.AllItems(args["input"])

    # Default dict (list) for all item slots
    items = collections.defaultdict(list)

    # Fetch every equipable item with an item slot value
    print(">>> Processing data by item slot...")
    for item in ai:
        if item.equipable:
            if item.item_equipment.slot is not None:
                items[item.item_equipment.slot].append(item)

    # Process each item found, and add to an individual file for each equipment slot
    print(">>> Saving items-slot files to current working directory...")
    for slot in items:
        json_out = {}
        for item in items[slot]:
            json_out_temp = item.construct_json()
            json_out[item.id] = json_out_temp
        out_fi = os.path.join("..", "..", "docs", "items-json-slot", "items-" + slot + ".json")
        with open(out_fi, "w", newline="\n") as f:
            json.dump(json_out, f)
