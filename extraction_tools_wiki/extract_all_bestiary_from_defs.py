# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/19

Description:
Extract all attackable NPCs (beasts) from NpcDefinition files

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
out_fi = "extract_all_bestiary_from_defs.txt"
fi = open(out_fi, "w", newline="\n")

for def_fi in def_fis:
    with open(def_fi) as f:
        json_data = json.load(f)
        # Look for Attack in right-click options
        if "Attack" in json_data["options"]:
            # Get useful data from NpcDefinition
            beast_name = json_data["name"]
            beast_id = json_data["id"]
            beast_combat_level = json_data["combatLevel"]
            # Print NPC name
            print(beast_name)
            # Skip strange beast names
            if beast_name.startswith("<col"):
                continue
            if beast_name == "null":
                continue
            # Write out details of beast
            # Format: id|name|norm_name|combatlevel
            fi.write("%s|%s|%s\n" % (beast_id, 
                                     beast_name, 
                                     beast_combat_level))

fi.close()
