"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Copyright (c) 2020, PH01L

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
from pathlib import Path
from dataclasses import asdict
from dataclasses import dataclass
from typing import Dict


@dataclass
class PrayerProperties:
    """This class defines the object structure and properties for an OSRS prayer.

    The PrayerProperties class is the object that retains all properties and stats
    for one specific prayer.
    """
    id: int = None
    name: str = None
    members: bool = None
    description: str = None
    drain_per_minute: float = None
    wiki_url: str = None
    requirements: Dict = None
    bonuses: Dict = None
    icon: str = None

    @classmethod
    def from_json(cls, json_dict: Dict) -> 'PrayerProperties':
        """Construct PrayerProperties object from dictionary/JSON."""
        return cls(**json_dict)

    def construct_json(self) -> Dict:
        """Construct dictionary for exporting or printing.

        :return: All class attributes stored in a dictionary.
        """
        return asdict(self)

    def export_json(self, pretty: bool, export_path: str):
        """Output PrayerProperties to JSON file.

        :param pretty: Toggles pretty (indented) JSON output.
        :param export_path: The folder location to save the JSON output to.
        """
        json_out = self.construct_json()
        out_file_name = str(self.id) + ".json"
        out_file_path = Path(export_path / out_file_name)
        with open(out_file_path, "w") as out_file:
            if pretty:
                json.dump(json_out, out_file, indent=4)
            else:
                json.dump(json_out, out_file)
