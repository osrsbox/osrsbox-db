# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/21

Description:
Extract all attackable NPCs (monsters) from NpcDefinition files

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

>>> CHANGELOG:
    1.0.0       Base functionality
"""

__version__ = "1.0.0"


import os
import json
import glob

# Parse NpcDefintion dump from RuneLite cache tool
def_fis = glob.glob("npcs/*.json")
def_fis = sorted(def_fis)

# Setup out files
out_fi = "extract_all_monsters_from_defs.txt"
all_monsters = open(out_fi, "w", newline="\n")

out_fi = "extract_all_monsters_from_defs_unique.txt"
all_monsters_unique = open(out_fi, "w", newline="\n")

known = list()
for def_fi in def_fis:
    with open(def_fi) as f:
        json_data = json.load(f)
        # Look for Attack in right-click options
        if "Attack" in json_data["options"]:
            # Get useful data from NpcDefinition
            monster_name = json_data["name"]
            monster_id = json_data["id"]
            monster_combat_level = json_data["combatLevel"]
            # Print NPC name
            print(monster_name)
            # Skip strange monster names
            if monster_name.startswith("<col"):
                continue
            if monster_name == "null":
                continue
            # Write out details of monster to all_monsters
            # Format: id|name|norm_name|combatlevel
            all_monsters.write("%s|%s|%s\n" % (monster_id, 
                                               monster_name, 
                                               monster_combat_level))
            
            unique_monster_name = monster_name + "_" + str(monster_combat_level)
            # Write out details of monster to all_monsters_unique
            # only is the monster is new
            if unique_monster_name not in known:
                all_monsters_unique.write("%s|%s|%s\n" % (monster_id, 
                                                          monster_name, 
                                                          monster_combat_level))

            # Add monsters name and level to a list
            known.append(unique_monster_name)

all_monsters.close()
all_monsters_unique.close()
