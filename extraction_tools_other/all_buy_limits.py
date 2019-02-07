# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/29

Description:
Simple caller script to print item names

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

import json

from item_api_tools import AllItems

################################################################################
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i",
                    "--input",
                    required=True,
                    help="Two options: 1) Directory of JSON item files (../docs/items-json), or 2) Single JSON file (../docs/items-complete.json) ")
    args = vars(ap.parse_args())

    ge_limits = dict()
    # Load the ge_limits.json file
    with open('ge_limits.json') as f:
        ge_limits = json.load(f)

    # Start processing
    ai = AllItems.AllItems(args["input"])

    # Get a dict with: id -> ItemDefinition
    all_item_ids = dict()
    for item in ai:
        all_item_ids[item.id] = item

    # Make a list of: name|buy_limit
    buy_limits_list = list()
    for entry in ge_limits:
        known_item_id = int(entry)
        buy_limit = ge_limits[entry]
        line = "%s|%d" % (all_item_ids[known_item_id].name, buy_limit)
        buy_limits_list.append(line)

    # Write out buy limit list
    f = open("all_buy_limits.txt", "w")
    for line in buy_limits_list:
        f.write(line)
        f.write("\n")
    f.close()
