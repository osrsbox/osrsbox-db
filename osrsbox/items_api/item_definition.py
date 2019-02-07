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
import datetime
import collections
from typing import List
from typing import Dict

import safe_cast

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
        self.properties = [
            "id",
            "name",
            "members",
            "tradeable",
            "tradeable_on_ge",
            "stackable",
            "noted",
            "noteable",
            "linked_id",
            "equipable",
            "cost",
            "lowalch",
            "highalch",
            "weight",
            "buy_limit",
            "quest_item",
            "release_date",
            "examine",
            "url"]

        # Initialize an empty ItemStats object
        self.item_stats: object = item_stats.ItemStats()
        # Initialize an empty ItemEquipment object
        self.item_equipment: object = item_equipment.ItemEquipment()
        # Initialize an empty output dictionary for an item
        self.json_out: Dict = collections.OrderedDict()

    @property
    def id(self) -> int:
        """The ID number of the item."""
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = safe_cast.safe_cast(value, int, default=None)

    @property
    def name(self) -> str:
        """The in-game name of the item."""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = safe_cast.safe_cast(value, str, default=None)

    @property
    def members(self) -> bool:
        """If the item is members-only, or not."""
        return self._members

    @members.setter
    def members(self, value: bool):
        self._members = safe_cast.safe_cast(value, bool, default=None)

    @property
    def tradeable(self) -> bool:
        """If the item is tradeable, or not."""
        return self._tradeable

    @tradeable.setter
    def tradeable(self, value: bool):
        self._tradeable = safe_cast.safe_cast(value, bool, default=None)

    @property
    def tradeable_on_ge(self) -> bool:
        """If the item is tradeable on the GE, or not."""
        return self._tradeable_on_ge

    @tradeable_on_ge.setter
    def tradeable_on_ge(self, value: bool):
        self._tradeable_on_ge = safe_cast.safe_cast(value, bool, default=None)

    @property
    def stackable(self) -> bool:
        """If the item is stackable, or not."""
        return self._stackable

    @stackable.setter
    def stackable(self, value: bool):
        self._stackable = safe_cast.safe_cast(value, bool, default=None)

    @property
    def noted(self) -> bool:
        """If the item is noted, or not."""
        return self._noted

    @noted.setter
    def noted(self, value: bool):
        self._noted = safe_cast.safe_cast(value, bool, default=None)

    @property
    def noteable(self) -> bool:
        """If the item is noteable, or not."""
        return self._noteable

    @noteable.setter
    def noteable(self, value: bool):
        self._noteable = safe_cast.safe_cast(value, bool, default=None)

    @property
    def linked_id(self) -> int:
        """The ID number of the linked item."""
        return self._linked_id

    @linked_id.setter
    def linked_id(self, value: int):
        self._linked_id = safe_cast.safe_cast(value, int, default=None)

    @property
    def equipable(self) -> int:
        """If the item is equipable, or not."""
        return self._equipable

    @equipable.setter
    def equipable(self, value: bool):
        self._equipable = safe_cast.safe_cast(value, bool, default=None)

    @property
    def cost(self) -> int:
        """The cost of the item."""
        return self._cost

    @cost.setter
    def cost(self, value: int):
        self._cost = safe_cast.safe_cast(value, int, default=None)

    @property
    def lowalch(self) -> int:
        """The low alchemy value of the item."""
        return self._lowalch

    @lowalch.setter
    def lowalch(self, value: int):
        self._lowalch = safe_cast.safe_cast(value, int, default=None)

    @property
    def highalch(self) -> int:
        """The high alchemy value of the item."""
        return self._highalch

    @highalch.setter
    def highalch(self, value: int):
        self._highalch = safe_cast.safe_cast(value, int, default=None)

    @property
    def weight(self) -> float:
        """The weight, in kilograms, of the item."""
        return self._weight

    @weight.setter
    def weight(self, value: float):
        self._weight = safe_cast.safe_cast(value, float, default=None)

    @property
    def buy_limit(self) -> int:
        """The GE buy limit of the item."""
        return self._buy_limit

    @buy_limit.setter
    def buy_limit(self, value: int):
        self._buy_limit = safe_cast.safe_cast(value, int, default=None)

    @property
    def quest_item(self) -> List:
        """A list of quests the item is associated with."""
        return self._quest_item

    @quest_item.setter
    def quest_item(self, value: List):
        self._quest_item = safe_cast.safe_cast(value, list, default=None)

    @property
    def release_date(self) -> object:
        """The release date of the item."""
        return self._release_date

    @release_date.setter
    def release_date(self, value: datetime):
        if not value:
            return None
        date = datetime.datetime.strptime(value, "%d %B %Y")
        date = date.strftime("%d %B %Y")
        self._release_date = date

    @property
    def seller(self) -> List:
        """A list of stores that sell the item."""
        return self._seller

    @seller.setter
    def seller(self, value: List):
        self._seller = safe_cast.safe_cast(value, list, default=None)

    @property
    def store_price(self) -> int:
        """The store price of the item."""
        return self._store_price

    @store_price.setter
    def store_price(self, value: int):
        self._store_price = safe_cast.safe_cast(value, int, default=None)

    @property
    def examine(self) -> str:
        """The text when examining the item."""
        return self._examine

    @examine.setter
    def examine(self, value: str):
        self._examine = safe_cast.safe_cast(value, str, default=None)

    @property
    def url(self) -> str:
        """The OSRS Wiki URL of the item."""
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = safe_cast.safe_cast(value, str, default=None)

    def load_item_definition_from_file(self, item_data: Dict):
        """Load an ItemDefinition object from an existing JSON file.

        :param item_data: A dictionary loaded from a JSON file.
        """
        for prop in self.properties:
            setattr(self, prop, item_data[prop])

        # If the item is equipable, it should have stats and equipment objects populated
        if self.equipable:
            # Populate items stats
            self.item_stats.load_item_stats_from_file(item_data["bonuses"])
            # Populate item equipment
            self.item_equipment.load_item_equipment_from_file(item_data["equipment"])

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON for exporting or printing.

        :return json_out: All class attributes stored in a dictionary.
        """
        for prop in self.properties:
            self.json_out[prop] = getattr(self, prop)

        if self.equipable:
            self.item_stats.construct_json()
            self.item_equipment.construct_json()

        return self.json_out

    def print_json(self, pretty: bool):
        """Output Item to console.

        :param pretty: Toggles pretty (indented) JSON output.
        """
        self.construct_json()
        if pretty:
            json_obj = json.dumps(self.json_out, indent=4)
        else:
            json_obj = json.dumps(self.json_out)
        print(json_obj)

    def export_json(self, pretty: bool):
        """Output Item to JSON file.

        :param pretty: Toggles pretty (indented) JSON output.
        """
        self.construct_json()
        out_file_name = str(self.id) + ".json"
        out_file_path = os.path.join("items-json", out_file_name)
        with open(out_file_path, "w") as out_file:
            if pretty:
                json.dump(self.json_out, out_file, indent=4)
            else:
                json.dump(self.json_out, out_file)
