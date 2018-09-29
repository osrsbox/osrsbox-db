# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/25

Description:
QuestDefinition is a class to process the raw data parsed from the
OSRS Wiki site to help make the osrsbox-db quest objects

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
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import os
import sys
import json
import datetime
import collections
import logging
import re

# Pip install required
import requests
import mwparserfromhell
import dateparser

sys.path.append(os.getcwd())
import QuestMetadata
import QuestDetails
import QuestRewards

###############################################################################
# QuestDefinition object
class QuestDefinition(object):
    def __init__(self, quest_name, wikicode):
        # Name of the quest
        self.quest_name = quest_name
        # Wikicode of the OSRS Wiki quest page
        self.wikicode = wikicode

        # Setup logging
        logging.basicConfig(filename="QuestDefintition.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def populate(self):
        # sys.stdout.write(">>> Processing: %s\r" % self.itemID)
        # print("Processing: %s" % quest_name)
        self.extract_InfoboxQuest()
        
    def extract_InfoboxQuest(self):
        wikicode = mwparserfromhell.parse(self.wikicode)

        templates = wikicode.filter_templates()
        for template in templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            if "infobox quest" in template_name:
                qm = QuestMetadata.QuestMetadata(template)
                qm.populate()
                json_out = qm.construct_json()
                print(qm.number, self.quest_name)
