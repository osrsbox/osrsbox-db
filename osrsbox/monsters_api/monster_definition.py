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

import json
from typing import Dict, List
from pathlib import Path
from dataclasses import dataclass, asdict

from osrsbox.monsters_api.monster_drop import MonsterDrop


@dataclass
class MonsterDefinition:
    """This class defines the object structure and properties for an OSRS monster.

    The MonsterDefinition class is the object that retains all properties and stats
    for one specific monster. Every monster has the properties defined in this class,
    as well as the stats.
    """
    id: int = None
    name: str = None
    incomplete: bool = None
    members: bool = None
    release_date: str = None
    combat_level: int = None
    size: int = None
    hitpoints: int = None
    max_hit: int = None
    attack_type: str = None
    attack_speed: int = None
    aggressive: bool = None
    poisonous: bool = None
    immune_poison: bool = None
    immune_venom: bool = None
    weakness: List = None
    slayer_monster: bool = None
    slayer_level: int = None
    slayer_xp: int = None
    slayer_masters: List = None
    examine: str = None
    wiki_name: str = None
    wiki_url: str = None
    attack_level: int = None
    strength_level: int = None
    defence_level: int = None
    magic_level: int = None
    ranged_level: int = None
    attack_stab: int = None
    attack_slash: int = None
    attack_crush: int = None
    attack_magic: int = None
    attack_ranged: int = None
    defence_stab: int = None
    defence_slash: int = None
    defence_crush: int = None
    defence_magic: int = None
    defence_ranged: int = None
    attack_accuracy: int = None
    melee_strength: int = None
    ranged_strength: int = None
    magic_damage: int = None
    drops: List[MonsterDrop] = None
    rare_drop_table: bool = None

    @classmethod
    def from_json(cls, json_dict: Dict) -> List[MonsterDrop]:
        """Convert the list under the 'drops' key into actual :class:`MonsterDrop`"""
        if json_dict.get("drops"):
            drops = json_dict.pop("drops")
            json_dict["drops"] = list(drops)

        return cls(**json_dict)

    def construct_json(self) -> Dict:
        """Construct dictionary/JSON for exporting or printing.

        :return json_out: All class attributes stored in a dictionary.
        """
        return asdict(self)

    def export_json(self, pretty: bool, export_path: str):
        """Output Monster to JSON file.

        :param pretty: Toggles pretty (indented) JSON output.
        :param export_path: The folder location to save the JSON output to.
        """
        json_out = self.construct_json()
        out_file_name = str(self.id) + ".json"
        out_file_path = Path(export_path / out_file_name)
        with open(out_file_path, "w", newline="\n") as out_file:
            if pretty:
                json.dump(json_out, out_file, indent=4)
            else:
                json.dump(json_out, out_file)
