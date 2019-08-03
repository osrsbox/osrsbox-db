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
from items_builder import item_builder

os.remove(Path(__file__).stem+".log")
logging.basicConfig(filename=Path(__file__).stem+".log",
                    level=logging.DEBUG)
logging.info(">>> Starting invalid_items_parser.py...")


def main(export_item: bool = False):
    # Load the current database contents
    items_compltete_file_path = Path(config.DOCS_PATH / "items-complete.json")
    with open(items_compltete_file_path) as f:
        all_db_items = json.load(f)

    # Load the item wikitext file
    wiki_text_file_path = Path(config.EXTRACTION_WIKI_PATH / "extract_page_text_items.json")
    with open(wiki_text_file_path) as f:
        all_wikitext_raw = json.load(f)

    # Load all wikitext, and map ID to version number and wikitext entry
    # template_names = ["infobox item", "infobox pet"]
    # wiki_text_data_ids = WikitextIDParser(wiki_text_file_path, template_names)
    # wiki_text_data_ids.process_osrswiki_data_dump()

    # Temp loading of item ID -> wikitext
    processed_wikitextfile_path = Path(config.EXTRACTION_WIKI_PATH / "processed_wikitext_items.json")
    with open(processed_wikitextfile_path) as f:
        all_wikitext_processed = json.load(f)

    # Load the invalid items file
    invalid_items_file_path = Path(config.DATA_PATH / "invalid-items.json")
    with open(invalid_items_file_path) as f:
        invalid_items_data = json.load(f)

    # Load buy limit data
    buy_limits_file_path = Path(config.DATA_PATH / "ge-limits-names.json")
    with open(buy_limits_file_path) as f:
        buy_limits_data = json.load(f)

    # Load skill requirement data
    skill_requirements_file_path = Path(config.DATA_PATH / "item-skill-requirements.json")
    with open(skill_requirements_file_path) as f:
        skill_requirements_data = json.load(f)

    # Load weapon_type data
    weapon_type_file_path = Path(config.DATA_PATH / "weapon-types.json")
    with open(weapon_type_file_path) as f:
        weapon_types_data = json.load(f)

    # Load stances data
    weapon_stance_file_path = Path(config.DATA_PATH / "weapon-stances.json")
    with open(weapon_stance_file_path) as f:
        weapon_stances_data = json.load(f)

    # Load the raw OSRS cache item data
    # This is the final data load, and used as baseline data for database population
    all_item_cache_data_path = Path(config.DATA_PATH / "items-cache-data.json")
    with open(all_item_cache_data_path) as f:
        all_item_cache_data = json.load(f)

    # Start processing every item!
    for item_id in all_item_cache_data:
        # Toggle to start, stop at a specific item ID
        # if int(item_id) < 23000:
        #     continue

        # Initialize the BuildItem class, used for all items
        builder = item_builder.BuildItem(item_id,
                                         all_item_cache_data,
                                         all_wikitext_processed,
                                         all_wikitext_raw,
                                         all_db_items,
                                         buy_limits_data,
                                         skill_requirements_data,
                                         weapon_types_data,
                                         weapon_stances_data,
                                         invalid_items_data,
                                         export_item)

        status = builder.preprocessing()
        if status:
            builder.populate_item()
            builder.generate_item_object()
            builder.compare_new_vs_old_item()
            builder.export_item_to_json()
            builder.validate_item()
        else:
            builder.populate_from_cache_data()
            builder.populate_non_wiki_item()
            builder.generate_item_object()
            builder.compare_new_vs_old_item()
            builder.export_item_to_json()
            builder.validate_item()

    # Done processing, rejoice!
    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build item database.")
    parser.add_argument('--export_item',
                        default=False,
                        required=False,
                        help='A boolean of whether to export data.')
    args = parser.parse_args()

    export_item = args.export_item
    main(export_item)
