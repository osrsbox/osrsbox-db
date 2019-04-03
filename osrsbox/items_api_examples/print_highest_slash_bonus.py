"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A very simple example script of how to load the osrsbox-db item database,
loop through the loaded items, and determine the weapons with the highest
slash attack bonus.

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

from collections import defaultdict

from osrsbox import items_api


if __name__ == "__main__":
    # Load all items
    all_db_items = items_api.load()

    top_attack_slash = defaultdict(list)

    # Loop the item database
    for item in all_db_items:
        if item.equipable_by_player:  # If item is equipable, continue processing
            # Append equipable item slash bonus, and item name
            top_attack_slash[item.equipment.attack_slash].append(item.name)

    # Loop sorted dictionary
    for slash_attack_bonus, items in sorted(top_attack_slash.items(), reverse=True):
        # Loop item list
        for item_name in items:
            print(f"{slash_attack_bonus:<5} {item_name}")
