"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Tests for module: osrsbox.monsters_api.all_monsters

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

from osrsbox.monsters_api import all_monsters

# The current number of monsters being loaded from the db
NUMBER_OF_MONSTERS = 2791


def test_all_monsters_load_monsters_json(path_to_docs_dir: Path):
    path_to_monsters_json_dir_no_slash = path_to_docs_dir / "monsters-json"
    path_to_monsters_json_dir_slash = os.path.join(path_to_docs_dir, "monsters-json", "")

    for path in (path_to_monsters_json_dir_slash, path_to_monsters_json_dir_no_slash):
        all_db_monsters = all_monsters.AllMonsters(str(path))
        assert len(all_db_monsters.all_monsters) == NUMBER_OF_MONSTERS


def test_all_monsters_load_monsters_complete(path_to_docs_dir: Path):
    path_to_monsters_complete = path_to_docs_dir / "monsters-complete.json"

    all_db_monsters = all_monsters.AllMonsters(str(path_to_monsters_complete))
    assert len(all_db_monsters.all_monsters) == NUMBER_OF_MONSTERS
