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


class ItemStats:
    """This class defines the stats structure and properties for an OSRS item."""
    def __init__(self):
        self._attack_stab = None
        self._attack_slash = None
        self._attack_crush = None
        self._attack_magic = None
        self._attack_ranged = None
        self._defence_stab = None
        self._defence_slash = None
        self._defence_crush = None
        self._defence_magic = None
        self._defence_ranged = None
        self._melee_strength = None
        self._ranged_strength = None
        self._magic_damage = None
        self._prayer = None

    @property
    def attack_stab(self) -> int:
        """The stab attack bonus of the item."""
        return self._attack_stab

    @attack_stab.setter
    def attack_stab(self, value):
        self._attack_stab = value

    @property
    def attack_slash(self) -> int:
        """The slash attack bonus of the item."""
        return self._attack_slash

    @attack_slash.setter
    def attack_slash(self, value):
        self._attack_slash = value

    @property
    def attack_crush(self) -> int:
        """The crush attack bonus of the item."""
        return self._attack_crush

    @attack_crush.setter
    def attack_crush(self, value):
        self._attack_crush = value

    @property
    def attack_magic(self) -> int:
        """The magic attack bonus of the item."""
        return self._attack_magic

    @attack_magic.setter
    def attack_magic(self, value):
        self._attack_magic = value

    @property
    def attack_ranged(self) -> int:
        """The ranged attack bonus of the item."""
        return self._attack_ranged

    @attack_ranged.setter
    def attack_ranged(self, value):
        self._attack_ranged = value

    @property
    def defence_stab(self) -> int:
        """The stab defence bonus of the item."""
        return self._defence_stab

    @defence_stab.setter
    def defence_stab(self, value):
        self._defence_stab = value

    @property
    def defence_slash(self) -> int:
        """The slash defence bonus of the item."""
        return self._defence_slash

    @defence_slash.setter
    def defence_slash(self, value):
        self._defence_slash = value

    @property
    def defence_crush(self) -> int:
        """The crush defence bonus of the item."""
        return self._defence_crush

    @defence_crush.setter
    def defence_crush(self, value):
        self._defence_crush = value

    @property
    def defence_magic(self) -> int:
        """The magic defence bonus of the item."""
        return self._defence_magic

    @defence_magic.setter
    def defence_magic(self, value):
        self._defence_magic = value

    @property
    def defence_ranged(self) -> int:
        """The ranged defence bonus of the item."""
        return self._defence_ranged

    @defence_ranged.setter
    def defence_ranged(self, value):
        self._defence_ranged = value

    @property
    def melee_strength(self) -> int:
        """The melee strength bonus of the item."""
        return self._melee_strength

    @melee_strength.setter
    def melee_strength(self, value):
        self._melee_strength = value

    @property
    def ranged_strength(self) -> int:
        """The ranged strength bonus of the item."""
        return self._ranged_strength

    @ranged_strength.setter
    def ranged_strength(self, value):
        self._ranged_strength = value

    @property
    def magic_damage(self) -> int:
        """The magic damage bonus of the item."""
        return self._magic_damage

    @magic_damage.setter
    def magic_damage(self, value):
        self._magic_damage = value

    @property
    def prayer(self) -> int:
        """The prayer bonus of the item."""
        return self._prayer

    @prayer.setter
    def prayer(self, value):
        self._prayer = value

    def load_item_stats_from_file(self, item_data: Dict):
        """Load an ItemStats object from an existing JSON file.

        :param item_data: A dictionary loaded from a JSON file.
        """
        for prop in vars(self):
            prop = prop[1:]
            setattr(self, prop, item_data[prop])

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON of ItemStats for exporting or printing.

        :return json_out: A dictionary of all stats properties.
        """
        json_out = collections.OrderedDict()
        for prop in vars(self):
            prop = prop[1:]
            json_out[prop] = getattr(self, prop)

        return json_out
