"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to update OSRS Cache data dump.

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
from scripts.cache import cache_constants
from scripts.cache import generate_items_cache_data
from scripts.cache import generate_monsters_cache_data
from scripts.cache import generate_cache_summary_files
from scripts.cache import generate_summary_model_ids


if __name__ == '__main__':
    print(">>> Generating items cache data...")
    generate_items_cache_data.generate_items_cache_data(cache_constants.ITEM_DEFINITIONS)

    print(">>> Generating monsters cache data...")
    generate_monsters_cache_data.generate_monsters_cache_data(cache_constants.NPC_DEFINITIONS)

    print(">>> Generating summary cache files...")
    for cache_type_name in cache_constants.CACHE_DUMP_TYPES:
        generate_cache_summary_files.generate_cache_summary_file(cache_type_name)

    print(">>> Generating model IDs file...")
    generate_summary_model_ids.generate_summary_model_ids()

    print(">>> Manual updates required:")
    # Check cache definition length for test.test_cache_data module
    for cache_type in cache_constants.CACHE_DUMP_TYPES:
        cache_data_path = Path(config.DATA_CACHE_PATH / cache_type)
        # Glob all files in cache type dir, convert generator to list, then determine file count
        cache_data_fis = list(Path(cache_data_path).glob("*.json"))
        cache_data_len = len(cache_data_fis)
        print(f"  > test.test_cache_data: {cache_type} - {cache_data_len}")
