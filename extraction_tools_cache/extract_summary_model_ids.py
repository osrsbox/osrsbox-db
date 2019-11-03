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
from pathlib import PurePath
from typing import List
from typing import Dict

import config
from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import osrs_cache_constants

SKIP_EMPTY_NAMES = ("null", "Null", "")


def extract_model_ids_int(json_data: Dict) -> List[Dict]:
    """Extracts the model ID numbers for NPCs and NPC Chat heads.

    :param json_data: A dictionary from an item, npc or object definition file.
    :return models: A list of dictionaries containing ID, type, type ID and model ID.
    """
    # Set up output dict (to be populated with 1 or more model_dict)
    models = {}

    model_keys = {
        "item_model_ground": "inventoryModel",
        "item_model_male0": "maleModel0",
        "item_model_male1": "maleModel1",
        "item_model_male2": "maleModel2",
        "item_model_female0": "femaleModel0",
        "item_model_female1": "femaleModel1",
        "item_model_female2": "femaleModel2"
    }

    for model_type, model_key in model_keys.items():
        model_dict = dict()
        # Set base properties
        model_dict["model_type"] = model_type
        model_dict["model_type_id"] = json_data["id"]
        model_dict["model_name"] = json_data["name"]

        # Extract NPC model numbers
        try:
            model_dict["model_ids"] = json_data[model_key]
        except KeyError:
            continue

        if model_dict["model_ids"] == -1:
            continue

        model_dict_key = f"{model_dict['model_type']}_{model_dict['model_type_id']}_{model_dict['model_ids']}"

        models[model_dict_key] = model_dict

    # Return a list of model_dicts
    return models


def extract_model_ids_list(json_data: Dict) -> List[Dict]:
    """Extracts the model ID numbers for ground, male and female item models.

    :param json_data: A dictionary from an item, npc or object definition file.
    :return models: A list of dictionaries containing ID, type, type ID and model ID.
    """
    # Set up output dict (to be populated with 1 or more model_dict)
    models = {}

    model_keys = {
        "npc_model": "models",
        "npc_chathead": "chatheadModels",
        "object_model": "objectModels"
    }

    for model_type, model_key in model_keys.items():
        model_dict = dict()
        # Set base properties
        model_dict["model_type"] = model_type
        model_dict["model_type_id"] = json_data["id"]
        model_dict["model_name"] = json_data["name"]

        # Extract NPC model numbers
        try:
            model_dict["model_ids"] = ", ".join(str(n) for n in json_data[model_key])
        except KeyError:
            continue

        model_dict_key = f"{model_dict['model_type']}_{model_dict['model_type_id']}_{model_dict['model_ids']}"

        models[model_dict_key] = model_dict

    # Return a list of model_dicts
    return models


def main(path_to_cache_definitions: Path):
    """Main function for extracting OSRS model ID numbers that map to names.

    :param path_to_cache_definitions: File location of compressed cache definition files.
    """
    all_models = {}

    # Loop the three cache dump files (items, npcs, objects)
    for cache_file in osrs_cache_constants.CACHE_DUMP_FILES:
        # Set the path to the compressed JSON files
        compressed_json_file = Path(path_to_cache_definitions / cache_file)

        # Set the current cache dump type
        cache_type = PurePath(cache_file)
        cache_type = str(cache_type.with_suffix(""))

        # Load and decompress the compressed definition file
        definitions = osrs_cache_data.CacheDefinitionFiles(compressed_json_file)
        definitions.decompress_cache_file()

        # Loop all entries in the decompressed and loaded definition file
        for id_number in definitions:
            # Fetch the decompressed JSON data
            json_data = definitions[id_number]

            # Name check (it is of no use if it is empty/null, so exclude)
            if json_data["name"] in SKIP_EMPTY_NAMES:
                continue

            # Process cache definition based on type (item, npc, object)
            # Items: Have single interger model IDs
            # NPCs: Have list of interger model IDs
            # Objects: Have list of integer model IDs
            if cache_type == "items":
                extracted_models = extract_model_ids_int(json_data)
            elif cache_type == "npcs":
                extracted_models = extract_model_ids_list(json_data)
            elif cache_type == "objects":
                extracted_models = extract_model_ids_list(json_data)

            # Add extracted models to all_models dictionary
            all_models.update(extracted_models)

    # Save all extracted models ID numbers to JSON file
    out_fi = Path(config.DOCS_PATH / "models-summary.json")
    with open(out_fi, "w") as f:
        json.dump(all_models, f, indent=4)


if __name__ == "__main__":
    main(config.EXTRACTION_CACHE_PATH)
