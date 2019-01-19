# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/19

Description:
BeastDefinition is a class to process and construct BeastObjects

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
import sys
import json
import datetime
import collections
import logging
import re

# These require pip install
import mwparserfromhell
import dateparser

# Import ItemBonuses and ItemEquipment class
sys.path.append(os.getcwd())
# import BeastSlayer
# import BeastStats
# import BeastDrops

###############################################################################
# Helper methods
def _strcast(val):
    """ Convert value to string. """
    if val is None:
        return None
    return str(val)

def _intcast(val):
    """ Convert input to integer. """
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        if val[0] == "-":
            if val[1:].isdigit():
                return int(val)
        else:
            if val.isdigit():
                return int(val)

def _floatcast(val):
    """ Convert input to float. """
    if val is None:
        return None
    if isinstance(val, float):
        return val
    if isinstance(val, str):
        return float(val)                
                
def _boolcast(val):
    """ Convert value to boolean object. """
    if val is None:
        return None
    elif val in ["True", "true", True, "Yes", "yes"]:
        return True
    elif val in ["False", "false", False, "No", "no"]:
        return False   

def _datecast(val):
    """ Check date by converting to datetime object, and convert back to str. """
    if val is None:
        return None
    if val is "":
        return None
    elif isinstance(val, datetime.date):
        return val.strftime("%d %B %Y")
    try:
        date = datetime.datetime.strptime(val, "%d %B %Y")
    except ValueError:
        date = dateparser.parse(val)
    return date.strftime("%d %B %Y")        

def _listcast(val):
    """ Check and convert to a list. """
    if val is None:
        return None
    elif isinstance(val, list):
        return val
    elif isinstance(val, str):
        temp_list = list()
        return temp_list.append(val)

