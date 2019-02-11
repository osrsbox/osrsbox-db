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
import collections
from typing import Dict

from osrsbox.items_api import item_stats
from osrsbox.items_api import item_equipment


class ItemDefinition:
    """This class defines the object structure and properties for an OSRS item.

    The ItemDefinition class is the object that retains all properties and stats
    for one specific item. Every item has the properties defined in this class.
    Equipable items have additional properties defined in the linked ItemStats
    and ItemEquipment classes.
    """

    def __init__(self):
        self._id = None
        self._name = None
        self._members = None
        self._tradeable = None
        self._tradeable_on_ge = None
        self._stackable = None
        self._noted = None
        self._noteable = None
        self._linked_id = None
        self._equipable = None
        self._cost = None
        self._lowalch = None
        self._highalch = None
        self._weight = None
        self._buy_limit = None
        self._quest_item = None
        self._release_date = None
        # self._seller = None
        # self._store_price = None
        self._examine = None
        self._url = None

    @property
    def id(self) -> int:
        """The ID number of the item."""
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def name(self) -> str:
        """The in-game name of the item."""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def members(self) -> bool:
        """If the item is members-only, or not."""
        return self._members

    @members.setter
    def members(self, value: bool):
        self._members = value

    @property
    def tradeable(self) -> bool:
        """If the item is tradeable, or not."""
        return self._tradeable

    @tradeable.setter
    def tradeable(self, value: bool):
        self._tradeable = value

    @property
    def tradeable_on_ge(self) -> bool:
        """If the item is tradeable on the GE, or not."""
        return self._tradeable_on_ge

    @tradeable_on_ge.setter
    def tradeable_on_ge(self, value: bool):
        self._tradeable_on_ge = value

    @property
    def stackable(self) -> bool:
        """If the item is stackable, or not."""
        return self._stackable

    @stackable.setter
    def stackable(self, value: bool):
        self._stackable = value

    @property
    def noted(self) -> bool:
        """If the item is noted, or not."""
        return self._noted

    @noted.setter
    def noted(self, value: bool):
        self._noted = value

    @property
    def noteable(self) -> bool:
        """If the item is noteable, or not."""
        return self._noteable

    @noteable.setter
    def noteable(self, value: bool):
        self._noteable = value

    @property
    def linked_id(self) -> int:
        """The ID number of the linked item."""
        return self._linked_id

    @linked_id.setter
    def linked_id(self, value: int):
        self._linked_id = value

    @property
    def equipable(self) -> int:
        """If the item is equipable, or not."""
        return self._equipable

    @equipable.setter
    def equipable(self, value: bool):
        self._equipable = value

    @property
    def cost(self) -> int:
        """The cost of the item."""
        return self._cost

    @cost.setter
    def cost(self, value: int):
        self._cost = value

    @property
    def lowalch(self) -> int:
        """The low alchemy value of the item."""
        return self._lowalch

    @lowalch.setter
    def lowalch(self, value: int):
        self._lowalch = value

    @property
    def highalch(self) -> int:
        """The high alchemy value of the item."""
        return self._highalch

    @highalch.setter
    def highalch(self, value: int):
        self._highalch = value

    @property
    def weight(self) -> float:
        """The weight, in kilograms, of the item."""
        return self._weight

    @weight.setter
    def weight(self, value: float):
        self._weight = value

    @property
    def buy_limit(self) -> int:
        """The GE buy limit of the item."""
        return self._buy_limit

    @buy_limit.setter
    def buy_limit(self, value: int):
        self._buy_limit = value

    @property
    def quest_item(self) -> bool:
        """If the item is associated with a quest, or not."""
        return self._quest_item

    @quest_item.setter
    def quest_item(self, value: bool):
        self._quest_item = value

    @property
    def release_date(self) -> str:
        """The release date of the item."""
        return self._release_date

    @release_date.setter
    def release_date(self, value: str):
        self._release_date = value

    # @property
    # def seller(self) -> List:
    #     """A list of stores/sellers that sell the item."""
    #     return self._seller
    #
    # @seller.setter
    # def seller(self, value: List):
    #     self._seller = value
    #
    # @property
    # def store_price(self) -> int:
    #     """The store price of the item."""
    #     return self._store_price
    #
    # @store_price.setter
    # def store_price(self, value: int):
    #     self._store_price = value

    @property
    def examine(self) -> str:
        """The text when examining the item."""
        return self._examine

    @examine.setter
    def examine(self, value: str):
        self._examine = value

    @property
    def url(self) -> str:
        """The OSRS Wiki URL of the item."""
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    def load_item_definition_from_file(self, item_data: Dict):
        """Load an ItemDefinition object from an existing JSON file.

        :param item_data: A dictionary loaded from a JSON file.
        """
        for prop in vars(self):
            prop = prop[1:]
            setattr(self, prop, item_data[prop])

        # If the item is equipable, it should have stats and equipment objects populated
        if self.equipable:
            # Initialize an empty ItemStats object
            self.item_stats: object = item_stats.ItemStats()

            # Populate items stats
            self.item_stats.load_item_stats_from_file(item_data["bonuses"])

            # Initialize an empty ItemEquipment object
            self.item_equipment: object = item_equipment.ItemEquipment()

            # Populate item equipment
            self.item_equipment.load_item_equipment_from_file(item_data["equipment"])

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON for exporting or printing.

        :return json_out: All class attributes stored in a dictionary.
        """
        json_out: Dict = collections.OrderedDict()
        for prop in vars(self):
            if prop.startswith("_"):
                prop = prop[1:]
                json_out[prop] = getattr(self, prop)

        if self.equipable:
            json_out["bonuses"] = self.item_stats.construct_json()
            json_out["equipment"] = self.item_equipment.construct_json()

        return json_out

    def export_json(self, pretty: bool, export_path: str):
        """Output Item to JSON file.

        :param pretty: Toggles pretty (indented) JSON output.
        :param export_path: The folder location to save the JSON output to.
        """
        json_out = self.construct_json()
        out_file_name = str(self.id) + ".json"
        out_file_path = os.path.join(export_path, out_file_name)
        with open(out_file_path, "w", newline="\n") as out_file:
            if pretty:
                json.dump(json_out, out_file, indent=4)
            else:
                json.dump(json_out, out_file)
