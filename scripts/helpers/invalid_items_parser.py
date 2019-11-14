"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Copyright (c) 2019, PH01L

Description:
A helper script to determine any invalid (difficult to handle items) and
generate a list to help keep the invalid-items.json file up to date.

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
from pathlib import Path

import config
from items_builder import item_builder

os.remove(Path(__file__).stem+".log")
logging.basicConfig(filename=Path(__file__).stem+".log",
                    level=logging.DEBUG)
logging.info(">>> Starting invalid_items_parser.py...")


def main():
    # Load the item wikitext file
    wiki_text_file_path = Path(config.EXTRACTION_WIKI_PATH / "extract_page_text_items.json")
    with open(wiki_text_file_path) as f:
        all_wikitext_raw = json.load(f)

    # Temp loading of item ID -> wikitext
    processed_wikitextfile_path = Path(config.EXTRACTION_WIKI_PATH / "processed_wikitext_items.json")
    with open(processed_wikitextfile_path) as f:
        all_wikitext_processed = json.load(f)

    # Load the invalid items file
    invalid_items_file_path = Path(config.DATA_PATH / "invalid-items.json")
    with open(invalid_items_file_path) as f:
        invalid_items_data = json.load(f)

    # Load the raw OSRS cache item data
    # This is the final data load, and used as baseline data for database population
    all_item_cache_data_path = Path(config.DATA_PATH / "items-cache-data.json")
    with open(all_item_cache_data_path) as f:
        all_item_cache_data = json.load(f)

    # Initialize a list of known items
    known_items = list()

    # Start processing every item!
    for item_id in all_item_cache_data:
        # Toggle to start, stop at a specific item ID
        # if int(item_id) > 1000:
        #     continue

        # Initialize the BuildItem class, used for all items
        builder = item_builder.BuildItem(item_id,
                                         all_item_cache_data,
                                         all_wikitext_processed,
                                         all_wikitext_raw,
                                         None,
                                         None,
                                         None,
                                         None,
                                         None,
                                         invalid_items_data,
                                         known_items,
                                         None)

        preprocessing_status = builder.preprocessing()
        item_id_original = builder.item_id_str
        item_id_to_process = builder.item_id_to_process_str

        # preprocessing_status is a dictionary
        # {'status': True, 'code': 'valid'}
        # A valid item with an OSRS Wiki page (found using id, linked_id, name):
        # preprocessing_status["code"] == "valid"
        # An invalid item without an OSRS Wiki page
        # preprocessing_status["code"] == "valid"

        if preprocessing_status["code"] == "valid":
            # Check for valid items in the invalid-items.json file
            if item_id_to_process in invalid_items_data:
                print(item_id_original, item_id_to_process, builder.item_name, invalid_items_data[item_id_to_process]["status"])

    # Done processing, rejoice!
    print("Done.")


if __name__ == "__main__":
    main()
