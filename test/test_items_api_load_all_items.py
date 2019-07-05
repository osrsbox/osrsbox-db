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
from pathlib import Path

from osrsbox.items_api import all_items

NUMBER_OF_ITEMS = 21905  # The current number of items being loaded from the db


def test_all_items_load_items_json(path_to_docs_dir: Path):
    path_to_items_json_dir_no_slash = path_to_docs_dir / "items-json"
    path_to_items_json_dir_slash = os.path.join(path_to_docs_dir, "items-json", "")

    for path in (path_to_items_json_dir_slash, path_to_items_json_dir_no_slash):
        all_db_items = all_items.AllItems(str(path))
        assert len(all_db_items.all_items) == NUMBER_OF_ITEMS


def test_all_items_load_items_complete(path_to_docs_dir: Path):
    path_to_items_complete = path_to_docs_dir / "items-complete.json"

    all_db_items = all_items.AllItems(str(path_to_items_complete))
    assert len(all_db_items.all_items) == NUMBER_OF_ITEMS
