"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Generate the monsters-cache-data.json file from raw NPC Definition files.

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
    """Main function to extract attackble NPC definition files."""
    definitions = cache_constants.NPC_DEFINITIONS
    attackable_npcs = dict()

    # Loop all entries in the loaded definition files
    for id_number in definitions:
        json_data = definitions[id_number]

        # Before checking if attackable, add a couple of
        # known monsters that are "death" versions...
        if json_data["id"] in [8622, 9432, 9433]:
            attackable_npcs[id_number] = json_data

        if "Attack" in json_data["actions"]:
            # Skip entries with variable menu list color in name
            if "<col" in json_data["name"]:
                continue
            if json_data["name"] in ["Null", "null", ""]:
                continue

            # Save the attackable NPC
            attackable_npcs[id_number] = json_data

    # Save all extracted attackable NPCs to JSON file
    out_fi = Path(config.DATA_MONSTERS_PATH / "monsters-cache-data-new.json")
    with open(out_fi, "w") as f:
        json.dump(attackable_npcs, f, indent=4)


if __name__ == "__main__":
    process()
