"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Parse the RuneLite Grand Exchange (GE) buy limits, and export to a new
JSON file that maps item name to buy limit. This is to provide more
search flexibility when looking up buy limits.

The ge_limits.json file can be downloaded from:
https://github.com/runelite/runelite/raw/master/runelite-client/src/main/
resources/net/runelite/client/plugins/grandexchange/ge_limits.json

Make sure to rename to ge-limits-ids.json to match this repository.

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
from osrsbox import items_api


def main():
    # Load all items from osrsbox item API
    all_db_items = items_api.load()

    # Get a dict with: id -> ItemProperties
    all_item_ids = dict()
    for item in all_db_items:
        all_item_ids[item.id] = item

    # Load the ge-limits-ids.json file from RuneLite
    ge_limits_path = Path(config.DATA_ITEMS_PATH / "ge-limits-ids.json")
    with open(ge_limits_path) as f:
        ge_limits = json.load(f)

    # Make a dict of: name -> buy_limit
    buy_limits = dict()
    for item_id, buy_limit in ge_limits.items():
        item_id = int(item_id)
        item_name = all_item_ids[item_id].name
        buy_limits[item_name] = buy_limit

    # Write out buy limit data file
    out_fi = Path(config.DATA_ITEMS_PATH / "ge-limits-names.json")
    with open(out_fi, "w") as f:
        json.dump(buy_limits, f, indent=4)


if __name__ == "__main__":
    main()
