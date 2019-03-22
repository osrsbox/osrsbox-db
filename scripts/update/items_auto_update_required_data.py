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

from pathlib import Path

import config
from extraction_tools_cache import osrs_cache_constants
from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import extract_model_ids
from extraction_tools_cache import extract_attackable_npcs


if __name__ == '__main__':
    # STAGE ONE: Handle all OSRS cache data updates
    print(">>> CACHE COMPRESSION: Compressing OSRS Cache data for Items, NPCs and Objects...")
    osrs_cache_data.main(config.EXTRACTION_CACHE_PATH, True)

    print(">>> MODEL IDS: Extracting OSRS model ID numbers from cache definition files...")
    extract_model_ids.main(config.EXTRACTION_CACHE_PATH)

    print(">>> ATTACKABLE NPCS: Extracting and merging OSRS attackable NPC definition files...")
    cache_dump_path_npcs = Path(config.EXTRACTION_CACHE_PATH / "npcs.json")
    extract_attackable_npcs.main(cache_dump_path_npcs)

    # STAGE TWO: Determine, then print any manual updates required (usually for tests)
    print(">>> Manual updates required:")

    # Check cache definition length for test.test_osrs_cache_data module
    for cache_type in osrs_cache_constants.CACHE_DUMP_TYPES:
        cache_data_path = Path(config.EXTRACTION_CACHE_PATH / cache_type)
        # Glob all files in cache type dir, convert generator to list, then determine file count
        cache_data_fis = list(Path(config.EXTRACTION_CACHE_PATH).glob("*.json"))
        cache_data_len = len(cache_data_fis)
        print(f"  > test.test_osrs_cache_data: {cache_type} - {cache_data_len}")
