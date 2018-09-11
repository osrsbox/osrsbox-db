# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/08

Description:
Compare newly extracted allitems.json, to existing allitems.json in
the osrsbox-db.

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

import json

###############################################################################
# DetermineNewItems object
class DetermineNewItems(object):
    def __init__(self, new_json, old_json):
        self.old_json = old_json
        self.new_json = new_json
        self.allitems_old = dict()
        self.allitems_new = dict()

    def process_allitems(self):
        print(">>> Processing old_json: %s" % self.old_json)
        with open(self.old_json) as f:
            self.allitems_old = json.load(f)
        # Print length of allitems dict
        print("  > Old item count: %d" % len(self.allitems_old))

        print(">>> Processing new_json: %s" % self.new_json)
        with open(self.new_json) as f:
            self.allitems_new = json.load(f)
        # Print length of allitems dict
        print("  > New item count: %d" % len(self.allitems_new))
        self.dict_compare()


    def dict_compare(self):
        d1_keys = set(self.allitems_old.keys())
        d2_keys = set(self.allitems_new.keys())
        added = d2_keys - d1_keys
        print("  > Number of new items: %d" % len(added))
        print(">>> The following items have been added...")
        for id in added:
            print("%s,%s" % (self.allitems_new[id]["id"], self.allitems_new[id]["name"]))
        # TODO: Should probably add a check for removed items as well

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", 
                    "--newfile", 
                    required=True,
                    help="NEW JSON file from ItemScraper RuneLite plugin")
    ap.add_argument("-o", 
                    "--oldfile", 
                    required=True,
                    help="Old JSON file from ItemScraper RuneLite plugin")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Starting processing...")
    print("  > Comparing old allitems.json to new allitems.json")
    
    c = DetermineNewItems(args["newfile"],
                          args["oldfile"])
    c.process_allitems()
