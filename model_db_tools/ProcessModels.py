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
import sys
import glob
import json

################################################################################
def parse_fi(fi, type_name):
    # Skip Java consolidation output from RuneLite
    if (os.path.basename(fi) == "NullObjectID.java" or
        os.path.basename(fi) == "ObjectID.java" or
        os.path.basename(fi) == "NpcID.java" or
        os.path.basename(fi) == "ItemID.java"):
        return list()
    
    # Load the JSON into a dict
    with open(fi) as f:
        json_data = json.loads(f.read())

    # Name check (it is of no use if its empty/null, so exclude)
    if json_data["name"] == "null" or json_data["name"] == "Null" or json_data["name"] == "":
        return list()

    # Setup output dict
    model_dict = dict()
    model_dict["type_id"] = json_data["id"]
    model_dict["name"] = json_data["name"]
    model_dict["type"] = type_name
    
    fi_model_list = None
    all_models = list()
    
    if type_name == "objects":
        try:
            fi_model_list = json_data["objectModels"]
            for model_id in fi_model_list:
                model_dict["model_id"] = model_id
                all_models.append(model_dict)
        except KeyError:
            pass

    if type_name == "npcs":
        try:
            fi_model_list = json_data["models"]
            for model_id in fi_model_list:
                model_dict["model_id"] = model_id
                all_models.append(model_dict)
        except KeyError:
            pass

        # try:
        #     fi_model_list = json_data["models_2"]
        #     for model_id in fi_model_list:
        #         if model_id == 0:
        #             pass
        #         model_dict["model_id"] = model_id
        #         all_models.append(model_dict)
        # except KeyError:
        #     pass
    
    if type_name == "items":
        try:
            model_id = json_data["inventoryModel"]
            model_dict["model_id"] = model_id
            all_models.append(model_dict)
        except KeyError:
            pass

    return all_models

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", 
                    "--directory", 
                    required=True,
                    help="Directory of definitions (in JSON) from RuneLite Cache tool")
    args = vars(ap.parse_args())    

    directory = args["directory"]
    items = os.path.join(directory, "items", "")
    npcs = os.path.join(directory, "npcs", "")
    objects = os.path.join(directory, "objects", "")

    models_dict = dict()

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

    # # Loop dict and remove entries with name = null and model_id = 0
    # to_delete = list()
    # for k in models_dict:
    #     if models_dict[k]["name"] == "null" and models_dict[k]["model_id"] == 0:
    #        to_delete.append(k)
    # for k in to_delete:
    #     del models_dict[k]

    # Save all objects to JSON file
    print(">>> Saving output JSON file...")
    out_fi = "models_summary.json"
    with open(out_fi, "w") as f:
        json.dump(models_dict, f)

    print(">>> Finished.")
