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

################################################################################
class DetermineNewItems(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

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

    new_json = args["newfile"]
    old_json = args["oldfile"]

    print(">>> Processing old_json: %s" % old_json)
    with open(old_json) as f:
        allitems_old = json.load(f)
    # Print length of allitems dict
    print("  > Old item count: %d" % len(allitems_old))

    print(">>> Processing new_json: %s" % new_json)
    with open(new_json) as f:
        allitems_new = json.load(f)
    # Print length of allitems dict
    print("  > New item count: %d" % len(allitems_new))
    
    dd  = DetermineNewItems(allitems_new, allitems_old)
    
    # Determine added items
    print(">>> Added items")
    added = dd.added()
    for itemID in added:
        print("%s,%s" % (itemID, allitems_new[itemID]["name"]))

    # Determine removed items
    removed = dd.removed()
    print(">>> Removed items")
    for itemID in removed:
        print("%s,%s" % (itemID, allitems_old[itemID]["name"]))        

    # Determine changed items
    changed = dd.changed()
    print(">>> Changed items")
    for itemID in changed:
        changed_keys = list()
        for key in allitems_new[itemID]:
            if(allitems_new[itemID][key] != allitems_old[itemID][key]):
                changed_keys.append(key)
        print("%s,%s,%s" % (itemID, allitems_new[itemID]["name"], changed_keys))

    # Determine unchanged items
    # This is commented out, as the results are always large
    # unchanged = dd.unchanged()
    # print(">>> Unchanged items")
    # for itemID in unchanged:
    #     print("%s,%s" % (itemID, allitems_new[itemID]["name"])) 
