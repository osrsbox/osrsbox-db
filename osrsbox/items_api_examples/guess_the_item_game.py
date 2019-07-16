"""
Author:  rosswf
Email:   ross@rossw.co.uk

Description:
    A very simple 'game' that gets a random item's examine text from the osrsbox-db item database
    and asks the user to guess the name of the item.

Copyright (c) 2019, rosswf

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
import random

if __name__ == "__main__":
    all_db_items = items_api.load()
    item_found = False
    item_name = ""
    while item_found is False:
        random_id = random.randint(1, len(all_db_items))
        for item in all_db_items:
            # Discard items with examine text on None, this is not a required field.
            if item.examine is not None and item.id == random_id:
                print(item.examine)
                item_found = True
                item_name = item.name

    answer = input("What is this item? ")

    if answer.lower() == item_name.lower():
        print("Well done!")
    else:
        print(f"No, this was {item_name}")
