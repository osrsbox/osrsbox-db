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

import os
import json
import glob
from pathlib import Path

import jsonschema


def test_item_database(path_to_docs_dir: Path):
    with open('test/item_schema.json', 'r') as f:
        schema_data = f.read()
    schema = json.loads(schema_data)

    path_to_items_json_dir = os.path.join(path_to_docs_dir, "items-json", "")
    fis = glob.glob(path_to_items_json_dir + "*.json")
    fis = sorted(fis)

    for json_file in fis:
        with open(json_file) as fi:
            item = json.load(fi)
            print(item["id"])
            print(json_file)
            jsonschema.validate(instance=item, schema=schema)
