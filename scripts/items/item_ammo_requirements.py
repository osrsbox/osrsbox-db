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

# These bad IDs are prayer scrolls that are also equiped in the ammo slot
BAD_IDS = [20220, 20223, 20226, 20229, 20232, 20235, 22941, 22943, 22945, 22947]


if __name__ == "__main__":
    # Start processing all items in database
    all_db_items = items_api.load()

    # Load current file
    iar_file = Path(config.DATA_PATH / "item-ammo-requirements.json")
    with open(iar_file) as f:
        known_ammo = json.load(f)

    done = list()
    for i in known_ammo:
        done.append(i)

    for item in all_db_items:
        if item.id in BAD_IDS:
            # Item ID is not really ammo, skip to next
            continue
        if str(item.id) in done:
            # Item is already processed...

            if not known_ammo[str(item.id)]:
                # If item has been processed before, but has a null value, print it...
                print(f"Item with null value: {item.name}")
                generic_output = (
                    f'    "{item.id}": {{\n'
                    f'        "ammo_type": unknown,\n'
                    f'        "ammo_tier": unknown\n'
                    f'    }}\n'
                )
                print(generic_output)

            # Item ID is already done, skip to next
            continue

        if item.equipable_by_player and item.equipment.slot == "ammo":
            # If item is equipable, an ammo slot item, and not processed... process it!
            print(f"Item that has not been processed: {item.name}")
            generic_output = (
                f'    "{item.id}": {{\n'
                f'        "ammo_type": unknown,\n'
                f'        "ammo_tier": unknown\n'
                f'    }}\n'
            )
            print(generic_output)
