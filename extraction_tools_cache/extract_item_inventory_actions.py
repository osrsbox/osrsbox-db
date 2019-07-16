"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
extract_item_inventory_actions.py is a Python script designed to parse the all of
the item definition cache dump and count the different types of interface
options - such as Drop, Wield, Equip etc. This makes it easy to analyse any
existing interface options and determine future changes. No output from this
script is saved.

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

import collections
from pathlib import Path
from typing import Union

import config
from extraction_tools_cache import osrs_cache_data


def extract_item_inventory_actions(compressed_json_file_path: Union[Path, str]):
    """Main function for extracting OSRS model ID numbers.

    :param compressed_json_file_path: File system location of compressed cache definition files.
    """
    inventory_actions = collections.defaultdict(int)

    # Load and decompress the compressed definition file
    definitions = osrs_cache_data.CacheDefinitionFiles(compressed_json_file_path)
    definitions.decompress_cache_file()

    # Loop all entries in the decompressed and loaded definition file
    for id_number in definitions:
        json_data = definitions[id_number]
        for option in json_data["interfaceOptions"]:
            inventory_actions[option] += 1

    inventory_actions = sorted(inventory_actions.items(), key=lambda x: int(x[1]), reverse=True)
    for action, count in inventory_actions:
        if not action:
            action = "None"
        print(f"{action:<24} {count}")


if __name__ == "__main__":
    # Set path to items.json compressed cache file
    path_to_definitions = Path(config.EXTRACTION_CACHE_PATH / "items.json")
    extract_item_inventory_actions(path_to_definitions)
