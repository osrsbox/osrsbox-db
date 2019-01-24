# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/01/10

Description:
Simple caller script to determine new items added after a game update. Takes
the items_itemscraper.json file from the ItemScraper RuneLite plugin as the 
new data input. The items_itemscraper.json file should be in the same dir
as this script.

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
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import os
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
    # Start processing

    print(">>> Processing OLD items_itemscraper.json file...")
    fi_name = ".." + os.sep + "docs" + os.sep + "items_itemscraper.json"
    with open(fi_name) as f:
        allitems_old = json.load(f)
    print("  > Old item count: %d" % len(allitems_old))

    print(">>> Processing NEW items_itemscraper.json file...")
    fi_name = "items_itemscraper.json"
    with open(fi_name) as f:
        allitems_new = json.load(f)
    print("  > New item count: %d" % len(allitems_new))

    dd  = DetermineNewItems(allitems_new, allitems_old)
    
    # Determine added items
    added = dd.added()
    added = sorted(added)
    print("- Added items: %d" % len(added))
    for itemID in added:
        print("    - %s,%s" % (itemID, allitems_new[itemID]["name"]))

    # Determine removed items
    removed = dd.removed()
    removed = sorted(removed)
    print("- Removed items: %d" % len(removed))
    for itemID in removed:
        print("    - %s,%s" % (itemID, allitems_old[itemID]["name"]))        

    # Determine changed items
    changed = dd.changed()
    changed = sorted(changed)
    print("- Changed items: %d" % len(changed))
    for itemID in changed:
        changed_keys = list()
        for key in allitems_new[itemID]:
            if(allitems_new[itemID][key] != allitems_old[itemID][key]):
                changed_keys.append(key)
        if changed_keys:
            print("    - %s,%s,%s" % (itemID, 
                                      allitems_old[itemID]["name"],
                                      '|'.join(changed_keys)))

    # Determine unchanged items
    # This is commented out, as the results are always large
    # unchanged = dd.unchanged()
    # unchanged = sorted(unchanged)
    # print("- Unchanged items: %d" % len(unchanged))
    # for itemID in unchanged:
    #     print("    - %s,%s" % (itemID, allitems_new[itemID]["name"]))