###############################################################################
# BeastDefinition object
class BeastDefinition(object):
    def __init__(self, beast_data, all_wiki_bestiary, wiki_extraction_errors):
        # Input beast_name
        beast_data = beast_data.split("|")
        self.beast_id = beast_data[0]
        self.beast_name = beast_data[1]
        self.beast_combat_level = beast_data[2]

        self.all_wiki_bestiary = all_wiki_bestiary

        self.wiki_extraction_errors = list()
        for error_name in wiki_extraction_errors:
            error_name = error_name.lower()
            self.wiki_extraction_errors.append(error_name)

        # Dict of all BeastDefinition properties
        # Not currently used, but kept for future
        self.properties = {
            "id" : None,
            "name" : None,
            "members" : None,
            "release_date" : None,
            "combat_level" : None,
            "examine" : None,
            "hitpoints" : None,
            "maxhit" : None,
            "aggressive" : None,
            "poison" : None,
            "weakness" : None,
            "attack_type" : None,
            "attack_style" : None,
            "url" : None}

        # Item Bonuses (if equipable, but initialize one anyway)   
        # self.itemBonuses = ItemBonuses.ItemBonuses(self.itemID)

        # Item Equipment (if equipable, but initialize one anyway)   
        # self.itemEquipment = ItemEquipment.ItemEquipment(self.itemID)        

        # Setup logging
        logging.basicConfig(filename="BeastDefinition.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    # Setters and Getters for each item property
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = _intcast(value)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = _strcast(value)

    @property
    def members(self):
        return self._members
    @members.setter
    def members(self, value):
        self._members = _boolcast(value)

    @property
    def release_date(self):
        return self._release_date
    @release_date.setter
    def release_date(self, value):
        self._release_date = _datecast(value)

    @property
    def combat_level(self):
        return self._combat_level
    @combat_level.setter
    def combat_level(self, value):
        self._combat_level = _intcast(value)

    @property
    def examine(self):
        return self._examine
    @examine.setter
    def examine(self, value):
        self._examine = _strcast(value)

    @property
    def hitpoints(self):
        return self._hitpoints
    @hitpoints.setter
    def hitpoints(self, value):
        self._hitpoints = _intcast(value)

    @property
    def maxhit(self):
        return self._maxhit
    @maxhit.setter
    def maxhit(self, value):
        self._maxhit = _intcast(value)

    @property
    def aggressive(self):
        return self._aggressive
    @aggressive.setter
    def aggressive(self, value):
        self._aggressive = _boolcast(value)

    @property
    def poison(self):
        return self._poison
    @poison.setter
    def poison(self, value):
        self._poison = _boolcast(value)

    @property
    def weakness(self):
        return self._weakness
    @weakness.setter
    def weakness(self, value):
        self._weakness = _listcast(value)

    @property
    def attack_type(self):
        return self._attack_type
    @attack_type.setter
    def attack_type(self, value):
        self._attack_type = _strcast(value)

    @property
    def attack_style(self):
        return self._attack_style
    @attack_style.setter
    def attack_style(self, value):
        self._attack_style = _strcast(value)

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = _strcast(value)

    def populate(self):
        # sys.stdout.write(">>> Processing: %s\r" % self.itemID)

        # Start section in logger
        self.logger.debug("============================================ START")
        self.logger.debug("beast_name: %s" % self.beast_name)

        self.name = self.beast_name
        self.id = self.beast_id
        self.combat_level = self.beast_combat_level

        print(">>>", self.name)

        if self.name.lower() in self.wiki_extraction_errors:
            return

        has_wiki_page = self.determine_wiki_page()

        print("has_wiki_page:", has_wiki_page)

        if has_wiki_page:
            self.wikitext = self.all_wiki_bestiary[self.name]
            has_infobox_monster = self.extract_InfoboxMonster()
        else:
            return

        print("has_infobox_monster:", has_infobox_monster)

        if has_infobox_monster:
            self.parse_InfoboxMonster()
            print(self.release_date)

        # print(self.beast_name, self.combat_level, has_wiki_page)

        # Infobox Monster

        # Actually output a JSON file, comment out for testing
        # self.export_pretty_json()

        # Finished. Return the entire ItemDefinition object
        return self

    def determine_wiki_page(self):
        self.logger.debug("Searching for item in OSRS Wiki by name...")
        
        # Check if the item name is in the Wiki API dump
        # Return True if found by self.beast_name
        # Return False if not found
        if self.name in self.all_wiki_bestiary:
            self.logger.debug(">>> BEAST FOUND:")
            self.logger.debug("  > name: %s" % self.name)
            # self.logger.debug("  > id: %s" % self.id)
            self.url = "https://oldschool.runescape.wiki/w/" + self.name
            return True
        else:
            return False

    def extract_InfoboxMonster(self):
        wikitext = mwparserfromhell.parse(self.wikitext)

        # Extract templates in the page
        templates = wikitext.filter_templates()
        for template in templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            if "infobox monster" in template_name:
                self.infobox_monster = template
                return True

        # Default to return false (no infobox found)
        return False        

    def strip_infobox(self, input):
        # Clean an passed InfoBox string
        clean_input = str(input)
        clean_input = clean_input.strip()
        clean_input = clean_input.replace("[", "")
        clean_input = clean_input.replace("]", "")
        return clean_input

    def clean_release_date(self, input):
        # Clean a release date value
        release_date = None
        release_date = input
        release_date = release_date.strip()
        release_date = release_date.replace("[", "")
        release_date = release_date.replace("]", "")        
        return release_date

    def extract_Infobox_value(self, template, key):
        value = None
        try:
            value = template.get(key).value
            return value
        except ValueError:
            return value

    def parse_InfoboxMonster(self):
        # Determine the release date of an item (TESTED)
        release_date = None
        # if self.current_version is not None:
        #     key = "release" + str(self.current_version)
        #     release_date = self.extract_Infobox_value(template, key)
        if release_date is None:
            release_date = self.extract_Infobox_value(self.infobox_monster, "release")
        if release_date is not None:
            self.release_date = self.clean_release_date(release_date)
        else:
            self.release_date = None


        return True

    def extract_InfoBoxBonuses(self):
        # Extract Infobox Bonuses from wikitext
        try:
            wikicode = mwparserfromhell.parse(self.all_wikia_items_bonuses[self.wiki_name])
        except KeyError:
            return False
        templates = wikicode.filter_templates()
        for template in templates:
            extracted_infobox = self.parse_InfoboxBonuses(template)
            if extracted_infobox:
                return True
            else:
                return False   
        return False
              
    def clean_InfoboxBonuses_value(self, template, prop):
        value = None
        # if self.current_version is not None:
        #     key = prop + str(self.current_version)
        #     value = self.extract_Infobox_value(template, key)
        if value is None:
            value = self.extract_Infobox_value(template, prop)
        if value is not None:
            #itemBonuses.attack_stab = self.strip_infobox(value)
            return self.strip_infobox(value)
          
    ###########################################################################
    # Handle item to JSON
    def print_json(self):
        # Print JSON to console
        self.construct_json()
        json_obj = json.dumps(self.json_out)
        print(json_obj)

    def print_pretty_json(self):
        # Pretty print JSON to console
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=4)
        print(json_obj)

    def print_debug_json(self):
        # Print JSON to log file
        self.construct_json()
        json_obj = json.dumps(self.json_out)
        self.logger.debug(json_obj)

    def print_pretty_debug_json(self):
        # Pretty print JSON to log file
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=4)
        self.logger.debug(json_obj)
            
    def export_json(self):
        # Export JSON to individual file
        self.construct_json()
        out_fi = "items-json" + os.sep + str(self.id) + ".json"
        with open(out_fi, "w") as f:
            json.dump(self.json_out, f)

    def export_pretty_json(self):
        # Export pretty JSON to individual file
        self.construct_json()
        out_fi = ".." + os.sep + "docs" + os.sep + "items-json" + os.sep + str(self.id) + ".json"
        with open(out_fi, "w", newline="\n") as f:
            json.dump(self.json_out, f, indent=4)

    def construct_json(self):
        # TODO: Update construction
        self.json_out = collections.OrderedDict()
        self.json_out["id"] = self.id
        self.json_out["name"] = self.name
        self.json_out["members"] = self.members
        self.json_out["tradeable"] = self.tradeable
        self.json_out["tradeable_on_ge"] = self.tradeable_on_ge
        self.json_out["stackable"] = self.stackable
        self.json_out["noted"] = self.noted
        self.json_out["noteable"] = self.noteable
        self.json_out["linked_id"] = self.linked_id
        self.json_out["equipable"] = self.equipable
        self.json_out["cost"] = self.cost
        self.json_out["lowalch"] = self.lowalch
        self.json_out["highalch"] = self.highalch        
        self.json_out["weight"] = self.weight
        self.json_out["buy_limit"] = self.buy_limit
        self.json_out["quest_item"] = self.quest_item
        self.json_out["release_date"] = self.release_date     
        self.json_out["examine"] = self.examine
        self.json_out["url"] = self.url
        if self.equipable:
            bonuses_in_json = self.itemBonuses.construct_json()
            self.json_out["bonuses"] = bonuses_in_json
            equipment_in_json = self.itemEquipment.construct_json()
            self.json_out["equipment"] = equipment_in_json

###########################################################################
if __name__=="__main__":
    # Run unit tests
    assert _intcast(-1) == -1
    assert _intcast("-1") == -1
  
    assert _boolcast("false") == False
    assert _boolcast("True")
    assert _boolcast("true")
    assert _boolcast(False) == False
    assert _boolcast(True)

    assert _strcast(1)
    assert _strcast("OSRS Rocks!")
    
    print("Module tests passed.")
