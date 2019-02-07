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

import safe_cast


class ItemStats:
    """This class defines the stats structure and properties for an OSRS item."""
    def __init__(self):
        self.properties = [
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
            "melee_strength",
            "ranged_strength",
            "magic_damage",
            "prayer"]

        self.json_out = collections.OrderedDict()

    @property
    def attack_stab(self) -> int:
        """The stab attack bonus of the item."""
        return self._attack_stab

    @attack_stab.setter
    def attack_stab(self, value):
        self._attack_stab = safe_cast.safe_cast(value, int, default=None)

    @property
    def attack_slash(self) -> int:
        """The slash attack bonus of the item."""
        return self._attack_slash

    @attack_slash.setter
    def attack_slash(self, value):
        self._attack_slash = safe_cast.safe_cast(value, int, default=None)

    @property
    def attack_crush(self) -> int:
        """The crush attack bonus of the item."""
        return self._attack_crush

    @attack_crush.setter
    def attack_crush(self, value):
        self._attack_crush = safe_cast.safe_cast(value, int, default=None)

    @property
    def attack_magic(self) -> int:
        """The magic attack bonus of the item."""
        return self._attack_magic

    @attack_magic.setter
    def attack_magic(self, value):
        self._attack_magic = safe_cast.safe_cast(value, int, default=None)

    @property
    def attack_ranged(self) -> int:
        """The ranged attack bonus of the item."""
        return self._attack_ranged

    @attack_ranged.setter
    def attack_ranged(self, value):
        self._attack_ranged = safe_cast.safe_cast(value, int, default=None)

    @property
    def defence_stab(self) -> int:
        """The stab defence bonus of the item."""
        return self._defence_stab

    @defence_stab.setter
    def defence_stab(self, value):
        self._defence_stab = safe_cast.safe_cast(value, int, default=None)

    @property
    def defence_slash(self) -> int:
        """The slash defence bonus of the item."""
        return self._defence_slash

    @defence_slash.setter
    def defence_slash(self, value):
        self._defence_slash = safe_cast.safe_cast(value, int, default=None)

    @property
    def defence_crush(self) -> int:
        """The crush defence bonus of the item."""
        return self._defence_crush

    @defence_crush.setter
    def defence_crush(self, value):
        self._defence_crush = safe_cast.safe_cast(value, int, default=None)

    @property
    def defence_magic(self) -> int:
        """The magic defence bonus of the item."""
        return self._defence_magic

    @defence_magic.setter
    def defence_magic(self, value):
        self._defence_magic = safe_cast.safe_cast(value, int, default=None)

    @property
    def defence_ranged(self) -> int:
        """The ranged defence bonus of the item."""
        return self._defence_ranged

    @defence_ranged.setter
    def defence_ranged(self, value):
        self._defence_ranged = safe_cast.safe_cast(value, int, default=None)

    @property
    def melee_strength(self) -> int:
        """The melee strength bonus of the item."""
        return self._melee_strength

    @melee_strength.setter
    def melee_strength(self, value):
        self._melee_strength = safe_cast.safe_cast(value, int, default=None)

    @property
    def ranged_strength(self) -> int:
        """The ranged strength bonus of the item."""
        return self._ranged_strength

    @ranged_strength.setter
    def ranged_strength(self, value):
        self._ranged_strength = safe_cast.safe_cast(value, int, default=None)

    @property
    def magic_damage(self) -> int:
        """The magic damage bonus of the item."""
        return self._magic_damage

    @magic_damage.setter
    def magic_damage(self, value):
        self._magic_damage = safe_cast.safe_cast(value, int, default=None)

    @property
    def prayer(self) -> int:
        """The prayer bonus of the item."""
        return self._prayer

    @prayer.setter
    def prayer(self, value):
        self._prayer = safe_cast.safe_cast(value, int, default=None)

    def load_item_stats_from_file(self, item_data: Dict):
        """Load an ItemStats object from an existing JSON file.

        :param item_data: A dictionary loaded from a JSON file.
        """
        for prop in self.properties:
            setattr(self, prop, item_data[prop])

    def construct_json(self):
        """Construct dictionary/JSON of ItemStats for exporting or printing."""
        for prop in self.properties:
            self.json_out[prop] = getattr(self, prop)
