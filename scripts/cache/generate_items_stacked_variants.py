"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Generate the item stacked variants.

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
from scripts.cache import cache_constants


def process():
    """Extract find all stacked item variants in ItemDefinition data."""
    definitions = cache_constants.ITEM_DEFINITIONS
    stacked_variants = dict()

    # Loop the loaded data
    for id_number in definitions:
        # Fetch the specific item definition being processed
        item_definition = definitions[id_number]

        # Determine if item has stacked variants
        try:
            is_stacked = item_definition["countObj"]
        except KeyError:
            is_stacked = False

        # Process stacked items
        if is_stacked:
            for stacked_id, stacked_count in zip(item_definition["countObj"], item_definition["countCo"]):
                # Skip any entry that is a zero (empty)
                if stacked_id == 0:
                    pass
                else:
                    # Skip any ID that has already been processed
                    if stacked_id in stacked_variants:
                        pass
                    else:
                        stacked_dict = dict()
                        stacked_dict["id"] = item_definition["id"]
                        stacked_dict["count"] = stacked_count
                        stacked_variants[stacked_id] = stacked_dict

    # Finally, dump the extracted stacked item IDs to the items-cache-data.json file
    out_fi = Path(config.DATA_ITEMS_PATH / "items-stacked.json")
    with open(out_fi, "w") as f:
        json.dump(stacked_variants, f, indent=4)


if __name__ == "__main__":
    # Determine items with stacked variants. Example:
    # 23663: 23661
    process()
