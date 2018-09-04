# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2017/11/28

Description:
ItemDefinition is a class to process the raw ItemDefinition data parsed
and exported by the Runelite Cache tool. The JSON files exported by the
Runelite Cache tool are individually processed by this class and the useful
information extracted and populated into a Python object. Since the JSON 
files have limited information, additional metadata is sourced from website
databases such as OSRS Wikia and 2007RSHelp to include item bonuses and
the weight of the item. All input and output is type checked to ensure 
correct values are set (using Python properties) and various helper methods
provided. 
Copyright (c) 2017, PH01L

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
import datetime
import collections

sys.path.append(os.getcwd())
import ScrapeItemFromWikia

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
    elif val in ["True", "true", True]:
        return True
    elif val in ["False", "false", False]:
        return False   
        
###############################################################################
# ItemDefinition object
class ItemDefinition(object):
    def __init__(self, json_file):
	    self.json_data = json.load(open(json_file))
		       
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = _intcast(value)		

    @property
    def noteable(self):
        return self._noteable
    @noteable.setter
    def noteable(self, value):
        self._noteable = _boolcast(value)		 

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
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = _strcast(value)	
		
    @property
    def tradeable(self):
        return self._tradeable
    @tradeable.setter
    def tradeable(self, value):
        self._tradeable = _boolcast(value)

    @property
    def equipable(self):
        return self._equipable
    @equipable.setter
    def equipable(self, value):
        self._equipable = _boolcast(value)	           

    @property
    def members(self):
        return self._members
    @members.setter
    def members(self, value):
        self._members = _boolcast(value)
        
    @property
    def buy_limit(self):
        return self._buy_limit
    @buy_limit.setter
    def buy_limit(self, value):
        self._buy_limit = _intcast(value)
        
    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, value):
        self._weight = _floatcast(value)
        
    @property
    def quest_item(self):
        return self._quest_item
    @quest_item.setter
    def quest_item(self, value):
        self._quest_item = _boolcast(value)
        
    @property
    def stackable(self):
        return self._stackable
    @stackable.setter
    def stackable(self, value):
        self._stackable = _boolcast(value)        
        
    @property
    def release_date(self):
        return self._release_date
    @release_date.setter
    def release_date(self, value):
        self._release_date = _strcast(value)	         
        
    def parse_all_from_runelite(self, fi):
        # The first argument must be the ItemID.java file from Runelite tool 
        self.all_items = collections.OrderedDict()
        self.total_item_count = 0
        with open(fi) as f:
            for line in f:
                line = line.strip()
                if line.startswith("public static final int"):
                    self.total_item_count += 1
                    line = line.replace("public static final int ", "")
                    line = line.replace(";", "")
                    # Check line.split("_") len -1 is a number
                    # Check last char is a number
                    line = line.replace("_", " ")
                    print(line)
                    name, id = line.split(" = ")
                    name = name.capitalize()
                    # Some names end with a number, which is a duplicate name
    
    def construct_from_runelite(self):
        print(">>> Constructing JSON object...")
        print("  > Item ID number: %s" % self.json_data.get("id")) 
        print("  > Item name: %s" % self.json_data.get("name")) 
        self.id = self.json_data.get("id")
        self.noteable = self.determine_noteable()
        self.name = self.json_data.get("name")
        self.tradeable = self.json_data.get("isTradeable")
        self.stackable = self.json_data.get("stackable")
        self.equipable = self.determine_equipability()
        self.members = self.json_data.get("members")
        self.cost = self.json_data.get("cost")
        self.lowalch = self.determine_lowalch(None)
        self.highalch = self.determine_highalch(None)
        
    def determine_noteable(self):
        if self.json_data.get("notedID") is -1:
            return False   
        else:
            return True     
        
    def determine_lowalch(self, cost):
        if cost == None:
            return int(self.cost * 0.4)   
        else:
            return int(cost * 0.4)  
            
    def determine_highalch(self, cost):
        if cost == None:
            return int(self.cost * 0.6)   
        else:
            return int(cost * 0.6)   
        
    def determine_equipability(self):
        if "Wear" in self.json_data.get("interfaceOptions"):
            return True
        elif "Wield" in self.json_data.get("interfaceOptions"):
            return True            
        else:
            return False
            
    def determine_item_bonuses(self):
        scfm = ScrapeItemFromWikia.ScrapeItemFromWikia(self.name, True)
        scfm.read_all_item_urls()
        if scfm.determine_item_url():
            self.bonuses, self.item_slot, self.weapon_speed = scfm.get_item_bonuses()
        else:
            answer = input("  > Would you like to set a ZERO table? [y, N]: ")
            if answer.lower() == "y":
                self.bonuses = {"attack_stab" : None,
                                "attack_slash" : None,
                                "attack_crush" : None,
                                "attack_magic" : None,
                                "attack_ranged" : None,
                                "defence_stab" : None,
                                "defence_slash" : None,
                                "defence_crush" : None,
                                "defence_magic" : None,
                                "defence_ranged" : None,
                                "melee_strength" : None,
                                "ranged_strength" : None,
                                "magic_damage" : None,
                                "prayer" : None}
                for key, value in self.bonuses.items():
                    self.bonuses[key] = 0
                self.item_slot = input("  > What slot is this item: ")
                self.weapon_speed = input("  > What speed is this item: ")            
        if self.bonuses == None:
            print(">>> ERROR: Could not fetch item stats")
            quit()
		
    def scrape_wiki(self):
        scfm = ScrapeItemFromWikia.ScrapeItemFromWikia(self.name, True)
        scfm.read_all_item_urls()
        cont, url = scfm.determine_item_url()
        if cont:
            self.url = url
            properties = scfm.get_item_properties()
            try:
                self.weight = properties["weight"]
            except:
                #self.weight = input("  > What is the weight? [float]:")
                self.weight = 0.0
            try:
                self.examine = properties["examine2"]
            except:
                if "Clue scroll" in self.name:
                        self.examine = "A clue!"
                else:
                    self.examine = input("  > Enter examine text? [string]:")
            try:
                self.buy_limit = properties["buy_limit"]
            except:
                #self.buy_limit = input("  > What is the buy limit? [int]:")
                self.buy_limit = -1
            try:
                self.quest_item = properties["quest_item"]
            except:
                self.quest_item = False
                #self.quest_item = input("  > Is this a quest item? [true, false]:")
            try:
                self.stackable = properties["stackable"]
            except:
                #self.stackable = input("  > Is this stackable? [true, false]:")
                self.stackable = False
            try:
                self.release_date = properties["release_date"]
            except:
                self.release_date = input("  > What is the release date?:")            
                #self.release_date = "31 May 2006"
            if "(broken)" in self.name:
                self.release_date = "21 July 2016"
                self.examine = input("  > Enter examine text? [string]:")
        else:
            self.examine = None
            self.url = None
            self.weight = -1
            self.buy_limit = -1
            self.quest_item = -1
            self.stackable = -1
            self.release_date = None
        if self.equipable:
            if "shayzien supply" in self.name.lower():
                self.equipable = False
            else:
                self.determine_item_bonuses()            
        
    def fecth_image(self):
        pass
        # fetch from GE
        # fecth from other sources?    

    def construct_json(self):
        self.json_out = collections.OrderedDict()
        self.json_out["id"] = self.id
        self.json_out["name"] = self.name
        self.json_out["tradeable"] = self.tradeable
        self.json_out["stackable"] = self.stackable
        self.json_out["noteable"] = self.noteable
        self.json_out["equipable"] = self.equipable
        self.json_out["members"] = self.members
        self.json_out["weight"] = self.weight
        self.json_out["buy_limit"] = self.buy_limit
        self.json_out["quest_item"] = self.quest_item
        self.json_out["release_date"] = self.release_date     
        self.json_out["cost"] = self.cost
        self.json_out["lowalch"] = self.lowalch
        self.json_out["highalch"] = self.highalch
        self.json_out["examine"] = self.examine
        self.json_out["url"] = self.url
        if self.equipable:
            self.json_out["bonuses"] = self.bonuses
            self.json_out["item_slot"] = self.item_slot
            if self.item_slot == "weapon" or self.item_slot == "two-handed":
                self.json_out["weapon_speed"] = self.weapon_speed
    
    def edit_json(self):
        """ Construct JSON, print JSON, manually check and edit the contents. """
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=2)
        print(json_obj)
        answer = input("Would you like to change a field? [y, N]: ")
        if answer.lower() == "y":
            field = input("Name of field to change: ")
            if field == "bonuses":
                subfield = input("Name of sub-field to change: ")
                subvalue = input("Enter new value for %s: " % subfield)
                self.bonuses[subfield] = subvalue
                self.check_json()
            else:
                value = input("Enter new value for %s: " % field)
                setattr(self, field, value)
            self.check_json()

    def check_json(self):
        """ Construct JSON, and auto check fields. """
        self.construct_json()
        required_fields = ["id",
                           "name",
                           "tradeable",
                           "noteable",
                           "equipable",
                           "members",
                           "weight",
                           "buy_limit",
                           "quest_item",
                           "stackable",
                           "release_date", 
                           "cost",
                           "lowalch",
                           "highalch"]
        for field in required_fields:
            if not hasattr(self, field):
                print("ERROR: Missing object attribute for: %s" % field)
        if self.equipable:
            if not self.bonuses:
                print("ERROR: Equipable object has no item bonuses")
                quit()
        
    def print_json(self):
        self.construct_json()
        json_obj = json.dumps(self.json_out, indent=2)
        print(json_obj)   
            
    def export_json(self):
        self.construct_json()
        out_fi = "output" + os.sep + str(self.id) + ".json"
        with open(out_fi, "w") as f:
            json.dump(self.json_out, f, indent=2)
        
        
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
    assert _strcast("Hello world!")
    
    print("\nModule tests passed.\n")
