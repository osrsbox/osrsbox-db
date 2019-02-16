"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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

from osrsbox.items_api import all_items


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i",
                    "--input",
                    required=True,
                    help="Either 1) Folder of JSON item (items-json), 2) Single JSON file (items-complete.json)")
    args = vars(ap.parse_args())

    # Load all items from osrsbox item API
    ai = all_items.AllItems(args["input"])

    # Get a dict with: id -> ItemDefinition
    all_item_ids = {}
    for item in ai:
        all_item_ids[item.id] = item

    # Load the ge-limits-ids.json file from RuneLite
    ge_limits_path = os.path.join("..", "data", "ge-limits-ids.json")
    with open(ge_limits_path) as f:
        ge_limits = json.load(f)

    # Make a dict of: name -> buy_limit
    buy_limits = dict()
    for item_id, buy_limit in ge_limits.items():
        item_id = int(item_id)
        item_name = all_item_ids[item_id].name
        buy_limits[item_name] = buy_limit

    # Write out buy limit data file
    out_fi = os.path.join("..", "data", "ge-limits-names.json")
    with open(out_fi, "w", newline="\n") as f:
        json.dump(buy_limits, f, indent=4)
