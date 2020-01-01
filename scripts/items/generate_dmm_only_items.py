"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to generate the data/items/dmm-only-items.json file which documents
any items that are unique to the old DMM tournaments.

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

import config
from osrsbox import items_api


DMM_MODE_ITEM_NAMES = [
    "Statius's full helm",
    "Statius's platebody",
    "Statius's platelegs",
    "Statius's warhammer",
    "Vesta's chainbody",
    "Vesta's plateskirt",
    "Vesta's longsword",
    "Vesta's spear",
    "Zuriel's hood",
    "Zuriel's robe top",
    "Zuriel's robe bottom",
    "Zuriel's staff",
    "Morrigan's coif",
    "Morrigan's leather body",
    "Morrigan's leather chaps",
    "Morrigan's throwing axe",
    "Morrigan's javelin"
]


def main():
    # Output dictionary of DMM-only items
    dmm_only_items = dict()

    # Start processing all items in database
    all_db_items = items_api.load()

    for item in all_db_items:
        if item.name in DMM_MODE_ITEM_NAMES:
            dmm_only_items[item.id] = item.name

    # Write out file
    out_fi_path = Path(config.DATA_ITEMS_PATH / "dmm-only-items.json")
    with open(out_fi_path, "w") as f:
        json.dump(dmm_only_items, f, indent=4)


if __name__ == "__main__":
    main()
