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
from typing import Dict


@dataclass
class MonsterDrop:
    """This class defines the drops of an OSRS monster.

    The MonsterDrop class is the object that retains all drop properties related
    to items dropped by a specific monster. This includes item properties (id,
    name) and drop properties (quantity, rarity, and drop requirements).
    """
    id: int = None
    name: str = None
    members: str = None
    quantity: str = None
    noted: bool = None
    rarity: str = None
    rolls: int = None

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON of drop entry in a list for exporting or printing.

        :return json_out: A dictionary of a single drop instance.
        """
        return asdict(self)
