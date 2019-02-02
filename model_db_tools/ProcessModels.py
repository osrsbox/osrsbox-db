# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/11/04

Description:
ProcessModels is a simple script to parse the objects output from the
RuneLite Cache tool. The script parses the individual JSON files, one
for each object, and extracts the object name, object id, and maps this
to the model id numbers. You can use this information to easily find the
name of a specific model id from the OSRS cache

Known keys for models:
- objectModels (objects)
- models (npcs)
- models_2 (npcs)
- inventoryModel (items)

Requirements:
No additional libraries required

Copyright (c) 2018, PH01L

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

>>> CHANGELOG:
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

import os
import glob
import json

SKIP_VALIDATION_FILES = ("NullObjectID.java", "ObjectID.java", "NpcID.java", "ItemID.java", "NullItemID.java",)
SKIP_EMPTY_NAMES = ("null", "Null", "")
TYPE_NAME_TO_JSON_KEY = {
    "objects": "objectModels",
    "npcs": "models",
    "items": "inventoryModel",
}


def extract_model_ids_from_def_file(fi, type_name):
    # Skip Java consolidation output from RuneLite
    if os.path.basename(fi) in SKIP_VALIDATION_FILES:
        return []

    # Load the JSON into a dict
    with open(fi) as f:
        json_data = json.loads(f.read())

    # Name check (it is of no use if its empty/null, so exclude)
    if json_data["name"] in SKIP_EMPTY_NAMES:
        return []

    # Setup output dict
    model_dict = {
        "type": type_name,
        "type_id": json_data["id"],
        "name": json_data["name"],
    }

    all_models = []
    json_data_key = TYPE_NAME_TO_JSON_KEY.get(type_name)

    if json_data_key is not None:
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


def main(path_to_definitions):
    cache_dump_names = ["items", "npcs", "objects"]
    # Create output dictionary to return
    models_dict = {}

    for cache_dump_name in cache_dump_names:
        print(f"  > Processing: {cache_dump_name}")
        # Set the path to the cache dump location
        cache_dump_path = os.path.join(path_to_definitions, cache_dump_name, "")

        # Get a list of all files in the cache directory
        cache_dump_fis = glob.glob(cache_dump_path + "*")

        for cache_file in cache_dump_fis:
            model_list = extract_model_ids_from_def_file(cache_file, cache_dump_name)
            for model in model_list:
                key = f"{model['type']}_{model['type_id']}_{model['model_id']}"
                models_dict[key] = model

    return models_dict


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d",
                    "--directory",
                    required=True,
                    help="Directory of definitions (in JSON) from RuneLite Cache tool")
    args = vars(ap.parse_args())
    path_to_definitions = args["directory"]

    models_dict = main(path_to_definitions)

    print(">>> Finished.")

    # Save all objects to JSON file
    print(">>> Saving output JSON file...")
    out_fi = "models_summary.json"
    with open(out_fi, "w") as f:
        json.dump(models_dict, f, indent=4)
