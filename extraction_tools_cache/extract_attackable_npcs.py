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
from pathlib import Path

import config
from extraction_tools_cache import osrs_cache_data


def main(compressed_json_file_path: str):
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
            # Save the attackable NPC
            attackable_npcs[id_number] = json_data

    # Save all extracted attackable NPCs to JSON file
    out_fi = Path(config.DATA_PATH / "attackable-npcs.json")
    with open(out_fi, "w") as f:
        json.dump(attackable_npcs, f)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-c",
                    "--cache",
                    required=True,
                    help="The compressed cache definitions file to process (npcs.json).")
    args = vars(ap.parse_args())
    path_to_compressed_json_file = args["cache"]

    main(path_to_compressed_json_file)
