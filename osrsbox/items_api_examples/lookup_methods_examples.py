"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A very simple example script of how to load the osrsbox-db item database,
loop through the loaded items, and print the item name to the console.

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

from osrsbox import items_api


if __name__ == "__main__":
    # Load all items
    all_db_items = items_api.load()

    # Lookup item with ID value of 12 - this will work
    print(">>> all_db_items.lookup_by_item_id(12)")
    item = all_db_items.lookup_by_item_id(12)
    print(item)

    # Lookup item with ID value of 2134314314134 - this will fail
    # This is why we wrap it in a try/except
    print(">>> all_db_items.lookup_by_item_id(2134314314134)")
    try:
        item = all_db_items.lookup_by_item_id(2134314314134)
        print(item)
    except KeyError:
        pass

    # Lookup item with name value of "Coal" - this will work
    print(">>> all_db_items.lookup_by_item_name(Coal)")
    item = all_db_items.lookup_by_item_name("Coal")
    print(item)

    # Lookup item with name value of "Meow" - this will fail
    print(">>> all_db_items.lookup_by_item_name(Meow)")
    try:
        item = all_db_items.lookup_by_item_name("Meow")
        print(item)
    except ValueError:
        pass

    # Lookup item with name value of "Overload (Nightmare Zone) (4 doses)" - this will pass
    print(">>> all_db_items.lookup_by_item_name(Overload (Nightmare Zone) (4 doses))")
    try:
        item = all_db_items.lookup_by_item_name("Overload (Nightmare Zone) (4 doses)", use_wiki_name=True)
        print(item)
    except ValueError:
        pass
