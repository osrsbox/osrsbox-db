# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/22

Description:


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

###############################################################################
# MonsterStats object
class MonsterStats(object):
    def __init__(self, monsterID):
        self.monsterID = monsterID
        self.properties = [
            "attack_level",
            "strength_level",
            "defence_level",
            "magic_level",
            "ranged_level",
            "attack_stab",
            "attack_slash",
            "attack_crush",
            "attack_magic",
            "attack_ranged",
            "defence_stab",
            "defence_slash",
            "defence_crush",
            "defence_magic",
            "defence_ranged",
            "attack_accuracy",
            "melee_strength",
            "ranged_strength",
            "magic_damage"]

        for prop in self.properties:
            setattr(self, prop, 0)
    
    # Combat levels
    @property
    def attack_level(self):
        return self._attack_level
    @attack_level.setter
    def attack_level(self, value):
        self._attack_level = _intcast(value)

    @property
    def strength_level(self):
        return self._strength_level
    @strength_level.setter
    def strength_level(self, value):
        self._strength_level = _intcast(value)

    @property
    def defence_level(self):
        return self._defence_level
    @defence_level.setter
    def defence_level(self, value):
        self._defence_level = _intcast(value)

    @property
    def magic_level(self):
        return self._magic_level
    @magic_level.setter
    def magic_level(self, value):
        self._magic_level = _intcast(value)

    @property
    def ranged_level(self):
        return self._ranged_level
    @ranged_level.setter
    def ranged_level(self, value):
        self._ranged_level = _intcast(value)                                    

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
    def attack_accuracy(self):
        return self._attack_accuracy
    @attack_accuracy.setter
    def attack_accuracy(self, value):
        self._attack_accuracy = _intcast(value)

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

    ###########################################################################
    # Handle template to object
    def extract_template_value(self, template, key):
        value = None
        try:
            value = template.get(key).value
            return value
        except ValueError:
            return value

    def parse_wikitext_template(self, template, version):
        # Parse the Infobox Monsters template to MonsterStats object
        self.attack_level = self.extract_template_value(template, "att" + version)
        self.strength_level = self.extract_template_value(template, "str" + version)
        self.defence_level = self.extract_template_value(template, "def" + version)
        self.magic_level = self.extract_template_value(template, "mage" + version)
        self.ranged_level = self.extract_template_value(template, "range" + version)
        self.attack_stab = self.extract_template_value(template, "astab" + version)
        self.attack_slash = self.extract_template_value(template, "aslash" + version)
        self.attack_crush = self.extract_template_value(template, "acrush" + version)
        self.attack_magic = self.extract_template_value(template, "amagic" + version)
        self.attack_ranged = self.extract_template_value(template, "arange" + version)
        self.defence_stab = self.extract_template_value(template, "dstab" + version)
        self.defence_slash = self.extract_template_value(template, "dslash" + version)
        self.defence_crush = self.extract_template_value(template, "dcrush" + version)
        self.defence_magic = self.extract_template_value(template, "dmagic" + version)
        self.defence_ranged = self.extract_template_value(template, "drange" + version)
        self.attack_accuracy = self.extract_template_value(template, "attbns" + version)
        self.melee_strength = self.extract_template_value(template, "strbns" + version)
        self.ranged_strength = self.extract_template_value(template, "rngbns" + version)
        self.magic_damage = self.extract_template_value(template, "mbns" + version)

    ###########################################################################
    # Handle item to JSON
    def construct_json(self):
        self.json_out = collections.OrderedDict()
        self.json_out["attack_level"] = self.attack_level
        self.json_out["strength_level"] = self.strength_level
        self.json_out["defence_level"] = self.defence_level
        self.json_out["magic_level"] = self.magic_level
        self.json_out["ranged_level"] = self.ranged_level
        self.json_out["attack_stab"] = self.attack_stab
        self.json_out["attack_slash"] = self.attack_slash
        self.json_out["attack_crush"] = self.attack_crush
        self.json_out["attack_magic"] = self.attack_magic
        self.json_out["attack_ranged"] = self.attack_ranged
        self.json_out["defence_stab"] = self.defence_stab
        self.json_out["defence_slash"] = self.defence_slash
        self.json_out["defence_crush"] = self.defence_crush
        self.json_out["defence_magic"] = self.defence_magic
        self.json_out["defence_ranged"] = self.defence_ranged
        self.json_out["attack_accuracy"] = self.attack_accuracy
        self.json_out["melee_strength"] = self.melee_strength
        self.json_out["ranged_strength"] = self.ranged_strength
        self.json_out["magic_damage"] = self.magic_damage
        return self.json_out     

################################################################################
if __name__=="__main__":
    # Run unit tests
    assert _intcast(-1) == -1
    assert _intcast("-1") == -1
    assert _intcast("1") == 1
    assert _intcast("+1") == 1
   
    print("Module tests passed.")
