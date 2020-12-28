"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A script to determine new items and monsters added after a game
update. This is used to help update the CHANGELOG in the repository.
This script takes two different files inputs for items and monsters:
    - items: data/items-cache-data.json
    - monsters: data/monsters-cache-data.json
When generated, both files should exist in: data/cache/ and the files
should be copied to: data/

Copyright (c) 2020, PH01L

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


class DetermineCacheChanges:
    """A class to determine added, removed, changed and unchanged entries.

    Every OSRS weekly update has the potential to add, remove or change item
    and monster properties. This class analyzes the OSRS cache dump of the
    existing entries and compares to a new database dump.

    :param current_dict: A dictionary of the new items_scraper.json file
    :param past_dict: A dictionary of the old items_scraper.json file
    """
    def __init__(self, current_dict: Dict, past_dict: Dict):
        self.current_dict = current_dict
        self.past_dict = past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self) -> List:
        """Return a set of only new IDs that is sorted."""
        added = self.set_current - self.intersect
        added = sorted(added)
        return added

    def removed(self) -> List:
        """Return a set of only removed IDs that is sorted."""
        removed = self.set_past - self.intersect
        removed = sorted(removed)
        return removed

    def changed(self) -> List:
        """Return a set of only changed entries (including properties) that is sorted."""
        changed = set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
        changed = sorted(changed)
        return changed

    def unchanged(self) -> List:
        """Return a set of only unchanged entries (including properties) that is sorted."""
        unchanged = set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
        unchanged = sorted(unchanged)
        return unchanged


def items():
    """The main function for determining item changes."""
    # Read in the old items-cache-data.json file
    fi_name = Path(config.DATA_ITEMS_PATH / "items-cache-data.json")
    with open(fi_name) as f:
        old_items = json.load(f)

    # Read in the new items-cache-data.json file
    fi_name = Path(config.DATA_ITEMS_PATH / "items-cache-data-new.json")
    with open(fi_name) as f:
        new_items = json.load(f)

    # Initialize class
    dd = DetermineCacheChanges(new_items, old_items)

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


def monsters():
    """The main function for determining monster changes."""
    # Read in the old monsters-cache-data.json file
    fi_name = Path(config.DATA_MONSTERS_PATH / "monsters-cache-data.json")
    with open(fi_name) as f:
        old_monsters = json.load(f)

    # Read in the new monsters-cache-data.json file
    fi_name = Path(config.DATA_MONSTERS_PATH / "monsters-cache-data-new.json")
    with open(fi_name) as f:
        new_monsters = json.load(f)

    # Initialize class
    dd = DetermineCacheChanges(new_monsters, old_monsters)

    # Determine added monsters
    added = dd.added()
    print("- Added monsters: %d" % len(added))
    for monsterID in added:
        print("    - %s,%s" % (monsterID,
                               new_monsters[monsterID]["name"]))

    # Determine removed monsters
    removed = dd.removed()
    print("- Removed monsters: %d" % len(removed))
    for monsterID in removed:
        print("    - %s,%s" % (monsterID,
                               old_monsters[monsterID]["name"]))

    # Determine changed monsters
    changed = dd.changed()
    print("- Changed monsters: %d" % len(changed))
    for monsterID in changed:
        changed_keys = list()
        for key in new_monsters[monsterID]:
            new_monsters_key = new_monsters[monsterID].get(key)
            old_monsters_key = old_monsters[monsterID].get(key)
            if new_monsters_key is None or old_monsters_key is None:
                continue
            if new_monsters[monsterID][key] != old_monsters[monsterID][key]:
                changed_keys.append(key)
        if changed_keys:
            print("    - %s,%s,%s" % (monsterID,
                                      old_monsters[monsterID]["name"],
                                      '|'.join(changed_keys)))

    # # Determine unchanged monsters
    # # This is commented out, as the results are always large
    # unchanged = dd.unchanged()
    # print("- Unchanged monsters: %d" % len(unchanged))
    # for monsterID in unchanged:
    #     print("    - %s,%s" % (monsterID,
    #                            new_monsters[monsterID]["name"]))


def move():
    """Move cache files."""
    old = Path(config.DATA_ITEMS_PATH / "items-cache-data.json")
    new = Path(config.DATA_ITEMS_PATH / "items-cache-data-new.json")
    old.unlink()
    new.rename(old)

    old = Path(config.DATA_MONSTERS_PATH / "monsters-cache-data.json")
    new = Path(config.DATA_MONSTERS_PATH / "monsters-cache-data-new.json")
    old.unlink()
    new.rename(old)


if __name__ == "__main__":
    print("Determining item changes using items-cache-data.json files...")
    items()

    print("Determining monster changes using monsters-cache-data.json files...")
    monsters()

    print("Overwrite old files")
    move()
