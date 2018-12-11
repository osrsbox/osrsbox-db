# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/07

Description:
ItemDefinition is a class to process the raw ItemDefinition data from
RuneLite extraction then add supplementaty information gatered from the
OSRS Wiki. 

Warning: This code grew from simple to spaghetti! It is currently out of 
control and needs a rewrite and reorganization!

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

# These require pip install
import mwparserfromhell
import dateparser

# Import ItemBonuses and ItemEquipment class
sys.path.append(os.getcwd())
import ItemBonuses
import ItemEquipment

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
# ItemDefinition object
class ItemDefinition(object):
    def __init__(self, itemID, itemJSON, all_wikia_items, all_wikia_items_bonuses, all_wikia_buylimits, all_wikia_normalized_names, item_exists_in_db, item_skill_requirements):
        # Input itemID number
        self.itemID = itemID
        # Input JSON file (from RuneLite ItemScraper)
        self.itemJSON = itemJSON

        # Bulk dict of all OSRS Wikia Item infoboxes
        self.all_wikia_items = all_wikia_items
        # Bulk dict of all OSRS Wikia Item bonuses
        self.all_wikia_items_bonuses = all_wikia_items_bonuses
        # Bulk dict of all OSRS Wikia buylimits
        self.all_wikia_buylimits = all_wikia_buylimits 
        # Bulk dict of normalized OSRS Wikia names
        self.all_wikia_normalized_names = all_wikia_normalized_names
        # Bulk dict of all equipable items with requirements
        self.item_skill_requirements = item_skill_requirements

        # Flag to determine if item already exists in db
        self.item_exists_in_db = item_exists_in_db
        
        # Dict of all ItemDefinition properties
        # Not currently used, but kept for future
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

        # Item Equipment (if equipable, but initialize one anyway)   
        self.itemEquipment = ItemEquipment.ItemEquipment(self.itemID)        

        # Setup logging
        logging.basicConfig(filename="ItemDefinition.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # The name of the item on OSRS Wiki (can vary from actual name)
        self.wiki_name = None

        # If a page does not have a wiki page, it may be given a status number
        self.status_code = None

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
        self._quest_item = _listcast(value)

    @property
    def release_date(self):
        return self._release_date
    @release_date.setter
    def release_date(self, value):
        self._release_date = _datecast(value)	

    @property
    def seller(self):
        return self._seller
    @seller.setter
    def seller(self, value):
        self._seller = _listcast(value)

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
        sys.stdout.write(">>> Processing: %s\r" % self.itemID)

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

        # print(">>>>>>>>>>>>>> Processing: %s, %s" % (self.itemID, self.name))

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
            # This item has an OSRS Wikia page
            # Try to extract the InfoboxItem template
            self.logger.debug("Starting: extract_InfoboxItem")
            has_infobox_item = self.extract_InfoboxItem()
            if has_infobox_item:
                self.logger.debug("Item InfoBox extracted successfully")
            elif self.status_code == 1:
                self.logger.debug("Invalid item saved")
                if self.equipable:
                    self.make_blank_bonuses()
                    self.logger.warning("Blank bonuses made.")
            elif self.status_code == 2:
                self.logger.debug("Unobtainable item saved")
                if self.equipable:
                    self.make_blank_bonuses()
                    self.logger.warning("Blank bonuses made.")
            elif self.status_code == 3:
                self.logger.debug("Unusable item saved")  
                if self.equipable:
                    self.make_blank_bonuses()
                    self.logger.warning("Blank bonuses made.")
            elif self.status_code == 4:
                self.logger.debug("Not really an item, item saved")   
                if self.equipable:
                    self.make_blank_bonuses()
                    self.logger.warning("Blank bonuses made.")
            elif self.status_code == 5:
                self.logger.debug("No dedicated wiki page for item, saved")  
                if self.equipable:
                    self.make_blank_bonuses()
                    self.logger.warning("Blank bonuses made.")
            else:
                self.logger.critical("Item InfoBox extraction error.")
                return # Could not finish, just exit
                # print("Item InfoBox extraction error.")
                # quit()
        else:
            self.logger.critical("Item has no OSRS Wikia page. Setting default values.")
            return # Could not finish, just exit
            # print("Item has no OSRS Wikia page. Setting default values.")
            # quit()

        # Continue processing... but only if equipable
        if self.equipable:
            self.logger.debug("Item is equipable... Trying to fetch bonuses...")
            if has_wikia_page:
                self.logger.debug("Starting: extract_InfoBoxBonuses")
                has_infobox_bonuses = self.extract_InfoBoxBonuses()
                if has_infobox_bonuses:
                    self.logger.debug("Item InfoBox Bonuses extracted successfully")
                elif self.status_code in [1,2,3,4,5,6]:
                    self.make_blank_bonuses()
                    self.logger.warning("Blank bonuses made.")
                else:
                    self.logger.critical("Item InfoBox Bonuses extraction error.")
                    self.logger.critical("Status Code: %s" % self.status_code)
                    self.make_blank_bonuses()
                    return # Could not finish, just exit 
            else:
                self.logger.critical("Item is equipable, but has not OSRS Wikia page. Need to manually fix this item.")
                return # Could not finish, just exit
                # print("Item is equipable, but has not OSRS Wikia page. Need to manually fix this item.")
                # quit()

        # Fix self.url and check
        self.url = self.url.replace(" ", "_")
        self.url = self.url.replace("'", "%27")
        self.url = self.url.replace("&", "%26")
        self.url = self.url.replace("+", "%2B")

        # Dirty hack
        if self.url:
            if self.url == "https://oldschool.runescape.wiki/w/":
                self.url = None
            if self.url == "https://oldschool.runescape.wiki/w/None":
                self.url = None

        # Log the second JSON input
        self.logger.debug("Dumping second input...")
        self.logger.debug("Starting: print_pretty_debug_json")
        self.print_pretty_debug_json()

        self.logger.debug("============================================ END")

        # Check if item already exists in db
        # changed = False
        # if self.item_exists_in_db:
        #     changed = self.compare_JSON_files()
        # if changed:
        #     print("CHANGED")

        # Actually output a JSON file, comment out for testing
        self.export_pretty_json()

        # Finished. Return the entire ItemDefinition object
        return self

    def determine_wiki_page(self):
        wiki_name = self.name.replace("&", "%26")
        wiki_name = wiki_name.replace("+", "%2B")  
        self.logger.debug("Searching for item in OSRS Wikia by name...")
        
        # Check if the item name is in the Wikia API Dump
        # Return True if found by self.name
        # Return False if not found
        if wiki_name in self.all_wikia_items:
            self.logger.debug(">>> ITEM FOUND:")
            self.logger.debug("  > name: %s" % self.name)
            self.logger.debug("  > id: %s" % self.id)
            self.url = "https://oldschool.runescape.wiki/w/" + self.name
            self.wiki_name = self.name
            return True
        elif str(self.id) in self.all_wikia_normalized_names:
            self.logger.debug(">>> ITEM FOUND IN NORMALIZED:")
            self.logger.debug("  > name: %s" % self.name)
            self.logger.debug("  > id: %s" % self.id)
            wikia_normalized_name = self.all_wikia_normalized_names[str(self.id)][1]
            self.url = "https://oldschool.runescape.wiki/w/" + wikia_normalized_name             
            self.wiki_name = wikia_normalized_name
            self.status_code = int(self.all_wikia_normalized_names[str(self.id)][2])
            return True    
        else:
            self.logger.debug(">>> ITEM NOT FOUND: %s" % self.name)
            self.logger.debug(">>> ITEM NOT FOUND: %s" % self.id)
            return False

    def extract_InfoboxItem(self):
        # Quick fix for url encoded names
        self.wiki_name = self.wiki_name.replace("&", "%26")
        self.wiki_name = self.wiki_name.replace("+", "%2B")   
        self.logger.debug(">>> wiki_name: %s" % self.wiki_name)
        try:
            wikicode = mwparserfromhell.parse(self.all_wikia_items[self.wiki_name])
        except KeyError:
            return False

        # Loop through templates in wikicode from wiki page
        # Then call Inforbox Item processing method
        templates = wikicode.filter_templates()
        for template in templates:
            extracted_infobox = self.parse_InfoboxItem(template)
            
            # Return true/false if the infobox is extractable
            if extracted_infobox:
                return True
            else:
                return False 

        # Default to return false (no infobox found)
        return False        

    def strip_infobox(self, input):
        # Clean an passed InfoBox string
        clean_input = str(input)
        clean_input = clean_input.strip()
        clean_input = clean_input.replace("[", "")
        clean_input = clean_input.replace("]", "")
        return clean_input

    def clean_quest(self, input):
        # Clean a quest value
        quest = None
        quest = input
        quest = quest.strip()

        quest = quest.replace("Growing Pains]] [[Fairy Tale II", "Growing Pains]] <br> [[Fairy Tale II")
        quest = quest.replace("[", "")
        quest = quest.replace("]", "")
        quest = quest.replace("{", "")
        quest = quest.replace("}", "")
        quest = quest.replace("*", "")
        quest = quest.replace("II|II", "II")
        quest = quest.replace("Tears of Guthix (quest)|", "")
        quest = quest.replace("(quest)", "")
        quest = quest.replace("(miniquest)", "")
        quest = quest.replace("miniquest", "")
        quest = quest.replace("Miniquest", "")
        quest = quest.replace("various", "Various")
        
        quest = quest.strip()
        
        # Generic test for not a quest item
        if quest.lower() == "no":
            return None
        if quest.lower() == "yes":
            # This returns none, as the db wants a quest name
            return None

        quest_list = list()
        # Start trying to split quests
        if ", <br>" in quest:
            quest_list = quest.split(", <br>")            
        elif ",<br>" in quest:
            quest_list = quest.split(",<br>")
        elif ",<br/>" in quest:
            quest_list = quest.split(",<br/>") 
        elif ", <br/>" in quest:
            quest_list = quest.split(", <br/>")             
        elif ",<br />" in quest:
            quest_list = quest.split(",<br />")    
        elif ", <br />" in quest:
            quest_list = quest.split(", <br />")       
        elif "<br>" in quest:
            quest_list = quest.split("<br>")
        elif "<br >" in quest:
            quest_list = quest.split("<br >")
        elif "<br/>" in quest:
            quest_list = quest.split("<br/>")
        elif "<br />" in quest:
            quest_list = quest.split("<br />")
        elif "&" in quest:
            quest_list = quest.split("&")            
        elif "\n" in quest:
            quest_list = quest.split("\n")
        if "," in quest:
            quest_list = quest.split(",")
        
        # Start creating the final list to return
        quest_list_fin = list()
        if quest_list:
            for quest_name in quest_list:
                quest_name = quest_name.strip()
                quest_name = quest_name.replace("<br>", "")
                quest_name = quest_name.replace("<br/>", "")
                quest_list_fin.append(quest_name)
        else:
            quest_list_fin.append(quest)

        return quest_list_fin

    def clean_weight(self, input):
        # Clean a weight value
        weight = None
        weight = str(input)
        weight = weight.strip()

        weight = weight.replace("[", "")
        weight = weight.replace("]", "")
        
        # Fix for weight ending in kg, or space kg
        if weight.endswith(" kg"):
            weight = weight.replace(" kg", "")
        if weight.endswith("kg"):
            weight = weight.replace("kg", "")
        if "kg" in weight:
            weight = weight.replace("kg", "")

        # Some items have Inventory/Equipped weights:
        # ValueError: could not convert string to float: "'''Inventory:''' 0.3{{kg}}<br> '''Equipped:''' -4.5"
        if "Inventory" in weight:
            weight = weight.replace("'''", "")
            weight = weight.replace("{", "")
            weight = weight.replace("}", "")
            weight_list = weight.split("<br>")
            weight = weight_list[0]
            weight = weight.replace("Inventory:", "")
            weight = weight.strip()

        if ">" in weight:
            weight = weight.replace(">", "")
        if "<" in weight:
            weight = weight.replace("<", "")

        if weight == "": # New addition
            weight = 0

        return weight

    def clean_release_date(self, input):
        # Clean a release date value
        release_date = None
        release_date = input
        release_date = release_date.strip()
        release_date = release_date.replace("[", "")
        release_date = release_date.replace("]", "")        
        return release_date

    def clean_examine(self, input):
        # Clean an examine text value
        examine = None
        examine = input
        examine = examine.strip()
        examine = examine.replace("'''", "")
        examine = examine.replace("''", "")
        examine = examine.replace("{", "")
        examine = examine.replace("}", "")
        examine = examine.replace("[", "")
        examine = examine.replace("]", "")  
        examine = examine.replace("*", "")
        examine = examine.replace("<nowiki>", "")     
        examine = examine.replace("</nowiki>", "")     
        examine = examine.replace("sic", "")
        examine = examine.replace("à", "") # TODO: Not working, only one item affected
        examine = examine.replace("(empty)", "Empty:")    
        examine = examine.replace("(full)", "Full:")      
        examine = examine.replace("(Player's Name)", "<players-name>") 
        examine = examine.replace("<number of cabbages>", "x") 
        examine = examine.replace("2!", "") 
        examine = examine.replace("In POH", "POH") 
        
        # Examine text fixes for some quest items
        examine = examine.replace("(Used in the Shield of Arrav quest)", "")
        examine = examine.replace("(Used in The Grand Tree quest)", "")
        examine = examine.replace("(Edgeville Dungeon entrance)", "")
        examine = examine.replace("(Used to open the muddy chest in the lava maze)", "")
        examine = examine.replace("(Used to open the sinister chest in Yanille dungeon)", "")
        examine = examine.replace("(Used in the Dragon Slayer quest)", "")
        examine = examine.replace("(Used in Heroes' Quest)", "")
        examine = examine.replace("(Provides access to the deeper parts of Taverley Dungeon)", "")
        examine = examine.replace("(Provides access to the Desert Mining Camp)", "")
        examine = examine.replace("(Unlocks the cell door in the Desert Mining Camp)", "")
        examine = examine.replace("(Access to the Desert Mining Camp's mine)", "")
        examine = examine.replace("(Used in the Tourist Trap quest)", "")
        examine = examine.replace("(Used in the Watchtower quest)", "")   
        examine = examine.replace("(Used in the Zogre Flesh Eaters quest)", "")
        examine = examine.replace("(Used in the Creature of Fenkenstrain quest)", "")
        examine = examine.replace("(Opens chests found in the Mort'ton catacombs)", "")
        examine = examine.replace("(Used in the Fremennik Trials quest)", "")
        examine = examine.replace("(Allows access to the Crystal mine from the Haunted mine quest)", "")
        examine = examine.replace("(Used in the Horror from the Deep quest)", "")
        examine = examine.replace("(Used in the Darkness of Hallowvale quest)", "")
        examine = examine.replace("(Used in the Priest in Peril quest)", "")
        examine = examine.replace("(Allows access to the Water Ravine Dungeon from the Spirits of the Elid quest)", "")
        examine = examine.replace("(Used to enter the cavern near the Temple of Light)", "")
        examine = examine.replace("(Opens the locked coffins in the cave at Jiggig)", "")
        examine = examine.replace("(Used to open a chest upstairs in Slepe church)", "")
        examine = examine.replace("(Unlocks the gate to the roof of the Slayer Tower)", "")
        examine = examine.replace("(Used in the Misthalin Mystery quest)", "")
        examine = examine.replace("(Allows access to the goblin kitchen in the Observatory Dungeon)", "")
        examine = examine.replace("(Used to access the prison cell inside of the Mourner HQ)", "")
        examine = examine.replace("(Provides access to the elemental workshop)", "")
        examine = examine.replace("(Provides access to the Black Knights jail cell in Taverley Dungeon)", "")
        examine = examine.replace("(Used in the In Aid of the Myreque quest)", "")
        examine = examine.replace("(Used in the Troll Stronghold quest)", "")
        examine = examine.replace("(Used in the Smoke Dungeon in Desert Treasure)", "")
        examine = examine.replace("(Quick access into the Temple of Ikov)", "")
        examine = examine.replace("(Used to access the prison cell inside of the Mourner HQ)", "")
        examine = examine.replace("(Used in The Golem quest)", "")
        examine = examine.replace("(Used in the Smoke Dungeon in Desert Treasure)", "")
        examine = examine.replace("(Allows access to the Crystal mine from the Haunted mine quest)", "")
        examine = examine.replace("(Used in the Eadgar's Ruse quest)", "")
        examine = examine.replace("(Used in the Troll Stronghold quest)", "")
        examine = examine.replace("(Used in the Plague City quest)", "")
        examine = examine.replace("(used to access the Hill Titan's lair)", "")
        examine = examine.replace("(Used in the Ernest the Chicken quest)", "")
        examine = examine.replace("(Unlocks a door found in the Waterfall Dungeon)", "")
        examine = examine.replace("(Opens the cell found in the Gnome Village Dungeon)", "")
        examine = examine.replace("(Used in the Biohazard quest)", "")
        examine = examine.replace("(Used in the Pirate's Treasure quest)", "")
        examine = examine.replace("(Provides access to Rashiliyia's Tomb)", "")
        examine = examine.replace("(Used in The Digsite quest)", "")
        examine = examine.replace("(Used in the Demon Slayer quest)", "")
        examine = examine.replace("(Used in the Hazeel Cult quest)", "")
        examine = examine.replace("(Used in the Witch's House quest)", "")
        examine = examine.replace("(Used in the Prince Ali Rescue quest)", "")
        examine = examine.replace("(Used in The Lost Tribe quest)", "")
        examine = examine.replace("(Used in the Recruitment Drive quest)", "")
        examine = examine.replace("(Used to open a chest deep in the HAM cave)", "")
        examine = examine.replace("(Used to open the hatch in the elemental workshop)", "")
        examine = examine.replace("(Used in Olaf's Quest)", "")
        examine = examine.replace("(Used in the Ghost Ahoy quest)", "")

        # # Specific fix for clue scroll items
        # examine_list = list()
        # if self.name == "Clue scroll (hard)":
        #     examine = examine.replace("\n", "")
        #     examine = examine.replace("(Player's Name)", "<players-name>")
        #     examine_list = re.split("<br/>|<br />", examine)         
        #     examine_list = [a+b for a, b in zip(examine_list[::2],examine_list[1::2])]
        # if self.name == "Clue scroll (elite)":
        #     examine_list.append(examine.split("\n")[0])
        #     examine_list.append("Sherlock: A clue suggested by <players-name>! ")

        # # Start splitting multiple examine texts to a list
        # elif ", <br>" in examine:
        #     examine_list = examine.split(", <br>")    
        # elif "<br>\n" in examine:
        #     examine_list = examine.split("<br>\n")
        # elif "<br />\n" in examine:
        #     examine_list = examine.split("<br />\n")                     
        # elif ",<br>" in examine:
        #     examine_list = examine.split(",<br>")
        # elif ",<br/>" in examine:
        #     examine_list = examine.split(",<br/>") 
        # elif ", <br/>" in examine:
        #     examine_list = examine.split(", <br/>")             
        # elif ",<br />" in examine:
        #     examine_list = examine.split(",<br />")    
        # elif ", <br />" in examine:
        #     examine_list = examine.split(", <br />")       
        # elif "<br>" in examine:
        #     examine_list = examine.split("<br>")
        # elif "<br >" in examine:
        #     examine_list = examine.split("<br >")
        # elif "<br/>" in examine:
        #     examine_list = examine.split("<br/>")
        # elif "<br />" in examine:
        #     examine_list = examine.split("<br />")
        # elif "\n" in examine:
        #     examine_list = examine.split("\n")                

        # # Quick and dirty fix for two different items
        # if self.name == "Key (medium)":
        #     examine_list = ["Inventory: This kitten seems to like you", "A key to some drawers.", "A key to unlock a treasure chest."]
        # if self.wiki_name == "Cat":
        #     examine_list = ["Inventory (Kitten): This kitten seems to like you.", "Inventory (Cat): This cat definitely likes you.", "Inventory (Overgrown): This cat is so well fed it can hardly move.", "Follower (Kitten): A friendly little pet.", "Follower (Cat): A fully grown feline.", "Follower (Overgrown): A friendly, not-so-little pet."]

        # # Start making a final list
        # examine_list_fin = list()
        # if examine_list:
        #     for examine_name in examine_list:
        #         examine_name = examine_name.strip()
        #         if "(Whole)" in examine_name:
        #             examine_name = examine_name.replace("(Whole)", "")
        #             examine_name = "Whole: " + examine_name
        #         if "(Half)" in examine_name:
        #             examine_name = examine_name.replace("(Half)", "")
        #             examine_name = "Half: " + examine_name
        #         if "(uncharged)" in examine_name:
        #             examine_name = examine_name.replace("(uncharged)", "")
        #             examine_name = "Uncharged: " + examine_name
        #         if "(charged)" in examine_name:
        #             examine_name = examine_name.replace("(charged)", "")
        #             examine_name = "Charged: " + examine_name
        #         if examine_name == "":
        #             continue              
        #         examine_list_fin.append(examine_name)
        # else:
        #     examine_list_fin.append(examine.strip())

        # Special cirumstances for clue scrolls:
        if self.name == "Clue scroll (easy)":
            examine = "A set of instructions to be followed.; A clue!; A piece of the world map, but where?; It points to great treasure!"
        if self.name == "Clue scroll (medium)":
            examine = "A set of instructions to be followed; A clue!; A piece of the world map,but where?; Perhaps someone at the observatory can teach me to navigate?; It points to great treasure!"
        if self.name == "Clue scroll (hard)":
            examine = "Emote: A set of instructions to be followed.; Anagram: A clue!, Map: A place of the world map, but where?; Coordinates: Perhaps someone at the observatory can teach me to navigate?; Fairy ring: A clue suggested by <players-name>!"
        if self.name == "Clue scroll (elite)":
            examine = "A clue!; Sherlock: A clue suggested by <players-name>!"

        return examine  

    def clean_store_price(self, input):
        # Clean a store price value
        store_price = None
        store_price = input
        store_price = store_price.strip()
        if store_price == "":
            return None
        return store_price

    def clean_seller(self, input):
        # Clean seller value
        seller = None
        seller = input
        seller = seller.strip()
        if seller == "" or seller.lower() == "no" or seller == None:
            return None

        seller = seller.replace("l/c", "")
        seller = seller.replace("l/o", "")
        seller = seller.replace("{", "")
        seller = seller.replace("}", "")
        seller = seller.replace("[", "")
        seller = seller.replace("]", "")
        
        seller = seller.replace(" - Mystic Robes", "")
        seller = seller.replace("41,600", "")   

        seller_list = list()
        if "!" in seller:
            seller_list.append(seller.split("!")[0])
        elif " and " in seller:
            seller_list = seller.split(" and ")
        elif " or " in seller:
            seller_list = seller.split(" or ")            

        seller_list_fin = list()
        if seller_list:
            for seller_name in seller_list:
                seller_name = seller_name.strip()
                seller_list_fin.append(seller_name)
        else:
            seller_list_fin.append(seller)

        return seller_list_fin               

    def extract_Infobox_value(self, template, key):
        value = None
        try:
            value = template.get(key).value
            return value
        except ValueError:
            return value

    def parse_InfoboxItem(self, template):
        # Parse an actual Infobox Item template
        self.logger.debug("Processing InfoBox template...")
        # self.logger.debug(template)
        # print("++++++++++++++++++++++", self.name)

        # Set defaults for versioned infoboxes
        self.is_versioned = False
        self.version_count = 0

        # Check if the infobox is versioned
        try:
            template.get("version1").value
            self.is_versioned = True
            # Now, try to determine how many versions are present
            i = 1
            while i <= 12: # Guessing max verison number is 12 (crystal bow)
                version_number = "version" + str(i) # e.g., version1, version2
                try:
                    template.get(version_number).value
                    self.version_count += 1
                except ValueError:
                    break
                i += 1
        except ValueError:
            pass

        # Output:
        # is_versioned = has multiple versions available
        # version_count = the number of versions available

        self.current_version = None

        if self.is_versioned:
            #print(self.name, self.is_versioned, self.version_count)
            try:
                template.get("name1").value
                i = 1
                while i <= self.version_count:
                    name_name = "name" + str(i)
                    if self.name == template.get(name_name).value.strip():
                        self.current_version = i
                    i += 1
            except ValueError:
                pass
            if self.current_version == None:
                self.current_version = 1
            self.logger.debug("NOTE: versioned infobox: %s" % self.current_version)

        # Determine if item is associated with a quest (TESTED)
        quest = None
        if self.current_version is not None:
            key = "quest" + str(self.current_version)
            quest = self.extract_Infobox_value(template, key)
        if quest is None:
            quest = self.extract_Infobox_value(template, "quest")
        if quest is not None:
            self.quest_item = self.clean_quest(quest)

        # try:
        #     quest = template.get("quest").value
        #     self.quest_item = self.clean_quest(quest)
        #     # if self.quest_item is not None:
        #     #     print(self.id, self.name)
        #     #     print(quest)
        #     #     print(self.quest_item)
        #     #     print("==================================")
        # except ValueError:
        #     self.quest_item = None

        # Determine the weight of an item (TESTED)
        weight = None
        if self.current_version is not None:
            key = "weight" + str(self.current_version)
            weight = self.extract_Infobox_value(template, key)
        if weight is None:
            weight = self.extract_Infobox_value(template, "weight")
        if weight is not None:
            self.weight = self.clean_weight(weight)

        # try:
        #     weight = template.get("weight").value
        #     self.weight = self.clean_weight(weight)
        #     # if self.weight is not None:
        #     #     print(self.id, self.name)
        #     #     print(weight)
        #     #     print(self.weight)
        #     #     print("==================================")            
        # except ValueError:
        #     self.weight = None

        # Determine the release date of an item (TESTED)
        release_date = None
        if self.current_version is not None:
            key = "release" + str(self.current_version)
            release_date = self.extract_Infobox_value(template, key)
        if release_date is None:
            release_date = self.extract_Infobox_value(template, "release")
        if release_date is not None:
            self.release_date = self.clean_release_date(release_date)

        # try:
        #     release_date = template.get("release").value
        #     self.release_date = self.clean_release_date(release_date)
        #     # if self.release_date is not None:
        #     #     print(self.id, self.name)
        #     #     print(release_date)
        #     #     print(self.release_date)
        #     #     print("==================================")             
        # except ValueError:
        #     self.release_date = None

        # Determine if item has a store price (TESTED)
        store_price = None
        if self.current_version is not None:
            key = "store" + str(self.current_version)
            store_price = self.extract_Infobox_value(template, key)
        if store_price is None:
            store_price = self.extract_Infobox_value(template, "store")
        if store_price is not None:
            self.store_price = self.clean_store_price(store_price)
        else:
            self.store_price = None            

        # try:
        #     store_price = template.get("store").value
        #     self.store_price = self.clean_store_price(store_price) 
        #     # if self.store_price is not None:
        #     #     print(self.id, self.name)
        #     #     print(store_price)
        #     #     print(self.store_price)
        #     #     print("==================================")                 
        # except ValueError:
        #     self.store_price = None
        
        # Determine if item has a store price (TESTED)
        seller = None
        if self.current_version is not None:
            key = "seller" + str(self.current_version)
            seller = self.extract_Infobox_value(template, key)
        if seller is None:
            seller = self.extract_Infobox_value(template, "seller")
        if seller is not None:
            self.seller = self.clean_seller(seller)
        else:
            self.seller = None

        # try:
        #     seller = template.get("seller").value
        #     self.seller = self.clean_seller(seller) 
        #     # if self.seller is not None:
        #     #     print(self.id, self.name)
        #     #     print(seller)
        #     #     print(self.seller)
        #     #     print("==================================")                 
        # except ValueError:
        #     self.seller = None

        # Determine the examine text of an item (TESTED)
        examine = None
        if self.current_version is not None:
            key = "examine" + str(self.current_version)
            examine = self.extract_Infobox_value(template, key)
        if examine is None:
            examine = self.extract_Infobox_value(template, "examine")
        if examine is not None:
            self.examine = self.clean_examine(examine)

        # try:
        #     examine = template.get("examine").value
        #     self.examine = self.clean_examine(examine)
        #     # if self.examine is not None:
        #     #     print(self.id, self.name)
        #     #     print(examine)
        #     #     print(self.examine)
        #     #     print(self.id, "||".join(self.examine))
        #     #     print("==================================")
        # except ValueError:
        #     self.examine = None            

        # Determine if item has a buy limit (TESTED)
        if not self.tradeable:
            self.buy_limit = None
        else:
            try:
                self.buy_limit = self.all_wikia_buylimits[self.name]
            except KeyError:
                self.buy_limit = None

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
        if self.current_version is not None:
            key = prop + str(self.current_version)
            value = self.extract_Infobox_value(template, key)
        if value is None:
            value = self.extract_Infobox_value(template, prop)
        if value is not None:
            #itemBonuses.attack_stab = self.strip_infobox(value)
            return self.strip_infobox(value)

    def parse_InfoboxBonuses(self, template):
        # Parse the Infobox Bonuses template
        self.logger.debug("Processing InfoBox template...")
        # self.logger.debug(template)
        itemBonuses = ItemBonuses.ItemBonuses(self.itemID)

        itemBonuses.attack_stab = self.clean_InfoboxBonuses_value(template, "astab")
        itemBonuses.attack_slash = self.clean_InfoboxBonuses_value(template, "aslash")
        itemBonuses.attack_crush = self.clean_InfoboxBonuses_value(template, "acrush")
        itemBonuses.attack_magic = self.clean_InfoboxBonuses_value(template, "amagic")
        itemBonuses.attack_ranged = self.clean_InfoboxBonuses_value(template, "arange")
        itemBonuses.defence_stab = self.clean_InfoboxBonuses_value(template, "dstab")
        itemBonuses.defence_slash = self.clean_InfoboxBonuses_value(template, "dslash")
        itemBonuses.defence_crush = self.clean_InfoboxBonuses_value(template, "dcrush")
        itemBonuses.defence_magic = self.clean_InfoboxBonuses_value(template, "dmagic")
        itemBonuses.defence_ranged = self.clean_InfoboxBonuses_value(template, "drange")
        itemBonuses.melee_strength = self.clean_InfoboxBonuses_value(template, "str")
        itemBonuses.ranged_strength = self.clean_InfoboxBonuses_value(template, "rstr")
        itemBonuses.magic_damage = self.clean_InfoboxBonuses_value(template, "mdmg")
        itemBonuses.prayer = self.clean_InfoboxBonuses_value(template, "prayer")

        # Assign the correctly extracted item bonuses to the object
        self.itemBonuses = itemBonuses

        # Old, un-versioned code
        # itemBonuses.attack_slash = self.strip_infobox(template.get("aslash").value)
        # itemBonuses.attack_crush = self.strip_infobox(template.get("acrush").value)
        # itemBonuses.attack_magic = self.strip_infobox(template.get("amagic").value)
        # itemBonuses.attack_ranged = self.strip_infobox(template.get("arange").value)
        # itemBonuses.defence_stab = self.strip_infobox(template.get("dstab").value)
        # itemBonuses.defence_slash = self.strip_infobox(template.get("dslash").value)
        # itemBonuses.defence_crush  = self.strip_infobox(template.get("dcrush").value)
        # itemBonuses.defence_magic = self.strip_infobox(template.get("dmagic").value)
        # itemBonuses.defence_ranged = self.strip_infobox(template.get("drange").value)
        # itemBonuses.melee_strength = self.strip_infobox(template.get("str").value)
        # itemBonuses.ranged_strength = self.strip_infobox(template.get("rstr").value)
        # itemBonuses.magic_damage = self.strip_infobox(template.get("mdmg").value)
        # itemBonuses.prayer = self.strip_infobox(template.get("prayer").value)
        
        # Item Equipment
        itemEquipment = ItemEquipment.ItemEquipment(self.itemID)

        try:
            itemEquipment.slot  = self.strip_infobox(template.get("slot").value)
            itemEquipment.slot = itemEquipment.slot.lower()
        except ValueError:
            itemEquipment.slot = None
            self.logger.critical("Could not determine equipable item slot")
            return False

        # If item is weapon, two-handed, or 2h determine attack speed
        if itemEquipment.slot == "weapon" or itemEquipment.slot == "two-handed" or itemEquipment.slot == "2h":
            try:
                itemEquipment.attack_speed = self.strip_infobox(template.get("aspeed").value) 
            except ValueError:
                itemEquipment.attack_speed = None
                self.logger.critical("Could not determine equipable item attack speed")
                return False
        if itemEquipment.attack_speed == 0:
            itemEquipment.attack_speed = None

        # Fetch item skill requirements
        try:
            skill_reqs = self.item_skill_requirements[str(self.id)]
            itemEquipment.skill_reqs = skill_reqs
        except KeyError:
            itemEquipment.skill_reqs = None

        # Assign the correctly extracted item equipment to the object
        self.itemEquipment = itemEquipment

        return True

    def make_blank_bonuses(self):
        # Parse the Infobox Bonuses template
        self.logger.debug("Making a default bonuses object...")
        # self.logger.debug(template)
        itemBonuses = ItemBonuses.ItemBonuses(self.itemID)
        itemBonuses.attack_stab = 0
        itemBonuses.attack_slash = 0
        itemBonuses.attack_crush = 0
        itemBonuses.attack_magic = 0
        itemBonuses.attack_ranged = 0
        itemBonuses.defence_stab = 0
        itemBonuses.defence_slash = 0
        itemBonuses.defence_crush  = 0
        itemBonuses.defence_magic = 0
        itemBonuses.defence_ranged = 0
        itemBonuses.melee_strength = 0
        itemBonuses.ranged_strength = 0
        itemBonuses.magic_damage = 0
        itemBonuses.prayer = 0
        # Assign the correctly extracted item bonuses to the object
        self.itemBonuses = itemBonuses

        itemEquipment = ItemEquipment.ItemEquipment(self.itemID)
        itemEquipment.slot = None
        itemEquipment.attack_speed = 0
        itemEquipment.skill_reqs = None
        self.itemEquipment = itemEquipment

        return True        
          
    ###########################################################################
    # Handle item to JSON
    def print_json(self):
        # Print JSON to console
        self.construct_json()
        json_obj = json.dumps(self.json_out)
        #print(json_obj)

    def print_pretty_json(self):
        # Pretty print JSON to console
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=4)
        #print(json_obj)

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
            equipment_in_json = self.itemEquipment.construct_json()
            self.json_out["equipment"] = equipment_in_json            

