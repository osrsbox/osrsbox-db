"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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
import glob

from extraction_tools_cache import osrs_cache_constants
from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import extract_model_ids
from extraction_tools_cache import extract_attackable_npcs
from extraction_tools_wiki import extract_wiki_data


if __name__ == '__main__':
    # STAGE ONE: Handle all OSRS cache data updates
    cache_dump_path = os.path.join("..", "extraction_tools_cache", "")

    print(">>> CACHE COMPRESSION: Compressing OSRS Cache data for Items, NPCs and Objects...")
    osrs_cache_data.main(cache_dump_path, True)

    print(">>> MODEL IDS: Extracting OSRS model ID numbers from cache definition files...")
    extract_model_ids.main(cache_dump_path)

    print(">>> ATTACKABLE NPCS: Extracting and merging OSRS attackable NPC definition files...")
    cache_dump_path_npcs = os.path.join("..", "extraction_tools_cache", "npcs", "")
    extract_attackable_npcs.main(cache_dump_path_npcs)

    # STAGE TWO: Handle all OSRS Wiki data dumps
    print(f">>> WIKI DATA ITEMS: Extracting page titles and wiki text...")
    categories = ["Items", "Construction", "Furniture", "Pets"]
    extract_wiki_data.main(categories)
    print(f">>> WIKI DATA MONSTERS: Extracting page titles and wiki text...")
    categories = ["Monsters"]
    extract_wiki_data.main(categories)
    print(f">>> WIKI DATA QUESTS: Extracting page titles and wiki text...")
    categories = ["Quests", "Miniquests", "Special_quests"]
    extract_wiki_data.main(categories)

    # STAGE THREE: Determine, then print any manual updates required (usually for tests)
    print(">>> Manual updates required:")

    # Check cache definition length for test.test_osrs_cache_data module
    for cache_type in osrs_cache_constants.CACHE_DUMP_TYPES:
        cache_data_path = os.path.join(cache_dump_path, cache_type, "")
        cache_data_len = len(glob.glob(cache_data_path + "*.json"))
        print(f"  > test.test_osrs_cache_data: {cache_type} - {cache_data_len}")
