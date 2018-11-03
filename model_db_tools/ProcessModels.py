# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/11/03

Description:
ProcessModels is a simple script to parse the objects output from the 
RuneLite Cache tool. The script parses the individual JSON files, one
for each object, and extracts the object name, object id, and maps this
to the model id numbers. You can use this information to easily find the
name of a specific model id from the OSRS cache 

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
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", 
                    "--directory", 
                    required=True,
                    help="Directory of definitions (in JSON) from RuneLite Cache tool")
    args = vars(ap.parse_args())    

    directory = args["directory"]

    # Start processing    
    print(">>> Starting processing...")

    fis = glob.glob(directory + os.sep + "*" + os.sep + "*")

    print("  > Found %d objects..." % len(fis))

    all_models = dict()
    count = 0

    for fi in fis:
        # Skip Java consolidation output from RuneLite
        if (os.path.basename(fi) == "NullObjectID.java" or
           os.path.basename(fi) == "ObjectID.java" or
           os.path.basename(fi) == "NpcID.java" or
           os.path.basename(fi) == "ItemID.java"):
           continue
        
        sys.stdout.write(">>> Processing: %d of %d\r" % (count, len(fis)))

        # Load the JSON into a dict
        with open(fi) as f:
            json_data = json.loads(f.read())

        # Setup output dict
        model_dict = dict()
        model_dict["id"] = json_data["id"]
        model_dict["name"] = json_data["name"]
        model_type = fi.split(os.sep)
        model_dict["type"] = model_type[len(model_type)-2]
        model_list = None
        
        # Known keys for models:
        # objectModels
        # models
        # models_2
        # inventoryModel

        try:
            model_list = json_data["objectModels"]
            for model in model_list:
                all_models[model] = model_dict
        except KeyError:
            pass

        try:
            model_list = json_data["models"]
            for model in model_list:
                all_models[model] = model_dict
        except KeyError:
            pass   

        try:
            model_list = json_data["models_2"]
            for model in model_list:
                all_models[model] = model_dict
        except KeyError:
            pass   
            
        try:
            model = json_data["inventoryModel"]
            all_models[model] = model_dict
        except KeyError:
            pass                                 

        # Increase count
        count += 1

    print(">>> Finished...")
    
    # Save all objects to JSON file
    out_fi = "models_summary.json"
    with open(out_fi, "w") as f:
        json.dump(all_models, f)