"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
extract_model_ids is a simple script to parse the output from the
RuneLite Cache tool. The script parses the individual JSON files, one
for each object, and extracts the object name, object id, and maps this
to the model id numbers. You can use this information to easily find the
name of a specific model id from the OSRS cache. Known keys for models:
- items: inventoryModel
- npcs: models, models_2 (version 2 does not seem to be used)
- objects: objectModels

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
import collections
from pathlib import Path
from typing import Union

import config


def extract_item_inventory_actions(path_to_cache_definitions: Union[Path, str]):
    """Main function for extracting OSRS model ID numbers.

    :param path_to_cache_definitions: File system location of compressed cache definition files.
    """
    inventory_actions = collections.defaultdict(int)

    print(path_to_cache_definitions)
    fis = path_to_cache_definitions.glob("*.json")
    for fi in fis:
        with open(fi) as f:
            temp = json.load(f)
            for option in temp["interfaceOptions"]:
                inventory_actions[option] += 1

    inventory_actions = sorted(inventory_actions.items(), key=lambda x: int(x[1]), reverse=True)
    for action, count in inventory_actions:
        if not action:
            action = "None"
        print(f"{action:<24} {count}")


if __name__ == "__main__":
    path_to_definitions = Path(config.EXTRACTION_CACHE_PATH / "items" / "")
    extract_item_inventory_actions(path_to_definitions)
