"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A script to parse the osrsbox item database and export the data to
the format needed by the ChuckTracker project:
https://github.com/Little0smit/ChunkTracker

Specified format:
{
    "id": 35,
    "name": "Excalibur",
    "equipable": true,
    "members": true,
    "stats": {
        "offensive": [20,29,-2,0,0],
        "defensive": [0,3,2,1,0],
        "other": [25,0,0,0,5]
    },
    "slot": "weapon",
    "skill_reqs": {
        "attack": 20
    }
}

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

import json

from osrsbox import items_api


if __name__ == "__main__":
    # Load the database
    all_db_items = items_api.load()

    # Setup output dictionary
    chunk_tracker_data = list()

    # Loop through all items in the database
    for item in all_db_items:
        # Convert stats if item is equipable
        if item.equipable_by_player:
            offensive = [item.equipment.attack_stab,
                         item.equipment.attack_slash,
                         item.equipment.attack_crush,
                         item.equipment.attack_magic,
                         item.equipment.attack_ranged]
            defensive = [item.equipment.defence_stab,
                         item.equipment.defence_slash,
                         item.equipment.defence_crush,
                         item.equipment.defence_magic,
                         item.equipment.defence_ranged]
            other = [item.equipment.melee_strength,
                     item.equipment.ranged_strength,
                     item.equipment.magic_damage,
                     item.equipment.prayer,
                     item.equipment.attack_speed]

            # Append extracted data to a dictionary
            stats_dict = dict()
            stats_dict["offensive"] = offensive
            stats_dict["defensive"] = defensive
            stats_dict["other"] = other

            # Set properties for the item dictionary
            item_dict = dict()
            item_dict["id"] = item.id
            item_dict["name"] = item.name
            item_dict["equipable"] = item.equipable
            item_dict["members"] = item.members
            item_dict["stats"] = stats_dict
            item_dict["slot"] = item.equipment.slot
            item_dict["skill_reqs"] = item.equipment.requirements

            # Add equipable item data to list of all equipable items
            chunk_tracker_data.append(item_dict)

    # Export extracted data
    out_file_name = "EquippableItems.json"
    with open(out_file_name, "w", newline="\n") as out_file:
        json.dump(chunk_tracker_data, out_file, indent=4)
