"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
extract_summary_cache_data.py is a script to process the compressed OSRS cache
definition files maintained in this project and process, then extract basic
information about an item (item ID and item name). The extracted information
is then saved to the items-summary.json file that is stored in the publicly
available docs folder.

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
from typing import Union

import config
from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import osrs_cache_constants


def extract_summary_file(compressed_json_file_path: Union[Path, str], cache_name: str):
    """Main function to extract item/npc/object summary information (ID and name).

    :param compressed_json_file_path: Compressed cache file.
    :param cache_name: The name of the cache (items, npcs or objects).
    """
    summary_data = {}

    # Load and decompress the compressed definition file
    definitions = osrs_cache_data.CacheDefinitionFiles(compressed_json_file_path)
    definitions.decompress_cache_file()

    # Loop all entries in the decompressed and loaded definition file
    for id_number in definitions:
        json_data = definitions[id_number]
        id = json_data["id"]
        name = json_data["name"]
        # Check if there is a non-valid name
        if "<col" in json_data["name"]:
            continue
        if "null" in json_data["name"].lower():
            continue
        summary_data[id] = {
            "id": id,
            "name": name
        }

    # Save all extracted entries to a JSON file
    if cache_name == "npcs":
        out_fi = Path(config.DOCS_PATH / "npcs-summary.json")
    elif cache_name == "objects":
        out_fi = Path(config.DOCS_PATH / "objects-summary.json")

    with open(out_fi, "w") as f:
        json.dump(summary_data, f)


if __name__ == "__main__":
    # Loop the three cache types (items, npcs and objects), and extract summary JSON file
    for cache_type_name in osrs_cache_constants.CACHE_DUMP_TYPES:
        # If cache type is "items", skip as null/linked items are difficult to correlate
        # The items-summary.json is instead generated using the items_cache_data.py script
        if cache_type_name == "items":
            continue
        # Set path to compressed cache file, then extract file
        compressed_cache_file_name = cache_type_name + ".json"
        compressed_cache_file = Path(config.EXTRACTION_CACHE_PATH) / compressed_cache_file_name
        extract_summary_file(compressed_cache_file, cache_type_name)
