"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A simple script to determine new items added after a game update_items. Takes
the items_scraper.json file from the ItemScraper RuneLite plugin as the
new data input and compares the entries to the old items_scraper.json
file that should be in the docs folder. Put the new items_scraper.json
file in this directory before running the script.

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

import json
from pathlib import Path
from typing import List
from typing import Dict

import config


class DetermineNewItems:
    """A simple class to determine added, removed, changed and unchanged items.

    Every OSRS weekly update_items has the potential to add, remove or change item
    properties. This class analyzes the OSRS cache dump of the existing
    database entries and compares to a new database dump.
    Calculate the difference between two dictionaries as:

    :param current_dict: A dictionary of the new items_scraper.json file
    :param past_dict: A dictionary of the old items_scraper.json file
    """
    def __init__(self, current_dict: Dict, past_dict: Dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self) -> List:
        """Return a set of only new item IDs that is sorted."""
        added_items = self.set_current - self.intersect
        added_items = sorted(added_items)
        return added_items

    def removed(self) -> List:
        """Return a set of only removed item IDs that is sorted."""
        removed_items = self.set_past - self.intersect
        removed_items = sorted(removed_items)
        return removed_items

    def changed(self) -> List:
        """Return a set of only changed items (including properties) that is sorted."""
        changed_items = set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
        changed_items = sorted(changed_items)
        return changed_items

    def unchanged(self) -> List:
        """Return a set of only unchanged items (including properties) that is sorted."""
        unchanged_items = set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
        unchanged_items = sorted(unchanged_items)
        return unchanged_items


def main():
    """The main function for determining new items added to the game."""
    # Read in the old item-scraper.json file
    fi_name = Path(config.DATA_PATH / "items-scraper.json")
    with open(fi_name) as f:
        old_items = json.load(f)

    # Read in the new item-scraper.json file
    fi_name = Path("items-scraper.json")
    with open(fi_name) as f:
        new_items = json.load(f)

    # Initialize class
    dd = DetermineNewItems(new_items, old_items)

    # Determine added items
    added = dd.added()
    print("- Added items: %d" % len(added))
    for itemID in added:
        print("    - %s,%s" % (itemID,
                               new_items[itemID]["name"]))

    # Determine removed items
    removed = dd.removed()
    print("- Removed items: %d" % len(removed))
    for itemID in removed:
        print("    - %s,%s" % (itemID,
                               old_items[itemID]["name"]))

    # Determine changed items
    changed = dd.changed()
    print("- Changed items: %d" % len(changed))
    for itemID in changed:
        changed_keys = list()
        for key in new_items[itemID]:
            if new_items[itemID][key] != old_items[itemID][key]:
                changed_keys.append(key)
        if changed_keys:
            print("    - %s,%s,%s" % (itemID,
                                      old_items[itemID]["name"],
                                      '|'.join(changed_keys)))

    # # Determine unchanged items
    # # This is commented out, as the results are always large
    # unchanged = dd.unchanged()
    # print("- Unchanged items: %d" % len(unchanged))
    # for itemID in unchanged:
    #     print("    - %s,%s" % (itemID,
    #                            new_items[itemID]["name"]))


if __name__ == "__main__":
    print("Determining new items using items-scraper.json files...")
    main()
