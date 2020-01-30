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
from typing import Dict, List, Union, Generator

from osrsbox.prayers_api.prayer_properties import PrayerProperties

PATH_TO_PRAYERS_COMPLETE_JSON = Path(__file__).absolute().parent / ".." / ".." / "docs" / "prayers-complete.json"
if not PATH_TO_PRAYERS_COMPLETE_JSON.is_file():
    PATH_TO_PRAYERS_COMPLETE_JSON = Path(__file__).absolute().parent / ".." / "docs" / "prayers-complete.json"
    if not PATH_TO_PRAYERS_COMPLETE_JSON.is_file():
        raise ValueError("Error: Default prayer database file not found. Exiting")


class AllPrayers:
    """This class handles loading of the osrsbox-db prayers database.

    :param input_data_file_or_directory: The osrsbox-db prayers folder of JSON files, or single JSON file.
    """
    def __init__(self, input_data_file_or_directory: Path = PATH_TO_PRAYERS_COMPLETE_JSON):
        self.all_prayers: List[PrayerProperties] = list()
        self.all_prayers_dict: Dict[int, PrayerProperties] = dict()
        self.load_all_prayers(input_data_file_or_directory)

    def __iter__(self) -> Generator[PrayerProperties, None, None]:
        """Iterate (loop) over each PrayerProperties object."""
        for prayer in self.all_prayers:
            yield prayer

    def __getitem__(self, id_number: int) -> PrayerProperties:
        """Return the prayer definition object for a loaded prayer.

        :param id_number: The prayer ID number.
        :return: The prayer definition object linked to a specific ID number.
        """
        return self.all_prayers_dict[id_number]

    def __len__(self) -> int:
        """Return the count of the total number of prayers.

        :return: The total number of prayers.
        """
        return len(self.all_prayers)

    def lookup_by_prayer_id(self, prayer_id_number: int) -> PrayerProperties:
        """Lookup a specific prayer ID and get the associated PrayerProperties object.

        :param prayer_id_number: The prayer ID to lookup.
        :return: The PrayerProperties object found from the lookup.
        :raises: KeyError when the prayer ID cannot be found.
        """
        try:
            prayer_properties = self.all_prayers_dict[prayer_id_number]
        except KeyError:
            raise KeyError("Cannot find the provided prayer ID number...")
        return prayer_properties

    def load_all_prayers(self, input_data_file_or_directory: Union[Path, str]) -> None:
        """Load the prayers database via a JSON file, or directory of JSON files.

        :param input_data_file_or_directory: The path to the data input.
        :raises ValueError: Valid input not found.
        """
        # Check if a str is supplied, if so, convert to Path object
        if isinstance(input_data_file_or_directory, str):
            input_data_file_or_directory = Path(input_data_file_or_directory)

        # Process the directory of JSON, or a single JSON file
        if input_data_file_or_directory.is_dir():
            self._load_prayers_from_directory(path_to_directory=input_data_file_or_directory)
        elif input_data_file_or_directory.is_file():
            self._load_prayers_from_file(path_to_json_file=input_data_file_or_directory)
        else:
            raise ValueError("Error: Valid input not found. Exiting.")

        # Sort the list of prayers
        self.all_prayers.sort(key=lambda x: x.id)

    def _load_prayers_from_directory(self, path_to_directory: Path) -> None:
        """Load prayer database from a directory of JSON files (`prayers-json`).

        :param path_to_directory: The path to the `prayers-json` directory.
        :raises ValueError: No JSON files found in supplied directory.
        """
        # Fetch all .json files in provided dir
        json_files = list(path_to_directory.glob("*.json"))

        try:
            json_files[0]
        except IndexError as e:
            raise ValueError("Error: No files found in directory, check the supplied path. Exiting.") from e

        # Loop through every prayer in JSON file
        for json_file in json_files:
            with open(json_file) as input_json_file:
                temp = json.load(input_json_file)

            self._load_prayer(temp)

    def _load_prayers_from_file(self, path_to_json_file: Path) -> None:
        """Load prayer database from a single JSON file (`prayers-complete.json`).

        :param path_to_json_file: The path to the `prayers-complete.json` file.
        """
        with open(path_to_json_file) as input_json_file:
            temp = json.load(input_json_file)

        for entry in temp:
            self._load_prayer(temp[entry])

    def _load_prayer(self, prayer_json: Dict) -> None:
        """Convert the `prayer_json` into a :class:`PrayerProperties` and store it.

        :param prayer_json: A dict from an open and loaded JSON file.
        :raises ValueError: Cannot populate prayer.
        """
        # Load the prayer using the PrayerProperties class
        try:
            prayer_def = PrayerProperties.from_json(prayer_json)
        except TypeError as e:
            raise ValueError("Error: Invalid JSON structure found, check supplied input. Exiting") from e

        # Add prayer to list
        self.all_prayers.append(prayer_def)
        self.all_prayers_dict[prayer_def.id] = prayer_def
