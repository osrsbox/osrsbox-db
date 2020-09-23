"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Fetch a list of item buy limits from the OSRS Wiki.

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

import requests

from osrsbox import items_api
import config


def main():
    # Get list of all tradeable items
    items = [item for item in items_api.load() if item.tradeable_on_ge]

    # Specify data structure for storage of buy_limits
    buy_limits = dict()

    for item in items:
        # Extract name to lookup from wiki_exchange property
        wiki_name = item.wiki_exchange.split(":")[2]

        # Get URL
        url = f"https://oldschool.runescape.wiki/w/Module:Exchange/{wiki_name}?action=raw"
        r = requests.get(url)
        data = r.text

        # Set default values
        item_id_checker = None
        buy_limit = None

        for line in data.split("\n"):
            if "itemId     =" in line:
                item_id_checker = line.split("=")[1]
                item_id_checker = item_id_checker.strip()
                item_id_checker = item_id_checker.replace(",", "")
                if item.id == int(item_id_checker):
                    continue
                else:
                    print("Warning: Item IDs don't match")
                    print(item.id, item_id_checker, item.name, wiki_name)
            if "limit      =" in line:
                buy_limit = line.split("=")[1]
                buy_limit = buy_limit.strip()
                buy_limit = buy_limit.replace(",", "")
                if buy_limit == "nil":
                    buy_limit = None
                else:
                    buy_limit = int(buy_limit)
        if not item_id_checker:
            print("Warning: No item ID", item.id, item_id_checker)
            buy_limits[item.id] = buy_limit
            continue
        if not buy_limit:
            print("Warning No item buy limit", item.id, item_id_checker)
            buy_limits[item_id_checker] = buy_limit
            continue
        buy_limits[item_id_checker] = buy_limit

    file_name = "ge-limits-ids.json"
    file_path = Path(config.DATA_ITEMS_PATH / file_name)
    with open(file_path, "w") as f:
        json.dump(buy_limits, f, indent=4)


if __name__ == "__main__":
    main()
