# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/18

Description:
AllItems is a class to handle multiple osrsbox-db item-json files or a
single items_complete.json file.

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

from . import ItemDefinition


###############################################################################
# AllItems object
class AllItems(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.all_items = list()
        self.all_items_dict = dict()
        self.load_all_items()

    def __iter__(self):
        # Generator
        for itemID in self.all_items:
            yield itemID          
        # Generator (for dict)
        # for itemID, object in self.all_items.items():
        #     yield itemID, object        

    def get_itemids_objects(self):
        # Return keys
        return self.all_items_dict.items()

    def get_itemids(self):
        # Return keys
        return self.all_items_dict.keys()

    def get_objects(self):
        # Return values
        return self.all_items_dict.values()

    def load_all_items(self):
        # Counter
        count = 0

        # Handle input_data (either items-json dir, or items_complete.json)
        if os.path.isdir(self.input_data):
            fis = glob.glob(self.input_data + "*")
            # Loop through every item
            for json_file in fis:
                # Load JSON file to allitems dict
                sys.stdout.write(">>> Processing: %d\r" % count)
                with open(json_file) as f:
                    temp = json.load(f)
                    # Load the item using the ItemDefinition class
                    id = ItemDefinition.ItemDefinition()
                    item = id.load_item(temp)
                    # Add item to list and dict
                    self.all_items.append(item)
                    self.all_items_dict[item.id] = item
                    count += 1

        elif os.path.isfile(self.input_data):
            json_file = self.input_data
            with open(json_file) as f:
                temp = json.load(f)
                for entry in temp:
                    # Load the item using the ItemDefinition class
                    id = ItemDefinition.ItemDefinition()
                    item = id.load_item(temp[entry])
                    # Add item to list and dict
                    self.all_items.append(item)
                    self.all_items_dict[item.id] = item
                    count += 1                    
