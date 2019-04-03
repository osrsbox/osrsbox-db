"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A very simple example script of how to load the osrsbox-db item database,
loop through the loaded items, and determine items with the highest
prayer bonus.

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

    prayer_items = dict()

    # Populate dict
    for item in all_db_items:
        if item.equipable_by_player:
            prayer_items[item.equipment.slot] = {"prayer_bonus": 0, "name": None}

    # Loop through all items in the database
    for item in all_db_items:
        if item.equipable_by_player:
            item_slot = item.equipment.slot
            prayer_bonus = item.equipment.prayer

            if prayer_bonus > prayer_items[item_slot]["prayer_bonus"]:
                prayer_items[item_slot] = {"prayer_bonus": prayer_bonus, "name": item.name}

    for item_slot, info_dict in prayer_items.items():
        print(f"{item_slot:<10} {info_dict['prayer_bonus']:<10} {info_dict['name']}")
