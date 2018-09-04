# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/04

Description:
ItemBonuses is a class to process handle the item bonuses for OSRS items
that are equipable; for example, weapons and armour.

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
import datetime
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
        else:
            if val.isdigit():
                return int(val)

###############################################################################
# ItemBonuses object
class ItemBonuses(object):
    def __init__(self, itemID, itemJSON):
        self.itemID = itemID
        self.itemJSON = itemJSON
        self.object = None
        self.properties = {
            "attack_stab" : None,
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
    
    # Attacking Stats
    @property
    def attack_stab(self):
        return self._attack_stab
    @attack_stab.setter
    def attack_stab(self, value):
        self._attack_stab = _intcast(value)

    @property
    def attack_slash(self):
        return self._attack_slash
    @attack_slash.setter
    def attack_slash(self, value):
        self._attack_slash = _intcast(value)

    @property
    def attack_crush(self):
        return self._attack_crush
    @attack_crush.setter
    def attack_crush(self, value):
        self._attack_crush = _intcast(value)

    @property
    def attack_magic(self):
        return self._attack_magic
    @attack_magic.setter
    def attack_magic(self, value):
        self._attack_magic = _intcast(value)

    @property
    def attack_ranged(self):
        return self._attack_ranged
    @attack_ranged.setter
    def attack_ranged(self, value):
        self._attack_ranged = _intcast(value)

    # Defensive Stats
    @property
    def defence_stab(self):
        return self._defence_stab
    @defence_stab.setter
    def defence_stab(self, value):
        self._defence_stab = _intcast(value)

    @property
    def defence_slash(self):
        return self._defence_slash
    @defence_slash.setter
    def defence_slash(self, value):
        self._defence_slash = _intcast(value)

    @property
    def defence_crush(self):
        return self._defence_crush
    @defence_crush.setter
    def defence_crush(self, value):
        self._defence_crush = _intcast(value)

    @property
    def defence_magic(self):
        return self._defence_magic
    @defence_magic.setter
    def defence_magic(self, value):
        self._defence_magic = _intcast(value)

    @property
    def defence_ranged(self):
        return self._defence_ranged
    @defence_ranged.setter
    def defence_ranged(self, value):
        self._defence_ranged = _intcast(value)

    # Bonus Stats
    @property
    def melee_strength(self):
        return self._melee_strength
    @melee_strength.setter
    def melee_strength(self, value):
        self._melee_strength = _intcast(value)

    @property
    def ranged_strength(self):
        return self._ranged_strength
    @ranged_strength.setter
    def ranged_strength(self, value):
        self._ranged_strength = _intcast(value)

    @property
    def magic_damage(self):
        return self._magic_damage
    @magic_damage.setter
    def magic_damage(self, value):
        self._magic_damage = _intcast(value)

    @property
    def prayer(self):
        return self._prayer
    @prayer.setter
    def prayer(self, value):
        self._prayer = _intcast(value)

    # def determine_item_bonuses(self):
    #     scfm = ScrapeItemFromWikia.ScrapeItemFromWikia(self.name, True)
    #     scfm.read_all_item_urls()
    #     if scfm.determine_item_url():
    #         self.bonuses, self.item_slot, self.weapon_speed = scfm.get_item_bonuses()
    #     else:
    #         answer = input("  > Would you like to set a ZERO table? [y, N]: ")
    #         if answer.lower() == "y":
    #             self.bonuses = {"attack_stab" : None,
    #                             "attack_slash" : None,
    #                             "attack_crush" : None,
    #                             "attack_magic" : None,
    #                             "attack_ranged" : None,
    #                             "defence_stab" : None,
    #                             "defence_slash" : None,
    #                             "defence_crush" : None,
    #                             "defence_magic" : None,
    #                             "defence_ranged" : None,
    #                             "melee_strength" : None,
    #                             "ranged_strength" : None,
    #                             "magic_damage" : None,
    #                             "prayer" : None}
    #             for key, value in self.bonuses.items():
    #                 self.bonuses[key] = 0
    #             self.item_slot = input("  > What slot is this item: ")
    #             self.weapon_speed = input("  > What speed is this item: ")            
    #     if self.bonuses == None:
    #         print(">>> ERROR: Could not fetch item stats")
    #         quit()              

################################################################################
if __name__=="__main__":
    # Run unit tests
    assert _intcast(-1) == -1
    assert _intcast("-1") == -1
    assert _intcast("1") == 1
   
    print("Module tests passed.")
