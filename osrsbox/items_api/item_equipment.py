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
from dataclasses import dataclass, asdict
from typing import Dict, Optional


@dataclass
class ItemEquipment:
    """This class defines the properties for an equipable OSRS item.

    The ItemEquipment class is the object that retains all items properties related
    to equipable items. This includes item stats (attack, defence bonuses) and
    additional properties about equipment slot, attack speed and skill requirements
    for the item.
    """
    attack_stab: int
    attack_slash: int
    attack_crush: int
    attack_magic: int
    attack_ranged: int
    defence_stab: int
    defence_slash: int
    defence_crush: int
    defence_magic: int
    defence_ranged: int
    melee_strength: int
    ranged_strength: int
    magic_damage: int
    prayer: int
    slot: str
    requirements: Optional[Dict]

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON of item_equipment property for exporting or printing.

        :return json_out: A dictionary of all equipment properties.
        """
        return asdict(self)
