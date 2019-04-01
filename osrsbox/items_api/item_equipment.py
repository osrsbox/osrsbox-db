"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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
"""

from typing import Dict


class ItemEquipment:
    """This class defines the properties for an equipable OSRS item.

    The ItemEquipment class is the object that retains all items properties related
    to equipable items. This includes item stats (attack, defence bonuses) and
    additional properties about equipment slot, attack speed and skill requirements
    for the item.
    """

    def __init__(self, attack_stab=None, attack_slash=None, attack_crush=None, attack_magic=None,
                 attack_ranged=None, defence_stab=None, defence_slash=None, defence_crush=None,
                 defence_magic=None, defence_ranged=None, melee_strength=None, ranged_strength=None,
                 magic_damage=None, prayer=None, slot=None, attack_speed=None, requirements=None):
        self.attack_stab = attack_stab
        self.attack_slash = attack_slash
        self.attack_crush = attack_crush
        self.attack_magic = attack_magic
        self.attack_ranged = attack_ranged
        self.defence_stab = defence_stab
        self.defence_slash = defence_slash
        self.defence_crush = defence_crush
        self.defence_magic = defence_magic
        self.defence_ranged = defence_ranged
        self.melee_strength = melee_strength
        self.ranged_strength = ranged_strength
        self.magic_damage = magic_damage
        self.prayer = prayer
        self.slot = slot
        self.attack_speed = attack_speed
        self.requirements = requirements

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON of item_equipment property for exporting or printing.

        :return json_out: A dictionary of all equipment properties.
        """
        json_out = dict()
        for prop in self.__dict__:
            json_out[prop] = getattr(self, prop)

        return json_out
