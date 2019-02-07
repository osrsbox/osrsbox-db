# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/21

Description:
Simple script to determine item names that have been extracted from the cache,
but are not in the OSRS Wiki Category:Item. Output to be used to determine
item names that require normalization.

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

>>> CHANGELOG:
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import os
import json

# Get the dictionary of item ID -> wikitext
all_wiki_items = dict()
extraction_path_wiki = os.path.join("..", "extraction_tools_wiki", "")
with open(extraction_path_wiki + "extract_all_items_templates_InfoboxItems.json") as f:
    all_wiki_items = json.load(f)

# Read in normalized_names.txt
all_wiki_normalized_names = dict()
all_wiki_normalized_ids = dict()
extraction_path_other = os.path.join("..", "extraction_tools_other", "")
with open(extraction_path_other + "normalized_names.txt") as f:
    for line in f:
        line = line.strip()
        if "#" in line or line.startswith("TODO"):
            continue
        line = line.split("|")
        all_wiki_normalized_ids[line[0]] = [line[1], line[2], line[3]]
        all_wiki_normalized_names[line[1]] = [line[0], line[2], line[3]]

# Get the latest cache dump
items = dict()
in_fi = os.path.join("..", "docs", "items-itemscraper.json")
with open(in_fi) as f:
    temp = json.load(f)
    for k, v in temp.items():
        items[k] = v

# Find items that are not problematic (they are in wiki dump)
for k in items:
    item_name = items[k]["name"]
    item_id = k
    # Comment/Uncomment as necessary...

    # Check 1: If name is in wiki_items and normalized
    # This shouldn't happen, and should be removed from normalized list
    if item_name in all_wiki_items:
        if item_name in all_wiki_normalized_names:
            print(item_name)

    # # Check 2: If name is not in wiki_items...
    # # This is a name that should be normalized
    # if item_name not in all_wiki_items:
    #     print(item_name)
