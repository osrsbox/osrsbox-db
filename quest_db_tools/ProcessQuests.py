# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
ProcessQuestss is a caller to parse the OSRS Wiki wikicode data
to automate population of JSON files. 

Requirements:
pip install requests
pip install mvparserfromhell
pip install dateparser

pip install wikitextparser

Copyright (c) 2018, PH01L

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
import QuestDefinition

################################################################################
if __name__=="__main__":
    
    # Start processing    
    print(">>> Starting processing...")

    wikia_extraction_path = ".." + os.sep + "wiki_extraction_tools" + os.sep

    with open(wikia_extraction_path + "extract_all_quests_page_wikitext.txt") as f:
        all_wikia_quest_pages = json.load(f)

    all_wikia_quest_names = list()
    with open(wikia_extraction_path + "extract_all_quests.txt") as f:
        for l in f:
            l = l.strip()
            all_wikia_quest_names.append(l)  

    # Make a dir for JSON output
    # directory = "quests-json"
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    quests = dict()

    for quest_name in all_wikia_quest_names:
        quest_wikicode = all_wikia_quest_pages[quest_name]       
        qd = QuestDefinition.QuestDefinition(quest_name, quest_wikicode)
        qd.extract_InfoboxQuest()
