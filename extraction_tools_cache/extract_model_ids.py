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
import pathlib
from typing import List
from typing import Dict

from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import osrs_cache_constants

SKIP_EMPTY_NAMES = ("null", "Null", "")
TYPE_NAME_TO_JSON_KEY = {
    "objects": "objectModels",
    "npcs": "models",
    "items": "inventoryModel",
}


def extract_model_ids(json_data: Dict, type_name: str) -> List[Dict]:
    """Extracts the model ID number from an item, npc or object from definition data.

    :param json_data: A dictionary from an item, npc or object definition file.
    :param type_name: The type of item definition (items, npcs, or objects).
    :return all_models: A list of dictionaries containing ID, type, type ID and model ID.
    """
    # Name check (it is of no use if it is empty/null, so exclude)
    if json_data["name"] in SKIP_EMPTY_NAMES:
        return []

    # Setup output dict
    model_dict = {
        "type": type_name,
        "type_id": json_data["id"],
        "name": json_data["name"],
    }

    # Set up output list (populated with 1+ model_dict)
    all_models = []

    # Get the specific JSON key which varies between items, npcs and objects
    json_data_key = TYPE_NAME_TO_JSON_KEY.get(type_name)

    if json_data_key is None:
        return all_models

    try:
        # The items type is modeled a bit differently and doesn't return a list.
        # To make everything work under the same process, we wrap it in a list so we can iterate over it.
        fi_model_list = [json_data[json_data_key]] if type_name == "items" else json_data[json_data_key]
    except KeyError:
        fi_model_list = []

    for model_id in fi_model_list:
        model_dict["model_id"] = model_id
        all_models.append(model_dict)

    return all_models


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d",
                    "--directory",
                    required=True,
                    help="Directory of compressed cache definitions dump.")
    args = vars(ap.parse_args())
    path_to_definitions = args["directory"]

    models_dict = {}

    # Loop the three cache dump files (items, npcs, objects)
    for cache_file in osrs_cache_constants.CACHE_DUMP_FILES:
        # Set the path to the compressed JSON files
        compressed_json_file = pathlib.Path() / path_to_definitions / cache_file

        # Set the current cache dump type
        cache_type = pathlib.PurePath(cache_file)
        cache_type = str(cache_type.with_suffix(""))

        # Load and decompress the compressed definition file
        definitions = osrs_cache_data.CacheDefinitionFiles(compressed_json_file)
        definitions.decompress_cache_file()

        # Loop all entries in the decompressed and loaded definition file
        for id_number in definitions:
            # Extract model ID numbers
            model_list = extract_model_ids(definitions[id_number], cache_type)

            # Loop the extracted model IDs
            for model in model_list:
                # Generate a unique key (e.g., items_10_2361, an item with ID of 10 and model ID of 2361)
                key = f"{model['type']}_{model['type_id']}_{model['model_id']}"
                # Add to the dict for outputting
                models_dict[key] = model

    # Save all extracted models ID numbers to JSON file
    print(">>> Saving output JSON file...")
    out_fi = pathlib.Path() / ".." / "docs" / "models-summary.json"
    with open(out_fi, "w", newline="\n") as f:
        json.dump(models_dict, f, indent=4)
