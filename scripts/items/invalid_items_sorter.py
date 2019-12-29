"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Sort the data/items/invalid-items.json file.

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

# Load the invalid items file
invalid_items_file_path = Path(config.DATA_ITEMS_PATH / "invalid-items.json")
with open(invalid_items_file_path) as f:
    invalid_items_data = json.load(f)

# Load and sort (numerically) the invalid items ID numbers
item_ids = [x for x in invalid_items_data]
item_ids.sort(key=int)

sorted_ids = dict()
for item_id in item_ids:
    print(item_id)
    sorted_ids[item_id] = invalid_items_data[item_id]

with open(invalid_items_file_path, "w") as f:
    json.dump(sorted_ids, f, indent=4)
