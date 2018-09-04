# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2017/11/28

Description:
OSRSItems is a class to hold a collection of ItemDefinition objects. 
Copyright (c) 2017, PH01L

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
import collections

sys.path.append(os.getcwd())
import ItemDefinition

###############################################################################
# Quest object
class OSRSItems(object):
    def __init__(self, input, output):
        """ Initializes the OSRSItems object. """
        self.input = input
        self.output = output
        self.files = None
        self.files_already_processed = list()
        self.item_count = 0
        
        # List of all OSRS items
        self._items_list = list()
        
        # Dict of all OSRS items
        self._items_dict = dict()
        
        # 
        self.noted_item_ids = dict()
        self.null_names = dict()

    def __iter__(self):
        """ Yields all attached ItemDefinition objects. """
        for i in self._items_list:
            yield i
            
    def process_dir(self):
        """ Process a directory of exported ItemDefinition JSON files. """
        
		# First, check a directory was given
        if not os.path.isdir(self.input):
            print(">>> ERROR: The parsed input is not a directory.")
            print(">>> Exiting.")
            quit()
		
        # Glob all JSON files, and print the total for the user
        self.files = glob.glob(self.input + os.sep + "*.json")    
        self.ordered_files = list()
        
        for fi in self.files:
            fi2 = fi.split(os.sep)[2]
            fi2 = fi2.replace(".json", "")
            fi2 = int(fi2)
            self.ordered_files.append(fi2)
        self.ordered_files.sort()
        
        print("  > Total number of items: %d" % len(self.files))
        
        # Check if there are actually files to process
        if len(self.files) == 0:
            print(">>> ERROR: The directory has no JSON files.")
            print(">>> Exiting.")
            quit()        
        
        # Second, check output directory is a directory
        if not os.path.isdir(self.output):
            print(">>> ERROR: The parsed input is not a directory.")
            print(">>> Exiting.")
            quit() 

        # Glob all JSON files, and print the total for the user
        temp = glob.glob(self.output + os.sep + "*.json")
        print(temp)
        # print("  > Total number of items: %d" % len(self.files)) 
      
        for fi in temp:
            item_id = os.path.basename(fi).replace(".json", "")
            item_id = int(item_id)
            self.files_already_processed.append(item_id)
        
        #print(self.files_already_processed)
        
        print(">>> Processing all files...")
        
        # Iterate each file, and process
        for fi in self.ordered_files:
            fi = "runelite_160_20171215" + os.sep + "items" + os.sep + str(fi) + ".json"
        
            item = ItemDefinition.ItemDefinition(fi)
            item.construct_from_runelite()
            
            if item.name.lower() == "null":
                # Skip any item without a name
                continue
                
            # Skip processing item if it already exists
            if item.id in self.files_already_processed:
                print("  > Skipping item, already exists.")
                continue
                
            # if "decorative" in item.name.lower():
                # continue
            # if "broken pickaxe" in item.name.lower():
                # continue
                
            
            item.scrape_wiki()
            item.check_json()
            # item.print_json()
            # item.edit_json()
            item.export_json()
            
            # Append to objects
            self._items_dict[item.id] = item
            self._items_list.append(item)
            
            # Increase count
            self.item_count += 1
            
            # Print status for user
            sys.stdout.write("  > Processed %d items\r" % self.item_count)
        print("  > Processed %d items" % self.item_count)

        # Check processed count, versus file count
        if self.item_count == len(self.files):
            print("  > Processed all files successfully...")
            
    def output_item_list(self):
        """ Output item ID and name to CSV file named 'itemids'. """
        with open("itemids.csv", "w") as f:
            for obj in self:
                f.write("%d,%s\n" % (obj.id, obj.name))
        f.close()
        
    # def create_better_json(self):
        # for item in self:
            # item.scrape_wiki()
            # item.check_json()
            # item.print_json()
            
            
      
################################################################################
if __name__=="__main__":
    pass
