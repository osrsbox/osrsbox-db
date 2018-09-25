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

pip install wikitextparser

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
import glob

sys.path.append(os.getcwd())
import ItemDefinition

###############################################################################
# ProcessItems object
class ProcessItems(object):
    def __init__(self, json_file, all_wikia_items, all_wikia_items_bonuses, all_wikia_quests, all_wikia_buylimits, all_wikia_normalized_names, all_wikia_items_construction):
        self.json_file = json_file
        self.all_wikia_items = all_wikia_items
        self.all_wikia_items_bonuses = all_wikia_items_bonuses
        self.all_wikia_quests = all_wikia_quests
        self.all_wikia_buylimits = all_wikia_buylimits
        self.all_wikia_normalized_names = all_wikia_normalized_names
        self.all_wikia_items_construction = all_wikia_items_construction
        self.allitems = dict()
        self.allitemdefs = dict()

        self.already_processed = list()

    def determine_already_processed(self):
        fis = glob.glob("items-json" + os.sep + "*")
        for fi in fis:
            fi = fi.replace(".json", "")
            fi = fi.replace("items-json", "")
            fi = fi.replace("\\", "")
            self.already_processed.append(fi)

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
        if itemID in self.already_processed:
            return
        itemdef = ItemDefinition.ItemDefinition(itemID, itemJSON, self.all_wikia_items, self.all_wikia_items_bonuses, self.all_wikia_quests, self.all_wikia_buylimits, self.all_wikia_normalized_names, self.all_wikia_items_construction) 
        item = itemdef.populate()
        if item:
            self.allitemdefs[itemID] = item 

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
    print(">>> Starting processing...")

    with open("extract_infoboxes_items.txt") as f:
        all_wikia_items = json.load(f)

    with open("extract_infoboxes_bonuses.txt") as f:
        all_wikia_items_bonuses = json.load(f)

    with open("extract_infoboxes_construction.txt") as f:
        all_wikia_items_construction = json.load(f)
   
    all_wikia_quests = list()
    with open("extract_all_quests.txt") as f:
        for l in f:
            l = l.strip()
            all_wikia_quests.append(l)

    all_wikia_buylimits = dict()
    with open("extract_buy_limits.txt") as f:
        for l in f:
            l = l.strip()
            l = l.split("|")
            all_wikia_buylimits[l[0]] = l[1]    

    all_wikia_normalized_names = dict()
    with open("normalized_names.txt") as f:
        for l in f:
            l = l.strip()
            if "TODO" in l:
                continue
            l = l.split("|")
            all_wikia_normalized_names[l[0]] = l[2]

    # Make a dir for JSON output
    directory = "items-json"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Next, process ItemScraper RuneLite plugin output file
    pi = ProcessItems(args["file"],
                      all_wikia_items,
                      all_wikia_items_bonuses,
                      all_wikia_quests,
                      all_wikia_buylimits,
                      all_wikia_normalized_names,
                      all_wikia_items_construction)
    pi.determine_already_processed()
    pi.process_allitems()
