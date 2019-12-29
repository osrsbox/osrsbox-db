"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Constant variables used in the OSRS cache tools in this repository.

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

import config

CACHE_DUMP_TYPES = [
    "items",
    "npcs",
    "objects"
]

ITEM_DEFINITIONS = dict()
NPC_DEFINITIONS = dict()
OBJECT_DEFINITIONS = dict()

all_cache_items = sorted(Path(config.DATA_CACHE_PATH / "items").glob("*.json"),
                         key=lambda path: int(path.stem))
if len(all_cache_items) == 0:
    print(">>> ERROR: scripts.cache.cache_constants")
    exit(">>> Could not load item cache files. Exiting.")
for cache_file in all_cache_items:
    with open(cache_file) as f:
        data = json.load(f)
        ITEM_DEFINITIONS[str(data["id"])] = data

all_cache_npcs = sorted(Path(config.DATA_CACHE_PATH / "npcs").glob("*.json"),
                        key=lambda path: int(path.stem))
if len(all_cache_npcs) == 0:
    print(">>> ERROR: scripts.cache.cache_constants")
    exit(">>> Could not load npc cache files. Exiting.")
for cache_file in all_cache_npcs:
    with open(cache_file) as f:
        data = json.load(f)
        NPC_DEFINITIONS[str(data["id"])] = data

all_cache_objects = sorted(Path(config.DATA_CACHE_PATH / "objects").glob("*.json"),
                           key=lambda path: int(path.stem))
if len(all_cache_objects) == 0:
    print(">>> ERROR: scripts.cache.cache_constants")
    exit(">>> Could not load object cache files. Exiting.")
for cache_file in all_cache_objects:
    with open(cache_file) as f:
        data = json.load(f)
        OBJECT_DEFINITIONS[str(data["id"])] = data
