# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/13

Description:
ProcessQuestss is a caller to parse the OSRS Wiki wikicode data
to automate population of JSON files.

Requirements:
pip install requests
pip install mvparserfromhell
pip install dateparser

pip install wikitextparser

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
import json
import glob


from . import QuestDefinition


################################################################################
if __name__ == "__main__":

    # Start processing
    print(">>> Starting processing...")

    wiki_extraction_path = os.path.join("..", "extraction_tools_wiki", "")

    # Load all JSON files with quest wikitext
    print(">>> Loading wikitext...")
    all_wiki_quest_pages = dict()

    wikitext_fis_path = os.path.join(wiki_extraction_path + "extract_all_quests_page_wikitext", "*")
    wikitext_fis = glob.glob(wikitext_fis_path)

    for fi in wikitext_fis:
        with open(fi) as f:
            data = json.load(f)
            quest_name = next(iter(data))
            wikitext_str = data[quest_name]
            all_wiki_quest_pages[quest_name] = wikitext_str

    all_quest_names = list()

    print(">>> Loading quest lists...")
    all_quest_names_normal = list()
    with open("quests.txt") as f:
        for line in f:
            line = line.strip()
            all_quest_names_normal.append(line)
            all_quest_names.append(line)

    all_quest_names_mini = list()
    # with open("miniquests.txt") as f:
    #     for l in f:
    #         l = l.strip()
    #         all_quest_names_mini.append(l)
    #         all_quest_names.append(l)

    # Make a dir for JSON output
    # directory = "quests-json"
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    quests = dict()
    all_quests = dict()

    print(">>> Processing quests...")
    for quest_name in all_quest_names:
        quest_type = ""
        # Determine what type of quest (normal, mini, sub)
        if quest_name in all_quest_names_mini:
            quest_type = "mini"
        elif quest_name in all_quest_names:
            quest_type = "normal"
        else:
            print(">>> Warning could not categorize quest...")

        # Get the wikicode for the quest
        quest_wikicode = all_wiki_quest_pages[quest_name]

        # Create a QuestDefinition object for the quest
        qd = QuestDefinition.QuestDefinition(quest_name, quest_type, quest_wikicode)
        quest = qd.populate()
        if quest_type == "normal":
            quests[int(quest.quest_metadata.number)] = quest
        all_quests[quest.quest_name] = quest

    # # Order the dictionary of the quests (not all quests)
    # od = collections.OrderedDict(sorted(quests.items()))

    # series = set()
    # for quest in sorted(od):
    #     if quests[quest].quest_type is not "mini":
    #         print(quest, quests[quest].quest_name, quests[quest].quest_metadata.series)
    #         if quests[quest].quest_metadata.series is not None:
    #             for s in quests[quest].quest_metadata.series:
    #                 series.add(s)
