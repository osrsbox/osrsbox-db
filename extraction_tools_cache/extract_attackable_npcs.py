"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
extract_attackable_npcs.py is a script to process the compressed OSRS cache
definition files maintained in this project and to extract the uncompressed NPC
definition JSON files. The extracted and decompressed data are the raw NPC
definition files for all attackable NPCs (monsters).

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


def extract_attackable_npcs(compressed_json_file_path: Union[Path, str]):
    """Main function to extract attackble NPC definition files

    :param compressed_json_file_path: Compressed cache file
    """
    attackable_npcs = {}

    # Load and decompress the compressed definition file
    definitions = osrs_cache_data.CacheDefinitionFiles(compressed_json_file_path)
    definitions.decompress_cache_file()

    # Loop all entries in the decompressed and loaded definition file
    for id_number in definitions:
        json_data = definitions[id_number]
        if "Attack" in json_data["options"]:
            # Skip entries with variable menu list color in name
            if "<col" in json_data["name"]:
                continue
            if json_data["name"] in ["Null", "null", ""]:
                continue
            # Save the attackable NPC
            attackable_npcs[id_number] = json_data

    # Save all extracted attackable NPCs to JSON file
    out_fi = Path(config.DATA_PATH / "attackable-npcs.json")
    with open(out_fi, "w") as f:
        json.dump(attackable_npcs, f)


if __name__ == "__main__":
    # Set path to npcs.json compressed cache file
    npcs_cache_file = Path(config.EXTRACTION_CACHE_PATH) / "npcs.json"
    extract_attackable_npcs(npcs_cache_file)
