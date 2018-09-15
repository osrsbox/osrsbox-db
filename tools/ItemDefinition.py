# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
ItemDefinition is a class to process the raw ItemDefinition data 

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

# Pip install required
import requests
import mwparserfromhell
import dateparser

sys.path.append(os.getcwd())
import ItemBonuses

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
    elif isinstance(val, datetime.date):
        return val.strftime("%d %B %Y")
    try:
        date = datetime.datetime.strptime(val, "%d %B %Y")   
        return date.strftime("%d %B %Y")
    except:
        print("  > %s" % val)
        val = input("  > Enter a correct date: ")
        return _datecast(val)

###############################################################################
# ItemDefinition object
class ItemDefinition(object):
    def __init__(self, itemID, itemJSON, all_wikia_items, all_wikia_items_bonuses):
        # Input itemID number
        self.itemID = itemID
        # Input JSON file (from RuneLite ItemScraper)
        self.itemJSON = itemJSON

        # Bulk dict of all OSRS Wikia Item pages
        self.all_wikia_items = all_wikia_items
        # Bulk dict of all OSRS Wikia Item buy_limits
        self.all_wikia_items_bonuses = all_wikia_items_bonuses
        
        # Dict of all ItemDefinition properties
        self.properties = {
            "id" : None,
            "name" : None,
            "members" : None,
            "tradeable" : None,
            "stackable" : None,
            "noted" : None,
            "noteable" : None,
            "equipable" : None,
            "cost" : None,
            "lowalch" : None,
            "highalch" : None,
            "weight" : None,
            "buy_limit" : None,
            "quest_item" : None,
            "release_date" : None,
            "examine" : None,
            "url" : None}

        # Item Bonuses (if equipable, but initialize one anyway)   
        self.itemBonuses = ItemBonuses.ItemBonuses(self.itemID)

        # Setup logging
        logging.basicConfig(filename="ItemDefinition.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # The name of the item on OSRS Wiki (can vary from actual name)
        self.wiki_name = None

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
    def tradeable(self):
        return self._tradeable
    @tradeable.setter
    def tradeable(self, value):
        self._tradeable = _boolcast(value)                		

    @property
    def stackable(self):
        return self._stackable
    @stackable.setter
    def stackable(self, value):
        self._stackable = _boolcast(value)  

    @property
    def noted(self):
        return self._noted
    @noted.setter
    def noted(self, value):
        self._noted = _boolcast(value)

    @property
    def noteable(self):
        return self._noteable
    @noteable.setter
    def noteable(self, value):
        self._noteable = _boolcast(value)

    @property
    def equipable(self):
        return self._equipable
    @equipable.setter
    def equipable(self, value):
        self._equipable = _boolcast(value)

    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, value):
        self._cost = _intcast(value)	

    @property
    def lowalch(self):
        return self._lowalch
    @lowalch.setter
    def lowalch(self, value):
        self._lowalch = _intcast(value)	          
        
    @property
    def highalch(self):
        return self._highalch
    @highalch.setter
    def highalch(self, value):
        self._highalch = _intcast(value)

    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, value):
        self._weight = _floatcast(value)

    @property
    def buy_limit(self):
        return self._buy_limit
    @buy_limit.setter
    def buy_limit(self, value):
        self._buy_limit = _intcast(value)

    @property
    def quest_item(self):
        return self._quest_item
    @quest_item.setter
    def quest_item(self, value):
        self._quest_item = _strcast(value)

    @property
    def release_date(self):
        return self._release_date
    @release_date.setter
    def release_date(self, value):
        self._release_date = _datecast(value)	

    @property
    def store_price(self):
        return self._store_price
    @store_price.setter
    def store_price(self, value):
        self._store_price = _intcast(value)

    @property
    def examine(self):
        return self._examine
    @examine.setter
    def examine(self, value):
        self._examine = _strcast(value)
	           
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = _strcast(value)

    def populate(self):
        # sys.stdout.write(">>> Processing: %s\r" % self.itemID)
        print(">>>>>>>>>>>> Processing: %s" % self.itemID)

        # Start section in logger
        self.logger.debug("============================================ START")
        self.logger.debug("ItemID: %s" % self.itemID)

        # Set all values from JSON input file into ItemDefinition object
        self.id = self.itemJSON["id"]
        self.name = self.itemJSON["name"]
        self.members = self.itemJSON["members"]
        self.tradeable = self.itemJSON["tradeable"]
        self.stackable = self.itemJSON["stackable"]
        self.noted = self.itemJSON["noted"]
        self.noteable = self.itemJSON["noteable"]
        self.equipable = self.itemJSON["equipable"]
        self.cost = self.itemJSON["cost"]
        self.lowalch = self.itemJSON["lowalch"]
        self.highalch = self.itemJSON["highalch"]        
        self.weight = self.itemJSON["weight"]
        self.buy_limit = self.itemJSON["buy_limit"]
        self.quest_item = self.itemJSON["quest_item"]
        self.release_date = self.itemJSON["release_date"]
        self.examine = self.itemJSON["examine"]
        self.url = self.itemJSON["url"]

        # Log the initial JSON input
        self.logger.debug("Dumping first input...")
        self.logger.debug("Starting: print_pretty_debug_json")
        self.print_pretty_debug_json()

        # All properties from ItemScraper RuneLite plugin are now loaded
        # Time to fetch other information of OSRS Wikia

        # Try to find a OSRS Wikia page for this item 
        self.logger.debug("Starting: determine_wiki_page")
        has_wikia_page = self.determine_wiki_page()
        
        # has_wikia_page indicates if OSRS Wikia page was found
        if has_wikia_page:
            self.wiki_name = self.name
            # This item has an OSRS Wikia page
            # Try to extract the InfoboxItem template
            self.logger.debug("Starting: extract_InfoboxItem")
            has_infobox_item = self.extract_InfoboxItem()
            if has_infobox_item:
                self.logger.debug("Item InfoBox extracted successfully")
            else:
                self.logger.critical("Item InfoBox extraction error.")
                print(">>>>>>>>>>>> CRITICAL: Item InfoBox extraction error")
                return # Could not finish, just exit
        else:
            self.logger.warning("Item has no OSRS Wikia page. Setting default values.")
            print(">>>>>>>>>>>> WARNING: No OSRS Wiki Page: %s" % self.name)
            return # Could not finish, just exit

        # Continue processing... but only if equipable
        if self.equipable:
            self.logger.debug("Item is equipable... Trying to fetch bonuses...")
            if has_wikia_page:
                self.logger.debug("Starting: extract_InfoBoxBonuses")
                has_infobox_bonuses = self.extract_InfoBoxBonuses()
                if has_infobox_bonuses:
                    self.logger.debug("Item InfoBox Bonuses extracted successfully")
                else:
                    self.logger.critical("Item InfoBox Bonuses extraction error.")
                    print(">>>>>>>>>>>> CRITICAL: Item InfoBox Bonuses extraction error")
                    return # Could not finish, just exit 
            else:
                self.logger.critical("Item is equipable, but has not OSRS Wikia page. Need to manually fix this item.")
                print(">>>>>>>>>>>> CRITICAL: Equipable item has no bonuses")
                return # Could not finish, just exit

        # Log the second JSON input
        self.logger.debug("Dumping second input...")
        self.logger.debug("Starting: print_pretty_debug_json")
        self.print_pretty_debug_json()

        self.logger.debug("============================================ END")

        # TODO: Move this check to another place, this is rediculous
        directory = "items-json"
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.export_pretty_json()

        # Finished. Return the entire ItemDefinition object
        return self

    def determine_wiki_page(self):
        # Log
        self.logger.debug("Searching for item in OSRS Wikia by name...")
        
        # Check if the item name is in the Wikia API Dump
        # Return True if found by self.name
        # Return False if not found
        if self.name in self.all_wikia_items:
            self.logger.debug(">>> ITEM FOUND:")
            self.logger.debug("  > name: %s" % self.name)
            self.logger.debug("  > id: %s" % self.id)
            self.url = "http://oldschoolrunescape.wikia.com/wiki/" + self.name
            return True
        else:
            self.logger.debug(">>> ITEM NOT FOUND: %s" % self.name)
            self.logger.debug(">>> ITEM NOT FOUND: %s" % self.id)
            return False

    def extract_InfoboxItem(self):
        wikicode = mwparserfromhell.parse(self.all_wikia_items[self.name])
        templates = wikicode.filter_templates()
        for template in templates:
            extracted_infobox = self.parse_InfoboxItem(template)
            if extracted_infobox:
                return True
            else:
                return False 
        return False

        # TODO: Add wikia URL               

    def strip_infobox(self, input):
        # Clean an passed InfoBox string
        input = str(input)
        # input = input.strip()
        # input = input.replace("[", "")
        # input = input.replace("]", "")
        return input

    def clean_weight(self, input):
        weight = None # Inventory weight
        input = str(input)
        # input = input.strip()
        # # Fix for weight ending in kg, or space kg
        # if input.endswith(" kg"):
        #     input = input.replace(" kg", "")
        # if input.endswith("kg"):
        #     input = input.replace("kg", "")
        # if "kg" in input:
        #     input = input.replace("kg", "")
        # # Some items have Inventory/Equipped weights:
        # # ValueError: could not convert string to float: "'''Inventory:''' 0.3{{kg}}<br> '''Equipped:''' -4.5"
        # if "Inventory" in input:
        #     input = input.replace("'''", "")
        #     input = input.replace("{", "")
        #     input = input.replace("}", "")
        #     weight_list = input.split("<br>")
        #     weight = weight_list[0]
        #     weight = weight.replace("Inventory:", "")
        #     weight = weight.strip()
        # else:
        #     weight = input

        return weight

    def clean_quest(self, input):
        quest = None
        quest = input
        # quest = quest.replace("'''", "")
        # quest = quest.replace("{", "")
        # quest = quest.replace("}", "")
        # quest = quest.replace("*", "")
        # if "&" in quest:
        #     quest = quest.replace("&", ",")
        # if "<br>" in quest:
        #     quest = quest.replace("<br> ", ",")
        #     quest = quest.replace("<br>", ",")
        # if "<br/>" in quest:
        #     quest = quest.replace("<br/> ", ",")
        #     quest = quest.replace("<br/>", ",")
        # if "II|II" in quest:
        #     quest = quest.replace("II|II", "II")

        # if quest.lower() == "no":
        #     return None
        # quest = quest.strip()
        # # Clean some spacing problems
        # quest = quest.replace(",,", ",")
        # quest = quest.replace(", ,", ",")
        # quest = quest.replace(" ,", ",")
        # quest = quest.replace(", ", ",")
        return quest

    def clean_release_date(self, input):
        release_date = None
        release_date = input
        # release_date = release_date.replace(" Update", "")
        # if release_date == "":
        #     return None
        # release_date = dateparser.parse(release_date)
        # # TODO: Should have a check here
        return release_date

    def clean_examine(self, input):
        examine_text = None
        examine_text = input
        # examine_text = examine_text.replace("'''", "")
        # examine_text = examine_text.replace("''", "")
        # examine_text = examine_text.replace("{", "")
        # examine_text = examine_text.replace("}", "")
        # examine_text = examine_text.replace("*", "")
        # examine_text = examine_text.replace("\n", ",")
        # if "<br>" in examine_text:
        #     examine_text = examine_text.replace("<br>", ",")        
        # if examine_text == "":
        #     return None
        # # TODO: Should handle a list, like weight
        # examine_text = examine_text.strip()
        return examine_text        

    def parse_InfoboxItem(self, template):
        self.logger.debug("Processing InfoBox template...")
        self.logger.debug(template)

        # Determine if item is associated with a quest
        try:
            quest = self.strip_infobox(template.get("quest").value)
            self.quest_item = self.clean_quest(quest)
        except ValueError:
            self.quest_item = None

        # Determine the weight of an item
        try:
            weight = self.strip_infobox(template.get("weight").value)
            self.weight = self.clean_weight(weight)
        except ValueError:
            self.weight = -1

        # Determine the release date of an item
        try:
            release_date = self.strip_infobox(template.get("release").value)
            self.release_date = self.clean_release_date(release_date)
        except ValueError:
            self.release_date = None

        # Determine the release date of an item
        try:
            examine = self.strip_infobox(template.get("examine").value)
            self.examine = self.clean_examine(examine)
        except ValueError:
            self.examine = None

        return True

        # Buy limit is not stored in infobox?!
        # if not self.tradeable:
        #     self.buy_limit = -1
        # else:
        #     self.buy_limit = 0

        # Used to have code to fetch store prive and seller information
        # try:
        #     store_price = self.strip_infobox(template.get("store").value)
        #     self.store_price = store_price      
        # except ValueError:
        #     self.store_price = -1
        # try:
        #     seller = self.strip_infobox(template.get("seller").value)
        #     self.seller = seller   
        # except ValueError:
        #     self.seller = ""

    def extract_InfoBoxBonuses(self):
        try:
            wikicode = mwparserfromhell.parse(self.all_wikia_items_bonuses[self.name])
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
              
    def parse_InfoboxBonuses(self, template):
        self.logger.debug("Processing InfoBox template...")
        self.logger.debug(template)
        itemBonuses = ItemBonuses.ItemBonuses(self.itemID)
        itemBonuses.attack_stab = self.strip_infobox(template.get("astab").value)
        itemBonuses.attack_slash = self.strip_infobox(template.get("aslash").value)
        itemBonuses.attack_crush = self.strip_infobox(template.get("acrush").value)
        itemBonuses.attack_magic = self.strip_infobox(template.get("amagic").value)
        itemBonuses.attack_ranged = self.strip_infobox(template.get("arange").value)
        itemBonuses.defence_stab = self.strip_infobox(template.get("dstab").value)
        itemBonuses.defence_slash = self.strip_infobox(template.get("dslash").value)
        itemBonuses.defence_crush  = self.strip_infobox(template.get("dcrush").value)
        itemBonuses.defence_magic = self.strip_infobox(template.get("dmagic").value)
        itemBonuses.defence_ranged = self.strip_infobox(template.get("drange").value)
        itemBonuses.melee_strength = self.strip_infobox(template.get("str").value)
        itemBonuses.ranged_strength = self.strip_infobox(template.get("rstr").value)
        itemBonuses.magic_damage = self.strip_infobox(template.get("mdmg").value)
        itemBonuses.prayer = self.strip_infobox(template.get("prayer").value)
        
        try:
            itemBonuses.slot  = self.strip_infobox(template.get("slot").value)
            itemBonuses.slot = itemBonuses.slot.lower()
        except ValueError:
            itemBonuses.slot = ""
            self.logger.critical("Could not determine equipable item slot")
            return False

        # If item is weapon, or 2h determine attack speed
        if itemBonuses.slot == "weapon" or itemBonuses.slot == "two-handed" or itemBonuses.slot == "2h":
            try:
                itemBonuses.attack_speed = self.strip_infobox(template.get("aspeed").value) 
            except ValueError:
                itemBonuses.attack_speed = -1
                return False  

        # Assign the correctly extracted item bonuses to the object
        self.itemBonuses = itemBonuses

        return True
          
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
        out_fi = "items-json" + os.sep + str(self.id) + ".json"
        with open(out_fi, "w") as f:
            json.dump(self.json_out, f, indent=4)

    def construct_json(self):
        self.json_out = collections.OrderedDict()
        self.json_out["id"] = self.id
        self.json_out["name"] = self.name
        self.json_out["members"] = self.members
        self.json_out["tradeable"] = self.tradeable
        self.json_out["stackable"] = self.stackable
        self.json_out["noted"] = self.noted
        self.json_out["noteable"] = self.noteable
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
            # Old code has item slot + weapon speed in main JSON body
            #self.json_out["item_slot"] = self.item_slot
            #if self.item_slot == "weapon" or self.item_slot == "two-handed":
            #    self.json_out["weapon_speed"] = self.weapon_speed
    
    # def edit_json(self):
    #     """ Construct JSON, print JSON, manually check and edit the contents. """
    #     self.print_pretty_json()
    #     answer = input("Would you like to change a field? [y, N]: ")
    #     if answer.lower() == "y":
    #         field = input("Name of field to change: ")
    #         if field == "bonuses":
    #             subfield = input("Name of sub-field to change: ")
    #             subvalue = input("Enter new value for %s: " % subfield)
    #             self.bonuses[subfield] = subvalue
    #             self.check_json()
    #         else:
    #             value = input("Enter new value for %s: " % field)
    #             setattr(self, field, value)
    #         self.check_json()

    # This should not be needed as everything is type/content checked
    # def check_json(self):
    #     """ Construct JSON, and auto check fields. """
    #     required_fields = ["id",
    #                        "name",
    #                        "tradeable",
    #                        "noteable",
    #                        "equipable",
    #                        "members",
    #                        "weight",
    #                        "buy_limit",
    #                        "quest_item",
    #                        "stackable",
    #                        "release_date", 
    #                        "cost",
    #                        "lowalch",
    #                        "highalch"]
    #                        #  Update this list
    #     for field in required_fields:
    #         if not hasattr(self, field):
    #             print("ERROR: Missing object attribute for: %s" % field)
    #     # This code needs to be more thorough and in ItemBonuses class
    #     # if self.equipable:
    #     #     if not self.bonuses:
    #     #         print("ERROR: Equipable object has no item bonuses")
    #     #         quit()

################################################################################
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
