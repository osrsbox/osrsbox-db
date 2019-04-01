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
from pathlib import Path

import config
from osrsbox import items_api


def main():
    """The main function for generating the `docs/items-complete.json` file"""
    # Read in the item database content
    path_to_items_json = Path(config.DOCS_PATH / "items-json")
    all_db_items = items_api.all_items.AllItems(path_to_items_json)

    items = {}

    for item in all_db_items:
        json_out = item.construct_json()
        items[item.id] = json_out

    # Save all items to docs/items_complete.json
    out_fi = Path(config.DOCS_PATH / "items-complete.json")
    with open(out_fi, "w") as f:
        json.dump(items, f)

    # Save all items to osrsbox/docs/items_complete.json
    out_fi = Path(config.PACKAGE_ROOT_PATH / "docs" / "items-complete.json")
    with open(out_fi, "w") as f:
        json.dump(items, f)


if __name__ == "__main__":
    print("Generating items-complete.json file...")
    main()
