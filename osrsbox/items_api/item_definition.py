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

import os
import json
from dataclasses import dataclass, asdict
from typing import Dict, Optional

from osrsbox.items_api.item_equipment import ItemEquipment


@dataclass
class ItemDefinition:
    """This class defines the object structure and properties for an OSRS item.

    The ItemDefinition class is the object that retains all properties and stats
    for one specific item. Every item has the properties defined in this class.
    Equipable items have additional properties defined in the linked ItemEquipment
    class.
    """
    id: int
    name: str
    members: bool
    tradeable: Optional[bool]
    tradeable_on_ge: bool
    stackable: bool
    noted: bool
    noteable: bool
    linked_id: Optional[int]
    placeholder: bool
    equipable: bool
    equipable_by_player: bool
    cost: int
    lowalch: int
    highalch: int
    weight: Optional[float]
    buy_limit: Optional[int]
    quest_item: Optional[bool]
    release_date: Optional[str]
    examine: Optional[str]
    url: Optional[str]
    equipment: Optional[ItemEquipment] = None

    @classmethod
    def from_json(cls, json_dict: Dict) -> "ItemDefinition":
        """Convert the dictionary under the 'equipment' key into actual :class:`ItemEquipment`"""
        if json_dict.get("equipable_by_player"):
            equipment = json_dict.pop("equipment")
            json_dict["equipment"] = ItemEquipment(**equipment)

        return cls(**json_dict)

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON for exporting or printing.

        :return json_out: All class attributes stored in a dictionary.
        """
        return asdict(self)

    def export_json(self, pretty: bool, export_path: str):
        """Output Item to JSON file.

        :param pretty: Toggles pretty (indented) JSON output.
        :param export_path: The folder location to save the JSON output to.
        """
        json_out = self.construct_json()
        out_file_name = str(self.id) + ".json"
        out_file_path = os.path.join(export_path, out_file_name)
        with open(out_file_path, "w") as out_file:
            if pretty:
                json.dump(json_out, out_file, indent=4)
            else:
                json.dump(json_out, out_file)
