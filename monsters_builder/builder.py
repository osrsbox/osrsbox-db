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
import json
import logging
import argparse
from pathlib import Path

import config
from monsters_builder import monster_builder
from osrsbox import items_api

os.remove(Path(__file__).stem+".log")
logging.basicConfig(filename=Path(__file__).stem+".log",
                    level=logging.DEBUG)
logging.info(">>> Starting builder.py to build monster database...")


def main(export_monster: bool = False):
    # Load the current database contents
    monsters_compltete_file_path = Path(config.DOCS_PATH / "monsters-complete.json")
    with open(monsters_compltete_file_path) as f:
        all_db_monsters = json.load(f)

    # Load the current item database contents
    all_db_items = items_api.load()

    # Load the item wikitext file
    wiki_text_file_path = Path(config.EXTRACTION_WIKI_PATH / "extract_page_text_monsters.json")
    with open(wiki_text_file_path) as f:
        all_wikitext_raw = json.load(f)

    # Temp loading of monster ID -> wikitext
    processed_wikitextfile_path = Path(config.EXTRACTION_WIKI_PATH / "processed_wikitext_monsters.json")
    with open(processed_wikitextfile_path) as f:
        all_wikitext_processed = json.load(f)

    # Load the raw OSRS cache monster data
    # This is the final data load, and used as baseline data for database population
    all_monster_cache_data_path = Path(config.DATA_PATH / "monsters-cache-data.json")
    with open(all_monster_cache_data_path) as f:
        all_monster_cache_data = json.load(f)

    # Initialize a list of known monsters
    known_monsters = list()

    # Start processing every monster!
    for monster_id in all_monster_cache_data:
        # Toggle to start, stop at a specific monster ID
        # if int(monster_id) < 231:
        #     continue

        # Initialize the BuildMonster class, used for all monster
        builder = monster_builder.BuildMonster(monster_id,
                                               all_monster_cache_data,
                                               all_wikitext_processed,
                                               all_wikitext_raw,
                                               all_db_monsters,
                                               all_db_items,
                                               known_monsters,
                                               export_monster)

        status = builder.preprocessing()
        if status:
            builder.populate_monster()
            known_monster = builder.check_duplicate_monster()
            known_monsters.append(known_monster)
            builder.parse_monster_drops()
            builder.generate_monster_object()
            builder.compare_new_vs_old_monster()
            builder.export_monster_to_json()
            builder.validate_monster()

    # Done processing, rejoice!
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build monster database.")
    parser.add_argument('--export_monster',
                        default=False,
                        required=False,
                        help='A boolean of whether to export data.')
    args = parser.parse_args()

    export_monster = args.export_monster
    main(export_monster)