###########################################################################
# Compare new JSON to existing JSON
    def compare_JSON_files(self):
        # Create JSON out object to compare:
        self.construct_json()

        # Load existing db entry
        fi_name = ".." + os.sep + "docs" + os.sep + "items-json" + os.sep + self.itemID + ".json"
        with open(fi_name) as f:
            existing_json_fi = json.load(f)
        
        ### Compare
        # First loop checks, second loop prints
        changed = False
        for prop in self.properties:
            if self.json_out[prop] != existing_json_fi[prop]:
                changed = True
                break
                if self.equipable:
                    for prop in self.itemBonuses.properties:
                        if self.json_out["bonuses"][prop] != existing_json_fi["bonuses"][prop]:
                            changed = True
                            break
                    for prop in self.itemEquipment.properties:
                        if self.json_out["equipment"][prop] != existing_json_fi["equipment"][prop]:
                            changed = True
                            break                            

        if changed:
            print("+++++++++++++++++++++++++", self.itemID, self.name)
            for prop in self.properties:
                if self.json_out[prop] != existing_json_fi[prop]:
                    print("+++ MISMATCH!:", prop)
                    print("NEW:", type(self.json_out[prop]), self.json_out[prop])
                    print("OLD:", type(existing_json_fi[prop]), existing_json_fi[prop])
            if self.equipable:
                for prop in self.itemBonuses.properties:
                    if self.json_out["bonuses"][prop] != existing_json_fi["bonuses"][prop]:
                        print("+++ BONUSES MISMATCH!:", prop)
                        print("NEW:", type(self.json_out["bonuses"][prop]), self.json_out["bonuses"][prop])
                        print("OLD:", type(existing_json_fi["bonuses"][prop]), existing_json_fi["bonuses"][prop])   
                    if self.json_out["equipment"][prop] != existing_json_fi["equipment"][prop]:
                        print("+++ equipment MISMATCH!:", prop)
                        print("NEW:", type(self.json_out["equipment"][prop]), self.json_out["equipment"][prop])
                        print("OLD:", type(existing_json_fi["equipment"][prop]), existing_json_fi["equipment"][prop])   


        return changed                 

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
