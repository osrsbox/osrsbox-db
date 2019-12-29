"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Here

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


if __name__ == "__main__":
    # Start processing all items in database
    all_db_items = items_api.load()

    # Load current file
    isr_file = Path(config.DATA_PATH / "item-skill-requirements.json")
    with open(isr_file) as f:
        known_items = json.load(f)

    done = list()
    for i in known_items:
        done.append(i)

    for item in all_db_items:
        if str(item.id) in done:
            # Item ID is already done, skip to next
            continue

        if item.equipable_by_player:
            # If item is equipable and not processed... process it!
            # Try to find the name in the existing file
            found = False
            for known_item_id in known_items:
                item_object = all_db_items[int(known_item_id)]
                if item_object.name == item.name:
                    # If we find a name match, fetch the requirements and break
                    requirements = known_items[str(item_object.id)]
                    if not requirements:
                        requirements = "null"
                    found = True
                    break

            # Print out JSON formatted data
            if found:
                print(f'    "{item.id}": \n        {requirements}\n    ,')
            else:
                print(item.name)
                print(f'    "{item.id}": {{\n        "skill": level\n    }},')
