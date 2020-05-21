"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to process the osrsbox.items_api database of all items and produce
a JSON file (items-search.json) of all items for the osrsbox website item
search tool. The output file contains id, name, type and duplicate status.

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
    # Output dictionary of all items in items-search
    items_search = dict()

    # Start processing all items in database
    all_db_items = items_api.load()

    for item in all_db_items:
        # Make a temporary dictionary for each item
        temp_dict = dict()

        # Add id, name, type and duplicate status
        temp_dict["id"] = item.id
        temp_dict["name"] = item.name
        temp_dict["type"] = None
        if item.noted:
            temp_dict["type"] = "noted"
        elif item.placeholder:
            temp_dict["type"] = "placeholder"
        else:
            temp_dict["type"] = "normal"
        temp_dict["duplicate"] = item.duplicate

        # Add temp_dict to all items
        items_search[item.id] = temp_dict

    # Write out file
    out_fi_path = Path(config.DOCS_PATH / "items-search.json")
    with open(out_fi_path, "w") as f:
        json.dump(items_search, f, indent=4)


if __name__ == "__main__":
    main()
