# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/18

Description:
Simple caller script to generate seperate JSON files for different
item slots. For example, the database is scanned and every item that
has the equipment slot of head is added to a file called items_head.json

Copyright (c) 2018, PH01L

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

>>> CHANGELOG:
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import os
import sys

# Import osrsbox-db API classes
sys.path.append(os.getcwd())
import AllItems
import ItemDefinition
import ItemBonuses

import collections
import json

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", 
                    "--input", 
                    required=True,
                    help="Two options: 1) Directory of JSON item files (../docs/items-json), or 2) Single JSON file (../docs/items_complete.json) ")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Reading in database contents...")
    ai = AllItems.AllItems(args["input"])

    # Create output directory for files
    print(">>> Create output directory...")
    directory = "items-json-slot"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Default dict (list) for all item slots
    items = collections.defaultdict(list)

    # Fetch every equipable item with an item slot value
    print(">>> Processing data by item slot...")
    for item in ai:
        if item.equipable:
            if item.equipment.slot is not None:
                items[item.equipment.slot].append(item)

    # Process each item found, and 
    for slot in items:
        json_out = dict()
        for item in items[slot]:
            json_item_out = item.construct_json()
            json_out[item.id] = json_item_out
        out_fi = os.path.join("items-json-slot", "items_" + slot + ".json")
        with open(out_fi, "w") as f:
            json.dump(json_out, f)
