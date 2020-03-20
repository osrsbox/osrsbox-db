"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Load the processed cache data for items, check each item for a corresponding
icon in the docs/items-icons folder.

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

    # Load current icons-items-complete.json file
    icons_items_file_path = Path(config.DATA_ICONS_PATH / "icons-items-complete.json")
    with open(icons_items_file_path) as f:
        icon_items = json.load(f)

    for item_id, item_data in items_cache_data.items():
        # Check for item ID key in icon_items file
        try:
            icon_items[item_id]
        except KeyError:
            print(f"  > No icon for item ID: {item_id}, {item_data['name']}")


if __name__ == "__main__":
    main()
