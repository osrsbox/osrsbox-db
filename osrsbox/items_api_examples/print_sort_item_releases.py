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

import collections
import datetime

from osrsbox import items_api


if __name__ == "__main__":
    # Load all items
    all_db_items = items_api.load()

    items_by_release_date = collections.defaultdict(list)

    # Loop through all items in the database
    for item in all_db_items:
        if item.release_date:  # Check item has a release date (aka, not None)
            # Convert date string to a Python datetime object
            datetime_object = datetime.datetime.strptime(item.release_date, '%Y-%m-%d')
            # Append item object to dictionary > list
            items_by_release_date[datetime_object].append(item)

    # Sort dictionary by release date
    items_by_release_date = sorted(items_by_release_date.items())

    # Loop dictionary
    for release_date, items in items_by_release_date:
        # Loop list of items
        for item in items:
            # Print release date (as string), followed by item ID and name
            print(f"{release_date.strftime('%Y-%m-%d'):<15} {item.id:<10} {item.name}")
