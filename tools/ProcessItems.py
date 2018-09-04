# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
ProcessItems is a class to amalgamate OSRS item information from a variety
of sources to produce rich item metadata files in JSON format. The ProcessItems
class sources information from the following locations:

1) Base item information from my ItemScraper RuneLite plugin. The ItemScraper
plugin returns a file named allitems.json which contains all the item 
information from the OSRS Cache
2) Any remaining information from the OSRS Wikia which is fetched using the 
MediaWiki API using my custom Python scripts and classes

Output: The output from this program is a folder called items-json which
contains a single file for every item in OSRS. Each file is named using the 
unique item ID. In addition, a single file is also exported which contains
every item in OSRS with rich metadata.

Requirements:
pip install requests
pip install mvparserfromhell
pip install dateparser

Copyright (c) 2018, PH01L

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
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

import os
import sys
import json
import datetime
import collections
import logging

sys.path.append(os.getcwd())
import ItemDefinition
import WikiaExtractor

###############################################################################
# ProcessItems object
class ProcessItems(object):
    def __init__(self, json_file, wikia_item_page_ids):
        self.json_file = json_file
        self.wikia_item_page_ids = wikia_item_page_ids
        self.allitems = dict()
        self.allitemdefs = dict()

    def process_allitems(self):
        print(">>> Processing file: %s" % self.json_file)
        # Load JSON file to allitems dict
        with open(self.json_file) as f:
            self.allitems = json.load(f)
        # Print length of allitems dict
        print("  > Total item count: %d" % len(self.allitems))
        # Individually process each item
        for k,v in self.allitems.items():
            self.construct_ItemDefinition(k, v)

    def construct_ItemDefinition(self, itemID, itemJSON):
        itemdef = ItemDefinition.ItemDefinition(itemID, itemJSON, self.wikia_item_page_ids) 
        item = itemdef.populate_from_allitems()
        self.allitemdefs[itemID] = item

    def extract_ItemDefinition(self):
        pass

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", 
                    "--file", 
                    required=True,
                    help="JSON file from ItemScraper RuneLite plugin")
    args = vars(ap.parse_args())
    
    # Start processing    
    print("Starting processing...")

    # Start by extracting all Category:Items pages from OSRS Wikia
    we = WikiaExtractor.WikiaExtractor()
    we.query_category_items()

    # Print item pages extracted from OSRS Wikia
    # for page_title, page_id in we.wikia_item_page_ids.items():
    #     print(page_title, page_id)

    # Next, process ItemScraper RuneLite plugin output file
    pi = ProcessItems(args["file"],
                      we.wikia_item_page_ids)
    pi.process_allitems()
