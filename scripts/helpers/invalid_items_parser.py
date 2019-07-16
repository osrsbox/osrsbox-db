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
from pathlib import Path

import config
from extraction_tools_wiki.wikitext_parser import WikitextTemplateParser
from osrsbox import items_api

# Delete old log file
if os.path.exists("template_parser.log"):
    os.remove("template_parser.log")

# Load the raw output from OSRS cache
scraper_path = Path(config.DATA_PATH / "items-cache-data.json")
with open(scraper_path) as f:
    cache_items = json.load(f)

# Load the wiki text file
wiki_text_file_path = Path(config.EXTRACTION_WIKI_PATH / "extract_page_text_items.json")
with open(wiki_text_file_path) as wiki_text_file:
    wiki_text = json.load(wiki_text_file)

# Load the invalid items file
invalid_items_file_path = Path(config.DATA_PATH / "invalid-items.json")
with open(invalid_items_file_path) as invalid_items_file:
    invalid_items = json.load(invalid_items_file)

# Output dictionaries
item_id_to_wikitext = dict()
item_id_to_version_number = dict()

# Loop all items in the OSRS Wiki data dump
for item_name, wikitext in wiki_text.items():
    if item_name.startswith("Category"):
        continue
    infobox_parser = WikitextTemplateParser(wikitext)
    has_infobox = infobox_parser.extract_infobox("infobox item")
    if has_infobox:
        is_versioned = infobox_parser.determine_infobox_versions()
        data = infobox_parser.extract_infobox_ids()
        for k, v in data.items():
            item_id_to_version_number[k] = v
    else:
        has_infobox = infobox_parser.extract_infobox("infobox pet")
        if has_infobox:
            is_versioned = infobox_parser.determine_infobox_versions()
            data = infobox_parser.extract_infobox_ids()
            for k, v in data.items():
                item_id_to_version_number[k] = v

# Structures for counting specific items
skipped_item = list()
missing_ids = list()
missing_names = list()

# Load current item database
all_db_items = items_api.load()
for item in all_db_items:
    # print("Processing:", item.id, item.name)
    if item.noted or item.placeholder:
        # print("  > SKIPPING NOTED/PLACEHOLDER ITEM:", item.id, item.name)
        skipped_item.append(item)
        continue
    if str(item.id) in invalid_items:
        # print("  > SKIPPING INVALID ITEM:", item.id, item.name)
        skipped_item.append(item)
        continue

    try:
        # Try perform ID lookup on OSRS Wiki data
        temp = item_id_to_version_number[item.id]
        # print("  > FOUND ITEM: Direct ID lookup:", item.id, item.name)
    except KeyError:
        try:
            # Try perform lookup on linked_id (instead of direct ID)
            temp = item_id_to_version_number[item.linked_id]
            # print("  > FOUND ITEM: Linked ID lookup:", item.id, item.name)
        except KeyError:
            missing_ids.append(item)
            try:
                # Try perform lookup using name instead of item ID
                temp = wiki_text[item.name]
                # print("  > FOUND ITEM: Name lookup:", item.id, item.name)
            except KeyError:
                # print("  > ITEM NOT FOUND:", item.id, item.name)
                missing_names.append(item)

print("\n>>> RESULTS:")
print("  > skipped_item ids:", len(skipped_item))
print("  > missing_ids:     ", len(missing_ids))
print("  > missing_names:   ", len(missing_names))
