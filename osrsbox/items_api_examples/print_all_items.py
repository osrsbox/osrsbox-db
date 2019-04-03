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

    # Loop through all items in the database and print the item name for each item
    for item in all_db_items:
        # print(item.id, item.name)  # Old, simple printing method
        print(f"{item.id:<6} {item.name}")  # New, f-strings printing method
