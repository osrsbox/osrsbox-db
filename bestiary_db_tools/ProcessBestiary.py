# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/19

Description:


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
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

import os
import sys
import json
import glob

sys.path.append(os.getcwd())
import MonsterDefinition

###############################################################################
# ProcessBestiary object
class ProcessBestiary(object):
    def __init__(self, all_wiki_monsters, all_monster_names, all_wiki_monsters_verisoned):
        self.all_wiki_monsters = all_wiki_monsters # Default wikitext dict from 
        self.all_monster_names = all_monster_names # From cache defs, not unique list
        self.all_wiki_monsters_verisoned = all_wiki_monsters_verisoned # Wikitext, with versioning

    def process_all_monsters(self):
        # Loop through every item
        print(">>> Processing all monsters...")
        # Print length
        print("  > Total beast count: %d" % len(self.all_monster_names))
        # Individually process each item
        # for monster_data in self.all_monster_names:
        #     self.construct_MonsterDefinition(monster_data)
        for monster_name in self.all_wiki_monsters_verisoned:
            self.construct_MonsterDefinition(self.all_wiki_monsters_verisoned[monster_name])

    def construct_MonsterDefinition(self, monster_data):
        monster_def = MonsterDefinition.MonsterDefinition(monster_data, self.all_wiki_monsters) 
        monster = monster_def.populate()

################################################################################
if __name__=="__main__":    
    # Start processing    
    print(">>> Starting processing...")

    # Remove old log file
    if os.path.exists("MonsterDefinition.log"):
        os.remove("MonsterDefinition.log")

    extraction_path_wiki = os.path.join("..", "extraction_tools_wiki", "")
    extraction_path_other = os.path.join("..", "extraction_tools_other", "")

    with open(extraction_path_wiki + "extract_all_monsters_page_wikitext.json") as f:
        all_wiki_monsters = json.load(f)

    with open("all_monsters_wikitext.json") as f:
        all_wiki_monsters_verisoned = json.load(f)

    all_monster_names = list()
    with open(extraction_path_wiki + "extract_all_monsters_from_defs_unique.txt") as f:
        for line in f:
            line = line.strip()
            all_monster_names.append(line)

    # Next, build the ProcessItems class to handle all items
    pb = ProcessBestiary(all_wiki_monsters,
                         all_monster_names,
                         all_wiki_monsters_verisoned)
    
    # Start processing each monster
    pb.process_all_monsters()
