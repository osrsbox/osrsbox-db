"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Parse the project schema files and produce markdown tables.

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
from typing import Dict

import config


def parse_json_schema(properties_dict: Dict):
    # Print markdown table header
    print("| Property | Data type | Description | Required |")
    print("| -------- | --------- | ----------- | -------- |")
    for prop in properties_dict:
        data_type = properties_dict[prop]["type"]
        # Determine if property can be set to null
        if "null" in data_type:
            required = "No"
            data_type.remove("null")
        else:
            required = "Yes"
        if isinstance(data_type, list):
            data_type = ", ".join(data_type)
        description = properties_dict[prop]["description"]

        # Print row
        print(f"| {prop} | {data_type} | {description} | {required} |")


# Read in the schema-items.json file
path_to_schema = Path(config.DATA_SCHEMAS_PATH / "schema-items.json")
with open(path_to_schema, 'r') as f:
    schema = json.loads(f.read())

# Process the base item properties
properties_dict = schema["properties"]
parse_json_schema(properties_dict)

# Process the equipment properties
properties_dict = schema["properties"]["equipment"]["properties"]
parse_json_schema(properties_dict)

# Process the weapon properties
properties_dict = schema["properties"]["weapon"]["properties"]
parse_json_schema(properties_dict)

# Read in the schema-monsters.json file
path_to_schema = Path(config.DATA_SCHEMAS_PATH / "schema-monsters.json")
with open(path_to_schema, 'r') as f:
    schema = json.loads(f.read())

# Process the base monster properties
properties_dict = schema["properties"]
parse_json_schema(properties_dict)
