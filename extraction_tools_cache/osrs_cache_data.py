"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A Python script to parse and compress all definition files from a OSRS cache
dump using the RuneLite Cache tool. The output from this tools are three
directories with individual JSON files for each item, npc, or object
definition file. Since the size of these cache dumps are so large this project
compresses the files into single JSON files that are compressed (using zlib),
converted to base64, then added to a single file.
This script provides methods to compress the original extracted data and also
a class to decompress the cache data on-the-fly so that it can be used in
other modules.

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
import glob
import zlib
import json
import binascii
from pathlib import Path
from typing import Dict
from typing import Union
from typing import Tuple
from typing import Generator
from base64 import b64encode, b64decode

import config
from extraction_tools_cache import osrs_cache_constants


class CacheDefinitionFiles:
    """A simple class to decompress OSRS cache data and provide access to definitions.

    The OSRS cache has a wealth of information provided in the cache definition files.
    The osrsbox-db repo provides all item, npc and object definition files in compressed
    JSON files. This class provides a simple wrapper to access the compressed definition
    file data on-the-fly by decompressing them and providing some easy accessors.

    :param compressed_cache_file: A compressed cache file for items, npcs or objects.
    """
    def __init__(self, compressed_cache_file: str):
        self.compressed_cache_file = compressed_cache_file
        self.definitions: Dict[str, str] = dict()

    def __len__(self) -> int:
        """Return the number of cache definitions.

        :return: The number of cache definitions available.
        """
        return len(self.definitions)

    def __getitem__(self, id_number: str) -> str:
        """Return the decompressed definition for an item, npc or object using the ID number.

        :param id_number: The item, npc or object definition ID number.
        :return: The JSON data linked to the specified item, npc or object ID number.
        """
        return self.definitions[id_number]

    def __iter__(self) -> Generator[str, None, None]:
        """Iterate (loop) over all of the OSRS cache definitions.

        :return: An OSRS cache definition ID number.
        """
        for id_number in self.definitions:
            yield id_number

    def decompress_cache_file(self):
        """Internal method to automatically decompress a compressed JSON file.

        :raises SystemExit:
        """

        try:
            # Open the file and try loading the JSON content
            with open(self.compressed_cache_file) as compressed_file:
                try:
                    json_data = json.loads(compressed_file.read())
                except json.JSONDecodeError:
                    raise SystemExit(">>> ERROR: The provided file is not a valid JSON file! Exiting.")
        except IOError:
            raise SystemExit(">>> ERROR: Could not open file.")

        # Try to decompress the first key to ensure correct file is provided
        compressed_json_data = json_data["1"]
        if not self._check_decompress_definition_data(compressed_json_data):
            raise SystemExit(">>> ERROR: The file does not have compressed JSON data! Exiting.")

        for id_number, compressed_json_data in json_data.items():
            decompressed_data = zlib.decompress(b64decode(compressed_json_data))
            definition_data = json.loads(decompressed_data)
            self.definitions[id_number] = definition_data

    @staticmethod
    def _check_decompress_definition_data(compressed_json_data: str) -> bool:
        """Internal method to decompress a single definition file entry.

        :param compressed_json_data: A string of compressed representation of a definition file.
        :return bool: True if file is able to be decompressed.
        """
        try:
            decoded_data = b64decode(compressed_json_data)
        except binascii.Error:
            return False
        try:
            decompressed_data = zlib.decompress(decoded_data)
        except zlib.error:
            return False
        try:
            json.loads(decompressed_data)
        except json.JSONDecodeError:
            return False

        return True


def compress_definition_file(json_data: Dict) -> Tuple[str, str]:
    """Compress a single cache definition file.

    :param json_data: The definition file JSON data to compress.
    :return id_number: The ID number of the cache definition file.
    :return json_out: A compressed representation of the cache definition file data.
    """
    # First, fetch the ID number, used for the key
    id_number = json_data["id"]

    # Convert JSON dictionary data to a string, and encode to bytes object
    json_bytes = json.dumps(json_data).encode("utf-8")
    # Compress the JSON bytes object
    json_compressed = zlib.compress(json_bytes)
    # Shrink into base64 encoded bytes object, and convert to an ASCII string
    json_out = b64encode(json_compressed).decode("ascii")

    # Return the ID number and compressed json data
    return id_number, json_out


def compress_single_cache_type(path_to_definition_files: Union[Path, str], output_json_file: Union[Path, str]):
    """Compress a directory of OSRS cache definition files.

    :param path_to_definition_files: The path to the directory of cache definition files.
    :param output_json_file: The file name for the compressed JSON file.
    """
    print(f"  > Compressing cache definitions in: {path_to_definition_files}")
    # Setup dictionary for JSON export
    all_definitions = {}

    # Get all files in cache dump directory, and sort numerically
    definition_files = Path(path_to_definition_files).glob("*.json")
    definition_files = sorted((fi for fi in definition_files), key=lambda fi: int(fi.stem))

    for definition_file in definition_files:
        # Skip any generated Java class files used by RuneLite
        if definition_file.stem in osrs_cache_constants.JAVA_CLASS_FILES:
            continue

        # Open each definition file for processing and dump the JSON content
        with open(str(definition_file)) as input_json_file:
            json_data = json.loads(input_json_file.read())
            id_number, json_out = compress_definition_file(json_data)
            all_definitions[id_number] = json_out

    with open(output_json_file, "w") as json_file:
        json.dump(all_definitions, json_file)


def compress_all_cache_types(cache_dump_path: Union[Path, str]):
    """Compress all OSRS cache definition files for items, npcs and objects."""
    print(f">>> Processing cache dump in the following root path: {cache_dump_path}")
    for cache_dump_type in osrs_cache_constants.CACHE_DUMP_TYPES:
        cache_dump_full_path = Path(cache_dump_path) / cache_dump_type / ""
        output_json_file_name = f"{cache_dump_type}.json"
        output_json_file_path = Path(cache_dump_path) / output_json_file_name
        compress_single_cache_type(cache_dump_full_path, output_json_file_path)


def main(cache_dump_path: Union[str, Path], process_all: bool):
    """Main function for compressing OSRS cache data

    :param cache_dump_path: The location of the cache directories exported by RuneLite
    :param process_all: Boolean to toggle processing of all cache dumps (items, npcs, objects)
    """
    # Check if a str is supplied, if so, convert to Path object
    if isinstance(cache_dump_path, str):
        cache_dump_path = Path(cache_dump_path)

    if process_all:
        # Compress all cache definition files (for items, npcs and objects folders)
        compress_all_cache_types(cache_dump_path)
    else:
        # Compress a single cache definition type
        out_file_name = f"{cache_dump_path}.json"
        compress_single_cache_type(cache_dump_path, out_file_name)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d",
                    "--directory",
                    help="<Required> Directory to compress",
                    required=True)
    ap.add_argument("-a",
                    action="store_true",
                    default=False)
    args = vars(ap.parse_args())

    # Set path as provided by the user
    cache_path = args["directory"]
    # Determine if the user wants to compress all, or one, dump
    process_mode = args["a"]

    main(cache_path, process_mode)
