# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/08

Description:
ItemDefinition is a class to load and manipulate osrsbox-db items-json
files.

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
    date = datetime.datetime.strptime(val, "%d %B %Y")   
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
    def __init__(self):     
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

    ###########################################################################
    # Helpers: Setters and Getters
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
        self._examine = _listcast(value)
	           
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, value):
        self._url = _strcast(value)

    ###########################################################################
    # Helpers: Processing
    def load_item(self, input):
        for prop in self.properties:
            setattr(self, prop, input[prop]) 
            # setattr(x, 'y', v) is equivalent to x.y = v

        if self.equipable:
            # Item Bonuses
            ib = ItemBonuses.ItemBonuses(self.id)
            bonuses = ib.load_item(input["bonuses"])
            self.bonuses = bonuses
            # # Item Equipment
            # ie = ItemEquipment.ItemEquipment(self.id)
            # equipment = ie.load_item(input["equipment"])
            # self.equipment = equipment            

        return self
          
    ###########################################################################
    # Helpers: JSON
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
            bonuses_in_json = self.bonuses.construct_json()
            self.json_out["bonuses"] = bonuses_in_json
            # equipment_in_json = self.equipment.construct_json()
            # self.json_out["equipment"] = equipment_in_json            

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
