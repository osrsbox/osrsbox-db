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

SKIP_VALIDATION_FILES = ("NullObjectID.java", "ObjectID.java", "NpcID.java", "ItemID.java",)
SKIP_EMPTY_NAMES = ("null", "Null", "")
TYPE_NAME_TO_JSON_KEY = {
    "objects": "objectModels",
    "npcs": "models",
    "items": "inventoryModel",
}


def parse_fi(fi, type_name):
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
        "type_id": json_data["id"],
        "name": json_data["name"],
        "type": type_name
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
    items = os.path.join(path_to_definitions, "items", "")
    npcs = os.path.join(path_to_definitions, "npcs", "")
    objects = os.path.join(path_to_definitions, "objects", "")
    models_dict = {}

    # TODO(@PH01L): The following 3 for loops can be simplified since they share common code.
    # Process item models
    items_fis = glob.glob(items + "*")
    print(">>> Processing %d items..." % len(items_fis))
    for fi in items_fis:
        md_list = parse_fi(fi, "items")
        for md in md_list:
            key = md["type"] + "_" + str(md["type_id"]) + "_" + str(md["model_id"])
            models_dict[key] = md

    # Process npcs models
    npcs_fis = glob.glob(npcs + "*")
    print(">>> Processing %d npcs..." % len(npcs_fis))
    for fi in npcs_fis:
        md_list = parse_fi(fi, "npcs")
        for md in md_list:
            key = md["type"] + "_" + str(md["type_id"]) + "_" + str(md["model_id"])
            models_dict[key] = md

    # Process objects models
    objects_fis = glob.glob(objects + "*")
    print(">>> Processing %d objects..." % len(objects_fis))
    for fi in objects_fis:
        md_list = parse_fi(fi, "objects")
        for md in md_list:
            key = md["type"] + "_" + str(md["type_id"]) + "_" + str(md["model_id"])
            models_dict[key] = md

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
        json.dump(models_dict, f)
