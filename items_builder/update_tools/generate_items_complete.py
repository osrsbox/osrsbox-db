"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Simple script to generate the items_complete.json file from the items-json
folder containing all the single JSON files in the osrsbox-db items
database.

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

from osrsbox.items_api import all_items

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i",
                    "--input",
                    required=True,
                    help="The folder of JSON item files (items-json)")
    args = vars(ap.parse_args())

    print(">>> Reading in items-json directory of JSON files...")
    ai = all_items.AllItems(args["input"])

    items = {}

    for item in ai:
        json_out = item.construct_json()
        items[item.id] = json_out

    # Save all items to items_complete.json
    print(">>> Saving items-complete.json file to current working directory...")
    out_fi = "items-complete.json"
    with open(out_fi, "w", newline="\n") as f:
        json.dump(items, f)
