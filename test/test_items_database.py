"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Tests for module: osrsbox.items_api.all_items

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

import jsonschema


def test_item_database(path_to_docs_dir: Path):
    """Unit test to check item database contents against JSON schema

    :param path_to_docs_dir: The path to the `docs` folder.
    """
    # Read in the item_schema.json file
    path_to_schema = Path("test/item_schema.json")
    with open(path_to_schema, 'r') as f:
        schema = json.loads(f.read())

    # Set the path to the items-json folder and get all the JSON files
    path_to_items_json_dir = Path(f"{path_to_docs_dir}/items-json")
    fis = path_to_items_json_dir.glob("*.json")
    fis = sorted(fis)

    # Validate each file
    for json_file in fis:
        with open(json_file) as fi:
            item = json.load(fi)
            # print(item["id"])
            jsonschema.validate(instance=item, schema=schema)
