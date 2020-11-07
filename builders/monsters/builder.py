"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Program to invoke monster database generation process.

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
import logging
import argparse
from pathlib import Path

import config
from builders.monsters import build_monster

from osrsbox import items_api

# Configure logging
log_file_path = Path(Path(__file__).stem+".log")
if log_file_path.exists():
    log_file_path.unlink()
log_file_path.touch()
logging.basicConfig(filename=Path(__file__).stem+".log",
                    level=logging.DEBUG)
logging.info(">>> Starting builders/monsters/builder.py...")


def main(export: bool = False, verbose: bool = False, validate: bool = True):
    # Load the current database contents
    monsters_complete_file_path = Path(config.DOCS_PATH / "monsters-complete.json")
    with open(monsters_complete_file_path) as f:
        all_db_monsters = json.load(f)

    # Load the current item database contents
    all_db_items = items_api.load()

    # Load the item wikitext file
    wiki_text_file_path = Path(config.DATA_WIKI_PATH / "page-text-monsters.json")
    with open(wiki_text_file_path) as f:
        all_wikitext_raw = json.load(f)

    # Temp loading of monster ID -> wikitext
    processed_wikitextfile_path = Path(config.DATA_WIKI_PATH / "processed-wikitext-monsters.json")
    with open(processed_wikitextfile_path) as f:
        all_wikitext_processed = json.load(f)

    # Load the raw OSRS cache monster data
    # This is the final data load, and used as baseline data for database population
    all_monster_cache_data_path = Path(config.DATA_MONSTERS_PATH / "monsters-cache-data.json")
    with open(all_monster_cache_data_path) as f:
        all_monster_cache_data = json.load(f)

    # Load schema data
    schema_file_path = Path(config.DATA_SCHEMAS_PATH / "schema-monsters.json")
    with open(schema_file_path) as f:
        schema_data = json.load(f)

    # Initialize a list of known monsters
    known_monsters = list()

    # Start processing every monster!
    for monster_id in all_monster_cache_data:
        # Toggle to start, stop at a specific monster ID
        # if int(monster_id) < 3852:
        #     continue
        if int(monster_id) == 5079:
            # Temp skip Delrith, due to ? stat
            continue

        # Initialize the BuildMonster class, used for all monster
        builder = build_monster.BuildMonster(monster_id=monster_id,
                                             all_monster_cache_data=all_monster_cache_data,
                                             all_wikitext_processed=all_wikitext_processed,
                                             all_wikitext_raw=all_wikitext_raw,
                                             all_db_monsters=all_db_monsters,
                                             all_db_items=all_db_items,
                                             known_monsters=known_monsters,
                                             schema_data=schema_data,
                                             export=export,
                                             verbose=verbose)

        status = builder.preprocessing()
        if status:
            builder.populate_monster()
            known_monster = builder.check_duplicate_monster()
            known_monsters.append(known_monster)
            builder.parse_monster_drops()
            builder.generate_monster_object()
            builder.compare_new_vs_old_monster()
            builder.export_monster_to_json()
            if validate:
                builder.validate_monster()

    # Done processing, rejoice!
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build monster database.")
    parser.add_argument('--export',
                        default=False,
                        required=False,
                        help='A boolean of whether to export data.')
    parser.add_argument('--verbose',
                        default=False,
                        required=False,
                        help='A boolean of whether to be verbose.')
    parser.add_argument('--validate',
                        default=True,
                        required=False,
                        help='A boolean of whether to validate using schema.')
    args = parser.parse_args()

    export = args.export
    verbose = args.verbose
    validate = args.validate
    main(export, verbose, validate)
