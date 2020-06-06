"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Determine any invalid items and generate a list to help keep the
invalid-items.json file up to date. The output is supposed to be
grepped to find informaton about item ID and status.

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

    # Dict of unalchable items
    unalchable_items_path = Path(config.DATA_WIKI_PATH / "page-titles-unalchable.json")
    with open(unalchable_items_path) as f:
        unalchable_items = json.load(f)

    # Load the invalid items file
    invalid_items_file_path = Path(config.DATA_ITEMS_PATH / "invalid-items.json")
    with open(invalid_items_file_path) as f:
        invalid_items_data = json.load(f)

    # Load buy limit data
    buy_limits_file_path = Path(config.DATA_ITEMS_PATH / "ge-limits-ids.json")
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

    # Load icon data
    icons_file_path = Path(config.DATA_ICONS_PATH / "icons-items-complete.json")
    with open(icons_file_path) as f:
        icons_data = json.load(f)

    # Load duplicate item data
    duplicates_file_path = Path(config.DATA_ITEMS_PATH / "duplicate-items.json")
    with open(duplicates_file_path) as f:
        duplicate_items = json.load(f)

    # Load schema data
    schema_file_path = Path(config.DATA_SCHEMAS_PATH / "schema-items.json")
    with open(schema_file_path) as f:
        schema_data = json.load(f)

    # Set export to false
    export = False
    # Set verbose to false
    verbose = False

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
                                       unalchable_items=unalchable_items,
                                       all_db_items=all_db_items,
                                       buy_limits_data=buy_limits_data,
                                       skill_requirements_data=skill_requirements_data,
                                       weapon_types_data=weapon_types_data,
                                       weapon_stances_data=weapon_stances_data,
                                       invalid_items_data=invalid_items_data,
                                       known_items=known_items,
                                       duplicate_items=duplicate_items,
                                       icons_data=icons_data,
                                       schema_data=schema_data,
                                       export=export,
                                       verbose=verbose)

        preprocessing_status = builder.preprocessing()
        item_id_original = builder.item_id_str
        item_id_to_process = builder.item_id_to_process_str

        # Preprocessing codes:
        # {'status': True, 'code': 'various_options_here_listed_below'}
        # lookup_passed_id: Found item in wiki using ID
        # lookup_passed_linked_id: Found item in wiki using linked ID
        # lookup_passed_name: Found item in wiki using name
        # Anything else is invalid...
        valid_item_codes = [
            "lookup_passed_id",
            "lookup_passed_linked_id",
            "lookup_passed_name"
        ]

        # Check for valid items in invalid-items.json file...
        if preprocessing_status["code"] in valid_item_codes:
            if item_id_to_process in invalid_items_data:
                print("ERROR: Item should not be invalid:")
                print(item_id_original, item_id_to_process, builder.item_name, invalid_items_data[item_id_to_process]["status"])

        # Preprocessing codes:
        # lookup_failed: No wiki entry
        # no_item_wikitext: No wikitext data
        # no_infobox_template: No wiki infobox data
        invalid_item_codes = [
            "lookup_failed",
            "no_item_wikitext",
            "no_infobox_template"
        ]

        # Check for items that failed lookup and are not in invalid-items.json file...
        if preprocessing_status["code"] in invalid_item_codes:
            try:
                invalid_items_data[item_id_to_process]
            except KeyError:
                print("ERROR: Item not marked as invalid:")
                print(item_id_original, item_id_to_process, builder.item_name)

    # Done processing, rejoice!
    print("Done.")


if __name__ == "__main__":
    main()
