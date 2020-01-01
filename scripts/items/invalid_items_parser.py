"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Determine any invalid items and generate a list to help keep the
invalid-items.json file up to date. The output is supposed to be
grepped to find informaton about item ID and status.

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
import logging
from pathlib import Path

import config
from builders.items import build_item

# Configure logging
log_file_path = Path(Path(__file__).stem+".log")
if log_file_path.exists():
    log_file_path.unlink()
log_file_path.touch()
logging.basicConfig(filename=Path(__file__).stem+".log",
                    level=logging.DEBUG)
logging.info(">>> Starting scripts/items/invalid_items_parser.py...")


def main():
    # Load the current database contents
    items_compltete_file_path = Path(config.DOCS_PATH / "items-complete.json")
    with open(items_compltete_file_path) as f:
        all_db_items = json.load(f)

    # Load the item wikitext file
    wiki_text_file_path = Path(config.DATA_WIKI_PATH / "page-text-items.json")
    with open(wiki_text_file_path) as f:
        all_wikitext_raw = json.load(f)

    # Temp loading of item ID -> wikitext
    processed_wikitextfile_path = Path(config.DATA_WIKI_PATH / "processed-wikitext-items.json")
    with open(processed_wikitextfile_path) as f:
        all_wikitext_processed = json.load(f)

    # Load the invalid items file
    invalid_items_file_path = Path(config.DATA_ITEMS_PATH / "invalid-items.json")
    with open(invalid_items_file_path) as f:
        invalid_items_data = json.load(f)

    # Load buy limit data
    buy_limits_file_path = Path(config.DATA_ITEMS_PATH / "ge-limits-names.json")
    with open(buy_limits_file_path) as f:
        buy_limits_data = json.load(f)

    # Load skill requirement data
    skill_requirements_file_path = Path(config.DATA_ITEMS_PATH / "skill-requirements.json")
    with open(skill_requirements_file_path) as f:
        skill_requirements_data = json.load(f)

    # Load weapon_type data
    weapon_type_file_path = Path(config.DATA_ITEMS_PATH / "weapon-types.json")
    with open(weapon_type_file_path) as f:
        weapon_types_data = json.load(f)

    # Load stances data
    weapon_stance_file_path = Path(config.DATA_ITEMS_PATH / "weapon-stances.json")
    with open(weapon_stance_file_path) as f:
        weapon_stances_data = json.load(f)

    # Load the raw OSRS cache item data
    # This is the final data load, and used as baseline data for database population
    all_item_cache_data_path = Path(config.DATA_ITEMS_PATH / "items-cache-data.json")
    with open(all_item_cache_data_path) as f:
        all_item_cache_data = json.load(f)

    # Set export to false
    export = False

    # Initialize a list of known items
    known_items = list()

    # Start processing every item!
    for item_id in all_item_cache_data:
        # Toggle to start, stop at a specific item ID
        # if int(item_id) < 24000:
        #     continue

        # Initialize the BuildItem class, used for all items
        builder = build_item.BuildItem(item_id=item_id,
                                       all_item_cache_data=all_item_cache_data,
                                       all_wikitext_processed=all_wikitext_processed,
                                       all_wikitext_raw=all_wikitext_raw,
                                       all_db_items=all_db_items,
                                       buy_limits_data=buy_limits_data,
                                       skill_requirements_data=skill_requirements_data,
                                       weapon_types_data=weapon_types_data,
                                       weapon_stances_data=weapon_stances_data,
                                       invalid_items_data=invalid_items_data,
                                       known_items=known_items,
                                       export=export)

        preprocessing_status = builder.preprocessing()
        item_id_original = builder.item_id_str
        item_id_to_process = builder.item_id_to_process_str

        # preprocessing_status is a dictionary
        # {'status': True, 'code': 'valid'}
        # A valid item with an OSRS Wiki page (found using id, linked_id, name):
        # preprocessing_status["code"] == "valid"
        # An invalid item without an OSRS Wiki page will have a variety of errors
        # See the builders/items/build_item.py module for error codes

        if preprocessing_status["code"] == "valid":
            # Check for valid items in the invalid-items.json file
            if item_id_to_process in invalid_items_data:
                print(item_id_original, item_id_to_process, builder.item_name, invalid_items_data[item_id_to_process]["status"])
        else:
            print(item_id_original, item_id_to_process, builder.item_name, preprocessing_status["code"])

    # Done processing, rejoice!
    print("Done.")


if __name__ == "__main__":
    main()
