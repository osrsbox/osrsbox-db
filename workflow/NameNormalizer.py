# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/08

Description:
Check the osrsbox-db contents (the actual single JSON files) to the
newly extracted allitem.json file to determine missing items.

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
import json
import glob

###############################################################################
# CompareAllitemsFiles object
class CompareAllitemsFiles(object):
    def __init__(self, allitems, allitems_db):
        self.allitems = allitems
        self.allitems_db = allitems_db
        self.allitems_dict = dict()
        self.allitems_db_dict = dict()
        self.normalized = dict()

    def process_allitems(self):
        print(">>> Processing allitems.json: %s" % self.allitems)
        with open(self.allitems) as f:
            self.allitems_dict = json.load(f)
        print("  > allitems.json count: %d" % len(self.allitems_dict))

        print(">>> Processing allitems_db.json: %s" % self.allitems_db)
        with open(self.allitems_db) as f:
            self.allitems_db_dict = json.load(f)
        print("  > allitems_db.json count: %d" % len(self.allitems_db_dict))
        self.dict_compare()
        self.print_dict()

    def dict_compare(self):
        d1_keys = set(self.allitems_dict.keys())
        d2_keys = set(self.allitems_db_dict.keys())
        self.added = d1_keys - d2_keys
        print("  > Number of new items: %d" % len(self.added))
        print(">>> The following items have been added...")
        self.added = list(self.added)
        self.added.sort(key=int)

        for id in self.added:
            self.print_dict(id)
        #     # print("%s,%s" % (self.allitems_dict[id]["id"], self.allitems_dict[id]["name"]))
        #     print("%s|" % (self.allitems_dict[id]["name"]))
        # TODO: Should probably add a check for removed items as well

        # for k,v in self.normalized.items():
        #     print("%s|%s" % (k,v))

    def print_dict(self, itemID):
        original_name = self.allitems_dict[itemID]["name"]
        wikia_name = None
        # fname = self.allitems_dict[itemID]["id"]
        fname = "items" + os.sep + str(self.allitems_dict[itemID]["id"]) + ".json"
        try:
            with open(fname) as f:
                theItem = json.load(f)
                wikia_name = theItem["url"]
                wikia_name = wikia_name.replace("", "")
                wikia_name = wikia_name.replace("http://2007.runescape.wikia.com/wiki/", "")
                wikia_name = wikia_name.replace("http://oldschoolrunescape.wikia.com/wiki/", "")
                wikia_name = wikia_name.replace("_", " ")
                wikia_name = wikia_name.replace("%27", "'")
                wikia_name = wikia_name.replace("%26", "&")
                wikia_name = wikia_name.replace("%2B", "+")
        except:
            pass
        print("%s|%s|%s" % (itemID, original_name, wikia_name))
        # if wikia_name is not None:
        #     self.normalized[original_name] = wikia_name
        # else:
        #     if wikia_name not in self.normalized:
        #         self.normalized[original_name] = wikia_name

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", 
                    "--file", 
                    required=True,
                    help="allitems.json")
    ap.add_argument("-d", 
                    "--db", 
                    required=True,
                    help="allitems_db.json")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Starting processing...")
    print("  > Comparing existing osrsbox-db contents to new allitems.json")
    
    c = CompareAllitemsFiles(args["file"],
                             args["db"])
    c.process_allitems()
