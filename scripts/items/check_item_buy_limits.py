"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Load the processed cache data for items, check equipable items for an
entry in the data/items/skill-requirements.json file, and print a generic
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

    # Load current skill-requirements file
    ge_limits_file_path = Path(config.DATA_ITEMS_PATH / "ge-limits-ids.json")
    with open(ge_limits_file_path) as f:
        ge_limits = json.load(f)

    for item_id, item_data in items_cache_data.items():
        # Check if item is equipable, skip if not
        if not item_data["tradeable_on_ge"]:
            continue

        # If item is equipable, and in invalid_items, skip
        if item_id in invalid_items:
            continue

        # Check for item ID in skill requirements file
        try:
            ge_limits[item_id]
        except KeyError:
            # "24537": null,
            item_name = item_data["name"].replace(" ", "_")
            print(f'    "{item_id}": {item_name},')


if __name__ == "__main__":
    main()
