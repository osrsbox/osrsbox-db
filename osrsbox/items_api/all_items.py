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

from osrsbox.items_api.item_definition import ItemDefinition

PATH_TO_ITEMS_COMPLETE_JSON = Path(__file__).absolute().parent / ".." / ".." / "docs" / "items-complete.json"
if not PATH_TO_ITEMS_COMPLETE_JSON.is_file():
    PATH_TO_ITEMS_COMPLETE_JSON = Path(__file__).absolute().parent / ".." / "docs" / "items-complete.json"
    if not PATH_TO_ITEMS_COMPLETE_JSON.is_file():
        raise ValueError("Error: Default item database file not found. Exiting")


class AllItems:
    """This class handles loading of the osrsbox-db items database.

    :param input_data_file_or_directory: The osrsbox-db items folder of JSON files, or single JSON file.
    """
    def __init__(self, input_data_file_or_directory: Path = PATH_TO_ITEMS_COMPLETE_JSON):
        self.all_items: List[ItemDefinition] = list()
        self.all_items_dict: Dict[int, ItemDefinition] = dict()
        self.load_all_items(input_data_file_or_directory)

    def __iter__(self) -> Generator[ItemDefinition, None, None]:
        """Iterate (loop) over each ItemDefinition object."""
        for item in self.all_items:
            yield item

    def __getitem__(self, id_number: int) -> ItemDefinition:
        """Return the item definition object for a loaded item.

        :param id_number: The item ID number.
        :return: The item definition object linked to a specific ID number.
        """
        return self.all_items_dict[id_number]

    def __len__(self) -> int:
        """Return the count of the total number of items.

        :return: The total number of items.
        """
        return len(self.all_items)

    def load_all_items(self, input_data_file_or_directory: Union[Path, str]) -> None:
        """Load the items database via a JSON file, or directory of JSON files.

        :param input_data_file_or_directory: The path to the data input.
        :raises ValueError: Valid input not found.
        """
        # Check if a str is supplied, if so, convert to Path object
        if isinstance(input_data_file_or_directory, str):
            input_data_file_or_directory = Path(input_data_file_or_directory)

        # Process the directory of JSON, or a single JSON file
        if input_data_file_or_directory.is_dir():
            self._load_items_from_directory(path_to_directory=input_data_file_or_directory)
        elif input_data_file_or_directory.is_file():
            self._load_items_from_file(path_to_json_file=input_data_file_or_directory)
        else:
            raise ValueError("Error: Valid input not found. Exiting.")

        # Sort the list of items
        self.all_items.sort(key=lambda x: x.id)

    def _load_items_from_directory(self, path_to_directory: Path) -> None:
        """Load item database from a directory of JSON files (`items-json`).

        :param path_to_directory: The path to the `items-json` directory.
        :raises ValueError: No JSON files found in supplied directory.
        """
        # Fetch all .json files in provided dir
        json_files = list(path_to_directory.glob("*.json"))

        try:
            json_files[0]
        except IndexError as e:
            raise ValueError("Error: No files found in directory, check the supplied path. Exiting.") from e

        # Loop through every item in JSON file
        for json_file in json_files:
            with open(json_file) as input_json_file:
                temp = json.load(input_json_file)

            self._load_item(temp)

    def _load_items_from_file(self, path_to_json_file: Path) -> None:
        """Load item database from a single JSON file (`items-complete.json`).

        :param path_to_json_file: The path to the `items-complete.json` file.
        """
        with open(path_to_json_file) as input_json_file:
            temp = json.load(input_json_file)

        for entry in temp:
            self._load_item(temp[entry])

    def _load_item(self, item_json: Dict) -> None:
        """Convert the `item_json` into a :class:`ItemDefinition` and store it.

        :param item_json: A dict from an open and loaded JSON file.
        :raises ValueError: Cannot populate item.
        """
        # Load the item using the ItemDefinition class
        try:
            item_def = ItemDefinition.from_json(item_json)
        except TypeError as e:
            raise ValueError("Error: Invalid JSON structure found, check supplied input. Exiting") from e

        # Add item to list
        self.all_items.append(item_def)
        self.all_items_dict[item_def.id] = item_def
