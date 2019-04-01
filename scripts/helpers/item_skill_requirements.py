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
            # If item is equipable and not process, process it!
            print(item.name)
            print('    "%s": {\n        "skill": level\n    }' % item.id)
