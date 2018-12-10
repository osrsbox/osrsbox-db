# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/10

Description:
ItemEquipment is a class to process handle the item equipment information 
for OSRS items that are equipable; for example, weapons and armour.

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

import json
import collections

###############################################################################
# Helper methods
def _intcast(val):
    """ Convert input to integer. """
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        if val == "":
            return (0)
        if val[0] == "-":
            if val[1:].isdigit():
                return int(val)
        if val[0] == "+":
            if val[1:].isdigit():
                return int(val)                
        else:
            if val.isdigit():
                return int(val)

def _strcast(val):
    """ Convert value to string. """
    if val is None:
        return None
    return str(val)

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
# ItemEquipment object
class ItemEquipment(object):
    def __init__(self, itemID):
        self.itemID = itemID
        self.properties = [
            "attack_speed",
            "slot",
            "skill_reqs"
            ]   
        for prop in self.properties:
            if prop == "slot":
                setattr(self, prop, "")
            elif prop == "skill_reqs":
                setattr(self, prop, [])
            else:
                setattr(self, prop, 0)
            
    
    # Setters and Getters
    @property
    def slot(self):
        return self._slot
    @slot.setter
    def slot(self, value):
        self._slot = _strcast(value)

    @property
    def attack_speed(self):
        return self._attack_speed
    @attack_speed.setter
    def attack_speed(self, value):
        self._attack_speed = _intcast(value)

    @property
    def skill_reqs(self):
        return self._skill_reqs
    @skill_reqs.setter
    def skill_reqs(self, value):
        self._skill_reqs = _listcast(value)      

    ###########################################################################
    # Handle item to JSON
    def construct_json(self):
        self.json_out = collections.OrderedDict()
        self.json_out["slot"] = self.slot
        self.json_out["attack_speed"] = self.attack_speed
        self.json_out["skill_reqs"] = self.skill_reqs
        return self.json_out     

################################################################################
if __name__=="__main__":
    # Run unit tests
    assert _intcast(-1) == -1
    assert _intcast("-1") == -1
    assert _intcast("1") == 1
    assert _intcast("+1") == 1
   
    print("Module tests passed.")