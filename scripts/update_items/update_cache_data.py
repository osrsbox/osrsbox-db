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
from extraction_tools_cache import extract_summary_cache_data
from extraction_tools_cache import extract_summary_model_ids
from extraction_tools_cache import extract_attackable_npcs
from extraction_tools_cache import extract_items_cache_data


if __name__ == '__main__':
    # STAGE ONE: Compress the raw item definitions files from the cache

    print(">>> CACHE COMPRESSION: Compressing OSRS Cache data for items, npcs and objects...")
    osrs_cache_data.main(config.EXTRACTION_CACHE_PATH, True)

    # STAGE TWO: Generate all the summary JSON files

    print(">>> SUMMARY FILES: Extracting summary files for items, npcs and objects...")
    # Loop the three cache types (items, npcs and objects), and extract summary JSON file
    for cache_type_name in osrs_cache_constants.CACHE_DUMP_TYPES:
        # Set path to compressed cache file, then extract file
        compressed_cache_file_name = cache_type_name + ".json"
        compressed_cache_file = Path(config.EXTRACTION_CACHE_PATH) / compressed_cache_file_name
        extract_summary_cache_data.extract_summary_file(compressed_cache_file, cache_type_name)

    # STAGE THREE: Generate additional cache-related JSON files

    print(">>> MODEL IDS: Extracting OSRS model ID numbers from cache definition files...")
    extract_summary_model_ids.main(config.EXTRACTION_CACHE_PATH)

    print(">>> ATTACKABLE NPCS: Extracting and merging OSRS attackable NPC definition files...")
    compressed_cache_file_npcs = Path(config.EXTRACTION_CACHE_PATH / "npcs.json")
    extract_attackable_npcs.extract_attackable_npcs(compressed_cache_file_npcs)

    print(">>> ITEMS CACHE DATA: Extracting detailed item metadata...")
    compressed_cache_file = Path(config.EXTRACTION_CACHE_PATH / "items.json")
    extract_items_cache_data.extract_items_cache_data(compressed_cache_file)

    # STAGE FOUR: Determine, then print any manual updates required (usually for tests)

    print(">>> Manual updates required:")
    # Check cache definition length for test.test_osrs_cache_data module
    for cache_type in osrs_cache_constants.CACHE_DUMP_TYPES:
        cache_data_path = Path(config.EXTRACTION_CACHE_PATH / cache_type)
        # Glob all files in cache type dir, convert generator to list, then determine file count
        cache_data_fis = list(Path(cache_data_path).glob("*.json"))
        cache_data_len = len(cache_data_fis)
        print(f"  > test.test_osrs_cache_data: {cache_type} - {cache_data_len}")
