"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Tests for module: docs/monsters-json

Copyright (c) 2020, PH01L

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


def test_monsters_data():
    """Unit test to check monsters database contents against JSON schema."""
    # Read in the monster schema file
    path_to_schema = Path(config.DATA_SCHEMAS_PATH / "schema-monsters.json")
    with open(path_to_schema, 'r') as f:
        schema = json.loads(f.read())

    # Validator object with schema attached
    v = config.MyValidator(schema)

    # Set the path to the monsters-json folder and get all the JSON files
    path_to_monsters_json_dir = Path(config.DOCS_PATH / "monsters-json")
    fis = path_to_monsters_json_dir.glob("*.json")
    fis = sorted(fis)

    # Validate each file
    for json_file in fis:
        with open(json_file) as fi:
            monster = json.load(fi)
            # print(monster["id"])
            assert v.validate(monster)
