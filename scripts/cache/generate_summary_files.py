"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Generate summary of item, npc and object cache definition files.

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
    """Main function to extract item/npc/object summary (ID and name)."""
    for cache_name in cache_constants.CACHE_DUMP_TYPES:
        summary_data = dict()

        if cache_name == "items":
            definitions = cache_constants.ITEM_DEFINITIONS
        elif cache_name == "npcs":
            definitions = cache_constants.NPC_DEFINITIONS
        elif cache_name == "objects":
            definitions = cache_constants.OBJECT_DEFINITIONS

        # Loop all entries in the decompressed and loaded definition file
        for id_number in definitions:
            json_data = definitions[id_number]
            id = json_data["id"]
            name = json_data["name"]
            # Check if there is a non-valid name
            if "<col" in json_data["name"]:
                continue
            if "null" in json_data["name"].lower():
                continue
            summary_data[id] = {
                "id": id,
                "name": name
            }

        # Save all extracted entries to a JSON file
        if cache_name == "items":
            out_fi = Path(config.DOCS_PATH / "items-summary.json")
        elif cache_name == "npcs":
            out_fi = Path(config.DOCS_PATH / "npcs-summary.json")
        elif cache_name == "objects":
            out_fi = Path(config.DOCS_PATH / "objects-summary.json")

        with open(out_fi, "w") as f:
            json.dump(summary_data, f, indent=4)


if __name__ == "__main__":
    process()
