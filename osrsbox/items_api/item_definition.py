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
from typing import Dict, Optional

from osrsbox.items_api.item_equipment import ItemEquipment


class ItemDefinition:
    """This class defines the object structure and properties for an OSRS item.

    The ItemDefinition class is the object that retains all properties and stats
    for one specific item. Every item has the properties defined in this class.
    Equipable items have additional properties defined in the linked ItemEquipment
    class.
    """

    def __init__(self, id=None, name=None, members=None, tradeable=None, tradeable_on_ge=None, stackable=None,
                 noted=None, noteable=None, linked_id=None, placeholder=None, equipable=None, equipable_by_player=None,
                 cost=None, lowalch=None, highalch=None, weight=None, buy_limit=None, quest_item=None,
                 release_date=None, examine=None, url=None, equipment=None):
        self.id = id
        self.name = name
        self.members = members
        self.tradeable = tradeable
        self.tradeable_on_ge = tradeable_on_ge
        self.stackable = stackable
        self.noted = noted
        self.noteable = noteable
        self.linked_id = linked_id
        self.placeholder = placeholder
        self.equipable = equipable
        self.equipable_by_player = equipable_by_player
        self.cost = cost
        self.lowalch = lowalch
        self.highalch = highalch
        self.weight = weight
        self.buy_limit = buy_limit
        self.quest_item = quest_item
        self.release_date = release_date
        self.examine = examine
        self.url = url

        self.equipment: Optional[ItemEquipment] = None

        if self.equipable_by_player:
            self.equipment = ItemEquipment(**equipment)

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON for exporting or printing.

        :return json_out: All class attributes stored in a dictionary.
        """
        json_out: Dict = dict()

        for prop in self.__dict__:
            if prop == "equipment":
                continue
            json_out[prop] = getattr(self, prop)

        if self.equipable_by_player:
            json_out["equipment"] = self.equipment.construct_json()

        return json_out

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
