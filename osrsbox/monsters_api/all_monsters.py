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
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union
from typing import Generator

from osrsbox.monsters_api.monster_properties import MonsterProperties

PATH_TO_MONSTERS_COMPLETE = Path(__file__).absolute().parent / ".." / ".." / "docs" / "monsters-complete.json"
if not PATH_TO_MONSTERS_COMPLETE.is_file():
    PATH_TO_MONSTERS_COMPLETE = Path(__file__).absolute().parent / ".." / "docs" / "monsters-complete.json"
    if not PATH_TO_MONSTERS_COMPLETE.is_file():
        raise ValueError("Error: Default monsters database file not found. Exiting")


class AllMonsters:
    """This class handles loading of the osrsbox-db monsters database.

    :param input_data_file_or_directory: The osrsbox-db monsters folder of JSON files, or single JSON file.
    """
    def __init__(self, input_data_file_or_directory: Path = PATH_TO_MONSTERS_COMPLETE):
        self.all_monsters: List[MonsterProperties] = list()
        self.all_monsters_dict: Dict[int, MonsterProperties] = dict()
        self.load_all_monsters(input_data_file_or_directory)

    def __iter__(self) -> Generator[MonsterProperties, None, None]:
        """Iterate (loop) over each MonsterProperties object."""
        for monster in self.all_monsters:
            yield monster

    def __getitem__(self, id_number: int) -> MonsterProperties:
        """Return the monster definition object for a loaded monster.

        :param id_number: The monster ID number.
        :return: The monster definition object linked to a specific ID number.
        """
        return self.all_monsters_dict[id_number]

    def __len__(self) -> int:
        """Return the count of the total number of monsters.

        :return: The total number of monsters.
        """
        return len(self.all_monsters)

    def load_all_monsters(self, input_data_file_or_directory: Union[Path, str]) -> None:
        """Load the monsters database via a JSON file, or directory of JSON files.

        :param input_data_file_or_directory: The path to the data input.
        :raises ValueError: Valid input not found.
        """
        # Check if a str is supplied, if so, convert to Path object
        if isinstance(input_data_file_or_directory, str):
            input_data_file_or_directory = Path(input_data_file_or_directory)

        # Process the directory of JSON, or a single JSON file
        if input_data_file_or_directory.is_dir():
            self._load_monsters_from_directory(path_to_directory=input_data_file_or_directory)
        elif input_data_file_or_directory.is_file():
            self._load_monsters_from_file(path_to_json_file=input_data_file_or_directory)
        else:
            raise ValueError("Error: Valid input not found. Exiting.")

        # Sort the list of monsters
        self.all_monsters.sort(key=lambda x: x.id)

    def _load_monsters_from_directory(self, path_to_directory: Path) -> None:
        """Load monster database from a directory of JSON files (`monsters-json`).

        :param path_to_directory: The path to the `monsters-json` directory.
        :raises ValueError: No JSON files found in supplied directory.
        """
        # Fetch all .json files in provided dir
        json_files = list(path_to_directory.glob("*.json"))

        try:
            json_files[0]
        except IndexError as e:
            raise ValueError("Error: No files found in directory, check the supplied path. Exiting.") from e

        # Loop through every monster in JSON file
        for json_file in json_files:
            with open(json_file) as input_json_file:
                temp = json.load(input_json_file)

            self._load_monster(temp)

    def _load_monsters_from_file(self, path_to_json_file: Path) -> None:
        """Load monster database from a single JSON file (`monster-complete.json`).

        :param path_to_json_file: The path to the `monster-complete.json` file.
        """
        with open(path_to_json_file) as input_json_file:
            temp = json.load(input_json_file)

        for entry in temp:
            self._load_monster(temp[entry])

    def _load_monster(self, monster_json: Dict) -> None:
        """Convert the `monster_json` into a :class:`MonsterProperties` and store it.

        :param monster_json: A dict from an open and loaded JSON file.
        :raises ValueError: Cannot populate monster.
        """
        # Load the monster using the MonsterProperties class
        try:
            monster_def = MonsterProperties.from_json(monster_json)
        except TypeError as e:
            raise ValueError("Error: Invalid JSON structure found, check supplied input. Exiting") from e

        # Add monsters to list
        self.all_monsters.append(monster_def)
        self.all_monsters_dict[monster_def.id] = monster_def
