"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A very simple example script of how to load the osrsbox-db item database,
loop through the loaded items, and export some of the item metadata to
a CSV file.

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

import csv

from osrsbox import items_api


if __name__ == "__main__":
    # Load all items
    all_db_items = items_api.load()

    # Loop through all items and export to CSV file
    with open('items.csv', mode="w", newline="") as items_out_fi:
        items_writer = csv.writer(items_out_fi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        items_writer.writerow(["ID", "NAME", "HIGHALCH"])
        for item in all_db_items:
            items_writer.writerow([item.id, item.name, item.highalch])
