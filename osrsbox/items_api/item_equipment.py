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

import collections
from typing import Dict
from typing import List

import safe_cast


class ItemEquipment:
    """This class defines the equipment structure and properties for an OSRS item."""
    def __init__(self):
        self.properties = [
            "attack_speed",
            "slot",
            "skill_reqs"]

        self.json_out = collections.OrderedDict()

    @property
    def slot(self) -> str:
        """The equipment slot of an item."""
        return self._slot

    @slot.setter
    def slot(self, value):
        self._slot = safe_cast.safe_cast(value, str, default=None)

    @property
    def attack_speed(self) -> int:
        """The attack speed of a weapon."""
        return self._attack_speed

    @attack_speed.setter
    def attack_speed(self, value):
        self._attack_speed = safe_cast.safe_cast(value, int, default=None)

    @property
    def skill_reqs(self) -> List:
        """A list of item skill requirements."""
        return self._skill_reqs

    @skill_reqs.setter
    def skill_reqs(self, value):
        self._skill_reqs = safe_cast.safe_cast(value, list, default=None)

    def load_item_equipment_from_file(self, item_data: Dict):
        """Load an ItemEquipment object from an existing JSON file entry.

        :param item_data: A dictionary loaded from a JSON file.
        """
        for prop in self.properties:
            setattr(self, prop, item_data[prop])

    def construct_json(self):
        """Construct dictionary/JSON of item_equipment property for exporting or printing."""
        for prop in self.properties:
            self.json_out[prop] = getattr(self, prop)
