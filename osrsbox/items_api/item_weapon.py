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
from osrsbox.items_api.item_equipment import ItemEquipment
from osrsbox.items_api.stance import Stance
from dataclasses import dataclass, asdict
from typing import List, Dict


@dataclass
class ItemWeapon(ItemEquipment):
    """This class defines the properties for an equipable OSRS item that is a weapon.

    The ItemWeapon class is the object that retains all items properties related
    to equipable items that are weapons. This includes weapon attack speed,
    weapon type, stance, experience, and bonuses.
    """
    attack_speed: int
    weapon_type: str
    stances: List

    @classmethod
    def from_json(cls, json_dict):
        weapon = json_dict.pop("weapon")
        stances_json = weapon.pop("stances")
        item_equipment = json_dict.pop("equipment")
        return cls(
            **json_dict,
            **item_equipment,
            **weapon,
            stances=[Stance.from_json(stance) for stance in stances_json],
        )

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON of item_equipment property for exporting or printing.

        :return json_out: A dictionary of all equipment properties.
        """
        return asdict(self)
